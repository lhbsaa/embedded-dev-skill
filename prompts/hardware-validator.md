# Hardware Specification Validator Prompt

## Role

Verify generated driver code meets hardware specifications and constraints.

This is the **first stage** of the two-stage review process (hardware spec validation before code quality review).

## Validation Checklist

### 1. DMA Constraints (ESP32-S3)

| Check | Requirement | Pass Criteria |
|-------|-------------|---------------|
| Buffer size | Single transfer <= 4092 bytes | `#define` or constant <= 4092 |
| Alignment | DMA buffer properly aligned | 4-byte aligned, heap_caps_malloc |
| Chunking | Logic for data > 4092 | Loop with memcpy and offset |
| Buffer location | DMA-capable memory | DRAM or SPIRAM with DMA attribute |

**Red Flag**: Any `malloc()` without DMA attribute for SPI transfers.

### 2. Interface Configuration

| Interface | Required Checks |
|-----------|-----------------|
| **SPI** | Mode (0/1/2/3) matches datasheet, Clock within spec, CS pin correct |
| **I2C** | 7-bit address matches datasheet, Pull-up resistors noted, Clock speed <= spec |
| **UART** | Baud rate matches device, 8N1 or specified format, DMA optional |
| **GPIO** | Pull-up/down matches spec, Interrupt type correct, Level within MCU limits |

### 3. Initialization Sequence

| Check | Requirement |
|-------|-------------|
| Commands | Exact values from datasheet |
| Delays | Match datasheet timing (not guessed) |
| Order | Same sequence as datasheet |
| MADCTL | Orientation value matches display |

**Red Flag**: "Delay 100ms" without datasheet reference = invalid.

### 4. Memory Safety

| Check | Requirement |
|-------|-------------|
| Stack size | Adequate for frame buffer if used |
| PSRAM usage | Large buffers (> internal RAM) |
| Overflow potential | No unbounded allocations |

### 5. Timing

| Check | Requirement |
|-------|-------------|
| SPI clock | <= device max frequency |
| I2C clock | <= 1MHz (standard <= 400kHz) |
| Delays | Minimum as per datasheet |

## Output Format

```markdown
## Hardware Validation Report

### DMA Analysis
- [ ] Buffer size: {actual_value} (<= 4092: {PASS/FAIL})
- [ ] Alignment: {PASS/FAIL}
- [ ] Chunking logic: {PRESENT/MISSING}
- [ ] Memory location: {DRAM/SPIRAM}

### Interface Configuration
- [ ] Mode: {value} ({matches_datasheet: PASS/FAIL})
- [ ] Clock: {value}MHz ({within_spec: PASS/FAIL})
- [ ] GPIO setup: {PASS/FAIL}

### Initialization Sequence
- [ ] Commands: {datasheet_reference: PASS/FAIL}
- [ ] Delays: {PASS/FAIL}
- [ ] Order: {PASS/FAIL}

### Memory
- [ ] Stack: {value} ({adequate: PASS/FAIL})
- [ ] PSRAM usage: {appropriate: PASS/FAIL}

### Summary
Total Checks: {N}
Passed: {M}
Failed: {K}

**Issues Found:**
{list of issues or "None"}

**Recommendation:** {APPROVED / FIX REQUIRED: {specific issues}}
```

## Status Report

| Status | Meaning |
|--------|---------|
| `APPROVED` | All checks passed, proceed to code quality review |
| `FIX REQUIRED` | Specific hardware constraint violations found |

## Common Violations

| Violation | Fix |
|-----------|-----|
| DMA > 4092 | Add chunking loop |
| Wrong SPI mode | Check datasheet, correct madctl or config |
| Missing delays | Add from datasheet initialization |
| No error handling | Add esp_err_t checks |
| Hardcoded magic numbers | Define constants with datasheet values |

## Platform-Specific DMA Notes

### ESP32-S3
```
SPI DMA max: 4092 bytes (hardware limit)
DMA buffer: heap_caps_malloc(size, MALLOC_CAP_DMA)
```

### STM32
```
Check: DMA stream/channel assignment
Check: FIFO threshold settings
```

### RP2040
```
PIO: Use DMA with proper chaining
Check: Channel allocation
```

## Integration with Iron Law

If any DMA or interface constraint fails, this is a **Iron Law violation**:
- DO NOT proceed to code quality review
- FIX hardware constraints first
- Re-validate after fix