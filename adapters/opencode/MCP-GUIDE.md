# MCP Server Configuration Guide for OpenCode

本文档详细说明如何在 OpenCode 中配置 MCP Server，以替代 Pi Coding Agent 的 TypeScript 扩展功能。

---

## 概述

OpenCode 使用 MCP (Model Context Protocol) 作为扩展机制，与 Pi 的 TypeScript 扩展不同。本指南提供：

1. MCP Server 安装和配置方法
2. 各扩展功能的 MCP 替代方案
3. 完整的 Python MCP Server 实现

---

## MCP vs Pi 扩展对比

| 功能 | Pi 扩展 | OpenCode MCP 替代 |
|------|---------|-------------------|
| 统一编译 | `build-wrapper.ts` | `embedded_build` tool |
| 错误诊断 | `build-wrapper.ts` | `embedded_diagnose` tool |
| 任务管理 | `todo.ts` | `todowrite` (内置) |
| 图片分析 | `image-read.ts` | `read` (内置图片支持) |

---

## 快速开始

### Step 1: 安装 MCP Server

```bash
# 复制 MCP Server 到 OpenCode MCP 目录
mkdir -p ~/.opencode/mcp
cp mcp-server-embedded.py ~/.opencode/mcp/

# 安装 Python 依赖
pip install mcp pyserial
```

### Step 2: 配置 OpenCode

编辑 OpenCode 配置文件：

```json
// ~/.config/opencode/opencode.json
{
  "mcpServers": {
    "embedded-dev": {
      "command": "python",
      "args": ["~/.opencode/mcp/mcp-server-embedded.py"],
      "env": {}
    }
  }
}
```

### Step 3: 重启 OpenCode

```bash
opencode --reload
```

---

## MCP Server 功能

### embedded_build

统一的嵌入式项目编译命令，支持多种平台。

**参数**:
```json
{
  "action": "build|flash|monitor|clean|detect|size",
  "target": "esp32s3|stm32f4|rp2040",
  "port": "COM3|/dev/ttyUSB0",
  "baud": 115200,
  "verbose": true,
  "clean": false
}
```

**支持的平台**:
- ESP-IDF (ESP32)
- STM32 (Make + OpenOCD)
- Pico SDK (RP2040)
- PlatformIO (多平台)
- Arduino CLI
- Zephyr

**示例调用**:

```json
// 检测项目类型
{
  "action": "detect"
}

// 编译项目
{
  "action": "build"
}

// 烧录到设备
{
  "action": "flash",
  "port": "COM3"
}

// 串口监控
{
  "action": "monitor",
  "port": "COM3",
  "baud": 115200
}
```

### embedded_diagnose

分析编译错误并提供修复建议。

**参数**:
```json
{
  "errorOutput": "...",
  "maxSuggestions": 5
}
```

**示例调用**:

```json
{
  "errorOutput": "main.c:123: error: format '%d' expects 'int'...",
  "maxSuggestions": 3
}
```

**返回格式**:
```json
{
  "errors": [
    {
      "file": "main.c",
      "line": 123,
      "severity": "error",
      "message": "format mismatch",
      "suggestion": "使用 %lu 或 PRIu32 宏"
    }
  ],
  "suggestions": [...]
}
```

---

## 无 MCP Server 替代方案

如果未配置 MCP Server，可使用 OpenCode 内置工具替代：

### 编译命令替代

使用 `bash` 工具直接执行：

```bash
# ESP-IDF
idf.py build
idf.py -p COM3 flash monitor

# STM32
make all
make flash

# Pico SDK
cd build && make
```

### 任务管理替代

使用 OpenCode 内置 `todowrite` 工具：

```json
todowrite todos=[
  {"content": "Configure SPI driver", "status": "pending", "priority": "high"},
  {"content": "Implement LCD init", "status": "in_progress", "priority": "high"}
]
```

### 图片分析替代

使用 OpenCode 内置图片读取能力：

```bash
# OpenCode 支持直接读取和分析图片
read screenshots/capture.png
```

---

## MCP Server 实现说明

### 文件位置

```
mcp-server-embedded.py
```

### 实现架构

```python
#!/usr/bin/env python3
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("embedded-dev-mcp")

# 注册工具
@app.list_tools()
async def list_tools():
    return [
        Tool(name="embedded_build", ...),
        Tool(name="embedded_diagnose", ...),
    ]

# 处理工具调用
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "embedded_build":
        return await handle_build(arguments)
    elif name == "embedded_diagnose":
        return await handle_diagnose(arguments)
```

### 项目类型检测

自动检测以下项目类型：

| 类型 | 标识文件 |
|------|----------|
| ESP-IDF | CMakeLists.txt, sdkconfig, main/ |
| STM32-CubeIDE | .project, .cproject |
| STM32-Makefile | Makefile, startup_ |
| Pico SDK | pico_sdk_import.cmake |
| PlatformIO | platformio.ini |
| Arduino | .ino |
| Zephyr | west.yml |
| nRF5 SDK | sdk_config.h |

---

## 高级配置

### 自定义编译命令

在 MCP Server 中添加自定义命令：

```python
# mcp-server-embedded.py 中添加
CUSTOM_BUILD_COMMANDS = {
    "custom_platform": {
        "build": "custom_build.sh",
        "flash": "custom_flash.sh --port {port}",
    }
}
```

### 环境变量配置

```json
// opencode.json
{
  "mcpServers": {
    "embedded-dev": {
      "command": "python",
      "args": ["~/.opencode/mcp/mcp-server-embedded.py"],
      "env": {
        "ESP_IDF_PATH": "/path/to/esp-idf",
        "STM32_CUBE_PATH": "/path/to/stm32cube"
      }
    }
  }
}
```

---

## 故障排除

### MCP Server 无法启动

```bash
# 检查 Python 环境
python --version  # 需要 >= 3.8

# 检查 MCP 包
pip show mcp

# 手动测试 MCP Server
python ~/.opencode/mcp/mcp-server-embedded.py
```

### 工具调用失败

```bash
# 检查 OpenCode 日志
opencode --debug

# 检查 MCP Server 输出
# 添加日志输出到 mcp-server-embedded.py
```

### 编译命令找不到

```bash
# 检查环境变量
echo $PATH

# 检查 ESP-IDF 环境
idf.py --version

# 检查 STM32 工具链
arm-none-eabi-gcc --version
```

---

## 性能优化

### 缓存编译结果

MCP Server 内部缓存编译结果，减少重复分析：

```python
# mcp-server-embedded.py
CACHE_DIR = "~/.opencode/cache/embedded"
```

### 并行任务

使用异步处理提高性能：

```python
async def handle_build(arguments):
    # 并行检测和编译
    project_type = await detect_project()
    build_result = await build_project(project_type)
```

---

## 扩展 MCP Server

### 添加新工具

```python
@app.list_tools()
async def list_tools():
    return [
        Tool(name="embedded_build", ...),
        Tool(name="embedded_diagnose", ...),
        Tool(name="embedded_flash_compare", ...),  # 新工具
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    # ... 添加处理逻辑
```

### 添加新平台支持

```python
PROJECT_MARKERS = {
    # ... 现有平台
    "risc-v": ["riscv-toolchain", "Makefile"],
    "arm-m33": ["arm-m33.ld", "startup_m33.c"],
}
```

---

## 参考资源

- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [OpenCode Documentation](https://opencode.ai/docs)
- [Pi Coding Agent](https://github.com/badlogic/pi-mono)

---

## 版本兼容性

| MCP Server 版本 | OpenCode 版本 | 更新说明 |
|-----------------|---------------|----------|
| 1.0.0 | >= 1.0.0 | 初始版本 |

---

Version: 1.0
Updated: 2026-04-13