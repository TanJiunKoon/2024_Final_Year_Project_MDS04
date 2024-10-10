# app/utils/device_setup.py

import torch

def setup_device():
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")
    return device
