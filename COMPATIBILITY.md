# Compatibility Guide

本文档说明如何将 Embedded Development Skill 适配到不同的 AI Coding Agent。

---

## 概述

本 Skill 原生设计支持 **Pi Coding Agent** 和 **OpenCode**，同时可适配其他 AI Coding Agent。

---

## 工具名称映射

不同 AI Coding Agent 使用不同的工具名称，需要进行映射：

### 核心工具映射表

| 功能 | Pi | OpenCode | Claude Code | Aider |
|------|-----|----------|-------------|-------|
| 读取文件 | `read` | `read` | `read` | `read` |
| 写入文件 | `write` | `write` | `write` | `write` |
| 编辑代码 | `edit` | `edit` | `edit` | `edit` |
| 执行命令 | `bash` | `bash` | `bash` | `bash` |
| 查找文件 | `glob` | `glob` | `glob` | `glob` |
| 搜索内容 | `grep` | `grep` | `grep` | `grep` |

**结论**: 核心工具名称完全兼容。

### 扩展工具映射表

| 功能 | Pi 扩展 | OpenCode | Claude Code | 其他 |
|------|---------|----------|-------------|------|
| 图片分析 | `image_read` | `read` (内置) | 直接粘贴图片 | 手动描述 |
| 任务管理 | `todo_list` | `todowrite` (内置) | MCP/TODO.md | TODO.md |
| 统一编译 | `embedded_build` | MCP Server | MCP Server | bash命令 |

---

## 适配指南

### Pi Coding Agent ✅

**状态**: 原生支持，无需修改

```bash
# 安装
cp -r embedded-dev-skill ~/.pi/agent/skills/
cp extensions/*.ts ~/.pi/agent/extensions/

# 使用扩展
pi
/reload
```

**扩展功能**:
- `image_read` - 图片读取分析
- `todo_list` - 任务管理
- `embedded_build` - 统一编译命令
- `/todo` 命令 - 快速任务管理
- `/build` 命令 - 快速编译

---

### OpenCode ✅

**状态**: 原生支持（通过适配器）

**相同点**:
- 核心工具名称相同 (`read`, `write`, `edit`, `bash`, `glob`, `grep`)
- 支持 AGENTS.md 上下文文件
- 内置 `todowrite` 任务管理
- 内置图片读取支持

**不同点**:
| 项目 | Pi | OpenCode |
|------|-----|----------|
| 扩展系统 | TypeScript 扩展 | MCP Server |
| 配置文件 | `~/.pi/agent/` | `~/.config/opencode/` |
| 图片支持 | 扩展实现 | 内置支持 |
| 任务管理 | 扩展实现 | 内置 `todowrite` |

**安装方式**:

#### 方式1: 直接使用核心 Skill (推荐)

```bash
# 复制 Skill 到 OpenCode 目录
mkdir -p ~/.opencode/skills/embedded-dev
cp -r embedded-dev/SKILL.md ~/.opencode/skills/embedded-dev/
cp -r embedded-dev/references ~/.opencode/skills/embedded-dev/
cp -r embedded-dev/scripts ~/.opencode/skills/embedded-dev/

# 安装 Python 依赖
pip install -r scripts/requirements.txt
```

#### 方式2: 使用 OpenCode 适配器

```bash
# 复制适配器
cp -r embedded-dev/adapters/opencode/* ~/.opencode/skills/embedded-dev/
```

#### 方式3: 配置 MCP Server (高级)

```bash
# 复制 MCP Server
cp embedded-dev/adapters/opencode/mcp-server-embedded.py ~/.opencode/mcp/

# 编辑 OpenCode 配置
# ~/.config/opencode/opencode.json
{
  "mcpServers": {
    "embedded-dev": {
      "command": "python",
      "args": ["~/.opencode/mcp/mcp-server-embedded.py"]
    }
  }
}
```

**MCP Server 工具**:
- `embedded_build`: 统一编译命令 (替代 build-wrapper.ts)
- `embedded_diagnose`: 编译错误诊断

**无 MCP Server 替代方案**:

使用 `bash` 工具直接执行：
```bash
# 编译
idf.py build

# 烧录
idf.py -p COM3 flash monitor

# 串口监控
python scripts/serial_monitor.py -p COM4 -d 30
```

---

### Claude Code ⚠️

**状态**: 需适配

**相同点**:
- 核心工具名称相同
- 支持 CLAUDE.md (等同于 AGENTS.md)
- 直接支持图片输入

**不同点**:
| 项目 | Pi | Claude Code |
|------|-----|-------------|
| 扩展系统 | TypeScript 扩展 | MCP |
| 配置文件 | `~/.pi/agent/` | `~/.claude/` |
| 上下文文件 | AGENTS.md | CLAUDE.md |

**适配步骤**:

1. **重命名上下文文件**:
   ```bash
   cp AGENTS.md CLAUDE.md
   ```

2. **使用 MCP 替代扩展**:
   - `embedded_build`: MCP Server 或 bash 命令
   - `embedded_diagnose`: MCP Server

3. **安装**:
   ```bash
   # 复制到 Claude Code 目录
   cp -r references/ ~/.claude/embedded-dev/
   cp SKILL.md ~/.claude/embedded-dev/
   ```

---

### Aider ⚠️

**状态**: 需适配

**相同点**:
- 核心工具名称相同
- 支持上下文文件

**不同点**:
| 项目 | Pi | Aider |
|------|-----|-------|
| 扩展系统 | TypeScript 扩展 | 无 |
| 配置方式 | 配置文件 | 命令行参数 |
| 上下文文件 | AGENTS.md | CONVENTIONS.md |

**适配步骤**:

1. **创建 CONVENTIONS.md**:
   ```bash
   cp AGENTS.md CONVENTIONS.md
   ```

2. **使用方式**:
   ```bash
   # 启动时指定
   aider --message "使用 references/ 中的规范配置 ESP32-S3 SPI"
   
   # 或将 references 内容添加到上下文
   aider --file references/*.md
   ```

3. **扩展替代**: 
   - 无扩展系统，需手动操作
   - 图片分析: 用户手动描述或粘贴图片
   - 任务管理: 使用 TODO.md 文件

---

### Cursor / Windsurf ⚠️

**状态**: 需适配

**不同点**:
| 项目 | Pi | Cursor/Windsurf |
|------|-----|-----------------|
| 配置方式 | SKILL.md | `.cursorrules` |
| 扩展系统 | TypeScript | 无 |

**适配步骤**:

1. **创建 .cursorrules**:
   ```
   # Embedded Development Rules
   
   ## Supported Chips
   - ESP32 (S3, C3, C6, H2)
   - STM32 (F4, F7, H7, L4, U5)
   - RP2040 (Pico, Pico 2)
   - nRF52 (52832, 52840)
   
   ## Workflow
   1. Read AGENTS.md for project context
   2. Use references/*.md for detailed specs
   3. Apply modular architecture patterns
   4. Compile-flash-monitor-test loop
   
   ## Key Constraints
   - DMA: ESP32-S3 SPI max 4092 bytes
   - Memory: Respect PSRAM/SRAM limits
   ```

2. **复制参考文档**:
   ```bash
   cp -r references/ .cursor/references/
   ```

---

## MCP 替代方案详细指南

### 什么是 MCP?

MCP (Model Context Protocol) 是一种标准化的扩展协议，用于 AI Coding Agent 与外部工具通信。

### 为什么需要 MCP?

Pi 使用 TypeScript 扩展，OpenCode 使用 MCP Server。功能相同，但实现方式不同。

### MCP Server vs Pi 扩展

| 功能 | Pi 扩展 | MCP Server |
|------|---------|------------|
| 语言 | TypeScript | Python/Node.js |
| 运行环境 | Pi 内部 | 独立进程 |
| 安装 | 复制到 extensions/ | 配置 JSON |
| 工具定义 | `pi.registerTool()` | `@app.list_tools()` |

### embedded_build MCP 工具

**参数**:
```json
{
  "action": "detect|build|flash|monitor|clean|size",
  "port": "COM3|/dev/ttyUSB0",
  "baud": 115200,
  "verbose": true
}
```

**支持平台**:
- ESP-IDF (ESP32)
- STM32 (Make + OpenOCD)
- Pico SDK (RP2040)
- PlatformIO
- Arduino CLI
- Zephyr

**调用示例**:

```json
// 检测项目类型
{"action": "detect"}

// 编译项目
{"action": "build"}

// 烧录到设备
{"action": "flash", "port": "COM3"}
```

### embedded_diagnose MCP 工具

**参数**:
```json
{
  "errorOutput": "编译错误输出字符串",
  "maxSuggestions": 5
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
  ]
}
```

---

## 通用替代方案

如果您的 AI Coding Agent 不支持扩展或 MCP，可以使用以下替代方案：

### 1. TODO.md 文件

```markdown
# TODO

- [ ] Configure SPI driver
- [ ] Implement LCD init sequence
- [x] Setup build environment
```

### 2. AGENTS.md / CLAUDE.md / CONVENTIONS.md

保持项目上下文，所有 Agent 都支持某种形式的上下文文件。

### 3. 参考文档

`references/` 目录下的 Markdown 文件可直接被任何 AI 读取。

### 4. Python 脚本

`scripts/` 目录下的脚本可独立运行：

```bash
# 串口监控
python scripts/serial_monitor.py -p COM4 -d 30

# 摄像头捕获
python scripts/camera_capture.py --session

# 图像对比
python scripts/image_compare.py --before img1.png --after img2.png
```

---

## 扩展工具替代方案汇总

### image_read (图片分析)

| Agent | 替代方案 |
|-------|----------|
| **Pi** | 使用 `image-read.ts` 扩展 |
| **OpenCode** | 内置 `read` 支持图片 |
| **Claude Code** | 直接粘贴图片 |
| **Aider** | 手动描述或使用 `--message-file` |
| **Cursor** | 直接粘贴图片到聊天 |

### todo_list (任务管理)

| Agent | 替代方案 |
|-------|----------|
| **Pi** | 使用 `todo.ts` 扩展 |
| **OpenCode** | 内置 `todowrite` 工具 |
| **Claude Code** | MCP Server 或 TODO.md |
| **Aider** | TODO.md 文件 |
| **Cursor** | TODO.md 文件 |

### embedded_build (统一编译)

| Agent | 替代方案 |
|-------|----------|
| **Pi** | 使用 `build-wrapper.ts` 扩展 |
| **OpenCode** | MCP Server 或 `bash` 命令 |
| **Claude Code** | MCP Server 或 `bash` 命令 |
| **其他** | 直接使用 bash 命令 |

---

## 贡献适配方案

如果您为其他 AI Coding Agent 创建了适配方案，欢迎贡献！

1. Fork 本仓库
2. 在 `adapters/` 目录创建适配文件
3. 提交 Pull Request

---

## 版本兼容性

| Skill 版本 | Pi 版本 | OpenCode 版本 | 更新说明 |
|-----------|---------|---------------|----------|
| 3.2.0 | >= 1.0.0 | >= 1.0.0 | Dual Platform Edition |
| 3.0.0 | >= 1.0.0 | - | Pi Edition |

---

如有问题，请在 [Issues](https://github.com/lhbsaa/embedded-dev-skill/issues) 反馈。