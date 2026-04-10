# Version History

本文档记录 Embedded Development Skill 的完整版本历程，供后续更新参考。

---

## 当前版本

**Version**: 3.0.0  
**Release Date**: 2026-04-10  
**Codename**: Pi Edition  

---

## 版本历程

### v3.0.0 - Pi Edition (2026-04-10)

**里程碑**: 完全适配 Pi Coding Agent，开源发布

#### 新增 (Added)

| 类别 | 内容 | 文件 |
|------|------|------|
| Pi适配 | 工具名称映射到 Pi 内置工具 | SKILL.md |
| 扩展 | `image-read.ts` 图片读取扩展 | extensions/ |
| 扩展 | `todo.ts` 任务管理扩展 | extensions/ |
| Pi特性 | Session Tree 调试回溯支持 | SKILL.md |
| Pi特性 | `pi.appendEntry()` 状态持久化 | extensions/todo.ts |
| 文档 | `README.md` GitHub 入口文档 | / |
| 文档 | `INSTALL.md` 安装说明 | / |
| 文档 | `CONTRIBUTING.md` 贡献指南 | / |
| 文档 | `LICENSE` MIT 许可证 | / |
| 文档 | `CHANGELOG.md` 变更日志 | / |
| 文档 | `COMPATIBILITY.md` 多 Agent 兼容指南 | / |
| 文档 | `VERSION_HISTORY.md` 版本历程 | / |
| 配置 | `package.json` Pi Package 配置 | / |
| 配置 | `.gitignore` Git 忽略规则 | / |

#### 变更 (Changed)

| 类别 | 原内容 | 新内容 |
|------|--------|--------|
| 工具名称 | `read_file` | `read` |
| 工具名称 | `write_file` | `write` |
| 工具名称 | `replace` | `edit` |
| 工具名称 | `run_shell_command` | `bash` |
| 工具名称 | `search_file_content` | `grep` |
| SKILL.md | 通用工具名称 | Pi 工具名称 |
| SKILL.md | 无 Pi 特性说明 | 添加 Pi 特性章节 |
| SKILL.md | 无扩展说明 | 添加扩展安装指引 |

#### 文件统计

```
总文件数: 23
新增文件: 9
修改文件: 10
删除文件: 0
```

---

### v2.2.0 - Security & Scripts (2026-04-09)

**里程碑**: 安全增强，GUI 辅助工具

#### 新增 (Added)

| 类别 | 内容 | 说明 |
|------|------|------|
| 安全 | Security Checklist | 部署前安全检查清单 |
| 脚本 | `camera_capture.py` | 摄像头捕获脚本 |
| 脚本 | `image_compare.py` | 图像对比脚本 |
| 脚本 | `requirements.txt` | Python 依赖 |

#### 变更 (Changed)

- 优化文档结构
- 更新硬件接口规范
- references 文档版本升级到 2.0

---

### v2.0.0 - Progressive Loading (2026-04-08)

**里程碑**: 渐进式加载架构，完整参考文档体系

#### 新增 (Added)

| 类别 | 文件 | 内容 |
|------|------|------|
| 参考 | `chips.md` | 芯片系列规格 |
| 参考 | `hardware-interfaces.md` | 硬件接口规范 |
| 参考 | `protocols.md` | 通信协议规范 |
| 参考 | `languages.md` | 编程规范 |
| 参考 | `tools.md` | 开发工具配置 |
| 参考 | `debugging.md` | 调试策略 |
| 参考 | `remote-tools.md` | 远程调试工具 |
| 参考 | `gui-feedback.md` | GUI 视觉反馈 |
| 参考 | `ai-patterns.md` | AI 集成模式 |
| 脚本 | `camera_capture.py` | 摄像头捕获 |
| 脚本 | `image_compare.py` | 图像对比 |

#### 变更 (Changed)

- 重构为渐进式加载架构
- 核心指令保持在 SKILL.md
- 详细规范存放在 references/

#### 架构设计

```
SKILL.md (核心，轻量)
    │
    └── references/ (按需加载)
        ├── chips.md
        ├── hardware-interfaces.md
        ├── protocols.md
        └── ...
```

---

### v1.0.0 - Initial Release (2026-04-01)

**里程碑**: 初始版本发布

#### 新增 (Added)

| 类别 | 内容 |
|------|------|
| 芯片支持 | ESP32, STM32, RP2040, nRF52 |
| 工作流程 | 6阶段开发流程 |
| 快速参考 | 硬件接口参考表 |
| 快速参考 | 通信协议参考表 |
| 跨平台 | Windows/Linux/macOS 命令对照 |
| 决策树 | 任务类型选择逻辑 |

#### 核心工作流程

```
Phase 1: Context Loading (加载上下文)
Phase 2: Task Planning (任务规划)
Phase 3: Code Generation (代码生成)
Phase 4: Verification (编译验证)
Phase 5: Visual Feedback (视觉反馈)
Phase 6: Completion (完成记录)
```

---

## 版本规划

### 下个版本 (v3.1.0) - 计划中

**预计内容**:
- [ ] 添加更多芯片支持 (RISC-V, ARM Cortex-M33)
- [ ] 新增 Zephyr RTOS 支持
- [ ] 优化扩展性能
- [ ] 添加单元测试

### 未来版本 (v4.0.0) - 构想中

**预计内容**:
- [ ] 支持 AI 模型自动选择最佳芯片
- [ ] 集成硬件仿真 (Wokwi)
- [ ] 自动生成数据手册摘要

---

## 版本更新指南

### 如何更新版本

1. **更新文件内容**
   - 修改需要变更的文件
   - 添加新功能或修复问题

2. **更新版本号**
   
   位置：`package.json`, `SKILL.md`, `CHANGELOG.md`
   
   ```json
   // package.json
   "version": "3.1.0"
   ```
   
   ```markdown
   // SKILL.md 末尾
   ---
   Version: 3.1.0
   Updated: YYYY-MM-DD
   ```

3. **更新 CHANGELOG.md**
   
   ```markdown
   ## [3.1.0] - YYYY-MM-DD
   
   ### Added
   - 新功能描述
   
   ### Changed
   - 变更描述
   
   ### Fixed
   - 修复描述
   ```

4. **更新本文档 (VERSION_HISTORY.md)**
   - 添加新版本详细记录

### 版本号规则

遵循 [语义化版本](https://semver.org/):

- **主版本号 (MAJOR)**: 不兼容的 API 更改
- **次版本号 (MINOR)**: 向后兼容的功能新增
- **修订号 (PATCH)**: 向后兼容的问题修复

示例:
- `3.0.0` → `3.1.0`: 新增功能
- `3.1.0` → `3.1.1`: 修复问题
- `3.1.1` → `4.0.0`: 重大变更

---

## 文件变更记录

### v3.0.0 文件清单

```
embedded-dev/
├── README.md               # 新增
├── LICENSE                 # 新增
├── CONTRIBUTING.md         # 新增
├── CHANGELOG.md            # 新增
├── COMPATIBILITY.md        # 新增
├── VERSION_HISTORY.md      # 新增 (本文件)
├── .gitignore              # 新增
├── package.json            # 新增
├── SKILL.md                # 修改
├── INSTALL.md              # 修改
├── extensions/
│   ├── image-read.ts       # 新增
│   └── todo.ts             # 新增
├── references/
│   ├── chips.md            # 继承
│   ├── hardware-interfaces.md
│   ├── protocols.md
│   ├── languages.md
│   ├── tools.md
│   ├── debugging.md
│   ├── remote-tools.md
│   ├── gui-feedback.md
│   └── ai-patterns.md
└── scripts/
    ├── camera_capture.py   # 继承
    ├── image_compare.py    # 继承
    └── requirements.txt    # 继承
```

---

## 贡献者

| 版本 | 贡献者 | 主要贡献 |
|------|--------|----------|
| v1.0.0 - v3.0.0 | @lhbsaa | 初始设计、架构重构、Pi适配 |

---

## 参考

- [语义化版本规范](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub 开源指南](https://opensource.guide/)

---

*最后更新: 2026-04-10*
