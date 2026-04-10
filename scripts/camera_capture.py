#!/usr/bin/env python3
"""
Camera Capture Script for GUI Visual Feedback
Usage: python camera_capture.py [options]

Options:
  --device, -d    Camera device index (default: 0)
  --output, -o    Output directory (default: screenshots/)
  --resolution    Resolution WxH (default: 1920x1080)
  --count, -c     Number of captures (default: 1)
  --interval, -i  Interval between captures in seconds (default: 0)
  --session       Create session folder with timestamp
  --list          List available cameras
"""

import argparse
import cv2
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def list_cameras(max_test=5):
    """List available camera devices"""
    available = []
    for i in range(max_test):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available


def capture_image(device_index, resolution=None):
    """Capture single image from camera"""
    cap = cv2.VideoCapture(device_index)
    
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera device {device_index}")
    
    # Set resolution if specified
    if resolution:
        width, height = resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    # Wait for auto exposure
    for _ in range(5):
        cap.read()
    
    # Capture frame
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise RuntimeError("Failed to capture frame")
    
    return frame


def save_capture(frame, output_dir, filename=None, metadata=None):
    """Save captured image with metadata"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.png"
    
    filepath = output_path / filename
    cv2.imwrite(str(filepath), frame)
    
    # Save metadata
    if metadata:
        meta_path = filepath.with_suffix('.json')
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    return str(filepath)


def create_session(base_dir):
    """Create session directory with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = Path(base_dir) / f"session_{timestamp}"
    session_dir.mkdir(parents=True, exist_ok=True)
    return str(session_dir)


def parse_resolution(res_str):
    """Parse resolution string (e.g., '1920x1080')"""
    if not res_str:
        return None
    try:
        w, h = res_str.lower().split('x')
        return (int(w), int(h))
    except:
        return None


def main():
    parser = argparse.ArgumentParser(description='Camera Capture for GUI Visual Feedback')
    parser.add_argument('--device', '-d', type=int, default=0, help='Camera device index')
    parser.add_argument('--output', '-o', type=str, default='screenshots', help='Output directory')
    parser.add_argument('--resolution', '-r', type=str, default='1920x1080', help='Resolution WxH')
    parser.add_argument('--count', '-c', type=int, default=1, help='Number of captures')
    parser.add_argument('--interval', '-i', type=float, default=0, help='Interval between captures')
    parser.add_argument('--session', '-s', action='store_true', help='Create session folder')
    parser.add_argument('--list', '-l', action='store_true', help='List available cameras')
    parser.add_argument('--metadata', '-m', type=str, default='{}', help='JSON metadata')
    
    args = parser.parse_args()
    
    # List cameras mode
    if args.list:
        cameras = list_cameras()
        print(json.dumps({"cameras": cameras, "count": len(cameras)}, indent=2))
        return 0
    
    # Parse resolution
    resolution = parse_resolution(args.resolution)
    
    # Create session directory if requested
    output_dir = args.output
    if args.session:
        output_dir = create_session(args.output)
        print(f"Session directory: {output_dir}")
    
    # Parse metadata
    try:
        metadata = json.loads(args.metadata)
    except:
        metadata = {}
    
    metadata['timestamp'] = datetime.now().isoformat()
    metadata['resolution'] = args.resolution
    metadata['device'] = args.device
    
    results = []
    
    # Capture images
    for i in range(args.count):
        try:
            frame = capture_image(args.device, resolution)
            
            # Generate filename
            if args.count > 1:
                filename = f"capture_{i+1:03d}.png"
            else:
                filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            filepath = save_capture(frame, output_dir, filename, metadata)
            results.append(filepath)
            print(f"Saved: {filepath}")
            
            if args.interval > 0 and i < args.count - 1:
                import time
                time.sleep(args.interval)
                
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    # Output result as JSON
    print(json.dumps({
        "success": True,
        "output_dir": output_dir,
        "captures": results,
        "count": len(results)
    }, indent=2))
    
    return 0


if __name__ == '__main__':
    sys.exit(main())