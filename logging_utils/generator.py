import logging
import logging.handlers
import os

from logging_utils.telegramhandler import TelegramLoggerHandler


def generate_logger(name,path=''):

    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logging.Formatter("[%(name)s] %(asctime)s - %(levelname)s:\n%(message)s\n"))
    streamHandler.setLevel(logging.DEBUG)


    logger.addHandler(streamHandler)
    logger.addHandler(TelegramLoggerHandler())
    logger.propagate = False

    if len(logger.handlers)>3:
        raise Exception('handelrs logging exception')

    print('{name} logger setted up'.format(name=name))

    return logger

def generate_writer_logger(name='root'):


    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    trfHandler = logging.handlers.TimedRotatingFileHandler(f'{os.path.dirname(os.path.abspath(__file__))}/../logs/debug_{name}.log', when='D', interval=60,backupCount=5)
    trfHandler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
    trfHandler.setLevel(logging.DEBUG)

    logger.addHandler(trfHandler)
    print('{name} logger setted up'.format(name=name))

    return logger
