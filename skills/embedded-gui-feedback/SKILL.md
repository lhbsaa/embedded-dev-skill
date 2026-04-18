---
name: embedded-gui-feedback
description: Use for LCD/GUI projects after verification passes - captures display via camera, analyzes layout/font/color, detects display issues
---

# Embedded GUI Feedback

## Overview

Visual verification for LCD/GUI projects. Human eye misses timing, alignment, and color issues. Camera capture + AI analysis catches them.

**Core principle:** Camera evidence, not human judgment.

**Context:** Run after `embedded-verification` passes for display projects.

**When NOT to use:** Projects without GUI/display components.

## When to Use

- LCD driver projects
- Display configuration changes
- GUI layout updates
- Font/color modifications
- Any visual output project

## Camera Setup

### Requirements
- USB webcam (1080p recommended)
- Centered on LCD screen
- Uniform lighting (avoid glare)
- Distance: 15-30cm from screen

### Windows Setup
```powershell
# List cameras
python scripts/camera_capture.py --list

# Capture
python scripts/camera_capture.py --resolution 1920x1080 --session
```

### Linux/macOS Setup
```bash
# List cameras
python scripts/camera_capture.py --list

# Capture
python scripts/camera_capture.py --resolution 1920x1080 --session
```

## Process

### 1. Check Camera Available

```
Run: python scripts/camera_capture.py --list

If no cameras:
- Prompt user to connect camera
- Offer alternative: manual photo upload
```

### 2. Capture Display

```
Run: python scripts/camera_capture.py --session

Output: screenshots/capture_YYYYMMDD_HHMMSS.png
```

**Session folder:** Creates timestamped folder for multiple captures.

### 3. Image Analysis

Use `image_read` tool with analysis prompt:

```markdown
Analyze LCD display for:
- Layout: Correct positioning?
- Font: Readable, correct size?
- Color: Expected colors displayed?
- Alignment: Elements aligned properly?
- Overlap: Any overlapping elements?
- Blank areas: Unexpected empty regions?

Compare to expected: [describe expected output]
```

### 4. Issue Detection

| Issue Type | Visual Indicator | Likely Cause |
|------------|------------------|--------------|
| Blank screen | No pixels | Init sequence wrong |
| Partial display | Top/bottom missing | MADCTL value incorrect |
| Color wrong | Wrong colors | Color format mismatch |
| Offset display | Content shifted | y_gap/x_gap incorrect |
| Mirror/flip | Content reversed | MADCTL rotation bits |
| Flickering | Brightness varies | Refresh timing |
| Lines missing | Horizontal gaps | DMA chunking issue |

### 5. Fix and Re-verify

```
If issues found:
1. Analyze cause from table
2. Apply fix
3. idf.py build flash monitor
4. Re-capture display
5. Re-analyze
6. Loop until approved
```

### 6. Save Evidence

```
Write: docs/embedded/screenshots/YYYY-MM-DD-<feature>-analysis.md

Include:
- Before/after captures
- Issue descriptions
- Fixes applied
- Final status
```

## Analysis Prompt Template

Use `prompts/gui-feedback.md` or inline:

```
Context: [Chip] + [Controller] + [Resolution]

Expected Display:
[Describe what should be shown]

Image: [path to capture]

Analyze for issues:
1. Blank screen → check init
2. Partial → check MADCTL
3. Wrong colors → check format
4. Offset → check gaps
5. Mirror → check rotation
6. Flickering → check timing
7. Gaps → check DMA

Provide:
- Issues found: [list]
- Likely cause: [analysis]
- Recommended fix: [action]
```

## Comparison Workflow

For before/after analysis:

```powershell
# Capture before
python scripts/camera_capture.py --session --count 1

# Apply fix
idf.py build flash monitor

# Capture after
python scripts/camera_capture.py --session --count 1

# Compare
python scripts/image_compare.py --before [before.png] --after [after.png]
```

## Common Fixes

| Issue | Fix Location | Parameter |
|-------|--------------|-----------|
| Blank | Driver init | Reset sequence |
| Partial | MADCTL | 0x00/0xC0/0x80 |
| Offset | Driver config | y_gap, x_gap |
| Mirror | MADCTL | Bit 5, 6, 7 |
| Color | Color format | RGB565/RGB666 |
| DMA overflow | Write function | Chunk size |

## Red Flags - STOP

- "Looks fine to me" (no camera)
- Skipping camera capture
- No analysis before claiming "correct"
- Single capture (no comparison available)
- Truncated image analysis

**ALL mean: STOP. Capture with camera, analyze properly.**

## Output Format

```markdown
## GUI Feedback Report

### Capture
Camera: [status]
File: screenshots/[filename].png
Resolution: 1920x1080

### Analysis
Layout: [PASS/FAIL] - [details]
Font: [PASS/FAIL] - [details]
Color: [PASS/FAIL] - [details]
Alignment: [PASS/FAIL] - [details]
Overlap: [PASS/FAIL] - [details]

### Issues
[list or "None detected"]

### Fixes Applied
[list or "None needed"]

### Final Status
GUI: APPROVED / NEEDS FIX
Evidence: [capture path]
```

## Transition

**If GUI APPROVED:**
```
GUI verification complete.
Project finished. Update AGENTS.md with findings.

Full workflow complete:
- brainstorming → driver-design → implementation → verification → gui-feedback
```

**If GUI NEEDS FIX:**
```
GUI issues detected. Apply fixes, re-verify, re-capture.
Do NOT claim completion until GUI approved.
```

## Anti-Patterns

| Bad | Good |
|-----|------|
| "Display looks correct" | Camera capture + analysis |
| Skip camera | Always capture for GUI projects |
| Single glance | Multiple captures, comparison |
| No before/after | Capture before fix, compare after |
| Human judgment only | AI analysis + visual evidence |