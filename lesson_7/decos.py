import sys
import inspect
from functools import wraps

from logs.client_log_config import LOGGER as CLIENT_LOGGER
from logs.server_log_config import LOGGER as SERVER_LOGGER

if 'client' in sys.argv[0]:
    LOGGER = CLIENT_LOGGER
else:
    LOGGER = SERVER_LOGGER


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        LOGGER.debug(f'Обращение к функции "{func.__name__}"\nАргументы: {args}\nИменованные аргументы: {kwargs}'
                     f'\nПроизведено из функции: {inspect.stack()[1].function}')
        return result
    return wrapper
