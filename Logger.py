import logging
import os

def initalize_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')

    if not os.path.exists('logs'):
        os.mkdir('logs')

    def add_logging_handler(handler, level):
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # console handler
    add_logging_handler(logging.StreamHandler(), logging.DEBUG)

    # file handler (errors)
    add_logging_handler(logging.FileHandler("logs/ERROR.log", "a"), logging.WARNING)