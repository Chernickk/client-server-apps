"""Программа-сервер"""
import asyncio
import socket
import sys
import json

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESSSE
from common.utils import async_get_message, async_send_message
from lesson_5.errors import IncorrectDataError
from lesson_5.logs.server_log_config import LOGGER


def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    '''
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESSSE: 400,
        ERROR: 'Bad Request'
    }


async def handle_client(client):
    try:
        message_from_client = await async_get_message(client)
        LOGGER.info(f'сообщение от клиента: {message_from_client}')
        response = process_client_message(message_from_client)
        await async_send_message(client, response)
        client.close()
    except (ValueError, json.JSONDecodeError):
        client.close()
        raise IncorrectDataError


async def run_server(listen_address, listen_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((listen_address, listen_port))
    server.listen(MAX_CONNECTIONS)
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client, client_address = await loop.sock_accept(server)
        loop.create_task(handle_client(client))


def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    :return:
    '''

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        LOGGER.error('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        LOGGER.error('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        LOGGER.error('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    LOGGER.info('Сервер запущен')
    asyncio.run(run_server(listen_address, listen_port))


if __name__ == '__main__':
    main()
