---
name: embedded-dev
description: Guide for embedded systems development on ESP32, STM32, RP2040, nRF52 chips. Use this skill whenever the user mentions embedded systems, firmware development, MCU programming, hardware drivers, sensors, LCD displays, IMU devices, SPI/I2C/UART interfaces, compilation, debugging, remote monitoring, Wi-Fi/BLE/MQTT protocols, or needs help with driver code generation, GUI layout design, hardware configuration, or device programming. Make sure to use this skill even if the user doesn't explicitly mention 'embedded' but asks about hardware, sensors, displays, device drivers, microcontrollers, or IoT applications.
license: MIT
---

# Embedded Development Skill (OpenCode Edition)

**Current Version**: v3.2.0 (2026-04-13)

AI辅助嵌入式系统开发的专项技能，支持驱动开发、UI设计、硬件调试、问题诊断。采用渐进式加载架构，核心指令保持在SKILL.md，详细规范存放在references目录。

**OpenCode 版本说明**: 本 Skill 已适配 OpenCode，使用 OpenCode 内置工具和 MCP 扩展系统。

---

## OpenCode Tools Used

### Built-in Tools (OpenCode 内置工具)

| OpenCode Tool | Function |
|---------------|----------|
| `read` | 读取源代码和数据手册 |
| `write` | 生成源代码和配置文件 |
| `edit` | 修改现有代码 |
| `bash` | 编译、烧录、串口监控 |
| `glob` | 查找项目文件 |
| `grep` | 搜索代码内容 |
| `todowrite` | 任务跟踪管理 (内置) |

### MCP Extension Tools (扩展工具)

| MCP Tool | Function | Install |
|----------|----------|---------|
| `embedded_build` | 统一编译命令包装 | `mcp-server-embedded.py` |
| `embedded_diagnose` | 编译错误诊断 | `mcp-server-embedded.py` |

**注**: 如果未配置 MCP Server，可使用 `bash` 工具直接执行编译命令。

---

## Quick Start for OpenCode

```bash
# 1. 安装 Skill
mkdir -p ~/.opencode/skills/embedded-dev
cp SKILL.md ~/.opencode/skills/embedded-dev/
cp -r references ~/.opencode/skills/embedded-dev/

# 2. (可选) 配置 MCP Server
# 参考 MCP-GUIDE.md

# 3. 开始嵌入式开发
"帮我配置 ESP32-S3 的 ST7789 LCD 驱动"
```

---

## Workflow (OpenCode Edition)

### Phase 1: Context Loading

Use OpenCode's `read` tool to load AGENTS.md:

```
read AGENTS.md
```

- If AGENTS.md missing → Use `write` to create template with project info
- Store key config in OpenCode session

### Phase 2: Task Planning

Use `todowrite` tool for task tracking:

```
todowrite todos=[{"content": "Configure SPI driver", "status": "pending", "priority": "high"}]
```

- Simple task → Execute directly
- Complex task → Decompose into subtasks

### Phase 3: Code Generation

Use OpenCode tools for code operations:

```
read src/driver.c          # 读取现有代码
write src/driver_new.c     # 创建新文件
edit src/driver.c          # 修改代码
```

- Check references/ for detailed specs
- Apply modular architecture patterns

### Phase 4: Verification

Use OpenCode's `bash` tool for build-flash-monitor loop:

```
bash: idf.py build
bash: idf.py -p COM3 flash monitor
```

- On Error → Analyze output → Fix → Retry
- Use MCP `embedded_diagnose` for error analysis (if configured)

### Phase 5: Visual Feedback (GUI)

Use Python scripts for LCD analysis:

```
bash: python scripts/camera_capture.py --session
bash: python scripts/image_compare.py --before img1.png --after img2.png
```

- Analyze layout, font, color issues
- Apply fixes → Re-verify

### Phase 6: Completion

Update AGENTS.md:

```
edit AGENTS.md  # Update findings
```

---

## Quick Reference Tables

### Supported Chip Families

| Family | Key Chips | Framework | Strength |
|--------|-----------|-----------|----------|
| **ESP32** | S3, C3, C6, H2 | ESP-IDF, Arduino | Wi-Fi, LCD, AI |
| **STM32** | F4, F7, H7, L4, U5 | STM32CubeIDE | Performance, DSP |
| **RP2040** | Pico, Pico 2 | Pico SDK | Low cost, PIO |
| **nRF52** | 52832, 52840 | nRF5 SDK | BLE, Low power |

### Hardware Interfaces Quick Guide

| Interface | Max Speed | Key Config | Common Use |
|-----------|-----------|------------|------------|
| **SPI** | 80MHz | Mode 0, DMA≤4092B | LCD, Flash |
| **I2C** | 1MHz | 7-bit addr, pull-up | Sensors |
| **UART** | 5Mbps | 8N1, DMA optional | Debug, Comm |
| **GPIO** | - | Pull-up/down, interrupt | Control |
| **ADC** | 12-bit | Calibration, averaging | Voltage |
| **PWM** | - | Frequency, duty cycle | LED, Motor |

### Communication Protocols Quick Guide

| Protocol | Transport | Security | Use Case |
|----------|-----------|----------|----------|
| **Wi-Fi** | Wireless | TLS | IoT Network |
| **TCP/IP** | Network | TLS | Socket Comm |
| **HTTP** | Network | HTTPS | REST API |
| **WebSocket** | Network | WSS | Real-time |
| **MQTT** | Network | TLS | IoT Messaging |
| **BLE** | Wireless | Low power | Near-field |
| **Modbus** | Serial/Network | None | Industrial |

---

## Decision Tree: Choosing Approach

```
User Request → Identify Task Type
    ├─ Driver Development
    │   └─ Read references/hardware-interfaces.md
    │   └─ Check chip family → Load references/chips.md
    │   
    ├─ Protocol Implementation  
    │   └─ Read references/protocols.md
    │   └─ Check security requirements → TLS or plain
    │   
    ├─ Code Quality
    │   └─ Read references/languages.md
    │   └─ Apply MISRA C / modular design
    │   
    ├─ Debugging
    │   └─ Read references/debugging.md
    │   └─ Check remote → references/remote-tools.md
    │   
    ├─ GUI Development
    │   └─ Capture screen → camera_capture.py
    │   └─ Read references/gui-feedback.md
    │   
    └─ Tool Setup
        └─ Read references/tools.md
        └─ Configure build/debug environment
```

---

## Platform Compatibility

This skill supports Windows, Linux, and macOS platforms.

### Platform-Specific Commands

| Task | Windows (PowerShell) | Linux/macOS (Bash) |
|------|---------------------|-------------------|
| List directory | `dir` | `ls` |
| Read file | `type file` | `cat file` |
| Copy file | `copy src dst` | `cp src dst` |
| Delete file | `del file` | `rm file` |
| Find file | `dir /s pattern` | `find . -name pattern` |
| Serial port | `COMx` | `/dev/ttyUSBx` or `/dev/ttyACMx` |
| Path separator | `\` | `/` |
| Environment var | `$env:VAR` | `$VAR` |

### Cross-Platform Commands (Same on All Platforms)

| Command | Description |
|---------|-------------|
| `idf.py build` | ESP-IDF compile |
| `idf.py flash` | Flash firmware |
| `idf.py monitor` | Serial monitor |
| `idf.py menuconfig` | Configuration |
| `python script.py` | Run Python |
| `git clone/commit/push` | Version control |

### Serial Port Examples

```yaml
# Windows
idf.py -p COM3 flash monitor

# Linux
idf.py -p /dev/ttyUSB0 flash monitor

# macOS
idf.py -p /dev/cu.usbserial-110 flash monitor
```

---

## Core Principles

### 1. Compile-Flash-Monitor-Test Loop

Always verify code through complete loop:

```
idf.py build → idf.py flash → idf.py monitor → Test → Fix
```

### 2. AGENTS.md Memory Management

```yaml
## 项目信息
project:
  name: [项目名称]
  target: [目标芯片]
  framework: [开发框架]

## 硬件配置  
hardware:
  lcd: {controller, interface, resolution}
  imu: {model, interface}

## 记忆库
memory:
  - "成功配置: [具体参数]"
  - "问题解决: [方案]"
```

### 3. DMA Buffer Constraints

ESP32-S3 SPI DMA: **Single transfer max 4092 bytes**
Use chunked transfer for larger data.

### 4. GUI Visual Feedback

Camera: 1920×1080 PNG, uniform lighting, centered screen.
Analysis: Layout, font, color, overlap detection.

### 5. Modular Architecture

Three-layer design:
- Application Layer (业务逻辑)
- HAL/Driver Layer (硬件抽象)
- Platform Layer (芯片SDK)

---

## Reference Documents

For detailed specifications, read the following reference files:

| Reference | Content | When to Read |
|-----------|---------|--------------|
| `references/chips.md` | Chip families, specs, frameworks | Driver development, chip selection |
| `references/hardware-interfaces.md` | SPI/I2C/UART/GPIO/ADC/PWM/DMA specs | Interface configuration |
| `references/protocols.md` | Wi-Fi/TCP/HTTP/MQTT/BLE/Modbus specs | Network/communication |
| `references/languages.md` | MISRA C, modular design, Rust/Zig | Code quality, architecture |
| `references/tools.md` | GCC, CMake, OpenOCD, VSCode config | Environment setup |
| `references/remote-tools.md` | WiFi/Serial/USB remote, cloud platforms | Remote debugging |
| `references/debugging.md` | Debug strategies, log analysis | Problem diagnosis |
| `references/gui-feedback.md` | Camera setup, analysis workflow | LCD/GUI development |
| `references/ai-patterns.md` | Agent patterns, skill universality | AI integration |
| `references/cases.md` | Real-world case studies | Learning from examples |
| `references/faq.md` | Common problems and solutions | Quick troubleshooting |

---

## Scripts

Helper scripts for GUI visual feedback and serial monitoring:

### serial_monitor.py

AI-friendly serial port monitoring with structured JSON output.

```bash
# List available ports
python scripts/serial_monitor.py --list

# Auto-detect ESP32 and monitor
python scripts/serial_monitor.py --detect --duration 30

# Monitor specific port
python scripts/serial_monitor.py -p COM4 -b 115200 -d 60

# Filter by log level (E/W/I/D/V)
python scripts/serial_monitor.py -p COM4 -f E

# Save to file
python scripts/serial_monitor.py -p COM4 -d 60 -o log.txt
```

### camera_capture.py

Capture LCD display via USB camera for visual analysis.

```bash
# List available cameras
python scripts/camera_capture.py --list

# Capture single image
python scripts/camera_capture.py --resolution 1920x1080

# Create session folder with timestamp
python scripts/camera_capture.py --session
```

### image_compare.py

Compare before/after images to detect changes.

```bash
# Basic comparison
python scripts/image_compare.py --before img1.png --after img2.png
```

### Dependencies

```bash
pip install -r scripts/requirements.txt
# Requires: opencv-python, numpy, pyserial
```

---

## MCP Server (Optional)

For advanced functionality, configure the MCP Server:

```bash
# Copy MCP Server
cp adapters/opencode/mcp-server-embedded.py ~/.opencode/mcp/

# Configure in OpenCode
# See MCP-GUIDE.md for detailed instructions
```

**MCP Tools**:
- `embedded_build`: Build, flash, monitor, clean
- `embedded_diagnose`: Analyze compile errors

---

## Security Checklist

Before deploying code, verify the following:

### Credentials & Secrets
- [ ] No hardcoded passwords, API keys, or tokens
- [ ] Wi-Fi credentials stored in NVS or secure storage
- [ ] TLS certificates properly configured
- [ ] Sensitive data encrypted at rest

### Network Security
- [ ] Use TLS/SSL for network communication
- [ ] Validate server certificates
- [ ] Implement proper authentication
- [ ] Close unused ports and services

### Memory Safety
- [ ] Buffer bounds checked
- [ ] No unchecked pointer dereferences
- [ ] Stack size adequate for tasks
- [ ] DMA buffers properly aligned

### Hardware Safety
- [ ] GPIO levels within spec
- [ ] Power supply stable
- [ ] ESD protection in place
- [ ] Thermal management adequate

---

## Constraints

- DMA: ESP32-S3 SPI max 4092 bytes per transfer
- Memory: Respect PSRAM/SRAM limits
- Timing: Hardware-specific parameters need verification
- Security: Manual review for credential code

---

## Best Practices

1. Load AGENTS.md at session start
2. Compile after each module completion
3. Use visual feedback for GUI work
4. Save important findings to memory
5. Read reference files as needed (progressive loading)

---

## Installation

```bash
# Copy Skill to OpenCode directory
mkdir -p ~/.opencode/skills/embedded-dev
cp -r SKILL.md references scripts ~/.opencode/skills/embedded-dev/

# Install Python dependencies (optional)
pip install -r scripts/requirements.txt

# Configure MCP Server (optional, advanced)
# See adapters/opencode/MCP-GUIDE.md
```

---
Version: 3.2.0 (OpenCode Edition - MCP Compatible)
Updated: 2026-04-13
OpenCode Compatibility: Full
MCP Server: Optional (see adapters/opencode/)