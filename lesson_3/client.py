"""Программа-клиент"""
import asyncio
import sys
import json
import socket
import time

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, PORT
from common.utils import async_get_message, async_send_message
from lesson_5.logs.client_log_config import LOGGER


def create_request(port, account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    """
    request = {
        ACTION: PRESENCE,
        TIME: time.time(),
        PORT: port,
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return request


def analyze_response(message):
    """
    Функция разбирает ответ сервера
    :param message:
    :return:
    """
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


async def main():
    """Загружаем параметры командной строки"""
    try:
        server_port = int(sys.argv[1])
        server_address = sys.argv[2]
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        LOGGER.error('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_request(server_port)
    await async_send_message(transport, message_to_server)
    try:
        answer = await async_get_message(transport)
        answer = analyze_response(answer)
        LOGGER.info(f'сообщение от сервера: {answer}')
    except (ValueError, json.JSONDecodeError):
        LOGGER.error('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
