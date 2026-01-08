import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np

# Load a lightweight CNN
_model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
_model.fc = nn.Linear(_model.fc.in_features, 2)  # real vs fake
_model.eval()

# TODO: replace with your fine-tuned weights when ready
# _model.load_state_dict(torch.load("deepfake_resnet18.pth", map_location="cpu"))

_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

@torch.no_grad()
def predict_frame(frame_bgr: np.ndarray) -> float:
    img = Image.fromarray(frame_bgr[:, :, ::-1])  # BGR → RGB
    x = _transform(img).unsqueeze(0)
    logits = _model(x)
    probs = torch.softmax(logits, dim=1)
    fake_prob = probs[0, 1].item()
    return fake_prob
