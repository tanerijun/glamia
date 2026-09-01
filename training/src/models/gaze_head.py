from torch import nn


class GazeHead(nn.Module):
    def __init__(self, in_channels, num_bins, dropout_rate=0.3):
        super().__init__()
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.flatten = nn.Flatten()

        self.dropout = nn.Dropout(dropout_rate)

        # Separate linear layers for pitch and yaw classification
        self.fc_pitch = nn.Linear(in_channels, num_bins)
        self.fc_yaw = nn.Linear(in_channels, num_bins)

    def forward(self, x):
        x = self.pool(x)  # [B, C, 1, 1]
        x = self.flatten(x)  # [B, C]
        x = self.dropout(x)

        # Get binned predictions
        pitch_logits = self.fc_pitch(x)  # [B, num_bins]
        yaw_logits = self.fc_yaw(x)  # [B, num_bins]

        return pitch_logits, yaw_logits
