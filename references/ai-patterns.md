# AI Agent Skill Usage Patterns

AI Agent使用模式和技能通用性设计规范。

---

## AI Agent核心设计模式

### ReAct模式 (Reasoning + Acting)

```
循环执行:
1. Thought: 分析当前状态，决定下一步行动
2. Action: 调用工具执行操作
3. Observation: 观察执行结果
4. 循环直到任务完成

示例:
Thought: 需要配置SPI接口
Action: read_file(references/hardware-interfaces.md)
Observation: 获取SPI配置模板
Thought: 根据模板生成配置代码
Action: write_file(spi_driver.c)
```

### Plan-and-Execute模式

```
阶段1: 规划
- 分析任务需求
- 分解为子任务
- 制定执行计划

阶段2: 执行
- 按计划依次执行子任务
- 记录执行进度
- 处理异常情况

示例:
Plan:
1. 加载AGENTS.md
2. 读取硬件配置
3. 生成驱动代码
4. 编译验证
5. 更新记忆

Execute:
Step 1/5: 完成
Step 2/5: 完成
...
```

---

## Claude Code Skill规范

### Skill结构

```yaml
SKILL.md:
  frontmatter:
    name: skill-name
    description: 触发描述（pushy写法）
  
  body:
    - Tools Required
    - Workflow
    - Quick Reference
    - Examples
    - Best Practices
```

### Description写法

```yaml
# 错误写法（undertrigger倾向）
description: "How to build LCD driver."

# 正确写法（pushy，避免undertrigger）
description: "Guide for LCD driver development. Use this skill whenever 
the user mentions LCD, display, screen, ST7789, ILI9341, SPI display, 
or needs help with display initialization, frame buffer, graphics drawing. 
Make sure to use this skill even if the user doesn't explicitly mention 
'LCD' but asks about display, screen, or visual output."
```

---

## 渐进式加载架构

### 三级加载系统

```yaml
Level 1 - 元数据层:
  内容: name + description
  大小: ~100词
  时机: 始终在上下文
  用途: 触发判断

Level 2 - SKILL.md主体:
  内容: 核心指令、工作流、示例
  大小: <500行（理想）
  时机: Skill触发时加载
  用途: 执行核心逻辑

Level 3 - References:
  内容: 详细规范、代码模板
  大小: 无限制
  时机: 按需加载
  用途: 获取详细信息
```

### 资源效率原则

```yaml
优化策略:
  - SKILL.md保持精简（<500行）
  - 详细内容移到references
  - 按需加载references文件
  - 避免一次性加载所有内容

示例:
  用户: "配置SPI"
  行为: 加载references/hardware-interfaces.md的SPI部分
  
  用户: "添加MQTT支持"
  行为: 加载references/protocols.md的MQTT部分
```

---

## 工具选择决策

### 决策流程

```
用户请求 → 识别任务类型
    ├─ 读取文件 → read_file
    ├─ 写入文件 → write_file
    ├─ 修改代码 → replace
    ├─ 执行命令 → run_shell_command
    ├─ 搜索内容 → search_file_content
    ├─ 查找文件 → glob
    ├─ 分析图片 → image_read
    └─ 保存记忆 → save_memory
```

### 工具使用最佳实践

| 工具 | 使用场景 | 注意事项 |
|------|----------|----------|
| read_file | 读取源码/文档 | 先检查文件大小 |
| write_file | 创建新文件 | 避免覆盖重要文件 |
| replace | 精确修改 | 提供足够上下文 |
| run_shell_command | 编译/烧录 | 设置合理超时 |

---

## AGENTS.md记忆管理

### 记忆格式

```yaml
## 项目信息
project:
  name: MimiClaw-1.3-LCD
  target: ESP32-S3
  framework: ESP-IDF

## 硬件配置
hardware:
  lcd:
    controller: SH8601
    interface: SPI
    resolution: 240x240
    config:
      y_gap: 0
      x_gap: 0
      madctl_val: 0x00

## 记忆库
memory:
  - "LCD正确配置: SH8601驱动，GUI刷新需Y轴翻转+行顺序翻转"
  - "全屏显示: 改y_gap=80，madctl_val=0xC0"
  - "DMA限制: SPI单次传输最大4092字节"

## 约束条件
constraints:
  - "DMA缓冲区不能超过4092字节"
  - "GUI刷新需要特殊处理"
```

---

## Skill通用性设计原则

### 跨平台抽象

```yaml
设计原则:
  - 定义通用接口
  - 平台特定实现分离
  - 配置参数化

示例:
  接口: display_init(width, height)
  ESP32实现: esp_lcd_init()
  STM32实现: ltdc_init()
```

### AI平台适配

```yaml
Claude Code:
  tools: read_file, write_file, replace, run_shell_command
  format: SKILL.md + references

OpenAI Function Calling:
  tools: functions定义
  format: JSON Schema

通用设计:
  - 核心逻辑平台无关
  - 工具调用抽象化
  - 输出格式标准化
```

---

## 提示工程规范

### 标准提示模板

```markdown
## 角色定义
你是一个嵌入式开发专家...

## 任务说明
配置SPI接口驱动LCD...

## 可用工具
- read_file: 读取文件
- write_file: 写入文件
...

## 输出格式
返回JSON格式结果...

## 约束条件
- DMA限制4092字节
...
```

### Chain-of-Thought提示

```
让我们一步步分析：
1. 首先，我需要理解硬件配置...
2. 然后，我需要查看参考文档...
3. 接着，我需要生成配置代码...
4. 最后，我需要验证编译...
```

---

## 最佳实践总结

1. **渐进式加载**: 核心在SKILL.md，详细在references
2. **Pushy描述**: 避免undertrigger，明确触发场景
3. **模块化设计**: 单一职责，清晰边界
4. **记忆管理**: 重要发现保存到AGENTS.md
5. **验证闭环**: 编译→烧录→监控→测试

---
Version: 2.0
Updated: 2026-04-09