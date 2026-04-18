---
name: embedded-driver-design
description: Use when hardware configuration confirmed - creates detailed implementation plan with bite-sized tasks, exact file paths, complete code steps
---

# Embedded Driver Design

## Overview

Create implementation plan assuming engineer has zero context and questionable taste. Document everything needed: files, code, testing, verification steps.

**Context:** Run after `embedded-brainstorming` approval.

**Save plans to:** `docs/embedded/plans/YYYY-MM-DD-<driver>-plan.md`

<HARD-GATE>
Do NOT generate code during this phase. This skill ONLY creates the plan.
Code generation happens in `embedded-implementation`.
</HARD-GATE>

## Process

### 1. Load Design Spec

```
read docs/embedded/specs/YYYY-MM-DD-<feature>-spec.md
```

### 2. Load References

Based on task type:

| Task Type | Reference File |
|-----------|----------------|
| Driver dev | references/chips.md + hardware-interfaces.md |
| Protocol | references/protocols.md |
| GUI | references/gui-feedback.md |
| Debugging | references/debugging.md |

### 3. Define File Structure

Map files BEFORE defining tasks:

| File | Responsibility |
|------|----------------|
| `include/driver.h` | API declarations, constants |
| `src/driver.c` | Implementation |
| `src/driver_test.c` | Unit tests (if applicable) |

### 4. Create Bite-Sized Tasks

**Each step = ONE action (2-5 minutes):**

```markdown
### Task 1: Driver Header

**Files:**
- Create: `include/lcd_st7789.h`

- [ ] **Step 1: Write header file**

```c
#ifndef LCD_ST7789_H
#define LCD_ST7789_H
// ... complete code
#endif
```

- [ ] **Step 2: Build to verify syntax**

Run: `idf.py build`
Expected: No errors in header

- [ ] **Step 3: Commit**

```bash
git add include/lcd_st7789.h
git commit -m "feat: add ST7789 header"
```

### Task 2: Driver Implementation

**Files:**
- Create: `src/lcd_st7789.c`
- Modify: `include/lcd_st7789.h` (if needed)

- [ ] **Step 1: Write init function**

```c
esp_err_t lcd_st7789_init(void) {
    // ... complete implementation
}
```

- [ ] **Step 2: Write DMA-chunked write function**

```c
esp_err_t lcd_st7789_write(const uint8_t *data, size_t len) {
    // Chunking for > 4092 bytes
}
```

- [ ] **Step 3: Build**

Run: `idf.py build`
Expected: Exit 0

- [ ] **Step 4: Commit**
```

### 5. Plan Document Header

Every plan MUST start with:

```markdown
# [Driver Name] Implementation Plan

> **For agentic workers:** REQUIRED: Use embedded-implementation skill to execute this plan task-by-task.

**Goal:** [One sentence]

**Architecture:** [2-3 sentences]

**Constraints:**
- DMA <= 4092 bytes
- [Other hardware limits]

---
```

### 6. Self-Review

After writing complete plan:

| Check | Action |
|-------|--------|
| Spec coverage | Every requirement has task |
| Placeholder scan | No "TBD", "TODO", "implement later" |
| Type consistency | Function names match across tasks |

### 7. Save Plan

```
write docs/embedded/plans/YYYY-MM-DD-<driver>-plan.md
```

### 8. Transition to Next Skill

**Offer execution choice:**

```
Plan saved to docs/embedded/plans/<plan>.md

Two execution options:

1. Subagent-Driven - Fresh subagent per task, two-stage review
2. Inline Execution - Execute in current session

Which approach?
```

**REQUIRED:** Invoke `embedded-implementation` next.

## No Placeholders

These are plan failures - never write them:
- "TBD", "TODO", "implement later"
- "Add appropriate error handling"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code)
- Steps without complete code blocks

## Task Template

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.c`
- Modify: `exact/path/to/file.c:123-145`

- [ ] **Step 1: [Action]**

[Complete code block]

- [ ] **Step 2: [Verification]**

Run: `[command]`
Expected: `[output]`

- [ ] **Step 3: Commit`

```bash
git add [files]
git commit -m "[message]"
```
```

## Red Flags - STOP

- Writing code during design phase
- "TBD" in any task
- Tasks without complete code
- Skipping file structure definition
- User hasn't approved brainstorming spec

## Output

```
Plan: docs/embedded/plans/YYYY-MM-DD-<driver>-plan.md
Tasks: N tasks defined
Status: READY FOR IMPLEMENTATION
Next: embedded-implementation
```