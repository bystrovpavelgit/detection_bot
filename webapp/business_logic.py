""" Apache License 2.0 Copyright (c) 2020 Pavel Bystrov
    business logic """
from object_detection.processing import process_picture
from object_detection.cars_counting import detect_all_autos
from sqlalchemy.sql import func
from webapp.user.models import Defects, CarCounts
from webapp.db import DB
from webapp.dl import CARS_RCNN_MODEL, DEFECTS_MODEL, LABEL_ENCODER


def detect(filename):
    """ Ищем дефекты """
    print("Ищем дефекты на " + filename)
    result, y_pred = process_picture(DEFECTS_MODEL, LABEL_ENCODER, filename)
    row = Defects(image=filename, object_class=int(y_pred), object_label=result)
    DB.session.add(row)
    DB.session.commit()
    return result


def get_stats():
    """ Расчет общей статистики """
    labels = ["асфальт", "дефект", "посторонний предмет"]
    asphalt_count = Defects.query.filter(Defects.object_class == 0).count()
    defects_count = Defects.query.filter(Defects.object_class == 1).count()
    other_count = Defects.query.filter(Defects.object_class == 2).count()
    tentity = CarCounts.query.with_entities(func.sum(CarCounts.car_count).label("total")).first()
    total = tentity.total
    query_count = CarCounts.query.count()
    messages = [f"всего найдено машин: {total} по {query_count} запросам",
                f"изображений с асфальтом: {asphalt_count}",
                f"изображений с дефектом: {defects_count}",
                f"изображений с посторонним предметом {other_count}"]
    return messages, [asphalt_count, defects_count, other_count], labels


def car_count(filename):
    """car count"""
    result = detect_all_autos(CARS_RCNN_MODEL, filename)
    row = CarCounts(image=filename, car_count=result[0], ratio=0.0)
    DB.session.add(row)
    DB.session.commit()
    return result[1:]
