---
name: embedded-dev
description: Use when developing firmware on ESP32/STM32/RP2040/nRF52, experiencing DMA overflow, SPI timeout, LCD blank display, frame corruption, GPIO conflicts, sensor reading errors, Wi-Fi disconnect, or needing driver configuration, hardware debugging, display/GUI setup, protocol implementation, serial monitoring. Use even if user doesn't mention 'embedded' but asks about hardware, sensors, displays, microcontrollers, IoT, or device programming.
license: MIT
compatible-with: pi-coding-agent, opencode
pi-version: ">=1.0.0"
opencode-version: ">=1.0.0"
---

# Embedded Development Skill (v3.3.0 - Superpowers Integration Edition)

**Current Version**: v3.3.0 | **Release Date**: 2026-04-18 | [Version History](VERSION_HISTORY.md)

AI辅助嵌入式系统开发的专项技能，支持驱动开发、UI设计、硬件调试、问题诊断。采用渐进式加载架构，核心指令保持在SKILL.md，详细规范存放在references目录。

**v3.3.0 核心改进**: 借鉴 Superpowers 的强制门控机制，新增 Iron Law、Red Flags、Rationalization Table、Verification Gate，以及 Skill Chain 链式调用。

**双平台支持**: 本 Skill 同时支持 **Pi Coding Agent** 和 **OpenCode**。

---

## Skill Chain (P2 新增)

本 Skill 支持链式调用工作流，借鉴 Superpowers 的 skill 链架构：

```
embedded-brainstorming → embedded-driver-design → embedded-implementation → embedded-verification → embedded-gui-feedback
        ↓                       ↓                       ↓                       ↓                       ↓
    硬件需求分析            设计实现方案             代码生成+评审            编译烧录验证            LCD视觉分析
```

### Skill Chain 文件

| Skill | 文件 | 用途 |
|-------|------|------|
| `embedded-brainstorming` | `skills/embedded-brainstorming/SKILL.md` | 硬件需求确认，设计批准 |
| `embedded-driver-design` | `skills/embedded-driver-design/SKILL.md` | 创建实现计划（不生成代码） |
| `embedded-implementation` | `skills/embedded-implementation/SKILL.md` | 执行计划 + 两阶段评审 |
| `embedded-verification` | `skills/embedded-verification/SKILL.md` | build-flash-monitor 强制验证 |
| `embedded-gui-feedback` | `skills/embedded-gui-feedback/SKILL.md` | LCD/GUI 视觉分析 |

### 链式调用规则

1. **HARD-GATE**: 每个 skill 有强制门控，必须完成才能进入下一个
2. **明确调用**: skill 结束时必须明确调用下一个 skill
3. **评审机制**: implementation 有两阶段评审（硬件规范 + MISRA C）
4. **Iron Law**: verification 强制 build-flash-monitor 循环

### 使用方式

复杂项目使用 skill 链：
```
"帮我配置 ST7789 LCD 驱动"
→ 自动触发 embedded-brainstorming
→ 确认设计后进入 embedded-driver-design
→ ...
```

简单任务直接使用主 SKILL.md 的 Phase 流程。

---

## Dual Platform Support

### Pi Coding Agent ✅

**状态**: 原生支持

使用 TypeScript 扩展系统：
- `extensions/image-read.ts` - 图片读取分析
- `extensions/todo.ts` - 任务管理
- `extensions/build-wrapper.ts` - 统一编译命令

**Pi 特性**:
- Session Tree 调试回溯
- `pi.appendEntry()` 状态持久化
- AGENTS.md 自动加载

### OpenCode ✅

**状态**: 完整适配

使用 MCP Server 或内置工具：
- `embedded_build` - 统一编译命令 (MCP)
- `embedded_diagnose` - 错误诊断 (MCP)
- `todowrite` - 任务管理 (内置)
- `read` - 图片分析 (内置)

**安装**:
```bash
# 方式1: 直接使用核心 Skill
cp -r embedded-dev ~/.opencode/skills/

# 方式2: 配置 MCP Server
cp adapters/opencode/mcp-server-embedded.py ~/.opencode/mcp/
```

详见 [adapters/opencode/MCP-GUIDE.md](adapters/opencode/MCP-GUIDE.md)。

---

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
| `embedded_build` | 统一编译命令包装 | `extensions/build-wrapper.ts` |

### Pi Features Used (Pi 特性)

| Feature | Usage |
|---------|-------|
| Session Tree | 调试场景分支回溯 |
| `pi.appendEntry()` | 状态持久化存储 |
| AGENTS.md | 项目上下文记忆 |

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

### MCP Extension Tools (可选)

| MCP Tool | Function | Install |
|----------|----------|---------|
| `embedded_build` | 统一编译命令 | `mcp-server-embedded.py` |
| `embedded_diagnose` | 编译错误诊断 | `mcp-server-embedded.py` |

---

## Extension Installation

### For Pi Coding Agent

本 Skill 依赖三个扩展，需先安装：

```bash
# 复制扩展到 Pi 扩展目录
cp extensions/image-read.ts ~/.pi/agent/extensions/
cp extensions/todo.ts ~/.pi/agent/extensions/
cp extensions/build-wrapper.ts ~/.pi/agent/extensions/

# 或通过 Pi 的 packages 安装
# pi install ./embedded-dev
```

### For OpenCode

详见 [adapters/opencode/MCP-GUIDE.md](adapters/opencode/MCP-GUIDE.md)。

```bash
# 方式1: 直接使用核心 Skill (推荐)
mkdir -p ~/.opencode/skills/embedded-dev
cp SKILL.md ~/.opencode/skills/embedded-dev/
cp -r references ~/.opencode/skills/embedded-dev/
cp -r scripts ~/.opencode/skills/embedded-dev/

# 方式2: 配置 MCP Server (高级)
cp adapters/opencode/mcp-server-embedded.py ~/.opencode/mcp/
# 编辑 ~/.config/opencode/opencode.json 添加 MCP Server
```

---

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

## Quick Start for OpenCode

```bash
# 1. 安装 Skill
mkdir -p ~/.opencode/skills/embedded-dev
cp -r SKILL.md references scripts ~/.opencode/skills/embedded-dev/

# 2. 安装 Python 依赖 (可选)
pip install -r scripts/requirements.txt

# 3. 开始嵌入式开发
"帮我配置 ESP32-S3 的 ST7789 LCD 驱动"
```

---

## Workflow Overview

6阶段工作流：`Context → Planning → Generation → Verification → Visual → Completion`

**详细流程见:** `workflow.md`

| Phase | Pi Command | OpenCode Command |
|-------|------------|------------------|
| 1. Context | `read AGENTS.md` | `read AGENTS.md` |
| 2. Planning | `todo_list` | `todowrite` |
| 3. Generation | `write/edit` | `write/edit` |
| 4. Verification | `idf.py build flash monitor` | `idf.py build flash monitor` |
| 5. Visual | `image_read` | `read screenshot` |
| 6. Completion | `edit AGENTS.md` | `edit AGENTS.md` |

**Verification Gate (强制):**
```
IDENTIFY → RUN → READ → VERIFY → CLAIM
```

**Platform Commands:**
```yaml
Windows: idf.py -p COM3 flash; if($?) {monitor}
Linux/macOS: idf.py -p /dev/ttyUSB0 flash monitor
```

---

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
    │   └─ Capture screen → image_read analysis
    │   └─ Read references/gui-feedback.md
    │   
    ├─ Quick Troubleshooting
    │   └─ Read references/faq.md
    │   └─ Check common problems and solutions
    │   
    ├─ Learning from Examples
    │   └─ Read references/cases.md
    │   └─ Study real-world case studies
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

---

## The Iron Law

```
NO CODE WITHOUT COMPILATION-FIRST VERIFICATION
```

Write code without building? Delete it. Start over.

**No exceptions:**
- Don't skip `idf.py build` step
- Don't assume configuration works without testing
- Don't claim completion without flash+monitor loop
- Verify means run the actual command

**Violating the letter of this process is violating the spirit of embedded development.**

This applies to:
- Driver configuration changes
- Hardware initialization code
- GUI/display updates
- Protocol implementations
- Any code that touches hardware

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

## Red Flags - STOP and Verify

If you catch yourself thinking:
- "直接改寄存器试试" → Read datasheet first
- "编译成功就算完成" → Run flash+monitor loop
- "GUI看起来没问题" → Use camera_capture for verification
- "这个参数应该可以" → Check chip specifications
- "DMA应该能处理更多" → ESP32-S3 limit is 4092 bytes
- "一次改多个配置" → Change one thing at a time
- "不需要读数据手册" → Datasheet is mandatory

**ALL of these mean: STOP. Run `idf.py build`. Then `idf.py flash monitor`.**

### Symptom-based Red Flags
- LCD blank → Check initialization sequence, verify data transfer
- Display glitch → DMA buffer overflow suspected (check ≤4092)
- SPI timeout → Check clock polarity and DMA alignment
- Random crash → Check stack size, look for memory corruption
- I2C no response → Check pull-up resistors, verify address
- Wi-Fi disconnect → Check power supply stability
- Sensor reading wrong → Check calibration data, verify interface

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to verify" | Simple code breaks. Build takes 10 seconds. |
| "I'll verify after" | Compilation pass ≠ runtime correct. |
| "Already manually tested" | Manual ≠ reproducible. No record, can't re-run. |
| "GUI looks fine to me" | Human eye misses timing/alignment issues. Use camera. |
| "Parameter should work" | "Should" ≠ proven. Datasheet specifies, not assumption. |
| "Just change register" | Blind changes damage hardware. Read datasheet first. |
| "DMA can handle more" | ESP32-S3 limit is 4092. Overflow causes corruption. |
| "Skip flash this time" | Skipping becomes habit → bugs slip through. |
| "Modify multiple at once" | Can't isolate which change caused issue. |
| "Trust the template code" | Templates are starting points. Verify with your hardware. |
| "This is different because..." | The Iron Law has no exceptions. Build first, always. |

---

## Examples Overview

**详细案例见:** `examples.md`

| Case | Task | Key Check |
|------|------|-----------|
| LCD Driver | Configure ST7789, SPI | DMA ≤4092, visual verification |
| Wi-Fi Setup | Connect to AP | Monitor shows "Connected" |
| Debug Blank Screen | Fix LCD display | Pi Session Tree /tree |
| Format String | uint32_t printf | Use PRIu32 or %lu |
| DMA Overflow | Large data transfer | Chunked transfer |
| IMU Sensor | I2C read | Correct sensor data |
| MQTT | Publish data | Message delivery |

**Common Workflow Pattern:**
```
read AGENTS.md → Load references → Generate code → Verify → Visual check → Update memory
```

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
| `references/cases.md` | Real-world case studies, problem diagnosis | Learning from examples |
| `references/faq.md` | Common problems and solutions | Quick troubleshooting |

---

## Prompt Templates

For subagent-driven development, use the following prompt templates:

| Prompt | Purpose | Review Stage |
|---------|---------|--------------|
| `prompts/driver-generator.md` | Generate driver code with DMA constraints | Implementation |
| `prompts/hardware-validator.md` | Validate hardware specs (DMA <= 4092, interface config) | Stage 1 Review |
| `prompts/code-quality.md` | MISRA C compliance, DRY/YAGNI check | Stage 2 Review |
| `prompts/debugging.md` | Systematic root cause analysis | Debugging |

**Two-Stage Review Process:**
```
Implementation → Hardware Validator → Code Quality Reviewer → Commit
```

---

## Hooks

Session start hooks inject embedded development context automatically:

| Hook | Trigger Keywords | Function |
|------|------------------|----------|
| `hooks/hooks.json` | embedded, hardware, driver, LCD, ESP32, STM32, sensor | Hook configuration |
| `hooks/session-start.cmd` | - | Windows PowerShell session context injection |

**Hook Configuration:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "embedded|hardware|driver|LCD|ESP32...",
        "hooks": [{ "type": "command", "command": "session-start.cmd" }]
      }
    ]
  }
}
```

---

## Scripts

Helper scripts for GUI visual feedback, serial monitoring and automation:

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

# Filter by module
python scripts/serial_monitor.py -p COM4 --module LCD

# Save to file
python scripts/serial_monitor.py -p COM4 -d 60 -o log.txt

# JSON output only
python scripts/serial_monitor.py -p COM4 --json
```

**Features**:
- Auto-detect ESP32 devices
- ESP-IDF log format parsing
- Error pattern detection (crash, panic, assert, timeout)
- Log level/module filtering
- JSON structured output for AI integration

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

### serial_monitor.ps1
PowerShell serial monitor (Windows fallback when Python unavailable).

```powershell
# List ports
.\serial_monitor.ps1 -ListPorts

# Monitor COM4 for 10 seconds
.\serial_monitor.ps1 -Port COM4 -Duration 10

# Save to file
.\serial_monitor.ps1 -Port COM4 -OutputFile "log.txt"
```

### Dependencies
```bash
pip install -r scripts/requirements.txt
# Requires: opencv-python, numpy, pyserial
```

---

## Best Practices

1. Load AGENTS.md at session start
2. Compile after each module completion
3. Use visual feedback for GUI work
4. Save important findings to memory
5. Read reference files as needed (progressive loading)
6. Use FAQ for quick troubleshooting
7. Study cases for learning best practices

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

## Adapters

本 Skill 提供不同 AI Coding Agent 的适配器：

| Adapter | Location | Description |
|---------|----------|-------------|
| OpenCode | `adapters/opencode/` | MCP Server + OpenCode 专用 Skill |

详见 [adapters/README.md](adapters/README.md)。

---

Version: 3.2.0 (Dual Platform Edition - Pi + OpenCode)
Updated: 2026-04-13
Pi Compatibility: Full (Extensions Required)
OpenCode Compatibility: Full (MCP Optional)