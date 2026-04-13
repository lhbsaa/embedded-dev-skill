# Embedded Development Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pi Compatible](https://img.shields.io/badge/Pi-Compatible-green.svg)](https://github.com/badlogic/pi-mono)
[![OpenCode Compatible](https://img.shields.io/badge/OpenCode-Compatible-blue.svg)](https://opencode.ai)
[![Version](https://img.shields.io/badge/version-3.2-purple.svg)](https://github.com/lhbsaa/embedded-dev-skill)

AI辅助嵌入式系统开发的专项技能，支持 **Pi Coding Agent** 和 **OpenCode** 双平台。

## 特性

- **双平台支持**: Pi Coding Agent + OpenCode
- **多芯片支持**: ESP32, STM32, RP2040, nRF52 系列
- **硬件接口**: SPI, I2C, UART, GPIO, ADC, PWM 配置模板
- **通信协议**: Wi-Fi, TCP/IP, HTTP, MQTT, BLE, Modbus
- **GUI视觉反馈**: 摄像头捕获 + 图像分析
- **串口监控**: AI友好的日志解析
- **实战案例**: 6个真实项目案例分析
- **FAQ**: 20个常见问题快速解答
- **任务管理**: 内置 todo 扩展
- **渐进式加载**: 核心轻量，按需加载详细文档
- **跨平台**: Windows, Linux, macOS

## 快速开始

### Pi Coding Agent 安装

```bash
# 克隆仓库
git clone https://github.com/lhbsaa/embedded-dev-skill.git

# 复制到 Pi 目录
cp -r embedded-dev-skill ~/.pi/agent/skills/embedded-dev
cp embedded-dev-skill/extensions/*.ts ~/.pi/agent/extensions/

# 安装 Python 依赖（可选，用于 GUI 反馈）
pip install -r embedded-dev-skill/scripts/requirements.txt
```

### OpenCode 安装

```bash
# 克隆仓库
git clone https://github.com/lhbsaa/embedded-dev-skill.git

# 复制到 OpenCode 目录
mkdir -p ~/.opencode/skills/embedded-dev
cp -r embedded-dev-skill/SKILL.md embedded-dev-skill/references embedded-dev-skill/scripts ~/.opencode/skills/embedded-dev/

# 安装 Python 依赖
pip install -r embedded-dev-skill/scripts/requirements.txt

# (可选) 配置 MCP Server
cp embedded-dev-skill/adapters/opencode/mcp-server-embedded.py ~/.opencode/mcp/
```

### 使用

在 Pi 或 OpenCode 中直接提问嵌入式相关问题：

```
"帮我配置 ESP32-S3 的 ST7789 LCD 驱动"
"STM32F4 如何配置 UART DMA"
"帮我调试 LCD 显示问题"
"编译提示格式字符串错误怎么办"
```

## 支持的芯片

| 系列 | 典型型号 | 框架 | 特点 |
|------|----------|------|------|
| **ESP32** | S3, C3, C6, H2 | ESP-IDF, Arduino | Wi-Fi, LCD, AI |
| **STM32** | F4, F7, H7, L4, U5 | STM32CubeIDE | 高性能, DSP |
| **RP2040** | Pico, Pico 2 | Pico SDK | 低成本, PIO |
| **nRF52** | 52832, 52840 | nRF5 SDK | BLE, 低功耗 |

## 目录结构

```
embedded-dev/
├── SKILL.md                # 核心 Skill 定义 (双平台版)
├── README.md               # GitHub 入口文档
├── INSTALL.md              # 安装说明 (Pi + OpenCode)
├── CHANGELOG.md            # 变更日志
├── VERSION_HISTORY.md      # 版本历程
├── COMPATIBILITY.md        # 多 Agent 兼容指南
├── LICENSE                 # MIT 许可证
├── package.json            # Pi Package 配置
├── extensions/             # Pi 扩展
│   ├── image-read.ts       # 图片读取
│   ├── todo.ts             # 任务管理
│   └── build-wrapper.ts    # 统一编译
├── adapters/               # Agent 适配器
│   ├── README.md           # 适配器概览
│   └─ opencode/            # OpenCode 适配器
│       ├── SKILL.md        # OpenCode 专用 Skill
│       ├── MCP-GUIDE.md    # MCP 配置指南
│       └─ mcp-server-embedded.py  # MCP Server
├── references/             # 详细参考文档 (11个)
│   ├── chips.md            # 芯片规格
│   ├── hardware-interfaces.md  # 硬件接口
│   ├── protocols.md        # 通信协议
│   ├── languages.md        # 编程规范
│   ├── tools.md            # 开发工具
│   ├── debugging.md        # 调试策略
│   ├── remote-tools.md     # 远程调试
│   ├── gui-feedback.md     # GUI 反馈
│   ├── ai-patterns.md      # AI 集成
│   ├── cases.md            # 实战案例 (NEW)
│   └─ faq.md               # 常见问题 (NEW)
└── scripts/                # 辅助脚本 (5个)
    ├── camera_capture.py   # 摄像头捕获
    ├── image_compare.py    # 图像对比
    ├── serial_monitor.py   # 串口监控 (NEW)
    ├── serial_monitor.ps1  # PowerShell 监控 (NEW)
    └── requirements.txt    # Python 依赖
```

## 工具映射

### Pi Coding Agent

| 功能 | Pi 工具 | 类型 |
|------|---------|------|
| 读取文件 | `read` | 内置 |
| 写入文件 | `write` | 内置 |
| 编辑代码 | `edit` | 内置 |
| 执行命令 | `bash` | 内置 |
| 查找文件 | `glob` | 内置 |
| 搜索内容 | `grep` | 内置 |
| 图片分析 | `image_read` | 扩展 |
| 任务管理 | `todo_list` | 扩展 |
| 统一编译 | `embedded_build` | 扩展 |

### OpenCode

| 功能 | OpenCode 工具 | 类型 |
|------|---------------|------|
| 读取文件 | `read` | 内置 |
| 写入文件 | `write` | 内置 |
| 编辑代码 | `edit` | 内置 |
| 执行命令 | `bash` | 内置 |
| 查找文件 | `glob` | 内置 |
| 搜索内容 | `grep` | 内置 |
| 图片分析 | `read` | 内置 |
| 任务管理 | `todowrite` | 内置 |
| 统一编译 | `embedded_build` | MCP |

## 新特性 (v3.2.0)

### 实战案例库 (`references/cases.md`)
- Case 1: ESP32-S3 LCD驱动内存溢出问题
- Case 2: 格式字符串编译错误诊断
- Case 3: UART缓冲区溢出安全漏洞
- Case 4: LCD初始化重试机制失效
- Case 5: 数据验证安全性不足
- Case 6: 多任务堆栈溢出风险

### 常见问题 FAQ (`references/faq.md`)
- 20个常见问题快速解答
- 编译、内存、LCD、通信、调试、硬件、性能分类

### 串口监控脚本 (`scripts/serial_monitor.py`)
- AI友好的 JSON 输出
- ESP-IDF 日志格式解析
- 错误模式自动检测
- Windows PowerShell 替代脚本

### OpenCode 适配器 (`adapters/opencode/`)
- OpenCode 专用 Skill
- MCP Server 实现
- 详细配置指南

## 示例

### LCD 驱动配置
```
User: "Configure ST7789 LCD, 240×240, SPI"

Pi/OpenCode 会自动:
1. 读取项目 AGENTS.md 了解硬件配置
2. 加载 references/chips.md 获取 ESP32-S3 SPI 配置
3. 生成驱动代码 (write)
4. 编译烧录 (bash: idf.py build flash)
5. 视觉反馈验证 (image_read/read)
```

### 快速排错
```
User: "编译提示格式字符串错误"

步骤:
1. read references/faq.md → Q1
2. 使用 %lu 或 PRIu32 宏
3. bash: idf.py build
```

### 调试会话回溯 (Pi)
使用 Pi 的 Session Tree 功能：
- `Escape` 两次 → 打开 `/tree` 导航
- 在任意历史点继续对话
- `/fork` 创建新分支

## 文档

- [安装说明](INSTALL.md)
- [变更日志](CHANGELOG.md)
- [版本历程](VERSION_HISTORY.md)
- [兼容性指南](COMPATIBILITY.md)
- [适配器说明](adapters/README.md)
- [OpenCode MCP 配置](adapters/opencode/MCP-GUIDE.md)

## 兼容性

### Pi Coding Agent
- **状态**: ✅ 完全支持
- **版本**: >= 1.0.0
- **Node.js**: >= 18.0.0 (用于扩展)
- **Python**: >= 3.8 (用于 GUI 脚本，可选)

### OpenCode
- **状态**: ✅ 完全支持
- **版本**: >= 1.0.0
- **Python**: >= 3.8 (用于脚本)
- **MCP**: 可选 (高级功能)

### 其他 AI Coding Agent

| Agent | 状态 | 说明 |
|-------|------|------|
| **Pi** | ✅ 完全支持 | 原生支持，使用扩展 |
| **OpenCode** | ✅ 完全支持 | 使用 MCP 或内置工具 |
| **Claude Code** | ⚠️ 需适配 | 工具名称兼容，见兼容指南 |
| **Cursor/Windsurf** | ⚠️ 需适配 | 需转换为 .cursorrules 格式 |

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

[MIT License](LICENSE)

## 作者

- GitHub: [@lhbsaa](https://github.com/lhbsaa)

## 致谢

- [Pi Coding Agent](https://github.com/badlogic/pi-mono) - Mario Zechner
- [OpenCode](https://opencode.ai)
- [ESP-IDF](https://github.com/espressif/esp-idf) - Espressif
- [STM32Cube](https://www.st.com/stm32cube) - STMicroelectronics