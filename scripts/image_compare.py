#!/usr/bin/env python3
"""
Image Comparison Script for GUI Visual Feedback
Usage: python image_compare.py [options]

Options:
  --before        Before image path
  --after         After image path
  --output        Output directory for diff image
  --threshold     Difference threshold (default: 30)
  --highlight     Highlight color for differences
"""

import argparse
import cv2
import json
import numpy as np
import sys
from pathlib import Path
from datetime import datetime


def load_image(path):
    """Load image from file"""
    img = cv2.imread(str(path))
    if img is None:
        raise RuntimeError(f"Cannot load image: {path}")
    return img


def compute_difference(before, after, threshold=30):
    """Compute pixel-wise difference between images"""
    # Ensure same size
    if before.shape != after.shape:
        # Resize to match
        after = cv2.resize(after, (before.shape[1], before.shape[0]))
    
    # Compute absolute difference
    diff = cv2.absdiff(before, after)
    
    # Convert to grayscale for thresholding
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold
    _, thresh = cv2.threshold(gray_diff, threshold, 255, cv2.THRESH_BINARY)
    
    # Find contours of changed regions
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return diff, thresh, contours


def compute_similarity(before, after):
    """Compute similarity metrics"""
    # Convert to grayscale
    gray1 = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
    
    # Structural Similarity (SSIM) - simplified
    # Using correlation coefficient as approximation
    corr = np.corrcoef(gray1.flatten(), gray2.flatten())[0, 1]
    
    # Mean Squared Error
    mse = np.mean((before.astype(float) - after.astype(float)) ** 2)
    
    # Histogram comparison
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
    hist_corr = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    
    return {
        "correlation": round(corr, 4),
        "mse": round(mse, 2),
        "histogram_correlation": round(hist_corr, 4),
        "similarity_percent": round(corr * 100, 2)
    }


def highlight_differences(base_img, contours, color=(0, 0, 255)):
    """Highlight changed regions on image"""
    result = base_img.copy()
    
    # Draw contours
    cv2.drawContours(result, contours, -1, color, 2)
    
    # Add labels for significant changes
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 100:  # Filter small changes
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(result, (x, y), (x+w, y+h), color, 1)
            cv2.putText(result, f"#{i+1}", (x, y-5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    return result


def analyze_changes(contours, img_shape):
    """Analyze change regions"""
    changes = []
    
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        
        # Calculate relative position
        rel_x = round(x / img_shape[1] * 100, 2)
        rel_y = round(y / img_shape[0] * 100, 2)
        rel_w = round(w / img_shape[1] * 100, 2)
        rel_h = round(h / img_shape[0] * 100, 2)
        
        changes.append({
            "id": i + 1,
            "area_pixels": int(area),
            "bbox": {"x": x, "y": y, "width": w, "height": h},
            "relative": {"x_percent": rel_x, "y_percent": rel_y, 
                         "width_percent": rel_w, "height_percent": rel_h}
        })
    
    return changes


def save_comparison(before_path, after_path, output_dir, threshold=30):
    """Perform full comparison and save results"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load images
    before = load_image(before_path)
    after = load_image(after_path)
    
    # Compute differences
    diff, thresh, contours = compute_difference(before, after, threshold)
    
    # Compute similarity
    similarity = compute_similarity(before, after)
    
    # Analyze changes
    changes = analyze_changes(contours, before.shape)
    
    # Create highlighted comparison
    highlighted_before = highlight_differences(before, contours, (0, 0, 255))
    highlighted_after = highlight_differences(after, contours, (0, 255, 0))
    
    # Save diff images
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    diff_path = output_path / f"diff_{timestamp}.png"
    cv2.imwrite(str(diff_path), diff)
    
    thresh_path = output_path / f"threshold_{timestamp}.png"
    cv2.imwrite(str(thresh_path), thresh)
    
    highlight_before_path = output_path / f"before_highlighted_{timestamp}.png"
    cv2.imwrite(str(highlight_before_path), highlighted_before)
    
    highlight_after_path = output_path / f"after_highlighted_{timestamp}.png"
    cv2.imwrite(str(highlight_after_path), highlighted_after)
    
    # Save comparison report
    report = {
        "timestamp": datetime.now().isoformat(),
        "before_image": str(before_path),
        "after_image": str(after_path),
        "threshold": threshold,
        "similarity": similarity,
        "change_count": len(contours),
        "significant_changes": len([c for c in changes if c["area_pixels"] > 100]),
        "changes": changes,
        "outputs": {
            "diff": str(diff_path),
            "threshold": str(thresh_path),
            "before_highlighted": str(highlight_before_path),
            "after_highlighted": str(highlight_after_path)
        }
    }
    
    report_path = output_path / f"report_{timestamp}.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Image Comparison for GUI Visual Feedback')
    parser.add_argument('--before', '-b', type=str, required=True, help='Before image path')
    parser.add_argument('--after', '-a', type=str, required=True, help='After image path')
    parser.add_argument('--output', '-o', type=str, default='compare', help='Output directory')
    parser.add_argument('--threshold', '-t', type=int, default=30, help='Difference threshold')
    parser.add_argument('--highlight', type=str, default='red', help='Highlight color')
    
    args = parser.parse_args()
    
    try:
        report = save_comparison(
            args.before, 
            args.after, 
            args.output, 
            args.threshold
        )
        
        # Print summary
        print(json.dumps(report, indent=2))
        
        # Print human-readable summary
        print("\n" + "="*50)
        print("COMPARISON SUMMARY")
        print("="*50)
        print(f"Similarity: {report['similarity']['similarity_percent']}%")
        print(f"Change regions: {report['change_count']}")
        print(f"Significant changes: {report['significant_changes']}")
        print("="*50)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
