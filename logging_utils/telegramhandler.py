import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import telebot

BOT_TOKEN=os.environ.get('BOT_TOKEN')


class TelegramLoggerHandler(logging.StreamHandler):

    def __init__(self):
        super(TelegramLoggerHandler, self).__init__()
        super(TelegramLoggerHandler, self).setFormatter(logging.Formatter("[%(name)s] - %(levelname)s:\n%(message)s"))
        super(TelegramLoggerHandler, self).setLevel(logging.INFO)

        token = BOT_TOKEN
        self.bot = telebot.TeleBot(token,threaded=False)
        self.CHANNEL_NAME = '-1001976773271'
    def snd(self,msg):

        def send_message(bot, channel='-1001976773271', msg='empty_message'):
            try:
                result =self.bot.send_message(channel, msg, timeout=10)

            except Exception as e:
                print("\nTelegramLoggerHandler try to send :\n", msg, "\n")
                print("but Telegram is not available now:\n", e, "\n")
            sys.exit()

        Thread(target=send_message, args=(bot, self.CHANNEL_NAME, msg)).start()


    def emit(self, record):
        msg = ''
        msg += self.format(record)
        msg += "\n(c) DeltaHedger"
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                pass
                future = executor.submit(self.snd, msg)

        except Exception as e:
            print("\nTelegramLoggerHandler try to send :\n", msg, "\n")
            print("but Telegram is not available now:\n", e, "\n")


