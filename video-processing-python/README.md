# Multi-Purpose Video Detection using YOLOv8

This project provides scripts for detecting various objects and violations in videos using YOLOv8 and generating a JSON file with timestamps. It can detect:

- **Garbage/Litter**: Bottles, cans, plastic, and other trash
- **Road Issues**: Potholes and broken roads 
- **Traffic Violations**: Two-wheelers without helmets

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. YOLOv8 will automatically download the model weights when you first run the script.

3. **Important Note for PyTorch 2.6+ Users**: 
   - These scripts automatically handle the PyTorch 2.6+ compatibility issue by patching the `torch.load` function.
   - The patch sets `weights_only=False` when loading models, which is required for YOLOv8 to function properly.
   - This approach is safe when using official YOLOv8 models from trusted sources.

## Basic Usage

```
python garbage_detection.py path/to/your/video.mp4 [options]
```

### Options

- `--output`, `-o`: Path to save the output JSON file (default: garbage_timestamps.json)
- `--confidence`, `-c`: Confidence threshold for detections (default: 0.5)

### Example

```
python garbage_detection.py my_video.mp4 --output results.json --confidence 0.45
```

## Advanced Usage with Multiple Detection Types

The advanced script offers more features, including visualization, model selection, and multiple detection types:

```
python garbage_detection_advanced.py path/to/your/video.mp4 [options]
```

### Additional Options in Advanced Script

- `--model`, `-m`: YOLOv8 model size (n, s, m, l, x) (default: n for nano)
- `--visualize`, `-v`: Create a visualization video showing the detections
- `--output-video`: Path to save the visualization video (default: input_detections.mp4)
- `--categories`: List of categories to detect (options: garbage, pothole, broken_road, no_helmet)

### Examples

#### Detect All Categories
```
python garbage_detection_advanced.py my_video.mp4 --visualize
```

#### Detect Only Garbage and Potholes
```
python garbage_detection_advanced.py my_video.mp4 --categories garbage pothole --visualize
```

#### Detect Two-wheelers Without Helmets with High Accuracy
```
python garbage_detection_advanced.py my_video.mp4 --model m --categories no_helmet --confidence 0.4 --visualize
```

## Output

The script will generate a JSON file with the following structure:

```json
{
    "video_file": "my_video.mp4",
    "duration_seconds": 120.5,
    "duration": "0:02:00.500000",
    "detection_summary": {
        "garbage": 10,
        "pothole": 5,
        "broken_road": 3,
        "no_helmet": 7
    },
    "detections": [
        {
            "timestamp_seconds": 10.5,
            "timestamp": "0:00:10.500000",
            "detections": [
                {
                    "category": "garbage",
                    "class": "bottle",
                    "confidence": 0.67,
                    "bounding_box": [100, 150, 200, 250]
                }
            ]
        },
        {
            "timestamp_seconds": 15.2,
            "timestamp": "0:00:15.200000",
            "detections": [
                {
                    "category": "pothole",
                    "class": "pothole",
                    "confidence": 0.85,
                    "bounding_box": [300, 400, 350, 450]
                },
                {
                    "category": "no_helmet",
                    "class": "no_helmet_rider",
                    "confidence": 0.72,
                    "bounding_box": [100, 200, 150, 300]
                }
            ]
        }
    ]
}
```

## Notes

- The script processes frames at regular intervals to speed up detection. You can adjust the `processing_interval` in the code if needed.
- For better accuracy but slower processing, use larger models (m/l/x).
- The visualization feature creates a new video file with detection highlights with different colors for each category:
  - Garbage: Green
  - Potholes: Red
  - Broken Roads: Blue
  - No Helmet Riders: Yellow
- **Implementation Notes**: In a real-world implementation, specialized models trained specifically for road defects and helmet detection would be used for better accuracy. The current implementation uses simulated detections for demonstration purposes.
- **PyTorch 2.6+ Compatibility**: These scripts automatically handle PyTorch 2.6+ compatibility by internally patching the `torch.load` function to use `weights_only=False`. This is necessary for YOLOv8 models to load properly without requiring manual specification of every class in `safe_globals`. 