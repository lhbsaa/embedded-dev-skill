# Embedded Development Skill - Installation Guide

## Pi Coding Agent 安装说明

### 1. 复制 Skill 到 Pi Skills 目录

```bash
# 方式一：复制到全局 Skills 目录
cp -r embedded-dev ~/.pi/agent/skills/

# 方式二：复制到项目级 Skills 目录
cp -r embedded-dev .pi/skills/
```

### 2. 安装扩展

本 Skill 包含两个 Pi 扩展，需要安装：

```bash
# 复制扩展到 Pi 扩展目录
cp embedded-dev/extensions/image-read.ts ~/.pi/agent/extensions/
cp embedded-dev/extensions/todo.ts ~/.pi/agent/extensions/
```

### 3. 安装 Python 依赖（可选，用于 GUI 视觉反馈）

```bash
pip install -r embedded-dev/scripts/requirements.txt
```

### 4. 验证安装

```bash
pi
/reload
```

扩展加载后，以下工具应该可用：
- `image_read` - 图片读取分析
- `todo_list` - 任务管理
- `/todo` 命令 - 快速任务管理

### 5. 使用 Skill

在 Pi 中直接提问嵌入式相关问题，Skill 会自动加载：

```
"帮我配置 ESP32-S3 的 SPI 驱动"
"STM32F4 如何配置 UART"
"帮我调试 LCD 显示问题"
```

## 文件结构

```
embedded-dev/
├── SKILL.md                    # 核心 Skill 定义 (Pi Edition)
├── extensions/
│   ├── image-read.ts           # 图片读取扩展
│   └── todo.ts                 # 任务管理扩展
├── references/
│   ├── chips.md                # 芯片规格
│   ├── hardware-interfaces.md  # 硬件接口
│   ├── protocols.md            # 通信协议
│   ├── languages.md            # 编程规范
│   ├── tools.md                # 开发工具
│   ├── remote-tools.md         # 远程调试
│   ├── debugging.md            # 调试策略
│   ├── gui-feedback.md         # GUI 反馈
│   └── ai-patterns.md          # AI 集成
└── scripts/
    ├── camera_capture.py       # 摄像头捕获
    ├── image_compare.py        # 图像对比
    └── requirements.txt        # Python 依赖
```

## Pi 工具映射

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

## 故障排除

### 扩展未加载
```bash
# 检查扩展目录
ls ~/.pi/agent/extensions/

# 重新加载
pi
/reload
```

### 工具不可用
检查日志：
```bash
cat ~/.pi/agent/log/latest.log | grep -i error
```

### Python 脚本报错
```bash
# 确保 OpenCV 已安装
pip install opencv-python numpy

# 测试摄像头
python scripts/camera_capture.py --list
```

---
Version: 1.0
Compatible: Pi Coding Agent >= 1.0.0
