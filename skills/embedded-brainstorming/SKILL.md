---
name: embedded-brainstorming
description: Use before any embedded development - explores hardware requirements, confirms configuration, validates feasibility, saves design spec
---

# Embedded Brainstorming

## Overview

Turn hardware ideas into fully formed designs through systematic exploration.

**Core principle:** No code generation until hardware configuration confirmed and design approved.

<HARD-GATE>
Do NOT generate any driver code, write any implementation, or take any coding action until you have presented the design and the user has approved it. This applies to EVERY embedded project regardless of perceived simplicity.
</HARD-GATE>

## Process Flow

```
1. Load Context → 2. Confirm Hardware → 3. Identify Constraints → 4. Propose Design → 5. Get Approval → 6. Next Skill
```

## Checklist

You MUST complete these items in order:

### 1. Load Context

```
read AGENTS.md
```

- If AGENTS.md missing → Create template with project info
- Store key config in session

### 2. Confirm Hardware

Ask questions one at a time:

| Question | Why |
|----------|-----|
| Target chip? | Determines framework and constraints |
| Interface type? | SPI/I2C/UART config differs |
| Controller/model? | Datasheet lookup required |
| Resolution/config? | Display/sensor specific |

**Prefer multiple choice when possible:**
```
"Which chip family?"
A) ESP32-S3 (Wi-Fi, LCD, AI)
B) STM32F4 (Performance, DSP)
C) RP2040 (Low cost, PIO)
D) nRF52 (BLE, Low power)
```

### 3. Identify Constraints

Check hard limits:

| Chip | Key Constraint |
|------|----------------|
| ESP32-S3 | SPI DMA <= 4092 bytes |
| STM32 | Check DMA stream limits |
| RP2040 | PIO instruction limit |
| nRF52 | SoftDevice memory |

### 4. Propose 2-3 Approaches

Present options with trade-offs:

```
Approach A: [Recommended]
- Pros: ...
- Cons: ...
- Why recommended: ...

Approach B: [Alternative]
- Pros: ...
- Cons: ...

Approach C: [Fallback]
- Pros: ...
- Cons: ...
```

### 5. Get Approval

Present design in sections (scaled to complexity):

```
## Hardware Configuration
- Chip: ESP32-S3
- Interface: SPI Mode 0, 40MHz
- Controller: ST7789
- Resolution: 240x240

## Architecture
- Three-layer: App → HAL → Driver

## Key Constraints
- DMA: 4092 byte chunks
- Frame buffer: Use PSRAM

## Implementation Plan
- Phase 1: Driver init
- Phase 2: Display functions
- Phase 3: GUI integration

Does this look correct?
```

### 6. Save Design Doc

Write validated design to:
```
docs/embedded/specs/YYYY-MM-DD-<feature>-spec.md
```

### 7. Transition to Next Skill

**After user approval:**
```
Design approved. Invoking embedded-driver-design skill to create implementation plan.
```

**REQUIRED:** Invoke `embedded-driver-design` skill next. Do NOT invoke any other skill.

## Anti-Patterns

| Bad Practice | Correct Approach |
|--------------|------------------|
| "Just generate the driver" | Brainstorm first, then implement |
| "This is simple, no design needed" | Every project needs design validation |
| Multiple questions in one message | Ask one at a time |
| Skip hardware confirmation | Verify chip/interface/controller |

## Red Flags - STOP

- "Let me just write the code"
- "I already know what to build"
- "No need for design, just config"
- User didn't approve design
- Missing chip/interface information

**ALL mean: STOP. Complete brainstorming process first.**

## Output

After approval, report:
```
Design Spec: docs/embedded/specs/YYYY-MM-DD-<feature>-spec.md
Status: APPROVED
Next: embedded-driver-design
```