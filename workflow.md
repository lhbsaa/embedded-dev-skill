# Embedded Development Workflow

本文档包含嵌入式开发的详细工作流程。核心 Skill 见 `SKILL.md`。

---

## Pi Edition Workflow

### Phase 1: Context Loading

Use Pi's `read` tool to load AGENTS.md:
```
read AGENTS.md
```

- If AGENTS.md missing → Use `write` to create template with project info
- Store key config in Pi session via `pi.appendEntry()`

**AGENTS.md Template:**
```markdown
## 项目信息
project:
  name: [项目名称]
  target: [目标芯片]
  framework: [开发框架]

## 硬件配置  
hardware:
  lcd: {controller, interface, resolution}
  imu: {model, interface}

## 记忆库
memory:
  - "成功配置: [具体参数]"
  - "问题解决: [方案]"
```

### Phase 2: Task Planning

Use `todo_list` extension for task tracking:
```
todo_list action=add "Configure SPI driver"
todo_list action=list
```

- Simple task → Execute directly
- Complex task → Decompose into subtasks

**Bite-Sized Task Rules:**
- Each step = ONE action (2-5 minutes)
- Include exact file paths
- Include complete code snippets
- Include verification commands

### Phase 3: Code Generation

Use Pi tools for code operations:
```
read src/driver.c          # 读取现有代码
write src/driver_new.c     # 创建新文件
edit src/driver.c          # 修改代码
```

- Check `references/` for detailed specs
- Apply modular architecture patterns
- Use `prompts/driver-generator.md` for complex drivers

### Phase 4: Verification Gate

**BEFORE claiming any status:**

```
1. IDENTIFY: What command proves this claim?
   - Code change → `idf.py build`
   - Runtime behavior → `idf.py flash monitor`
   - GUI display → `camera_capture.py` + `image_read`

2. RUN: Execute the FULL command (fresh, complete)
   - Don't use previous session's results
   - Don't truncate output

3. READ: Full output, check for:
   - Build: errors, warnings, exit code 0
   - Monitor: crashes, panics, assertions
   - Image: layout, font, color alignment

4. VERIFY: Does output confirm the claim?
   - If NO → State actual status with evidence
   - If YES → State claim WITH evidence

5. ONLY THEN: Make the claim
```

**Verification commands (Windows PowerShell):**
```powershell
# Build
idf.py build
# Check: exit code 0, no errors

# Flash and monitor (PowerShell 5.1 - 注意 && 不支持)
idf.py -p COM3 flash; if($?) {idf.py monitor}
# Check: no crash, correct output
```

**Verification commands (Linux/macOS Bash):**
```bash
idf.py build && idf.py -p /dev/ttyUSB0 flash monitor
```

**On Error**: Analyze output → Fix → Retry
**Use `/tree`**: Navigate to previous working state if stuck

### Phase 5: Visual Feedback (GUI)

Use `image_read` extension for LCD analysis:
```
bash: python scripts/camera_capture.py --session
image_read screenshots/capture_xxx.png
```

- Analyze layout, font, color issues
- Apply fixes → Re-verify

**Camera Setup Requirements:**
- USB webcam (1080p recommended)
- Centered on LCD screen
- Uniform lighting (avoid glare)
- Distance: 15-30cm from screen

### Phase 6: Completion

Update AGENTS.md and save to Pi session:
```
edit AGENTS.md  # Update findings
```

Use Pi's session tree to save checkpoints:
- Press Escape twice → `/tree` → Navigate → Shift+L to label

---

## OpenCode Edition Workflow

### Phase 1: Context Loading
```
read AGENTS.md
```

### Phase 2: Task Planning
```
todowrite todos=[{"content": "Configure SPI driver", "status": "pending", "priority": "high"}]
```

### Phase 3: Code Generation
```
read src/driver.c
write src/driver_new.c
edit src/driver.c
```

### Phase 4: Verification Gate

**BEFORE claiming any status:**

```
1. IDENTIFY: What command proves this claim?
2. RUN: Execute FULL command (fresh, complete)
3. READ: Full output, check exit code and errors
4. VERIFY: Does output confirm?
5. ONLY THEN: Make the claim
```

**Verification commands:**
```
bash: idf.py build
# Check: exit code 0, no errors

bash: idf.py -p COM3 flash monitor
# Check: no crash, correct runtime output
```

**Claim Types:**

| Claim | Required Verification | Not Sufficient |
|-------|----------------------|----------------|
| Driver complete | `idf.py build` exit 0 | "No errors in log" |
| LCD displays correctly | flash + camera_capture | "Backlight on" |
| Sensor working | monitor shows correct data | "Code looks correct" |
| SPI timing correct | Oscilloscope/waveform | "Frequency looks right" |

### Phase 5: Visual Feedback (GUI)
```
bash: python scripts/camera_capture.py --session
bash: python scripts/serial_monitor.py -p COM4 -d 30
```

### Phase 6: Completion
```
edit AGENTS.md
```

---

## Verification Report Template

```markdown
## Verification Report

### Build
Command: idf.py build
Status: PASS / FAIL
Exit Code: 0 / [code]
Errors: [list or "None"]

### Flash
Command: idf.py -p COM3 flash
Status: PASS / FAIL
Port: COM3 / [actual port]

### Monitor
Duration: 30 seconds
Status: PASS / FAIL
Crashes: None / [error type]
Output: [key logs]

### Runtime
Feature: [name]
Status: PASS / FAIL
Evidence: [specific output]

### Summary
Verification: COMPLETE / INCOMPLETE
Ready for GUI Feedback: YES / NO
```

---

## Platform Command Differences

| Task | Windows PowerShell | Linux/macOS Bash |
|------|-------------------|------------------|
| Chain success | `cmd1; if($?) {cmd2}` | `cmd1 && cmd2` |
| Chain failure | `cmd1; if(-not $?) {cmd2}` | `cmd1 || cmd2` |
| Serial port | COM1, COM2, COM3 | /dev/ttyUSB0, /dev/ttyACM0 |
| Path separator | `\` | `/` |
| Environment var | `$env:VAR` | `$VAR` |

**Important: PowerShell 5.1 does NOT support `&&` or `||`.**

---

## Decision Tree

```
User Request → Identify Task Type
    ├─ Driver Development
    │   └─ Read references/hardware-interfaces.md
    │   └─ Check chip family → Load references/chips.md
    │   └─ Generate driver → Run Verification Gate
    │   
    ├─ Protocol Implementation  
    │   └─ Read references/protocols.md
    │   └─ Check security requirements → TLS or plain
    │   └─ Implement → Verify connectivity
    │   
    ├─ Code Quality
    │   └─ Read references/languages.md
    │   └─ Apply MISRA C / modular design
    │   └─ Two-stage review (hardware + code quality)
    │   
    ├─ Debugging
    │   └─ Read references/debugging.md
    │   └─ Check remote → references/remote-tools.md
    │   └─ Apply systematic debugging phases
    │   
    ├─ GUI Development
    │   └─ Capture screen → image_read analysis
    │   └─ Read references/gui-feedback.md
    │   └─ Apply fixes → Re-verify with camera
    │   
    ├─ Quick Troubleshooting
    │   └─ Read references/faq.md
    │   └─ Check common problems and solutions
    │   
    ├─ Learning from Examples
    │   └─ Read references/cases.md
    │   └─ Study real-world case studies
    │   
    └─ Tool Setup
        └─ Read references/tools.md
        └─ Configure build/debug environment
```

---

详见:
- Skill Chain: `skills/embedded-*/SKILL.md`
- Prompts: `prompts/*.md`
- References: `references/*.md`