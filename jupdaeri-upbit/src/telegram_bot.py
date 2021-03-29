"""
telegram 실시간 대화 예제
"""
import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


telegram_access_token = os.environ['TELEGRAM_BOT_ACCESS_TOKEN']
telegram_server_url = os.environ['TELEGRAM_SERVER_URL']
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

updater = Updater(token=telegram_access_token)
dispatcher = updater.dispatcher


def start(update, context):
    """
    시작
    """
    update.message.reply_text("I'm a bot, please talk to me!")


def echo(update, context):
    """
    따라말하기 (예제)
    """
    update.message.reply_text(update.message.text)


def caps(update, context):
    """
    대문자변환 (예제)
    """
    text_caps = ' '.join(context.args).upper()
    text_caps and update.message.reply_text(text_caps)


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
dispatcher.add_handler(CommandHandler('caps', caps))


updater.start_polling()
updater.idle()
