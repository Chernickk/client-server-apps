import os
import logging
import sys
from logging import handlers

FORMATTER = logging.Formatter('%(asctime)s %(levelname)-10s %(filename)-20s %(message)s')

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(PATH):
    os.mkdir(PATH)
PATH = os.path.join(PATH, 'server.log')

STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setLevel(logging.INFO)
FILE_HANDLER = handlers.TimedRotatingFileHandler(
    filename=PATH,
    when='d',
    interval=1,
    encoding='utf-8'
)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.ERROR)

LOGGER = logging.getLogger('SERVER')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.INFO)


if __name__ == '__main__':
    LOGGER.debug('debug')
    LOGGER.info('info')
    LOGGER.warning('warning')
    LOGGER.error('error')
    LOGGER.critical('critical')