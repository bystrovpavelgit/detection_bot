""" 
    DL constants
"""
from torch import nn
import torchvision
from torchvision.models import mobilenet_v2
from webapp.config import CLSF_MODEL, ENCODER_FILE


def get_model(name, n_outputs=3):
    """load pretrained model"""
    simple_cnn = mobilenet_v2(pretrained=False)
    simple_cnn.classifier = nn.Sequential(
        nn.Dropout(0.2), nn.BatchNorm1d(1280), nn.Linear(1280, n_outputs, bias=True)
    )
    simple_cnn.load_state_dict(torch.load(name, map_location=torch.device("cpu")))
    return simple_cnn


LABEL_ENCODER = {0: "0", 1: "1", 2: "2"}
CARS_RCNN_MODEL = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
DEFECTS_MODEL = get_model("../model/mobilenetv2_80_3_cl.dict")
