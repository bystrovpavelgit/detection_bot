""" bot handlers """
import os
from pymongo import MongoClient
from utils import main_keyboard
import settings
from db import get_or_create_user, save_detected_defects, save_car_counts
from db import defects_stat, cars_stat
from processing import process_picture
from cars_counting import detect_all_autos
from dl import CARS_RCNN_MODEL, DEFECTS_MODEL, LABEL_ENCODER

CLIENT = MongoClient(settings.MONGO_LINK)
DB = CLIENT["testdb"]


def detect_defects(update, context):
    """ detect defects """
    get_or_create_user(DB, update.effective_user, update.message.chat.id)
    os.makedirs("downloads", exist_ok=True)
    if "last_image" not in context.user_data:
        update.message.reply_text("Загрyзите изображение")
        return
    image = context.user_data["last_image"]
    print("Ищем дефекты")
    result, y_pred = process_picture(DEFECTS_MODEL, LABEL_ENCODER, image)
    user_id = update.effective_user.id
    save_detected_defects(DB, user_id, y_pred, result, img_name=image)
    update.message.reply_text("Это " + result, reply_markup=main_keyboard())



def get_stats(update, context):
    """ get stats """
    results = defects_stat(DB)
    total = cars_stat(DB)
    text = f"""
    всего найдено машин: {total}
    изображений с асфальтом: {results[0]}
    изображений с дефектом: {results[1]}
    изображений с посторонним предметом: {results[2]}"""
    update.message.reply_text(text, reply_markup=main_keyboard())


def count_cars(update, context):
    """ count cars """
    get_or_create_user(DB, update.effective_user, update.message.chat.id)
    os.makedirs("downloads", exist_ok=True)
    if "last_image" not in context.user_data:
        update.message.reply_text("Загрyзите изображение")
        return
    update.message.reply_text("Пожалуйста подождите - идет обработка")
    print("Ищем машины на " + context.user_data["last_image"])
    car_count, msg, out_file = detect_all_autos(CARS_RCNN_MODEL, context.user_data["last_image"])
    user_id = update.effective_user.id
    save_car_counts(DB, user_id, car_count, 0.0, img_name=context.user_data["last_image"])
    chat_id = update.effective_chat.id
    with open(out_file, "rb") as img:
        context.bot.send_photo(chat_id=chat_id, photo=img)
    update.message.reply_text(msg, reply_markup=main_keyboard())


def start(update, context):
    """ start function """
    update.message.reply_text("Hello", reply_markup=main_keyboard())
