""" chat bot app """
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import API_KEY
from handlers import detect_defects, count_cars, get_stats, start
from utils import get_picture


def main():
    """ main function """
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    bot = Updater(API_KEY, use_context=True)

    dispatcher = bot.dispatcher

    dispatcher.add_handler(CommandHandler("statistics", get_stats))

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(MessageHandler(Filters.photo, get_picture))

    dispatcher.add_handler(MessageHandler(Filters.regex("^(Detect Defects)$"), detect_defects))
    dispatcher.add_handler(MessageHandler(Filters.regex("^(Count Cars)$"), count_cars))

    # Командуем боту начать ходить в Telegram за сообщениями
    print("bot started")
    bot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    bot.idle()


if __name__ == "__main__":
    main()
