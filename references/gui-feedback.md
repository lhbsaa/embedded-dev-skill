# GUI Visual Feedback Implementation Guide

## Overview

This guide explains how to implement GUI visual feedback for embedded development, enabling AI agents to capture, analyze, and compare LCD display outputs.

---

## System Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  USB Camera │────▶│ Python Script│────▶│ Image File  │
│  (Hardware) │     │ (Capture)    │     │ (.png)      │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ AI Agent    │────▶│ image_read   │────▶│ Analysis    │
│ (Claude)    │     │ (VL Model)   │     │ Report      │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## Agent Workflow

### Step 1: Capture GUI Image

```yaml
Agent Action: run_shell_command
Command: python scripts/camera_capture.py --session --resolution 1920x1080
Output: {
  "success": true,
  "output_dir": "screenshots/session_20260409_162300",
  "captures": ["screenshots/session_20260409_162300/capture_001.png"],
  "count": 1
}
```

### Step 2: Analyze with image_read

```yaml
Agent Action: image_read
Input: screenshots/session_20260409_162300/capture_001.png
Prompt: "Analyze this LCD display. Check:
  - Layout: element positions, spacing, alignment
  - Text: font size, clarity, overflow, truncation
  - Colors: RGB values, contrast, saturation
  - Issues: overlapping elements, missing content, rendering errors
  
  Output JSON format with: current_state, issues, suggestions"
```

### Step 3: Apply Code Changes

```yaml
Agent Action: replace/write_file
Based on analysis, modify display code:
  - Adjust font sizes
  - Fix layout positions
  - Correct color values
```

### Step 4: Capture After Changes

```yaml
Agent Action: run_shell_command
Command: python scripts/camera_capture.py --output screenshots/session_20260409_162300
Filename: capture_002.png (after)
```

### Step 5: Compare Before/After

```yaml
Agent Action: run_shell_command
Command: python scripts/image_compare.py 
         --before screenshots/session_.../capture_001.png
         --after screenshots/session_.../capture_002.png
         --output screenshots/session_.../compare

Output: {
  "similarity": {"similarity_percent": 85.5},
  "change_count": 12,
  "significant_changes": 3,
  "changes": [...]
}
```

### Step 6: Verify Changes

```yaml
Agent Action: image_read
Input: diff image or highlighted comparison
Verify: Changes applied correctly, no new issues introduced
```

---

## Camera Configuration

### Recommended Hardware

| Camera | Resolution | FPS | Notes |
|--------|------------|-----|-------|
| Logitech C920 | 1920x1080 | 30 | Good quality, auto-focus |
| Logitech C270 | 1280x720 | 30 | Budget option |
| USB Webcam Generic | 640x480 | 30 | Basic testing |

### Camera Positioning

```
    ┌──────────────────┐
    │   USB Camera     │  ← Position 15-20cm from screen
    │   (top view)     │
    └──────────────────┘
           │
           ▼
    ┌──────────────────┐
    │   LCD Display    │  ← Target device
    │   (MimiClaw-1.3) │
    └──────────────────┘
```

### Lighting Requirements

- Avoid direct light reflections
- Use diffused lighting
- Dark environment preferred for OLED/LCD
- White background for contrast

---

## Script Usage

### camera_capture.py

```bash
# List available cameras
python scripts/camera_capture.py --list

# Single capture
python scripts/camera_capture.py --resolution 1920x1080

# Session capture (creates timestamped folder)
python scripts/camera_capture.py --session

# Multiple captures with interval
python scripts/camera_capture.py --count 5 --interval 2

# Custom output directory
python scripts/camera_capture.py --output my_screenshots

# With metadata
python scripts/camera_capture.py --metadata '{"device":"ESP32-S3","lcd":"SH8601"}'
```

### image_compare.py

```bash
# Basic comparison
python scripts/image_compare.py --before img1.png --after img2.png

# Custom threshold (sensitivity)
python scripts/image_compare.py --before img1.png --after img2.png --threshold 50

# Custom output directory
python scripts/image_compare.py --before img1.png --after img2.png --output my_compare
```

---

## Output Format

### Capture Metadata (JSON)

```json
{
  "timestamp": "2026-04-09T16:23:00",
  "resolution": "1920x1080",
  "device": 0,
  "device_info": "ESP32-S3",
  "lcd": "SH8601"
}
```

### Comparison Report (JSON)

```json
{
  "timestamp": "2026-04-09T16:25:00",
  "similarity": {
    "correlation": 0.855,
    "mse": 125.5,
    "similarity_percent": 85.5
  },
  "change_count": 12,
  "significant_changes": 3,
  "changes": [
    {
      "id": 1,
      "area_pixels": 2500,
      "bbox": {"x": 100, "y": 50, "width": 80, "height": 30},
      "relative": {"x_percent": 5.2, "y_percent": 2.6}
    }
  ]
}
```

---

## Agent Prompt Templates

### GUI Analysis Prompt

```markdown
Analyze this embedded device LCD display screenshot.

Context:
- Device: {device_name}
- LCD: {lcd_driver}
- Resolution: {resolution}

Tasks:
1. Layout Analysis
   - Identify all visible elements (text, icons, graphics)
   - Check positions and spacing
   - Detect alignment issues

2. Text Analysis
   - Read all visible text content
   - Check font sizes and clarity
   - Detect overflow or truncation

3. Color Analysis
   - Identify dominant colors with RGB values
   - Check contrast ratios
   - Detect color anomalies

4. Issue Detection
   - Overlapping elements
   - Missing content
   - Rendering errors
   - Pixel artifacts

Output Format (JSON):
{
  "elements": [...],
  "text_content": {...},
  "colors": {...},
  "issues": [...],
  "suggestions": [...],
  "code_changes": [...]
}
```

---

## Integration with Embedded Development

### Typical Workflow

```yaml
Phase 1: Development
  - Write display driver code
  - Compile and flash: idf.py build flash
  
Phase 2: Visual Check
  - Capture: python scripts/camera_capture.py --session
  - Analyze: image_read with VL prompt
  
Phase 3: Iteration
  - Apply fixes based on analysis
  - Recapture and compare
  
Phase 4: Validation
  - Compare before/after
  - Verify all issues resolved
  - Update AGENTS.md with findings
```

---

## Best Practices

1. **Consistent Capture Conditions**
   - Same camera position
   - Same lighting
   - Same resolution

2. **Session Organization**
   - Use --session for grouped captures
   - Keep before/after pairs together

3. **Metadata Documentation**
   - Include device info in metadata
   - Record firmware version

4. **Comparison Threshold**
   - Default: 30 (medium sensitivity)
   - Lower (15-20): More sensitive, detects subtle changes
   - Higher (40-50): Less sensitive, only major changes

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Camera not detected | Check USB connection, try different port |
| Poor image quality | Adjust lighting, clean camera lens |
| Reflection on screen | Use polarizing filter or change angle |
| Low resolution | Specify --resolution 1920x1080 |
| Comparison shows too many changes | Increase threshold (50-80) |