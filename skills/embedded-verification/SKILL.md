---
name: embedded-verification
description: Use after implementation complete - runs build-flash-monitor loop, verifies runtime behavior, no completion claims without fresh evidence
---

# Embedded Verification

## Overview

The Iron Law enforcement phase. No completion claims without fresh verification evidence.

**Core principle:** Evidence before claims, always.

**Context:** Run after `embedded-implementation` completes all tasks.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT BUILD-FLASH-MONITOR VERIFICATION
```

## Verification Gate

```
BEFORE claiming ANY status:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute FULL command (fresh, complete)
3. READ: Full output, check exit code, errors
4. VERIFY: Does output confirm?
5. ONLY THEN: Make the claim
```

## Verification Types

| Type | Command | Expected |
|------|---------|----------|
| **Build** | `idf.py build` | Exit 0, no errors |
| **Flash** | `idf.py -p COM3 flash` | Exit 0, flash success |
| **Monitor** | `idf.py monitor` | No crash, correct output |
| **Full Loop** | `idf.py build flash monitor` | All pass |

## Platform Commands

### Windows PowerShell
```powershell
# Build
idf.py build
if($LASTEXITCODE -eq 0) { echo "Build PASS" } else { echo "Build FAIL" }

# Flash + Monitor
idf.py -p COM3 flash; if($?) { idf.py monitor }
```

### Linux/macOS Bash
```bash
# Build
idf.py build && echo "Build PASS"

# Flash + Monitor
idf.py -p /dev/ttyUSB0 flash monitor
```

## Process

### 1. Build Verification

```
Run: idf.py build

Check:
- Exit code = 0
- No errors in output
- No unexpected warnings

If FAIL:
- Analyze error
- Fix
- Re-build
```

### 2. Flash Verification

```
Run: idf.py -p [PORT] flash

Check:
- Flash successful message
- No timeout errors

If FAIL:
- Check port (COMx / /dev/ttyUSBx)
- Check connection
- Re-flash
```

### 3. Monitor Verification

```
Run: idf.py monitor

Duration: 30-60 seconds minimum

Check:
- No Guru Meditation Error
- No assertion failures
- Expected log output present
- Initialization sequence logged

Use: scripts/serial_monitor.py for structured output
```

### 4. Runtime Behavior Check

Based on design spec:

| Feature | Verification |
|---------|--------------|
| Display driver | Monitor shows init success |
| Sensor | Correct readings in log |
| Wi-Fi | Connected to AP |
| Protocol | Data transmission logged |

### 5. Update AGENTS.md

```yaml
memory:
  - "[Driver] verified: build-flash-monitor complete"
  - "Hardware config: [specifics]"
```

## Claim Types

| Claim | Required Evidence | Not Sufficient |
|-------|-------------------|----------------|
| "Driver complete" | Full loop pass | Build only |
| "Display works" | Monitor + visual | Monitor only |
| "Sensor reading" | Correct data in log | No output |
| "Wi-Fi connected" | Connection log | Code looks right |

## Red Flags - STOP

- "Should work now"
- "Build passed earlier"
- "Looks correct"
- Using truncated output
- Previous session verification
- Skipping monitor phase
- "I'm confident" without running commands

**ALL mean: STOP. Run verification commands.**

## Output Format

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

### Issues
[list or "None"]
```

## Transition

**If ALL verification PASS:**
```
Verification complete. Invoking embedded-gui-feedback for display check.
```

**If ANY verification FAIL:**
```
Verification failed. Analyze issues, fix, re-verify.
Do NOT proceed to GUI feedback until full loop passes.
```

**REQUIRED:** Only invoke `embedded-gui-feedback` after ALL verification passes.

## Anti-Patterns

| Bad | Good |
|-----|------|
| "Build passed" (no flash) | Full loop: build → flash → monitor |
| "Earlier session verified" | Fresh verification now |
| Truncated output reading | Full output check |
| Skip monitor phase | 30+ seconds monitoring |
| Claim without evidence | Evidence THEN claim |