"""Программа-клиент"""
import asyncio
import sys
import json
import socket
import time
import argparse

from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, MESSAGE, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, PORT, MESSAGE_TEXT
from common.utils import async_get_message, async_send_message
from logs.client_log_config import LOGGER
from decos import log


class SocketClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = None
        self.port = None
        self.mode = None
        self.name = 'Guest'

        self.arg_parser()

        self.sock.connect((self.address, self.port))

    @log
    def arg_parser(self):
        """
        Парсер аргументов командной строки
        :return:
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
        parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
        parser.add_argument('mode', default='listen', nargs='?')
        parser.add_argument('name', default='Guest', nargs='?')

        arguments = parser.parse_args(sys.argv[1:])

        self.address = arguments.addr
        self.port = arguments.port
        self.mode = arguments.mode
        self.name = arguments.name

        if self.port < 1024 or self.port > 65535:
            LOGGER.critical('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)

        if self.mode not in ('listen', 'send'):
            LOGGER.critical('Некорректный режим работы')
            sys.exit(1)

    @log
    def create_presence(self):
        """
        Функция генерирует запрос о присутствии клиента
        """
        presence = {
            ACTION: PRESENCE,
            TIME: time.time(),
            ACCOUNT_NAME: self.name,
        }
        return presence

    @log
    def create_message(self,):
        """
        Функция генерирует сообщение от клиента
        """
        user_input = input('Введите сообщение (или "!!!" для выхода)')

        if user_input == '!!!':
            self.sock.close()
            LOGGER.info('Закрытие сокета')
            sys.exit(0)

        message = {
            ACTION: MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: self.name,
            MESSAGE_TEXT: user_input,
        }

        return message

    @log
    def handle_presence_response(self, message):
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

    @log
    def handle_server_message(self, message):
        """
        Функция разбирает ответ сервера
        """
        if ACTION in message and ACCOUNT_NAME in message and message[ACTION] == MESSAGE:
            print(f'Сообщение от пользователя {message[ACCOUNT_NAME]}, содержание: {message.get(MESSAGE_TEXT)}')
        elif message == {RESPONSE: 200}:
            print('Успешное подключение к серверу')
        else:
            LOGGER.error(f'Получено некорректное сообщение {message}')

    @log
    async def main(self):
        initial_message = self.create_presence()
        await async_send_message(self.sock, initial_message)

        while True:
            try:
                if self.mode == 'send':
                    message = self.create_message()

                    await async_send_message(self.sock, message)

                if self.mode == 'listen':
                    answer = await async_get_message(self.sock)
                    self.handle_server_message(answer)

            except (ValueError, json.JSONDecodeError):
                LOGGER.error('Не удалось декодировать сообщение сервера.')
            except BrokenPipeError:
                LOGGER.error('Сервер разорвал соединение')
                sys.exit(1)

    def run(self):
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.main())


if __name__ == '__main__':
    client_sock = SocketClient()
    client_sock.run()
