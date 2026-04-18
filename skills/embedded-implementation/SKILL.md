---
name: embedded-implementation
description: Use when implementation plan is ready - executes plan task-by-task with two-stage review (hardware spec then MISRA C)
---

# Embedded Implementation

## Overview

Execute implementation plan with two-stage review after each task.

**Core principle:** Fresh subagent per task + hardware validation + code quality review = high quality.

**Context:** Run after `embedded-driver-design` creates plan.

## Two-Stage Review Process

```
Task Execution → Hardware Validator → Code Quality Reviewer → Commit
     ↓                ↓                     ↓
  Generate code    DMA/GPIO check        MISRA C check
```

**Stage 1: Hardware Validator**
- Use `prompts/hardware-validator.md`
- Checks: DMA <= 4092, interface config, init sequence

**Stage 2: Code Quality Reviewer**
- Use `prompts/code-quality.md`
- Checks: MISRA C, DRY, YAGNI, clean code

## Process

### 1. Load Plan

```
read docs/embedded/plans/YYYY-MM-DD-<driver>-plan.md
```

Extract ALL tasks with full text and context.

### 2. Create Todo List

```
todowrite todos=[{task: "Task 1: Header file", status: "pending"}, ...]
```

### 3. Execute Per Task

For each task:

```
#### Task N Execution

1. Mark todo: in_progress

2. Get task text and context (already extracted)

3. Dispatch implementation (use prompts/driver-generator.md)
   - Generate code
   - Build verification

4. Stage 1 Review: Hardware Validator
   - Use prompts/hardware-validator.md
   - Check DMA, interface, init sequence
   
5. If Stage 1 FAILS:
   - Fix issues
   - Re-review
   - Don't proceed until APPROVED

6. Stage 2 Review: Code Quality
   - Use prompts/code-quality.md
   - Check MISRA C, DRY, YAGNI
   
7. If Stage 2 FAILS:
   - Fix issues
   - Re-review
   - Don't proceed until APPROVED

8. Both stages APPROVED:
   - Mark todo: completed
   - Commit changes
```

### 4. After All Tasks

```
Dispatch final review for entire implementation
```

### 5. Transition to Verification

```
All tasks complete. Invoking embedded-verification for build-flash-monitor loop.
```

**REQUIRED:** Invoke `embedded-verification` next.

## Implementation Prompt

Use `prompts/driver-generator.md` for code generation:

| Input | From |
|-------|------|
| Chip family | Design spec |
| Interface | Design spec |
| Controller | Design spec |
| Task requirements | Plan task text |

## Status Handling

| Status | Meaning | Action |
|--------|---------|--------|
| `DONE` | Code built successfully | Proceed to Stage 1 review |
| `DONE_WITH_CONCERNS` | Completed with doubts | Review concerns before proceeding |
| `NEEDS_DATASHEET` | Missing init sequence | Provide datasheet, re-dispatch |
| `BLOCKED` | Cannot proceed | Analyze blocker, escalate if needed |

## Review Output Format

### Stage 1 (Hardware)
```markdown
Hardware Validation: APPROVED / FIX REQUIRED
Issues: [list or "None"]
```

### Stage 2 (Code Quality)
```markdown
Code Quality: APPROVED / FIX REQUIRED
MISRA C: N/M rules passed
Issues: [list or "None"]
```

## Red Flags - STOP

- Skipping Stage 1 review (hardware)
- Skipping Stage 2 review (code quality)
- Proceeding with unfixed issues
- "Just commit it" without reviews
- Starting Stage 2 before Stage 1 APPROVED
- Moving to next task while review has open issues

**ALL mean: STOP. Complete reviews first.**

## Anti-Patterns

| Bad Practice | Correct Approach |
|--------------|------------------|
| Skip hardware review | DMA overflow causes corruption |
| Skip code quality review | MISRA violations shipped |
| Multiple fixes at once | Fix one, review, repeat |
| "Close enough" on reviews | APPROVED only, no exceptions |

## Output

After all tasks:
```
Tasks: N/M completed
Reviews: All approved
Status: READY FOR VERIFICATION
Next: embedded-verification
```