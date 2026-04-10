# Compatibility Guide

本文档说明如何将 Embedded Development Skill 适配到不同的 AI Coding Agent。

## 概述

本 Skill 原生设计用于 **Pi Coding Agent**，但由于采用了标准的 Skill 结构，可以适配到其他 AI Coding Agent。

## 工具名称映射

不同 AI Coding Agent 使用不同的工具名称，需要进行映射：

### Pi → 其他 Agent 工具映射表

| 功能 | Pi | OpenCode | Claude Code | Aider |
|------|-----|----------|-------------|-------|
| 读取文件 | `read` | `read` | `read` | `read` |
| 写入文件 | `write` | `write` | `write` | `write` |
| 编辑代码 | `edit` | `edit` | `edit` | `edit` |
| 执行命令 | `bash` | `bash` | `bash` | `bash` |
| 查找文件 | `glob` | `glob` | `glob` | `glob` |
| 搜索内容 | `grep` | `grep` | `grep` | `grep` |

**结论**: 大部分工具名称相同，主要差异在扩展工具。

## 适配指南

### Pi Coding Agent ✅

**状态**: 原生支持，无需修改

```bash
# 安装
cp -r embedded-dev-skill ~/.pi/agent/skills/
cp extensions/*.ts ~/.pi/agent/extensions/
```

### OpenCode ⚠️

**状态**: 需适配

**相同点**:
- 核心工具名称相同 (`read`, `write`, `edit`, `bash`, `glob`, `grep`)
- 支持 AGENTS.md 上下文文件
- 支持自定义命令

**不同点**:
| 项目 | Pi | OpenCode |
|------|-----|----------|
| 扩展系统 | TypeScript 扩展 | MCP Server |
| 配置文件 | `~/.pi/agent/` | `~/.config/opencode/` |
| 图片支持 | 扩展实现 | 内置 `webfetch` |
| 任务管理 | 扩展实现 | 需 MCP |

**适配步骤**:

1. **核心 Skill**: SKILL.md 可直接使用，工具名称兼容

2. **扩展转换**: 需要将 Pi 扩展转换为 MCP Server 或使用替代方案

   ```bash
   # image_read 替代方案
   # 使用 OpenCode 内置能力
   # 用户手动截图后让 AI 分析

   # todo_list 替代方案
   # 使用 OpenCode 的 /compact 或外部工具
   ```

3. **配置路径**:
   ```bash
   # OpenCode 配置目录
   ~/.config/opencode/opencode.json
   ~/.config/opencode/AGENTS.md
   ```

4. **安装**:
   ```bash
   # 复制 references 到项目目录
   cp -r references/ .opencode/references/
   cp SKILL.md .opencode/SKILL.md
   ```

### Claude Code ⚠️

**状态**: 需适配

**相同点**:
- 核心工具名称相同
- 支持 CLAUDE.md (等同于 AGENTS.md)

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
   - image_read: 使用 `mcp-server-filesystem` 或手动截图
   - todo_list: 使用第三方 MCP server 或文本文件

3. **安装**:
   ```bash
   # 复制到 Claude Code 目录
   cp -r references/ ~/.claude/embedded-dev/
   cp SKILL.md ~/.claude/embedded-dev/
   ```

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
   - image_read: 用户手动描述或粘贴图片
   - todo_list: 使用文本文件或外部工具

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
   ```

2. **复制参考文档**:
   ```bash
   cp -r references/ .cursor/references/
   ```

## 扩展工具替代方案

### image_read (图片读取分析)

| Agent | 替代方案 |
|-------|----------|
| **Pi** | 使用 `image-read.ts` 扩展 |
| **OpenCode** | 内置 `webfetch` 或手动描述 |
| **Claude Code** | 直接粘贴图片（Claude 支持图片输入） |
| **Aider** | 手动描述或使用 `--message-file` |
| **Cursor** | 直接粘贴图片到聊天 |

### todo_list (任务管理)

| Agent | 替代方案 |
|-------|----------|
| **Pi** | 使用 `todo.ts` 扩展 |
| **OpenCode** | 使用 MCP server 或文本文件 |
| **Claude Code** | 使用 MCP server 或 TODO.md 文件 |
| **Aider** | 使用 TODO.md 文件 |
| **Cursor** | 使用 TODO.md 文件 |

## 通用替代方案

如果您的 AI Coding Agent 不支持扩展，可以使用以下替代方案：

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

## 贡献适配方案

如果您为其他 AI Coding Agent 创建了适配方案，欢迎贡献！

1. Fork 本仓库
2. 在 `adapters/` 目录创建适配文件
3. 提交 Pull Request

## 版本兼容性

| Skill 版本 | Pi 版本 | 更新说明 |
|-----------|---------|----------|
| 3.0.0 | >= 1.0.0 | Pi Edition |
| 2.2.0 | - | 通用版本 |

---

如有问题，请在 [Issues](https://github.com/lhbsaa/embedded-dev-skill/issues) 反馈。
