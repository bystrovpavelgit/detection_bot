""" author Pavel Bystrov
    object detection functions"""
import torch
import numpy as np
from torch import nn
from torchvision import transforms
from torchvision.models import mobilenet_v2
from PIL import Image

RESCALE_SIZE = 224


def get_model(name, n_outputs=3):
    """load pretrained model"""
    simple_cnn = mobilenet_v2(pretrained=False)
    simple_cnn.classifier = nn.Sequential(
        nn.Dropout(0.2), nn.BatchNorm1d(1280), nn.Linear(1280, n_outputs, bias=True)
    )
    simple_cnn.load_state_dict(torch.load(name, map_location=torch.device("cpu")))
    return simple_cnn


def predict_one_sample(model, inputs):
    """Предсказание, для одной картинки"""
    with torch.no_grad():
        model.eval()
        logit = model(inputs).cpu()
        probs = torch.nn.functional.softmax(logit, dim=-1).numpy()
    return probs


def get_image(img_name):
    """преобразованиe изображений в тензоры PyTorch и нормализации входа"""
    # для преобразования изображений в тензоры PyTorch и нормализации входа
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    image = Image.open(img_name)
    image.load()
    out = np.array(image.resize((RESCALE_SIZE, RESCALE_SIZE)))
    out = np.array(out / 255., dtype="float32")
    out = transform(out)
    return out


def process_picture(model, label_encoder, picture_filename):
    """get prediction and returns description of this picture"""
    img = get_image(picture_filename)
    prob_pred = predict_one_sample(model, img[None, ...])
    y_pred = np.argmax(prob_pred)
    predicted_label = label_encoder.classes_[int(y_pred)]

    other = "асфальт" if predicted_label == "0" else "посторонний предмет"
    result = "дефект" if predicted_label == "1" else other
    return (result, int(y_pred))
