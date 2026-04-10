# Embedded Development Skill for Pi Coding Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pi Compatible](https://img.shields.io/badge/Pi-Compatible-green.svg)](https://github.com/badlogic/pi-mono)
[![Version](https://img.shields.io/badge/version-3.0-blue.svg)](https://github.com/lhbsaa/embedded-dev-skill)

AI辅助嵌入式系统开发的专项技能，专为 [Pi Coding Agent](https://github.com/badlogic/pi-mono) 设计。

## 特性

- **多芯片支持**: ESP32, STM32, RP2040, nRF52 系列
- **硬件接口**: SPI, I2C, UART, GPIO, ADC, PWM 配置模板
- **通信协议**: Wi-Fi, TCP/IP, HTTP, MQTT, BLE, Modbus
- **GUI视觉反馈**: 摄像头捕获 + 图像分析
- **任务管理**: 内置 todo 扩展
- **渐进式加载**: 核心轻量，按需加载详细文档
- **跨平台**: Windows, Linux, macOS

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/lhbsaa/embedded-dev-skill.git

# 复制到 Pi 目录
cp -r embedded-dev-skill ~/.pi/agent/skills/embedded-dev
cp embedded-dev-skill/extensions/*.ts ~/.pi/agent/extensions/

# 安装 Python 依赖（可选，用于 GUI 反馈）
pip install -r embedded-dev-skill/scripts/requirements.txt
```

### 使用

在 Pi 中直接提问嵌入式相关问题：

```
"帮我配置 ESP32-S3 的 ST7789 LCD 驱动"
"STM32F4 如何配置 UART DMA"
"帮我调试 LCD 显示问题"
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
├── SKILL.md                # 核心 Skill 定义
├── extensions/             # Pi 扩展
│   ├── image-read.ts       # 图片读取
│   └── todo.ts             # 任务管理
├── references/             # 详细参考文档
│   ├── chips.md            # 芯片规格
│   ├── hardware-interfaces.md  # 硬件接口
│   ├── protocols.md        # 通信协议
│   ├── languages.md        # 编程规范
│   ├── tools.md            # 开发工具
│   ├── debugging.md        # 调试策略
│   ├── remote-tools.md     # 远程调试
│   ├── gui-feedback.md     # GUI 反馈
│   └── ai-patterns.md      # AI 集成
└── scripts/                # 辅助脚本
    ├── camera_capture.py   # 摄像头捕获
    ├── image_compare.py    # 图像对比
    └── requirements.txt    # Python 依赖
```

## 工具映射

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

## 示例

### LCD 驱动配置

```
User: "Configure ST7789 LCD, 240×240, SPI"

Pi 会自动:
1. 读取项目 AGENTS.md 了解硬件配置
2. 加载 references/chips.md 获取 ESP32-S3 SPI 配置
3. 生成驱动代码 (write)
4. 编译烧录 (bash: idf.py build flash)
5. 视觉反馈验证 (image_read)
```

### 调试会话回溯

使用 Pi 的 Session Tree 功能：
- `Escape` 两次 → 打开 `/tree` 导航
- 在任意历史点继续对话
- `/fork` 创建新分支

## 文档

- [安装说明](INSTALL.md)
- [变更日志](CHANGELOG.md)
- [贡献指南](CONTRIBUTING.md)

## 兼容性

### Pi Coding Agent
- **状态**: ✅ 完全支持
- **版本**: >= 1.0.0
- **Node.js**: >= 18.0.0 (用于扩展)
- **Python**: >= 3.8 (用于 GUI 脚本，可选)

### 其他 AI Coding Agent

本 Skill 可适配其他 AI Coding Agent，详见 [COMPATIBILITY.md](COMPATIBILITY.md)。

| Agent | 状态 | 说明 |
|-------|------|------|
| **Pi** | ✅ 完全支持 | 原生支持，无需修改 |
| **OpenCode** | ⚠️ 需适配 | 工具名称不同，见兼容指南 |
| **Claude Code** | ⚠️ 需适配 | 工具名称不同，见兼容指南 |
| **Aider** | ⚠️ 需适配 | 工具名称不同，见兼容指南 |
| **Cursor/Windsurf** | ⚠️ 需适配 | 需转换为 .cursorrules 格式 |

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

[MIT License](LICENSE)

## 作者

- GitHub: [@lhbsaa](https://github.com/lhbsaa)

## 致谢

- [Pi Coding Agent](https://github.com/badlogic/pi-mono) - Mario Zechner
- [ESP-IDF](https://github.com/espressif/esp-idf) - Espressif
- [STM32Cube](https://www.st.com/stm32cube) - STMicroelectronics
