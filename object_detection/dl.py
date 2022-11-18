"""  DL constants """
import pickle
import torchvision
from processing import get_model


def get_encoder():
    """ loading encoder """
    with open("../model/label_encoder.pkl", "rb") as file:
        label_encoder = pickle.load(file)
    return label_encoder


LABEL_ENCODER = get_encoder()
CARS_RCNN_MODEL = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
DEFECTS_MODEL = get_model("../model/mobilenetv2_80_3_cl.dict")
