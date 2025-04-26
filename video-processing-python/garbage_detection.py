import os
import cv2
import json
import time
import argparse
import torch
from ultralytics import YOLO
from datetime import timedelta

def detect_garbage(video_path, output_json, confidence=0.5):
    if not os.path.isfile(video_path):
        print(f"Error: Video file '{video_path}' not found")
        return
    
    original_torch_load = torch.load
    
    def patched_torch_load(*args, **kwargs):
        if 'weights_only' not in kwargs:
            kwargs['weights_only'] = False
        return original_torch_load(*args, **kwargs)
    
    torch.load = patched_torch_load
    
    print("Loading YOLOv8 model...")
    model = YOLO("yolov8n.pt")
    
    print(f"Processing video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    print(f"Video FPS: {fps}")
    print(f"Total frames: {total_frames}")
    print(f"Duration: {timedelta(seconds=duration)}")
    
    garbage_timestamps = []
    garbage_classes = ['trash', 'garbage', 'waste', 'litter', 'bottle', 'can', 'plastic']
    
    frame_count = 0
    last_percent = 0
    
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % 5 == 0:
            timestamp = frame_count / fps
            formatted_time = str(timedelta(seconds=timestamp))
            
            percent_complete = int((frame_count / total_frames) * 100)
            if percent_complete > last_percent:
                print(f"Progress: {percent_complete}% - Current time: {formatted_time}", end='\r')
                last_percent = percent_complete
            
            results = model(frame, verbose=False)
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    class_id = int(box.cls.item())
                    class_name = model.names[class_id]
                    conf = box.conf.item()
                    
                    if (class_name.lower() in garbage_classes or 'garbage' in class_name.lower()) and conf >= confidence:
                        close_timestamps = [t for t in garbage_timestamps if abs(t["timestamp_seconds"] - timestamp) < 1.0]
                        if not close_timestamps:
                            garbage_timestamps.append({
                                "timestamp_seconds": timestamp,
                                "timestamp": formatted_time,
                                "confidence": conf,
                                "class": class_name
                            })
                        break
        
        frame_count += 1
    
    cap.release()
    
    process_time = time.time() - start_time
    print(f"\nProcessing completed in {process_time:.2f} seconds")
    print(f"Found garbage in {len(garbage_timestamps)} timestamps")
    
    with open(output_json, 'w') as f:
        json.dump({
            "video_file": os.path.basename(video_path),
            "duration_seconds": duration,
            "duration": str(timedelta(seconds=duration)),
            "garbage_detections": garbage_timestamps
        }, f, indent=4)
    
    print(f"Results saved to {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect garbage in videos using YOLOv8")
    parser.add_argument("video_path", help="Path to the input video file")
    parser.add_argument("--output", "-o", default="garbage_timestamps.json", 
                        help="Path to save the output JSON file (default: garbage_timestamps.json)")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for detections (default: 0.5)")
    
    args = parser.parse_args()
    
    detect_garbage(args.video_path, args.output, args.confidence) 