""" Apache License 2.0 Copyright (c) 2020 Pavel Bystrov
    business logic """
import logging
from sqlite3 import IntegrityError
from object_detection.processing import process_picture
from object_detection.cars_counting import detect_all_autos
from sqlalchemy.exc import SQLAlchemyError, PendingRollbackError
from sqlalchemy.sql import func
from webapp.stat.models import Defects, CarCounts
from webapp.config import CLASS_MAP
from webapp.db import DB
from webapp.dl import CARS_RCNN_MODEL, DEFECTS_MODEL


def add_defect(filename, y_pred, result):
    """ add defect record """
    try:
        row = Defects(image=filename, object_class=int(y_pred), object_label=result)
        DB.session.add(row)
        DB.session.commit()
    except (SQLAlchemyError, IntegrityError, PendingRollbackError) as err:
        error = str(err.__dict__['orig'])
        logging.error("Exception in add_defect:" + error)
        DB.session.rollback()


def add_car_count(filename, count):
    """ add CarCounts record """
    try:
        row = CarCounts(image=filename, car_count=count, ratio=0.0)
        DB.session.add(row)
        DB.session.commit()
    except (SQLAlchemyError, IntegrityError, PendingRollbackError) as err:
        error = str(err.__dict__['orig'])
        logging.error("Exception in add_car_count:" + error)
        DB.session.rollback()


def detect(filename):
    """ Ищем дефекты """
    print(f"Ищем дефекты на {filename}")
    result, y_pred = process_picture(DEFECTS_MODEL, CLASS_MAP, filename)
    try:
        pred = int(y_pred)
        add_defect(filename, pred, result)
    except ValueError:
        logging.error("Int conversion error for " + str(y_pred))
    return result


def get_stats():
    """ Расчет общей статистики """
    labels = ["асфальт", "дефект", "посторонний предмет"]
    asphalt_count = Defects.query.filter(Defects.object_class == 0).count()
    defects_count = Defects.query.filter(Defects.object_class == 1).count()
    other_count = Defects.query.filter(Defects.object_class == 2).count()
    entity = CarCounts.query.with_entities(func.sum(CarCounts.car_count).label("total")).first()
    total = entity.total
    query_count = CarCounts.query.count()
    messages = [f"всего найдено машин: {total} по {query_count} запросам",
                f"изображений с асфальтом: {asphalt_count}",
                f"изображений с дефектом: {defects_count}",
                f"изображений с посторонним предметом {other_count}"]
    return messages, [asphalt_count, defects_count, other_count], labels


def car_count(filename):
    """car count"""
    result = detect_all_autos(CARS_RCNN_MODEL, filename)
    if len(result) > 1:
        add_car_count(filename, result[0])
        return result[1:]
    return []
