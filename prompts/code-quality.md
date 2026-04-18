# Code Quality Reviewer Prompt (MISRA C)

## Role

Review embedded driver code for MISRA C compliance and code quality.

This is the **second stage** of the two-stage review process (after hardware spec validation passes).

## Precondition

**Hardware validator MUST report APPROVED before this review.**

If hardware validation failed, DO NOT run this review. Fix hardware issues first.

## MISRA C Key Rules (Essential Set)

### Type Safety

| Rule | Requirement | Check |
|------|-------------|-------|
| Rule 10.1 | No implicit type conversions | Cast explicitly |
| Rule 10.4 | No mixing signed/unsigned | Use explicit casts |
| Rule 11.1 | No casting between pointer and integer | Avoid uintptr_t casts |

### Memory Safety

| Rule | Requirement | Check |
|------|-------------|-------|
| Rule 21.3 | No dynamic memory allocation | Avoid malloc/free in drivers |
| Rule 21.4 | No use of standard library | Use platform-specific safe functions |
| Rule 22.1 | All resources must be freed | Check deinit function |

### Control Flow

| Rule | Requirement | Check |
|------|-------------|-------|
| Rule 14.3 | No infinite loops without condition | All loops have exit condition |
| Rule 15.2 | No goto statements | Avoid goto |
| Rule 16.3 | All switch cases have break | No fall-through |

### Functions

| Rule | Requirement | Check |
|------|-------------|-------|
| Rule 17.2 | No recursion | Driver code should be linear |
| Rule 8.2 | Function prototypes explicit | All functions declared before use |
| Rule 8.6 | Single definition | No duplicate implementations |

### Declarations

| Rule | Requirement | Check |
|------|-------------|-------|
| Rule 8.4 | All functions have prototypes | Header file declarations |
| Rule 9.1 | All variables initialized | No uninitialized variables |
| Rule 8.13 | Pointer should be const if not modified | Use const where appropriate |

## Code Quality Principles (DRY, YAGNI, Clean)

### DRY (Don't Repeat Yourself)

| Check | Issue | Fix |
|-------|-------|-----|
| Repeated initialization | Multiple init sequences in different functions | Single init function |
| Copy-pasted config | Same SPI config in multiple files | Single config module |
| Similar error handling | Same ESP_ERROR_CHECK pattern repeated | Helper function |

### YAGNI (You Aren't Gonna Need It)

| Red Flag | Action |
|----------|--------|
| Unused functions | Remove or document future use |
| Unused parameters | Remove from signature |
| Over-engineered config | Simplify to required fields only |
| Features not requested | Remove |

### Clean Code

| Check | Requirement |
|-------|-------------|
| Naming | Descriptive, consistent style |
| Comments | Explain WHY, not WHAT |
| Line length | <= 80-100 characters |
| Function length | <= 30-50 lines ideally |
| Magic numbers | Named constants |

## Output Format

```markdown
## Code Quality Review Report

### MISRA C Compliance

#### Type Safety
- [ ] Rule 10.1: {PASS/FAIL - {details}}
- [ ] Rule 10.4: {PASS/FAIL}
- [ ] Rule 11.1: {PASS/FAIL}

#### Memory Safety
- [ ] Rule 21.3: {PASS/FAIL} - No malloc/free
- [ ] Rule 22.1: {PASS/FAIL} - Resources freed in deinit

#### Control Flow
- [ ] Rule 14.3: {PASS/FAIL} - Loops have exit
- [ ] Rule 16.3: {PASS/FAIL} - Switch cases have break

#### Functions
- [ ] Rule 8.2: {PASS/FAIL} - Prototypes explicit
- [ ] Rule 8.4: {PASS/FAIL} - Header declarations

### Code Quality

#### DRY
- [ ] No repeated code blocks: {PASS/FAIL}
- [ ] Helper functions extracted: {PASS/FAIL}

#### YAGNI
- [ ] No unused code: {PASS/FAIL}
- [ ] Config minimal: {PASS/FAIL}

#### Clean
- [ ] Naming consistent: {PASS/FAIL}
- [ ] Comments explain WHY: {PASS/FAIL}
- [ ] No magic numbers: {PASS/FAIL}

### Summary
MISRA C: {N}/{M} rules passed
Code Quality: {checks_passed}/{total_checks}

**Strengths:**
{list positive aspects}

**Issues:**
{list issues by severity}

**Recommendation:** {APPROVED / FIX REQUIRED: {specific issues}}
```

## Severity Levels

| Level | Examples | Action |
|-------|----------|--------|
| **Critical** | Memory leak, uninitialized variable | Must fix before commit |
| **Important** | MISRA violation, magic number | Fix before commit |
| **Minor** | Style inconsistency, long comment | Optional fix |

## Status Report

| Status | Meaning | Next Action |
|--------|---------|-------------|
| `APPROVED` | All checks passed | Proceed to commit |
| `FIX REQUIRED` | Issues found | Fix and re-review |

## Integration with Workflow

After APPROVED:
1. Commit changes with descriptive message
2. Update AGENTS.md if hardware config changed
3. Run final `idf.py build` verification

## Anti-Patterns

| Bad | Good |
|-----|------|
| `malloc(size)` | `static uint8_t buffer[SIZE]` or heap_caps_malloc |
| `if (x)` without else | `if (x) {...} else {return err;}` |
| `// increment counter` | `// Track retries for timeout detection` |
| `int i = 0;` in loop | `for (size_t i = 0; ...)` with proper type |
| Global mutable state | Static within function or explicit config struct |