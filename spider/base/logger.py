#coding:utf-8

"""
Author:hanlu
"""

import logging
from logging.handlers import TimedRotatingFileHandler,RotatingFileHandler

def PrintLog(filename):
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.DEBUG)
    handler = RotatingFileHandler(filename=filename,maxBytes=10*1024*1024,backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s -%(filename)s-%(lineno)s -  %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
