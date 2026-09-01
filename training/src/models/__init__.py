import torch.nn as nn

from .backbone_mobileone import MobileOneBackbone
from .gaze_head import GazeHead
from .gaze_model import GazeModel


def build_model(config, **backbone_kwargs):
    """
    Builds the complete gaze model (MobileOne backbone + binned pitch/yaw head)
    from the config. Any additional keyword arguments are passed directly to the
    backbone constructor.
    """
    backbone_name = config["backbone"]

    if not backbone_name.startswith("mobileone"):
        raise ValueError(
            f"Unknown backbone: {backbone_name}. "
            "This release only supports the MobileOne family (e.g. 'mobileone_s1')."
        )

    backbone = MobileOneBackbone(
        arch=backbone_name,
        pretrained=config.get("pretrained", True),
        **backbone_kwargs,
    )

    head = GazeHead(in_channels=backbone.out_channels, num_bins=config["num_bins"])

    model = GazeModel(backbone, head)

    return model
