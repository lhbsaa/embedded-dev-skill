# Embedded Debugging Prompt

## Overview

Systematic debugging approach for embedded systems. Follow phases strictly - random fixes waste time and create new bugs.

**Core Principle:** Find root cause BEFORE attempting fixes.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## Debugging Phases

### Phase 1: Evidence Collection

**BEFORE proposing any fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - Read stack traces completely
   - Note line numbers, error codes, assertion messages

2. **Capture Monitor Output**
   ```bash
   # Windows PowerShell
   python scripts/serial_monitor.py -p COM3 -d 60 -o debug.log
   
   # Linux/macOS
   python scripts/serial_monitor.py -p /dev/ttyUSB0 -d 60 -o debug.log
   ```

3. **Check Build Output**
   ```bash
   idf.py build
   # Read full output, check warnings
   ```

4. **Identify Symptom Type**

| Symptom | Likely Cause | Investigation |
|---------|--------------|---------------|
| Blank LCD | Init sequence, power, data | Check init logs, backlight |
| Display glitch | DMA overflow, timing | Verify buffer <= 4092 |
| SPI timeout | Clock mode, DMA alignment | Check SPI config |
| Random crash | Stack overflow, memory | Check stack size, heap |
| I2C no response | Address, pull-up, wiring | Verify address, check resistors |
| Wi-Fi disconnect | Power, antenna, config | Check power supply |

### Phase 2: Root Cause Analysis

**Trace backward from symptom:**

```
Symptom → Where does bad state originate? → What caused that? → Source
```

**Multi-layer systems:**
```
For EACH layer:
  - Log input to layer
  - Log output from layer
  - Check state propagation
  
Example trace:
  Application call → HAL function → Driver write → SPI DMA → Hardware
```

**Common Root Causes:**

| Layer | Typical Issues |
|-------|----------------|
| Application | Wrong API usage, missing config |
| HAL | Incorrect abstraction, missing error handling |
| Driver | Wrong register values, timing violations |
| Interface | DMA overflow, clock mismatch, alignment |
| Hardware | Power, wiring, timing |

### Phase 3: Hypothesis Testing

**Scientific method:**

1. **Form Single Hypothesis**
   ```
   "I think X is root cause because Y evidence shows..."
   ```
   Write it down - be specific

2. **Test Minimally**
   - ONE change at a time
   - Smallest possible modification
   - Don't fix multiple things together

3. **Verify Before Continuing**
   - Did fix work? → Document solution
   - Didn't work? → NEW hypothesis (don't add more fixes)

4. **If 3+ Fixes Failed**
   STOP. Question the architecture or approach.
   Discuss with your human partner.

### Phase 4: Fix Implementation

**Fix root cause, not symptom:**

1. **Create Failing Test (if possible)**
   ```c
   TEST_CASE("dma_overflow_detection") {
       // Test that triggers the bug
   }
   ```

2. **Implement Single Fix**
   - Address identified root cause
   - ONE change
   - No "while I'm here" improvements

3. **Verify Fix**
   ```bash
   # Full verification
   idf.py build
   idf.py -p COM3 flash monitor
   ```

4. **Document in AGENTS.md**
   ```yaml
   memory:
     - "Fixed DMA overflow: chunked transfer for >4092 bytes"
   ```

## Red Flags - STOP

If you catch yourself:
- "Quick fix, investigate later"
- "Just try changing X"
- "Multiple changes at once"
- "Skip test, manually verify"
- "It's probably X"
- "One more fix attempt" (after 2+)

**STOP. Return to Phase 1.**

## Common Embedded Errors

| Error | Pattern | Fix |
|-------|---------|-----|
| `Guru Meditation Error` | Memory corruption | Check pointer validity, stack size |
| `assert failed` | Logic error | Read assertion message, trace caller |
| `SPI DMA error` | Buffer too large | Chunk to <= 4092 |
| `Task watchdog` | Infinite loop/blocking | Check task flow, add yield |
| ` Brownout reset` | Power insufficient | Check power supply, reduce load |
| `I2C ACK error` | Device not responding | Check address, pull-ups, wiring |

## Platform-Specific Debug

### ESP32-S3

```bash
# Core dump analysis
idf.py coredump-info

# JTAG debug
idf.py openocd
idf.py gdb

# Memory analysis
idf.py size-components
```

### Windows PowerShell Serial
```powershell
# Quick check
python scripts/serial_monitor.ps1 -Port COM3 -Duration 30
```

### GUI Debug
```bash
# Capture current state
python scripts/camera_capture.py --session
# Compare with expected
python scripts/image_compare.py --before expected.png --after capture.png
```

## Output Format

```markdown
## Debug Session Report

### Symptom
{description of observed behavior}

### Evidence
- Monitor output: {key lines}
- Build status: {errors/warnings}
- Log analysis: {patterns found}

### Root Cause Hypothesis
"{specific hypothesis with evidence}"

### Fix Applied
{single change description}

### Verification
- Build: {PASS/FAIL}
- Monitor: {PASS/FAIL}
- Expected behavior restored: {YES/NO}

### Resolution
{final status: RESOLVED / NEEDS_INVESTIGATION}
```

## Integration with Iron Law

Every debug session MUST follow:
1. Evidence → 2. Root Cause → 3. Hypothesis → 4. Fix → 5. Verify

Skip any step = violation = wasted time