""" 2020
    Created by Dariya
    utility functions
"""
import glob
import os
from re import search
from telegram import ReplyKeyboardMarkup


def give_menu(update, context):
    """ give menu """
    update.message.reply_text("Hello, user", reply_markup=main_keyboard())


def send_picture(update, context, picture_filename):
    """ send picture """
    chat_id = update.effective_chat.id
    with open(picture_filename, "rb") as jpg_file:
        context.bot.send_photo(
            chat_id=chat_id,
            photo=jpg_file,
            reply_markup=main_keyboard(),
        )


def get_picture_token(chat_id):
    """ get picture token """
    try:
        jpg_images = glob.glob(f"downloads/{chat_id}-*.jpg")
        if len(jpg_images) < 1:
            return 1
        max_token = 0
        for image in jpg_images:
            token = int(search(r"\-(.*?)\.", image).group(1))
            if token > max_token:
                max_token = token
        return max_token + 1
    except ValueError:
        return 1


def get_picture(update, context):
    """ get picture """
    update.message.reply_text("Обрабатываю фото")
    os.makedirs("downloads", exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[0].file_id)
    if photo_file is not None and photo_file.file_path.split(".")[-1] == "jpg":
        token = get_picture_token(update.message.chat.id)
        filename = os.path.join("downloads", f"{update.message.chat.id}-{token}.jpg")
        photo_file.download(filename)
        context.user_data["last_image"] = filename
        update.message.reply_text("Файл сохранен", reply_markup=main_keyboard())
    else:
        update.message.reply_text("Загрузите jpg файл", reply_markup=main_keyboard())


def main_keyboard():
    """ main keyboard """
    return ReplyKeyboardMarkup([["Count Cars"], ["Detect Defects"]])
