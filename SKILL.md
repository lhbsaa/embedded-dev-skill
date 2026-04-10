---
name: embedded-dev
description: Guide for embedded systems development on ESP32, STM32, RP2040, nRF52 chips. Use this skill whenever the user mentions embedded systems, firmware development, MCU programming, hardware drivers, sensors, LCD displays, IMU devices, SPI/I2C/UART interfaces, compilation, debugging, remote monitoring, Wi-Fi/BLE/MQTT protocols, or needs help with driver code generation, GUI layout design, hardware configuration, or device programming. Make sure to use this skill even if the user doesn't explicitly mention 'embedded' but asks about hardware, sensors, displays, device drivers, microcontrollers, or IoT applications.
license: MIT
compatible-with: pi-coding-agent
pi-version: ">=1.0.0"
---

# Embedded Development Skill (Pi Edition)

AI辅助嵌入式系统开发的专项技能，支持驱动开发、UI设计、硬件调试、问题诊断。采用渐进式加载架构，核心指令保持在SKILL.md，详细规范存放在references目录。

**Pi 版本说明**: 本 Skill 已适配 Pi Coding Agent，使用 Pi 内置工具和扩展系统。

## Pi Tools Used

### Built-in Tools (Pi 内置工具)
| Pi Tool | Function | Original Tool |
|---------|----------|---------------|
| `read` | 读取源代码和数据手册 | read_file |
| `write` | 生成源代码和配置文件 | write_file |
| `edit` | 修改现有代码 | replace |
| `bash` | 编译、烧录、串口监控 | run_shell_command |
| `glob` | 查找项目文件 | glob |
| `grep` | 搜索代码内容 | search_file_content |

### Extension Tools (扩展工具)
| Extension Tool | Function | Install |
|----------------|----------|---------|
| `image_read` | GUI视觉反馈分析 | `extensions/image-read.ts` |
| `todo_list` | 任务跟踪管理 | `extensions/todo.ts` |
| `build_wrapper` | 统一编译命令包装 | `extensions/build-wrapper.ts` |

### Pi Features Used (Pi 特性)
| Feature | Usage |
|---------|-------|
| Session Tree | 调试场景分支回溯 |
| `pi.appendEntry()` | 状态持久化存储 |
| AGENTS.md | 项目上下文记忆 |

## Extension Installation

本 Skill 依赖三个扩展，需先安装：

```bash
# 复制扩展到 Pi 扩展目录
cp extensions/image-read.ts ~/.pi/agent/extensions/
cp extensions/todo.ts ~/.pi/agent/extensions/
cp extensions/build-wrapper.ts ~/.pi/agent/extensions/

# 或通过 Pi 的 packages 安装
# pi install ./embedded-dev
```

## Quick Start for Pi

```bash
# 1. 确保扩展已加载
pi
/reload

# 2. 检查扩展状态
# image_read 和 todo_list 工具应已可用

# 3. 开始嵌入式开发
"帮我配置 ESP32-S3 的 ST7789 LCD 驱动"
```

## Workflow (Pi Edition)

### Phase 1: Context Loading
Use Pi's `read` tool to load AGENTS.md:
```
read AGENTS.md
```
- If AGENTS.md missing → Use `write` to create template with project info
- Store key config in Pi session via `pi.appendEntry()`

### Phase 2: Task Planning
Use `todo_list` extension for task tracking:
```
todo_list action=add "Configure SPI driver"
todo_list action=list
```
- Simple task → Execute directly
- Complex task → Decompose into subtasks

### Phase 3: Code Generation
Use Pi tools for code operations:
```
read src/driver.c          # 读取现有代码
write src/driver_new.c     # 创建新文件
edit src/driver.c          # 修改代码
```
- Check references/ for detailed specs
- Apply modular architecture patterns

### Phase 4: Verification
Use Pi's `bash` tool for build-flash-monitor loop:
```
bash: idf.py build
bash: idf.py -p COM3 flash monitor
```
- On Error → Analyze output → Fix → Retry
- Use `/tree` to navigate to previous working state

### Phase 5: Visual Feedback (GUI)
Use `image_read` extension for LCD analysis:
```
bash: python scripts/camera_capture.py --session
image_read screenshots/capture_xxx.png
```
- Analyze layout, font, color issues
- Apply fixes → Re-verify

### Phase 6: Completion
Update AGENTS.md and save to Pi session:
```
edit AGENTS.md  # Update findings
```
Use Pi's session tree to save checkpoints:
- Press Escape twice → `/tree` → Navigate → Shift+L to label

## Pi-Specific Features

### Session Tree for Debugging
Pi's session tree is valuable for embedded debugging:
```
/tree              # Open session navigator
# Navigate to earlier working state
# Branch from that point to try fix
/fork              # Create new session file if needed
```

### State Persistence with pi.appendEntry()
When using Pi's extension API:
```typescript
pi.appendEntry("embedded-config", {
  chip: "ESP32-S3",
  lcd: { controller: "ST7789", resolution: "240x240" },
  lastError: "DMA overflow"
});
```

### Context Files (AGENTS.md)
Pi automatically loads AGENTS.md from project root. Template:
```markdown
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
    │   └─ Capture screen → image_read analysis
    │   └─ Read references/gui-feedback.md
    │   
    └─ Tool Setup
        └─ Read references/tools.md
        └─ Configure build/debug environment
```

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

### Platform Detection

```yaml
Windows:
  - Path contains backslash (\)
  - Serial ports: COM1, COM2, COM3...
  - PowerShell: && 不支持，用 ; if($?) {cmd}

Linux:
  - Path contains forward slash (/)
  - Serial ports: /dev/ttyUSB0, /dev/ttyACM0...
  - Bash: && 和 || 正常工作

macOS:
  - Path contains forward slash (/)
  - Serial ports: /dev/cu.usbserial*, /dev/tty.usbmodem*
  - Bash: && 和 || 正常工作
```

### Command Chaining

```yaml
# Windows PowerShell 5.1
cmd1; if($?) {cmd2}     # 成功后执行
cmd1; if(-not $?) {cmd2}  # 失败后执行

# Linux/macOS Bash
cmd1 && cmd2    # 成功后执行
cmd1 || cmd2    # 失败后执行
```

### Serial Port Examples

```yaml
# Windows
idf.py -p COM3 flash monitor

# Linux
idf.py -p /dev/ttyUSB0 flash monitor

# macOS
idf.py -p /dev/cu.usbserial-110 flash monitor
```

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

## Examples

### Example 1: LCD Driver
```
User: "Configure ST7789 LCD, 240×240, SPI"

Steps:
1. read AGENTS.md → check constraints
2. Load references/chips.md → ESP32-S3 SPI config
3. Generate driver code:
   write src/lcd_st7789.c
   write include/lcd_st7789.h
4. bash: idf.py build
5. bash: idf.py -p COM3 flash monitor
6. Visual feedback:
   bash: python scripts/camera_capture.py --session
   image_read screenshots/capture_xxx.png
7. Adjust if needed → Re-verify
```

### Example 2: Wi-Fi Setup
```
User: "Connect to Wi-Fi AP"

Steps:
1. Load references/protocols.md → Wi-Fi section
2. Configure STA mode, SSID, password:
   read main/wifi_config.c
   edit main/wifi_config.c
3. Add event handlers for connection
4. bash: idf.py build flash monitor
5. Test connectivity
```

### Example 3: Debugging with Pi Session Tree
```
User: "LCD shows nothing after flash"

Steps:
1. Analyze monitor output from bash command
2. Check SPI initialization logs
3. Verify pin assignments: read src/lcd.c
4. Check backlight control
5. Apply fix: edit src/lcd.c
6. Verify: bash: idf.py build flash monitor
7. If still broken, use Pi's session tree:
   - Press Escape twice → /tree
   - Navigate to earlier working version
   - /fork to create new branch
   - Try different fix approach
```

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

## Scripts

Helper scripts for GUI visual feedback and automation:

### camera_capture.py
Capture LCD display via USB camera for visual analysis.

```bash
# List available cameras
python scripts/camera_capture.py --list

# Capture single image
python scripts/camera_capture.py --resolution 1920x1080

# Create session folder with timestamp
python scripts/camera_capture.py --session

# Multiple captures with interval
python scripts/camera_capture.py --count 5 --interval 2
```

### image_compare.py
Compare before/after images to detect changes.

```bash
# Basic comparison
python scripts/image_compare.py --before img1.png --after img2.png

# Custom sensitivity threshold
python scripts/image_compare.py --before img1.png --after img2.png --threshold 50
```

### Dependencies
```bash
pip install -r scripts/requirements.txt
# Requires: opencv-python, numpy
```

## Best Practices
1. Load AGENTS.md at session start
2. Compile after each module completion
3. Use visual feedback for GUI work
4. Save important findings to memory
5. Read reference files as needed (progressive loading)

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

## Constraints
- DMA: ESP32-S3 SPI max 4092 bytes per transfer
- Memory: Respect PSRAM/SRAM limits
- Timing: Hardware-specific parameters need verification
- Security: Manual review for credential code

---
Version: 3.1 (Pi Edition - Tools Adapted + Extensions Added)
Updated: 2026-04-10
Pi Compatibility: Full
Extensions Required: image-read.ts, todo.ts, build-wrapper.ts (included in extensions/)