#!/usr/bin/env python
"""
Example usage of the video detection scripts.
This script demonstrates how to:
1. Run detection on a video for garbage, potholes, broken roads, and two-wheelers without helmets
2. Parse the JSON output
3. Create a visualization video

You can modify the video_path variable to point to your own video file.
"""

import os
import json
import subprocess
from datetime import timedelta

# Set the path to your video file here
video_path = "video.mp4"  # Replace with your actual video path

def run_basic_garbage_detection(video_path, output_json="results_basic.json"):
    """Run basic garbage detection"""
    print("\n===== Running Basic Garbage Detection =====")
    cmd = f"python garbage_detection.py {video_path} --output {output_json} --confidence 0.45"
    print(f"Executing: {cmd}")
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Detection completed successfully. Results saved to {output_json}")
        return output_json
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running detection: {e}")
        return None

def run_advanced_detection(video_path, output_json="results_advanced.json", categories=None):
    """Run advanced detection with multiple categories and visualization"""
    category_str = " ".join(categories) if categories else ""
    category_arg = f"--categories {category_str}" if categories else ""
    
    print(f"\n===== Running Advanced Detection ({category_str or 'All Categories'}) with Visualization =====")
    cmd = (f"python garbage_detection_advanced.py {video_path} --output {output_json} "
           f"--model m --confidence 0.45 --visualize {category_arg}")
    print(f"Executing: {cmd}")
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Detection completed successfully. Results saved to {output_json}")
        
        # Determine the visualization output path
        basename, ext = os.path.splitext(video_path)
        viz_path = f"{basename}_detections{ext}"
        print(f"✅ Visualization saved to {viz_path}")
        
        return output_json
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running detection: {e}")
        return None

def parse_and_display_results(json_path):
    """Parse and display the detection results"""
    if not os.path.isfile(json_path):
        print(f"❌ Result file not found: {json_path}")
        return
    
    print(f"\n===== Results from {json_path} =====")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    video_file = data.get("video_file", "Unknown")
    duration = data.get("duration", "Unknown")
    
    # Check if it's the new format or old format
    if "detections" in data:
        # New format with multiple categories
        detections = data.get("detections", [])
        summary = data.get("detection_summary", {})
        
        print(f"Video: {video_file}")
        print(f"Duration: {duration}")
        print("\nDetection Summary:")
        for category, count in summary.items():
            print(f"- {category.capitalize()}: {count} detections")
        
        print(f"\nTotal frames with detections: {len(detections)}")
        
        if detections:
            print("\nSample detections (first 10 frames):")
            for i, frame_detection in enumerate(detections[:10], 1):
                timestamp = frame_detection.get("timestamp", "Unknown")
                items = frame_detection.get("detections", [])
                print(f"{i}. {timestamp} - {len(items)} items detected:")
                for item in items[:3]:  # Show max 3 items per frame
                    category = item.get("category", "Unknown")
                    class_name = item.get("class", "Unknown")
                    confidence = item.get("confidence", 0.0)
                    print(f"   - {category}: {class_name} (confidence: {confidence:.2f})")
                
                if len(items) > 3:
                    print(f"   - ... and {len(items) - 3} more items")
            
            if len(detections) > 10:
                print(f"... and {len(detections) - 10} more frames with detections")
    
    else:
        # Old format with only garbage detections
        detections = data.get("garbage_detections", [])
        
        print(f"Video: {video_file}")
        print(f"Duration: {duration}")
        print(f"Total garbage detections: {len(detections)}")
        
        if detections:
            print("\nTimestamps where garbage was detected:")
            for i, detection in enumerate(detections[:10], 1):  # Show first 10 detections
                timestamp = detection.get("timestamp", "Unknown")
                confidence = detection.get("confidence", 0.0)
                class_name = detection.get("class", "Unknown")
                print(f"{i}. {timestamp} - {class_name} (confidence: {confidence:.2f})")
            
            if len(detections) > 10:
                print(f"... and {len(detections) - 10} more detections")

def main():
    print("=" * 70)
    print("MULTI-PURPOSE VIDEO DETECTION EXAMPLE")
    print("=" * 70)
    
    # Check if video file exists
    if not os.path.isfile(video_path):
        print(f"❌ Video file not found: {video_path}")
        print("Please modify the 'video_path' variable in this script to point to your actual video file.")
        return
    
    # Run basic detection (garbage only)
    basic_results = run_basic_garbage_detection(video_path)
    if basic_results:
        parse_and_display_results(basic_results)
    
    # Run advanced detection with all categories
    advanced_results = run_advanced_detection(video_path, "results_all_categories.json")
    if advanced_results:
        parse_and_display_results(advanced_results)
    
    # Run just garbage and potholes detection
    garbage_pothole_results = run_advanced_detection(
        video_path, 
        "results_garbage_potholes.json", 
        ["garbage", "pothole"]
    )
    if garbage_pothole_results:
        parse_and_display_results(garbage_pothole_results)
    
    # Run just helmet detection with higher sensitivity
    helmet_results = run_advanced_detection(
        video_path, 
        "results_no_helmet.json", 
        ["no_helmet"]
    )
    if helmet_results:
        parse_and_display_results(helmet_results)
    
    print("\n" + "=" * 70)
    print("Example completed. You can now view the JSON files and visualization videos.")
    print("=" * 70)

if __name__ == "__main__":
    main() 