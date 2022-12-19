""" Apache License 2.0 Copyright (c) 2020 Pavel Bystrov
    DL constants"""
import torchvision
from object_detection.processing import get_model, load_encoder
from webapp.config import CLSF_MODEL, ENCODER_FILE


LABEL_ENCODER = load_encoder(ENCODER_FILE)
CARS_RCNN_MODEL = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
DEFECTS_MODEL = get_model(CLSF_MODEL)
