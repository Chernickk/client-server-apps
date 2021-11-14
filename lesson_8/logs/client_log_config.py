import os
import logging
import sys

FORMATTER = logging.Formatter('%(asctime)s %(levelname)-10s %(filename)-20s %(message)s')

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.exists(PATH):
    os.mkdir(PATH)
PATH = os.path.join(PATH, 'client.log')

STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setLevel(logging.INFO)
FILE_HANDLER = logging.FileHandler(
    filename=PATH,
    encoding='utf-8'
)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.ERROR)

LOGGER = logging.getLogger('CLIENT')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.INFO)


if __name__ == '__main__':
    LOGGER.debug('debug')
    LOGGER.info('info')
    LOGGER.warning('warning')
    LOGGER.error('error')
    LOGGER.critical('critical')