# app/models.py

from ultralytics import YOLOv10  # Correct class import
import torch
from .utils.device_setup import setup_device
import logging
from collections import deque
from datetime import timedelta

logger = logging.getLogger(__name__)

device = setup_device()
selected_model = None
model_loaded = False

# Shared variables
category_dict = {
    0: "Grade A Birdnest",
    1: "Grade B Birdnest",
    2: "Grade C Birdnest",
    3: "Unknown",
}

birdnest_descriptions = {
    "Grade A Birdnest": "Grade A edible bird nests are of the highest quality...",
    "Grade B Birdnest": "Grade B edible bird nests are considered mid-tier in quality...",
    "Grade C Birdnest": "Grade C edible bird nests are of the lowest quality among the three grades.",
    "Unknown": "other objects",
}

latest_detected_class = None
latest_confidence_score = 0.0
recent_images = deque(maxlen=5)
accumulated_counts = {
    "Grade A Birdnest": 0,
    "Grade B Birdnest": 0,
    "Grade C Birdnest": 0,
}

# Cooldown mechanism
last_count_time = {
    "Grade A Birdnest": None,
    "Grade B Birdnest": None,
    "Grade C Birdnest": None,
}
cooldown_period = timedelta(seconds=10)  # Adjust as needed

def load_model(model_name: str = "yolov10", model_path: str = ""):
    global selected_model, model_loaded
    if not model_path:
        model_path = "previous_best.pt"  # Set default to 'current_best.pt'
    try:
        logger.info(f"Attempting to load model '{model_name}' from path: {model_path}")
        if model_name in ["yolov8", "yolov9", "yolov10"]:
            selected_model = YOLOv10(model_path).to(device)
            model_loaded = True
            logger.info(f"{model_name} loaded successfully from {model_path}.")
        else:
            raise ValueError("Unsupported model selected.")
    except Exception as e:
        logger.error(f"Failed to load model '{model_name}' from '{model_path}': {e}")
        raise

 