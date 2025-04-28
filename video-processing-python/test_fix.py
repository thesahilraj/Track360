import torch
from ultralytics import YOLO
from ultralytics.nn.tasks import DetectionModel
import torch.nn as nn

def test_model_loading():
    """Test if the model loading fix works with PyTorch 2.6+"""
    print("Testing YOLOv8 model loading with PyTorch fix...")
    print(f"PyTorch version: {torch.__version__}")
    
    # Fix for PyTorch 2.6+ weights_only issue by patching torch.load
    original_torch_load = torch.load
    
    def patched_torch_load(*args, **kwargs):
        # Force weights_only to False for PyTorch 2.6+
        if 'weights_only' not in kwargs:
            kwargs['weights_only'] = False
        return original_torch_load(*args, **kwargs)
    
    # Replace the original torch.load with our patched version
    torch.load = patched_torch_load
    
    try:
        # Try to load the model
        model = YOLO("yolov8n.pt")
        print("✅ Success! Model loaded correctly.")
        print(f"Model type: {type(model)}")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

if __name__ == "__main__":
    test_model_loading() 