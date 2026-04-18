# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.3.0] - 2026-04-18

### Added - Superpowers Integration

借鉴 [Superpowers](https://github.com/obra/superpowers) (by Jesse Vincent) 的强制门控机制和模块化设计。

#### P0: 强制门控机制
- **Iron Law**: 编译优先验证强制门控 - `NO CODE WITHOUT BUILD-FIRST VERIFICATION`
- **Red Flags**: 12个停止信号 + 7个症状信号 - 硬件开发危险信号列表
- **Rationalization Table**: 11个借口反驳表 - 嵌入式开发常见借口及反驳
- **Verification Gate**: 5步验证流程 + Claim Types 表格 - 证据优先声明

#### P1: Hooks + Prompts 分离
- **Hooks SessionStart**: 关键词触发自动注入嵌入式上下文
- **hooks/hooks.json**: 嵌入式关键词触发配置
- **hooks/session-start.cmd**: Windows PowerShell 启动脚本
- **prompts/driver-generator.md**: 驱动代码生成 Prompt（含 DMA 约束模板）
- **prompts/hardware-validator.md**: 硬件规范评审 Prompt（DMA ≤4092 检查）
- **prompts/code-quality.md**: MISRA C 质量评审 Prompt
- **prompts/debugging.md**: 嵌入式调试 Prompt（4阶段系统调试）

#### P2: Skill Chain 链式调用
- **skills/embedded-brainstorming/**: 硬件需求分析 + HARD-GATE
- **skills/embedded-driver-design/**: 实现计划创建（不生成代码）
- **skills/embedded-implementation/**: 代码执行 + 两阶段评审
- **skills/embedded-verification/**: build-flash-monitor 强制验证
- **skills/embedded-gui-feedback/**: LCD 视觉分析
- **Two-Stage Review**: 硬件规范评审 + MISRA C 评审流程

#### P3: Token 效率优化
- **workflow.md**: 详细6阶段工作流独立文件（Verification Report 模板）
- **examples.md**: 7个实战案例独立文件
- **SKILL.md 精简**: 保留核心，链接外部文件

### Changed
- **SKILL.md**: 
  - Description 优化为纯触发条件 + symptom 关键词
  - Phase 4 Verification 改为 Verification Gate 5步流程
  - 新增 Skill Chain 引用、Prompts/Hooks 引用表格
  - Workflow/Examples 部分精简，链接外部文件
- **VERSION_HISTORY.md**: 添加 P0-P3 详细改进记录

### Design Philosophy
借鉴 Superpowers 核心概念：
- **Iron Law**: "Violating the letter is violating the spirit" → 嵌入式编译强制
- **HARD-GATE**: 每个 skill 有强制门控
- **No Code in Design Phase**: driver-design 只创建计划
- **No Placeholders**: 计划中不能有 TBD/TODO
- **Two-Stage Review**: 规范合规 + 代码质量 → 硬件规范 + MISRA C

### Files Added
```
hooks/: 2 files
prompts/: 4 files  
skills/: 5 skill directories
workflow.md: 1 file
examples.md: 1 file
Total: 13 new files
```

## [3.2.0] - 2026-04-13

### Added
- **Dual Platform Support**: 同时支持 Pi Coding Agent 和 OpenCode
- **Real-World Cases**: 新增 `references/cases.md` - 6个实战案例
  - ESP32-S3 LCD驱动内存溢出
  - 格式字符串编译错误诊断
  - UART缓冲区溢出安全漏洞
  - LCD初始化重试机制失效
  - 数据验证安全性不足
  - 多任务堆栈溢出风险
- **FAQ**: 新增 `references/faq.md` - 20个常见问题快速解答
- **Serial Monitor**: 新增 `scripts/serial_monitor.py` - AI友好的串口监控
  - ESP-IDF 日志格式解析
  - 错误模式自动检测
  - JSON 结构化输出
- **PowerShell Monitor**: 新增 `scripts/serial_monitor.ps1` - Windows 备用脚本
- **OpenCode Adapter**: 新增 `adapters/opencode/` 目录
  - OpenCode 专用 SKILL.md
  - MCP-GUIDE.md 配置指南
  - mcp-server-embedded.py MCP Server 实现
- **MCP Server**: Python MCP Server 实现
  - `embedded_build` 统一编译命令
  - `embedded_diagnose` 编译错误诊断

### Changed
- **SKILL.md**: 从 Pi 单平台升级到 Pi + OpenCode 双平台
- **README.md**: 添加双平台说明和 OpenCode 安装指南
- **COMPATIBILITY.md**: 大幅扩展 MCP 替代方案详细说明
- **INSTALL.md**: 添加 OpenCode 安装方式
- **VERSION_HISTORY.md**: 合并自用版本的质量评分系统
- **package.json**: version 3.1 → 3.2, keywords 添加 opencode
- **requirements.txt**: 添加 pyserial 依赖

### Merged
- 合并开源版本 (skills/embedded-dev) 与自用版本 (skills-a/embedded-dev)
- 案例库已脱敏处理移除项目名称

## [3.1.0] - 2026-04-10

### Added
- **Extensions**: 新增 `build-wrapper.ts` 扩展实现统一编译命令
- **Documentation**: 新增 `Embedded-Build-Environment-AI-Interface.md` 编译环境 AI 接口探究文档

### Changed
- **SKILL.md**: 添加 build-wrapper 扩展说明
- **Extension Tools**: 扩展工具表格新增 build_wrapper

## [3.0.0] - 2026-04-10

### Added
- **Pi Edition**: 完全适配 Pi Coding Agent
- **Extensions**: 新增 `image-read.ts` 扩展实现图片读取
- **Extensions**: 新增 `todo.ts` 扩展实现任务管理
- **Pi Features**: 支持 Session Tree 调试回溯
- **Pi Features**: 支持 `pi.appendEntry()` 状态持久化
- **Documentation**: 新增 `INSTALL.md` 安装说明
- **Documentation**: 新增 `README.md` GitHub 入口文档
- **Documentation**: 新增 `CONTRIBUTING.md` 贡献指南
- **Documentation**: 新增 `LICENSE` MIT 许可证
- **GitHub**: 完整的开源项目文件结构

### Changed
- **Tools**: 工具名称映射到 Pi 内置工具
  - `read_file` → `read`
  - `write_file` → `write`
  - `replace` → `edit`
  - `run_shell_command` → `bash`
  - `search_file_content` → `grep`
- **SKILL.md**: 更新所有示例使用 Pi 工具名称
- **SKILL.md**: 添加 Pi 特性使用说明

## [2.2.0] - 2026-04-09

### Added
- **Security Checklist**: 部署前安全检查清单
- **GUI Scripts**: 摄像头捕获和图像对比脚本
- **Progressive Loading**: 渐进式加载架构

### Changed
- 优化文档结构
- 更新硬件接口规范

## [2.0.0] - 2026-04-08

### Added
- **References**: 完整的参考文档体系
  - `chips.md` - 芯片规格
  - `hardware-interfaces.md` - 硬件接口
  - `protocols.md` - 通信协议
  - `languages.md` - 编程规范
  - `tools.md` - 开发工具
  - `debugging.md` - 调试策略
  - `remote-tools.md` - 远程调试
  - `gui-feedback.md` - GUI 反馈
  - `ai-patterns.md` - AI 集成模式
- **Scripts**: Python 辅助脚本
  - `camera_capture.py` - 摄像头捕获
  - `image_compare.py` - 图像对比

### Changed
- 重构为渐进式加载架构
- 核心指令保持在 SKILL.md

## [1.0.0] - 2026-04-01

### Added
- 初始版本
- 支持 ESP32, STM32, RP2040, nRF52
- 基础工作流程定义
- 硬件接口快速参考表
- 跨平台命令对照

---

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| 3.2.0 | 2026-04-13 | Dual Platform + Cases + FAQ + Serial Monitor + MCP Server |
| 3.1.0 | 2026-04-10 | Build Wrapper Extension + AI Interface Doc |
| 3.0.0 | 2026-04-10 | Pi Edition - 完整适配 + 扩展 |
| 2.2.0 | 2026-04-09 | Security Checklist + GUI Scripts |
| 2.0.0 | 2026-04-08 | Progressive Loading Architecture |
| 1.0.0 | 2026-04-01 | Initial Release |