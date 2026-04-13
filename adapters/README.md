# Embedded Development Skill Adapters

本目录包含 Embedded Development Skill 在不同 AI Coding Agent 上的适配器。

---

## 目录结构

```
adapters/
├── README.md                   # 本文件
└── opencode/                   # OpenCode 适配器
    ├── SKILL.md                # OpenCode 专用 Skill 文件
    ├── MCP-GUIDE.md            # MCP 配置指南
    └── mcp-server-embedded.py  # Python MCP Server 实现
```

---

## 支持的 Agent

| Agent | 适配状态 | 适配器位置 |
|-------|----------|-----------|
| **Pi Coding Agent** | ✅ 原生支持 | 无需适配器，使用主目录 |
| **OpenCode** | ✅ 完整适配 | `adapters/opencode/` |
| **Claude Code** | ⚠️ 部分适配 | 参见 COMPATIBILITY.md |
| **Cursor/Windsurf** | ⚠️ 部分适配 | 参见 COMPATIBILITY.md |

---

## 如何使用适配器

### Pi Coding Agent (原生)

直接使用主目录的 Skill：

```bash
# 安装
cp -r skills/embedded-dev ~/.pi/agent/skills/
cp skills/embedded-dev/extensions/*.ts ~/.pi/agent/extensions/

# 使用
pi
"帮我配置 ESP32-S3 的 ST7789 LCD 驱动"
```

### OpenCode

使用 OpenCode 适配器：

```bash
# 方式1: 直接使用核心 Skill (推荐)
cp skills/embedded-dev/SKILL.md ~/.opencode/skills/embedded-dev/
cp -r skills/embedded-dev/references ~/.opencode/skills/embedded-dev/

# 方式2: 使用完整适配器
cp -r skills/embedded-dev/adapters/opencode/* ~/.opencode/skills/embedded-dev/

# 方式3: 配置 MCP Server (高级)
cp skills/embedded-dev/adapters/opencode/mcp-server-embedded.py ~/.opencode/mcp/
# 参考 MCP-GUIDE.md 配置 MCP Server
```

---

## 适配器说明

### OpenCode 适配器 (`opencode/`)

OpenCode 使用 MCP (Model Context Protocol) 作为扩展机制，与 Pi 的 TypeScript 扩展不同。

**提供的文件**:

| 文件 | 用途 |
|------|------|
| `SKILL.md` | OpenCode 专用 Skill，移除 Pi 特定内容 |
| `MCP-GUIDE.md` | MCP Server 配置详细指南 |
| `mcp-server-embedded.py` | Python MCP Server 实现 |

**MCP Server 功能**:

- `embedded_build`: 统一编译命令 (替代 build-wrapper.ts)
- `embedded_diagnose`: 编译错误诊断 (替代 build-wrapper.ts)
- `todo_list`: 任务管理 (替代 todo.ts)
- `image_read`: 图片分析 (替代 image-read.ts)

---

## 核心文件兼容性

以下核心文件在所有 Agent 上通用：

| 文件 | 兼容性 | 说明 |
|------|--------|------|
| `references/*.md` | ✅ 100% | Markdown 文件，所有 Agent 可读取 |
| `scripts/*.py` | ✅ 100% | Python 脚本，独立运行 |
| `scripts/*.ps1` | ✅ Windows | PowerShell 脚本 |
| `SKILL.md` | ⚠️ 部分 | Pi 特定内容需移除 |
| `extensions/*.ts` | ❌ Pi Only | TypeScript 扩展仅 Pi 支持 |

---

## 贡献适配器

如果您为其他 Agent 创建了适配器，欢迎贡献：

1. 在 `adapters/` 下创建新目录 (如 `adapters/claude-code/`)
2. 包含必要的适配文件
3. 提交 Pull Request

---

Version: 1.0
Updated: 2026-04-13