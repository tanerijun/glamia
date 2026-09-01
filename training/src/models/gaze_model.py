from torch import nn


class GazeModel(nn.Module):
    def __init__(self, backbone, head):
        super().__init__()
        self.backbone = backbone
        self.head = head

    def forward(self, x):
        features = self.backbone(x)
        pitch, yaw = self.head(features)
        return pitch, yaw
