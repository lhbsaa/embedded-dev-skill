# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
| 3.0.0 | 2026-04-10 | Pi Edition - 完整适配 + 扩展 |
| 2.2.0 | 2026-04-09 | Security Checklist + GUI Scripts |
| 2.0.0 | 2026-04-08 | Progressive Loading Architecture |
| 1.0.0 | 2026-04-01 | Initial Release |
