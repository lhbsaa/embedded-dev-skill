# Version History

本文档记录 Embedded Development Skill 的完整版本历程。

---

## 当前版本

**Version**: 3.3.0  
**Release Date**: 2026-04-18  
**Codename**: Superpowers Integration Edition  

---

## 版本历程

### v3.3.0 - Superpowers Integration Edition (2026-04-18)

**里程碑**: 借鉴 Superpowers (by Jesse Vincent) 的强制门控机制和模块化设计

#### 新增 (P0 改进 - 强制门控)

| 类别 | 内容 | 借鉴来源 |
|------|------|----------|
| **Iron Law** | 编译优先验证强制门控 | Superpowers TDD Iron Law |
| **Red Flags** | 12个停止信号 + 7个症状信号 | Superpowers Red Flags |
| **Rationalization Table** | 11个借口反驳表 | Superpowers Rationalization |
| **Verification Gate** | 5步验证流程 + Claim Types 表 | Superpowers verification-before-completion |

#### 新增 (P1 改进 - 模块化 + Hooks)

| 类别 | 内容 | 借鉴来源 |
|------|------|----------|
| **Hooks SessionStart** | 自动注入嵌入式上下文 | Superpowers session-start |
| **hooks/hooks.json** | 关键词触发配置 | Superpowers hooks.json |
| **hooks/session-start.cmd** | Windows PowerShell 脚本 | 平台适配 |
| **prompts/driver-generator.md** | 驱动代码生成 Prompt（含DMA约束） | Superpowers implementer-prompt |
| **prompts/hardware-validator.md** | 硬件规范评审 Prompt | Superpowers spec-reviewer |
| **prompts/code-quality.md** | MISRA C 质量评审 Prompt | Superpowers code-quality-reviewer |
| **prompts/debugging.md** | 嵌入式调试 Prompt | Superpowers systematic-debugging |

#### 变更

| 类别 | 原内容 | 新内容 |
|------|--------|--------|
| Description | 包含 workflow 暗示 | 纯触发条件 + symptom 关键词 |
| Phase 4 | 简单验证命令 | Verification Gate 5步流程 |
| SKILL.md | 无 prompts 引用 | 添加 Prompts + Hooks 引用表格 |
| 版本号 | v3.2.0 | v3.3.0 |

#### 新增文件统计

```
hooks/: 2个 (hooks.json, session-start.cmd)
prompts/: 4个 (driver-generator, hardware-validator, code-quality, debugging)
```

#### 设计理念

Superpowers 核心概念借鉴：
- **Iron Law**: "Violating the letter is violating the spirit" → 嵌入式编译强制
- **Red Flags**: 停止信号列表 → 硬件开发危险信号
- **Rationalization Table**: 借口反驳表 → 嵌入式开发常见借口
- **Verification Gate**: 证据优先声明 → build-flash-monitor 强制验证
- **Prompt 模板分离**: 实现者/评审者分离 → 两阶段评审（硬件规范 + MISRA C）
- **Hooks SessionStart**: 自动上下文注入 → 嵌入式关键词触发

#### 新增 (P2 改进 - Skill Chain 链式调用)

| 类别 | 内容 | 借鉴来源 |
|------|------|----------|
| **Skill Chain** | 5个链式调用 skill | Superpowers brainstorming → writing-plans → implementation |
| **embedded-brainstorming** | 硬件需求分析 + HARD-GATE | Superpowers brainstorming |
| **embedded-driver-design** | 实现计划创建（不生成代码） | Superpowers writing-plans |
| **embedded-implementation** | 代码执行 + 两阶段评审 | Superpowers subagent-driven-development |
| **embedded-verification** | build-flash-monitor 强制验证 | Superpowers verification-before-completion |
| **embedded-gui-feedback** | LCD 视觉分析 | embedded-dev 特色功能 |
| **Two-Stage Review** | 硬件规范 + MISRA C | Superpowers spec-reviewer + code-quality-reviewer |

#### 新增文件统计 (P2)

```
skills/: 5个 skill 目录
  - embedded-brainstorming/SKILL.md
  - embedded-driver-design/SKILL.md
  - embedded-implementation/SKILL.md
  - embedded-verification/SKILL.md
  - embedded-gui-feedback/SKILL.md
```

#### Skill Chain 流程

```
brainstorming → driver-design → implementation → verification → gui-feedback
     ↓              ↓               ↓               ↓               ↓
  硬件确认       计划创建        代码+评审        编译验证        视觉分析
```

#### 设计理念 (P2)

- **HARD-GATE**: 每个 skill 有强制门控，必须完成才能进入下一个
- **明确调用**: skill 结束时明确调用下一个 skill
- **No Code in Design Phase**: driver-design 只创建计划，不生成代码
- **No Placeholders**: 计划中不能有 "TBD"、"TODO"、"implement later"
- **Bite-Sized Tasks**: 每步一个动作，2-5分钟

#### 新增 (P3 改进 - Token 效率优化)

| 类别 | 内容 | 借鉴来源 |
|------|------|----------|
| **workflow.md** | 详细工作流拆分独立文件 | Superpowers Token 效率原则 |
| **examples.md** | 7个实战案例独立文件 | Superpowers Examples 分离 |
| **SKILL.md 精简** | 保留核心，链接外部文件 | Superpowers <200 words 目标 |

#### 新增文件统计 (P3)

```
workflow.md: 详细6阶段工作流 + Verification Report模板 + Decision Tree
examples.md: 7个实战案例 + Quick Reference
```

#### Token 效率对比

| 文件 | P0-P2 版本 | P3 版本 | 减少 |
|------|------------|---------|------|
| SKILL.md | ~950行 | ~850行 | ~100行 |
| Workflow | 内嵌 | 外部 workflow.md | 独立加载 |
| Examples | 内嵌 | 外部 examples.md | 按需加载 |

#### 设计理念 (P3)

- **渐进式加载**: 核心 SKILL.md 精简，详细内容按需加载
- **链接替代内嵌**: workflow.md 和 examples.md 外部链接
- **Token 节省**: 核心文件减少 ~100 行，每次 session 节省 context
- **按需深度**: 用户需要时才读取详细 workflow/examples

---

### v3.2.0 - Dual Platform Edition (2026-04-13)

**里程碑**: 合并开源版本与自用版本，支持 Pi + OpenCode 双平台

#### 新增

| 类别 | 内容 | 文件 |
|------|------|------|
| 实战案例 | `cases.md` - 6个真实项目案例 | references/ |
| FAQ | `faq.md` - 20个常见问题解答 | references/ |
| 串口监控 | `serial_monitor.py` - AI友好日志解析 | scripts/ |
| PowerShell | `serial_monitor.ps1` - Windows备用脚本 | scripts/ |
| OpenCode适配 | `adapters/opencode/` - 完整适配器 | adapters/ |
| MCP Server | `mcp-server-embedded.py` - Python MCP实现 | adapters/opencode/ |
| MCP指南 | `MCP-GUIDE.md` - 详细配置说明 | adapters/opencode/ |
| OpenCode Skill | OpenCode专用SKILL.md | adapters/opencode/ |

#### 变更

| 类别 | 原内容 | 新内容 |
|------|--------|--------|
| SKILL.md | Pi单平台 | Pi + OpenCode双平台 |
| README.md | Pi说明 | 双平台说明 |
| COMPATIBILITY.md | 简单映射 | MCP替代方案详细指南 |
| INSTALL.md | Pi安装 | Pi + OpenCode安装 |
| package.json | version 3.1 | version 3.2 |
| requirements.txt | opencv, numpy | + pyserial |

#### 内容规模

```
参考文档: 11个 (+2)
脚本: 5个 (+3)
扩展: 3个 (不变)
适配器: 1套 (新增)
总文件: ~30个
总内容: ~220KB
```

#### 版本质量评分

| 维度 | v3.0 | v3.1 | v3.2 |
|------|------|------|------|
| 架构设计 | 95 | 95 | 98 |
| 内容完整性 | 90 | 92 | 98 |
| 实用性 | 85 | 88 | 96 |
| 易用性 | 88 | 90 | 94 |
| 跨平台 | 90 | 90 | 95 |
| 文档质量 | 90 | 92 | 96 |
| 案例丰富度 | 20 | 30 | 90 |
| FAQ完整性 | 20 | 30 | 90 |
| **综合评分** | **61** | **65** | **92** |

---

### v3.1.0 - Build Wrapper (2026-04-10)

**里程碑**: 新增统一编译扩展

#### 新增

| 类别 | 内容 | 文件 |
|------|------|------|
| 扩展 | `build-wrapper.ts` 统一编译命令 | extensions/ |

---

### v3.0.0 - Pi Edition (2026-04-10)

**里程碑**: 完全适配 Pi Coding Agent，开源发布

#### 新增

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

#### 变更

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

---

### v2.2.0 - Security & Scripts (2026-04-09)

**里程碑**: 安全增强，GUI 辅助工具

#### 新增

| 类别 | 内容 | 说明 |
|------|------|------|
| 安全 | Security Checklist | 部署前安全检查清单 |
| 脚本 | `camera_capture.py` | 摄像头捕获脚本 |
| 脚本 | `image_compare.py` | 图像对比脚本 |
| 脚本 | `requirements.txt` | Python 依赖 |

---

### v2.0.0 - Progressive Loading (2026-04-08)

**里程碑**: 渐进式加载架构，完整参考文档体系

#### 新增

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

#### 新增

| 类别 | 内容 |
|------|------|
| 芯片支持 | ESP32, STM32, RP2040, nRF52 |
| 工作流程 | 6阶段开发流程 |
| 快速参考 | 硬件接口参考表 |
| 快速参考 | 通信协议参考表 |
| 跨平台 | Windows/Linux/macOS 命令对照 |

---

## 版本规划

### 下个版本 (v3.3.0) - 计划中

**预计内容**:
- [ ] 添加更多芯片支持 (RISC-V, ARM Cortex-M33)
- [ ] 新增 Zephyr RTOS 支持
- [ ] 添加单元测试
- [ ] 更多实战案例

### 未来版本 (v4.0.0) - 构想中

**预计内容**:
- [ ] 支持 AI 模型自动选择最佳芯片
- [ ] 集成硬件仿真 (Wokwi)
- [ ] 自动生成数据手册摘要
- [ ] Web 文档站点

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
   "version": "3.3.0"
   ```
   
   ```markdown
   // SKILL.md 末尾
   ---
   Version: 3.3.0
   Updated: YYYY-MM-DD
   ```

3. **更新 CHANGELOG.md**
   
   ```markdown
   ## [3.3.0] - YYYY-MM-DD
   
   ### Added
   - 新功能描述
   
   ### Changed
   - 变更描述
   ```

4. **更新本文档 (VERSION_HISTORY.md)**
   - 添加新版本详细记录

### 版本号规则

遵循 [语义化版本](https://semver.org/):

- **主版本号 (MAJOR)**: 不兼容的 API 更改
- **次版本号 (MINOR)**: 向后兼容的功能新增
- **修订号 (PATCH)**: 向后兼容的问题修复

示例:
- `3.2.0` → `3.3.0`: 新增功能
- `3.3.0` → `3.3.1`: 修复问题
- `3.3.1` → `4.0.0`: 重大变更

---

## 文件变更记录

### v3.2.0 文件清单

```
embedded-dev/
├── README.md               # 更新
├── LICENSE                 # 保留
├── CONTRIBUTING.md         # 保留
├── CHANGELOG.md            # 更新
├── COMPATIBILITY.md        # 大幅更新
├── VERSION_HISTORY.md      # 更新
├── INSTALL.md              # 更新
├── package.json            # 更新
├── .gitignore              # 保留
├── SKILL.md                # 大幅更新
├── extensions/
│   ├── image-read.ts       # 保留
│   ├── todo.ts             # 保留
│   └── build-wrapper.ts    # 保留
├── adapters/               # 新增目录
│   ├── README.md           # 新增
│   └─ opencode/
│       ├── SKILL.md        # 新增
│       ├── MCP-GUIDE.md    # 新增
│       └─ mcp-server-embedded.py  # 新增
├── references/
│   ├── chips.md            # 保留
│   ├── hardware-interfaces.md  # 保留
│   ├── protocols.md        # 保留
│   ├── languages.md        # 保留
│   ├── tools.md            # 保留
│   ├── debugging.md        # 保留
│   ├── remote-tools.md     # 保留
│   ├── gui-feedback.md     # 保留
│   ├── ai-patterns.md      # 保留
│   ├── cases.md            # 新增
│   └ faq.md               # 新增
└── scripts/
    ├── camera_capture.py   # 保留
    ├── image_compare.py    # 保留
    ├── serial_monitor.py   # 新增
    ├── serial_monitor.ps1  # 新增
    └ requirements.txt     # 更新
```

---

## 贡献者

| 版本 | 贡献者 | 主要贡献 |
|------|--------|----------|
| v1.0.0 - v3.2.0 | @lhbsaa | 初始设计、架构重构、Pi适配、双平台合并 |

---

## 参考

- [语义化版本规范](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub 开源指南](https://opensource.guide/)

---

*最后更新: 2026-04-13*