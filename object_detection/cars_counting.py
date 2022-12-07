""" 
    cars counting functions
"""
import cv2
import numpy as np
from cv2 import UMat, rectangle
from torch import from_numpy
from PIL import Image


def detect_auto(model, image):
    """detect auto"""
    # переводим модель в тестовый режим
    model = model.eval()
    # загружаем картинку со стандартным преобразованием цветов
    img_numpy = image[:,:,::-1]
    # преобразуем картинку в torch тензор
    img = from_numpy(img_numpy.astype("float32")).permute(2,0,1)
    # приводим масштаб цветов к (0. , 1.)
    img = img / 255.
    # нейросеть предсказывает, что находится на картинке и обводит распознанные обьекты рамкой
    predictions = model(img[None,...])
    return predictions


def intersection_over_union(box_a, box_b):
    """ intersection over union"""
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])

    inter_area = max(0, x_b - x_a + 1.) * max(0, y_b - y_a + 1.)
    box_a_area = (box_a[2] - box_a[0] + 1.) * (box_a[3] - box_a[1] + 1.)
    box_b_area = (box_b[2] - box_b[0] + 1.) * (box_b[3] - box_b[1] + 1.)
    iou = float(inter_area) / float(box_a_area + box_b_area - inter_area)
    return iou


def intersection_over_b_area(box_a, box_b):
    """ intersection over area 2"""
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])

    inter_area = max(0, x_b - x_a + 1.) * max(0, y_b - y_a + 1.)
    box_b_area = (box_b[2] - box_b[0] + 1.) * (box_b[3] - box_b[1] + 1.)
    return float(inter_area)/float(box_b_area)


def plot_non_max_suppression(numpy_img, preds, label, color):
    """ non max suppression + duplicates suppression"""
    def suppress(box, boxes, indexes):
        ious_50 = [i for i in indexes if intersection_over_union(box, boxes[i]) >= 0.50]
        duplicates = [i for i in indexes if intersection_over_b_area(box, boxes[i]) >= 0.91]
        for i in set(duplicates).union(set(ious_50)):
            indexes.remove(i)

    labels = preds["labels"].detach().numpy()
    scores = preds["scores"].detach().numpy()
    boxes = preds["boxes"].detach().numpy()[(labels == label) & (scores >= 0.55)]
    indexes = list(np.arange(len(boxes)))
    result_boxes = []
    # suppression algorithm
    while len(indexes) > 0:
        box = boxes[indexes[0]]
        indexes.remove(indexes[0])
        suppress(box, boxes, indexes)
        result_boxes.append(box)
    # adding rectangles
    nimg = UMat(numpy_img)
    for box in result_boxes:
        nimg = rectangle(nimg,
            (box[0], box[1]),
            (box[2], box[3]),
            color = color,
            thickness = 2)
    return (result_boxes, nimg.get())


def get_all_boxes(image, predictions):
    """ all boxes"""
    colors = [(255, 0, 0),
         (0, 255, 0),
         (0, 0, 255)]
    all_boxes = []
    counts = []
    color = 0
    for label in [3, 6, 8]:
        img_with_boxes = plot_non_max_suppression(image, predictions[0], label, colors[color])
        color += 1
        image = img_with_boxes[1]
        all_boxes.extend(img_with_boxes[0])
        counts.append(len(img_with_boxes[0]))
    return (all_boxes, image, counts)


def detect_all_autos(model, fname):
    """detect all autos"""
    img_numpy = cv2.imread(fname)[:,:,::-1]
    print("in count_cars: stage 1")
    predictions = detect_auto(model, img_numpy)
    result = get_all_boxes(img_numpy, predictions)
    counts = result[2]
    total_count = len(result[0])
    msg = f"Общее количество машин на фото {total_count} (Всего автомобилей {counts[0]}, \
        всего автобусов {counts[1]}, всего грузовиков {counts[2]})"
    img_array = result[1].astype("uint8")
    image = Image.fromarray(img_array, "RGB")
    out_file = fname.split(".")[0] + "_file.jpg"
    image.save(out_file)
    image.close()
    return (total_count, msg, out_file)
