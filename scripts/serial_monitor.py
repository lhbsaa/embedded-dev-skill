#!/usr/bin/env python3
"""
Serial Monitor Script for Embedded Development
AI-friendly serial port monitoring with structured JSON output.

Usage: python serial_monitor.py [options]

Options:
  --port, -p      Serial port (e.g., COM4, /dev/ttyUSB0)
  --baud, -b      Baud rate (default: 115200)
  --duration, -d  Monitor duration in seconds (default: 10)
  --output, -o    Output file for captured data
  --filter, -f    Log level filter (E/W/I/D/V, default: all)
  --module, -m    Module filter (e.g., LCD, SPI)
  --detect        Auto-detect ESP32 devices
  --list          List available serial ports
  --json          Output in JSON format only
  --parse         Parse ESP-IDF log format

Examples:
  # List ports
  python serial_monitor.py --list

  # Auto-detect and monitor
  python serial_monitor.py --detect --duration 30

  # Monitor with filter
  python serial_monitor.py -p COM4 -b 115200 -f E --module LCD

  # Save to file
  python serial_monitor.py -p COM4 -d 60 -o log.txt
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("Error: pyserial not installed. Run: pip install pyserial")
    sys.exit(1)


# ESP-IDF log format regex
ESP_LOG_PATTERN = re.compile(
    r'^(\d{2}:\d{2}:\d{2}\.\d{3})\s+([EWIDV])\s+\(\d+\)\s+([a-zA-Z0-9_-]+):\s+(.*)$'
)

# Error patterns to detect
ERROR_PATTERNS = [
    (r'Guru Meditation Error', 'CRASH'),
    (r'panic', 'PANIC'),
    (r'assert failed', 'ASSERT'),
    (r'ERROR', 'ERROR'),
    (r'Failed', 'FAIL'),
    (r'Timeout', 'TIMEOUT'),
    (r'overflow', 'OVERFLOW'),
    (r'leak', 'MEMORY_LEAK'),
    (r'watchdog', 'WATCHDOG'),
]


def list_ports():
    """List all available serial ports"""
    ports = serial.tools.list_ports.comports()
    result = []
    
    for port in ports:
        info = {
            "device": port.device,
            "description": port.description,
            "hwid": port.hwid or "N/A",
            "manufacturer": port.manufacturer or "N/A",
        }
        
        # Detect ESP32 devices
        if any(x in port.description.upper() for x in ['ESP32', 'ESP', 'CH340', 'CH341', 'CH343', 'CP210', 'SILABS']):
            info["likely_esp32"] = True
        
        result.append(info)
    
    return result


def detect_esp32_port():
    """Auto-detect ESP32 device port"""
    ports = list_ports()
    
    # Priority: ESP32 specific devices
    for port in ports:
        if port.get("likely_esp32"):
            return port["device"], 115200
    
    # Fallback: first available port (excluding COM1 on Windows)
    for port in ports:
        if port["device"] not in ["COM1"]:
            return port["device"], 115200
    
    return None, None


def parse_esp_log(line):
    """Parse ESP-IDF log format"""
    match = ESP_LOG_PATTERN.match(line.strip())
    
    if match:
        timestamp, level, module, message = match.groups()
        return {
            "timestamp": timestamp,
            "level": level,
            "module": module,
            "message": message,
            "raw": line.strip()
        }
    
    # Non-standard format
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:12],
        "level": "U",  # Unknown
        "module": "raw",
        "message": line.strip(),
        "raw": line.strip()
    }


def detect_errors(line):
    """Detect error patterns in log"""
    detected = []
    
    for pattern, error_type in ERROR_PATTERNS:
        if re.search(pattern, line, re.IGNORECASE):
            detected.append(error_type)
    
    return detected


def filter_log(parsed_log, level_filter=None, module_filter=None):
    """Filter log by level and module"""
    if level_filter and parsed_log["level"] not in level_filter:
        return False
    
    if module_filter and parsed_log["module"].lower() != module_filter.lower():
        return False
    
    return True


class SerialMonitor:
    """Serial port monitor with structured output"""
    
    def __init__(self, port, baudrate=115200, timeout=1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.lines = []
        self.errors = []
        self.start_time = None
    
    def connect(self):
        """Connect to serial port"""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            self.start_time = time.time()
            return True
        except serial.SerialException as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from serial port"""
        if self.serial and self.serial.is_open:
            self.serial.close()
    
    def read_line(self):
        """Read a single line from serial"""
        try:
            line = self.serial.readline()
            if line:
                return line.decode('utf-8', errors='ignore').strip()
        except serial.SerialException:
            pass
        return None
    
    def monitor(self, duration, level_filter=None, module_filter=None, parse_logs=True):
        """Monitor serial port for specified duration"""
        if not self.connect():
            return self.get_result(success=False, error="Connection failed")
        
        result_lines = []
        detected_errors = []
        modules_seen = set()
        levels_seen = set()
        
        end_time = time.time() + duration
        
        while time.time() < end_time:
            line = self.read_line()
            
            if line:
                # Parse log
                parsed = parse_esp_log(line) if parse_logs else {"raw": line, "level": "U"}
                
                # Filter
                if filter_log(parsed, level_filter, module_filter):
                    result_lines.append(parsed)
                    modules_seen.add(parsed.get("module", "raw"))
                    levels_seen.add(parsed.get("level", "U"))
                
                # Detect errors
                errors = detect_errors(line)
                if errors:
                    detected_errors.append({
                        "timestamp": parsed.get("timestamp"),
                        "types": errors,
                        "line": line[:200]  # Truncate long lines
                    })
        
        self.disconnect()
        
        return self.get_result(
            success=True,
            lines=result_lines,
            errors=detected_errors,
            modules=list(modules_seen),
            levels=list(levels_seen),
            duration=duration
        )
    
    def get_result(self, success, lines=None, errors=None, modules=None, 
                   levels=None, duration=None, error=None):
        """Generate structured result"""
        result = {
            "success": success,
            "port": self.port,
            "baudrate": self.baudrate,
            "timestamp": datetime.now().isoformat(),
        }
        
        if success:
            result["duration"] = duration
            result["lines_count"] = len(lines) if lines else 0
            result["error_count"] = len(errors) if errors else 0
            result["modules"] = modules or []
            result["levels"] = levels or []
            result["data"] = lines or []
            result["errors"] = errors or []
        else:
            result["error"] = error
        
        return result


def main():
    parser = argparse.ArgumentParser(
        description='Serial Monitor for Embedded Development',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--port', '-p', type=str, help='Serial port device')
    parser.add_argument('--baud', '-b', type=int, default=115200, help='Baud rate')
    parser.add_argument('--duration', '-d', type=int, default=10, help='Monitor duration (seconds)')
    parser.add_argument('--output', '-o', type=str, help='Output file path')
    parser.add_argument('--filter', '-f', type=str, help='Log level filter (E/W/I/D/V)')
    parser.add_argument('--module', '-m', type=str, help='Module filter')
    parser.add_argument('--detect', action='store_true', help='Auto-detect ESP32 device')
    parser.add_argument('--list', '-l', action='store_true', help='List available ports')
    parser.add_argument('--json', '-j', action='store_true', help='Output JSON only')
    parser.add_argument('--parse', action='store_true', default=True, help='Parse ESP-IDF logs')
    
    args = parser.parse_args()
    
    # List ports mode
    if args.list:
        ports = list_ports()
        result = {"ports": ports, "count": len(ports)}
        print(json.dumps(result, indent=2))
        return 0
    
    # Auto-detect mode
    if args.detect:
        port, baud = detect_esp32_port()
        if not port:
            print(json.dumps({"success": False, "error": "No ESP32 device detected"}))
            return 1
        args.port = port
        args.baud = baud or args.baud
        if not args.json:
            print(f"Detected: {port} @ {args.baud} baud")
    
    # Require port
    if not args.port:
        print("Error: --port required (or use --detect)")
        parser.print_help()
        return 1
    
    # Parse filter
    level_filter = args.filter.upper() if args.filter else None
    
    # Monitor
    monitor = SerialMonitor(args.port, args.baud)
    result = monitor.monitor(
        duration=args.duration,
        level_filter=level_filter,
        module_filter=args.module,
        parse_logs=args.parse
    )
    
    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write raw lines
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in result.get("data", []):
                f.write(line.get("raw", "") + "\n")
        
        result["output_file"] = str(output_path)
    
    # Print result
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable summary
        print("\n" + "="*50)
        print("SERIAL MONITOR RESULT")
        print("="*50)
        print(f"Port: {result['port']}")
        print(f"Baud: {result['baudrate']}")
        print(f"Duration: {result['duration']}s")
        print(f"Lines: {result['lines_count']}")
        print(f"Errors: {result['error_count']}")
        print(f"Modules: {', '.join(result['modules'][:5])}{'...' if len(result['modules']) > 5 else ''}")
        
        if result['errors']:
            print("\nDetected Errors:")
            for err in result['errors'][:3]:
                print(f"  [{err['timestamp']}] {', '.join(err['types'])}")
        
        print("="*50)
        
        # Print last 10 lines
        if result['data']:
            print("\nLast 10 lines:")
            for line in result['data'][-10:]:
                print(f"  [{line.get('level', 'U')}] {line.get('module', 'raw')}: {line.get('message', '')[:60]}")
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
