# Embedded Development Skill - Installation Guide

本文档提供 Pi Coding Agent 和 OpenCode 的完整安装说明。

---

## Pi Coding Agent 安装

### 1. 复制 Skill 到 Pi Skills 目录

```bash
# 方式一：复制到全局 Skills 目录
cp -r embedded-dev ~/.pi/agent/skills/

# 方式二：复制到项目级 Skills 目录
cp -r embedded-dev .pi/skills/
```

### 2. 安装扩展

本 Skill 包含三个 Pi 扩展，需要安装：

```bash
# 复制扩展到 Pi 扩展目录
cp embedded-dev/extensions/image-read.ts ~/.pi/agent/extensions/
cp embedded-dev/extensions/todo.ts ~/.pi/agent/extensions/
cp embedded-dev/extensions/build-wrapper.ts ~/.pi/agent/extensions/

# 或通过 Pi 的 packages 安装
# pi install ./embedded-dev
```

### 3. 安装 Python 依赖（可选）

```bash
pip install -r embedded-dev/scripts/requirements.txt
# 包含: opencv-python, numpy, pyserial
```

### 4. 验证安装

```bash
pi
/reload
```

扩展加载后，以下工具应该可用：
- `image_read` - 图片读取分析
- `todo_list` - 任务管理
- `embedded_build` - 统一编译命令
- `/todo` 命令 - 快速任务管理
- `/build` 命令 - 快速编译

### 5. 使用 Skill

在 Pi 中直接提问嵌入式相关问题：

```
"帮我配置 ESP32-S3 的 SPI 驱动"
"STM32F4 如何配置 UART"
"帮我调试 LCD 显示问题"
```

---

## OpenCode 安装

### 方式1: 直接使用核心 Skill (推荐)

```bash
# 1. 创建 Skill 目录
mkdir -p ~/.opencode/skills/embedded-dev

# 2. 复制核心文件
cp embedded-dev/SKILL.md ~/.opencode/skills/embedded-dev/
cp -r embedded-dev/references ~/.opencode/skills/embedded-dev/
cp -r embedded-dev/scripts ~/.opencode/skills/embedded-dev/

# 3. 安装 Python 依赖
pip install -r embedded-dev/scripts/requirements.txt
```

### 方式2: 使用 OpenCode 适配器

```bash
# 1. 复制适配器文件
mkdir -p ~/.opencode/skills/embedded-dev
cp -r embedded-dev/adapters/opencode/* ~/.opencode/skills/embedded-dev/

# 2. 安装 Python 依赖
pip install -r embedded-dev/scripts/requirements.txt
```

### 方式3: 配置 MCP Server (高级)

```bash
# 1. 创建 MCP 目录
mkdir -p ~/.opencode/mcp

# 2. 复制 MCP Server
cp embedded-dev/adapters/opencode/mcp-server-embedded.py ~/.opencode/mcp/

# 3. 安装 MCP 依赖
pip install mcp pyserial

# 4. 配置 OpenCode
# 编辑 ~/.config/opencode/opencode.json
{
  "mcpServers": {
    "embedded-dev": {
      "command": "python",
      "args": ["~/.opencode/mcp/mcp-server-embedded.py"],
      "env": {}
    }
  }
}

# 5. 重启 OpenCode
opencode --reload
```

### OpenCode 使用 Skill

在 OpenCode 中直接提问：

```
"帮我配置 ESP32-S3 的 ST7789 LCD 驱动"
"编译提示格式字符串错误怎么办"
"帮我调试 LCD 显示问题"
```

---

## 文件结构

```
embedded-dev/
├── SKILL.md                    # 核心 Skill (双平台版)
├── extensions/                 # Pi 扩展
│   ├── image-read.ts           # 图片读取
│   ├── todo.ts                 # 任务管理
│   └ build-wrapper.ts         # 统一编译
├── adapters/                   # OpenCode 适配器
│   ├── README.md
│   └─ opencode/
│       ├── SKILL.md            # OpenCode 专用
│       ├── MCP-GUIDE.md        # MCP 配置指南
│       └─ mcp-server-embedded.py  # MCP Server
├── references/                 # 参考文档 (11个)
│   ├── chips.md
│   ├── hardware-interfaces.md
│   ├── protocols.md
│   ├── languages.md
│   ├── tools.md
│   ├── debugging.md
│   ├── remote-tools.md
│   ├── gui-feedback.md
│   ├── ai-patterns.md
│   ├── cases.md                # NEW: 实战案例
│   └ faq.md                   # NEW: 常见问题
└ scripts/                     # 辅助脚本 (5个)
    ├── camera_capture.py
    ├── image_compare.py
    ├── serial_monitor.py       # NEW: 串口监控
    ├── serial_monitor.ps1      # NEW: PowerShell监控
    └ requirements.txt
```

---

## 工具映射

### Pi Coding Agent

| 原 Skill 工具 | Pi 工具 | 说明 |
|--------------|---------|------|
| read_file | read | 内置 |
| write_file | write | 内置 |
| replace | edit | 内置 |
| run_shell_command | bash | 内置 |
| glob | glob | 内置 |
| search_file_content | grep | 内置 |
| image_read | image_read | 扩展 |
| todo_read/write | todo_list | 扩展 |
| save_memory | pi.appendEntry() | Pi API |

### OpenCode

| 原 Skill 工具 | OpenCode 工具 | 说明 |
|--------------|---------------|------|
| read_file | read | 内置 |
| write_file | write | 内置 |
| replace | edit | 内置 |
| run_shell_command | bash | 内置 |
| glob | glob | 内置 |
| search_file_content | grep | 内置 |
| image_read | read (图片) | 内置 |
| todo_read/write | todowrite | 内置 |
| embedded_build | embedded_build | MCP |

---

## Pi 特有功能

### Session Tree（会话树）
调试时可以使用 Pi 的会话树功能：
- `Escape` 两次 → 打开 `/tree` 导航
- 在任意历史点继续对话
- `/fork` 创建新分支
- `Shift+L` 标签书签

### 状态持久化
使用 `pi.appendEntry()` 保存状态：
- todo 列表自动持久化
- 会话恢复时自动加载

### AGENTS.md 自动加载
Pi 启动时自动加载项目根目录的 AGENTS.md，用于存储：
- 项目硬件配置
- 已解决的方案
- 芯片特定注意事项

---

## 新功能使用 (v3.2.0)

### 实战案例库

```bash
# 查看案例
# 在 AI 中直接读取
read references/cases.md
```

案例包括：
- ESP32-S3 LCD驱动内存溢出
- 格式字符串编译错误
- UART缓冲区溢出安全漏洞
- LCD初始化重试机制
- 数据验证安全性
- 多任务堆栈溢出

### FAQ 快速排错

```bash
# 查看常见问题
read references/faq.md
```

20个常见问题涵盖：
- 编译相关 (4个)
- 内存相关 (3个)
- LCD显示 (3个)
- 通信协议 (3个)
- 调试相关 (3个)
- 硬件相关 (2个)
- 性能优化 (2个)

### 串口监控脚本

```bash
# Python 版 (跨平台)
python scripts/serial_monitor.py --detect --duration 30
python scripts/serial_monitor.py -p COM4 -f E --module LCD
python scripts/serial_monitor.py -p COM4 --json

# PowerShell 版 (Windows)
.\scripts\serial_monitor.ps1 -Port COM4 -Duration 10
```

---

## 故障排除

### Pi 扩展未加载

```bash
# 检查扩展目录
ls ~/.pi/agent/extensions/

# 重新加载
pi
/reload
```

### OpenCode MCP Server 无法启动

```bash
# 检查 Python 环境
python --version  # 需要 >= 3.8

# 检查 MCP 包
pip show mcp

# 手动测试
python ~/.opencode/mcp/mcp-server-embedded.py
```

### 工具不可用

检查日志：
```bash
# Pi
cat ~/.pi/agent/log/latest.log | grep -i error

# OpenCode
opencode --debug
```

### Python 脚本报错

```bash
# 确保依赖已安装
pip install -r scripts/requirements.txt

# 测试摄像头
python scripts/camera_capture.py --list

# 测试串口
python scripts/serial_monitor.py --list
```

---

## 快速验证

### Pi

```bash
pi
/reload
"帮我检测当前项目类型"
# embedded_build 工具应可用
```

### OpenCode

```bash
opencode
"列出可用的嵌入式开发参考文档"
# 应列出 references/ 下的文件
```

---

Version: 2.0
Updated: 2026-04-13
Compatible: Pi Coding Agent >= 1.0.0, OpenCode >= 1.0.0