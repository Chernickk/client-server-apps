"""Программа-клиент"""
import asyncio
import sys
import json
import socket
import time
import argparse
import threading

from common.variables import ACTION, PRESENCE, TIME, ACCOUNT_NAME, MESSAGE, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE_TEXT, DESTINATION, ALL
from common.utils import async_get_message, async_send_message
from logs.client_log_config import LOGGER
from decos import log


class SocketClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = None
        self.port = None
        self.mode = 'default'
        self.destination = ALL
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
        parser.add_argument('name', default='Guest', nargs='?')

        arguments = parser.parse_args(sys.argv[1:])

        self.address = arguments.addr
        self.port = arguments.port
        self.name = arguments.name

        if self.port < 1024 or self.port > 65535:
            LOGGER.critical('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
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
    def create_message(self):
        """
        Функция генерирует сообщение от клиента
        """
        user_input = input()

        if user_input == '!!!':
            self.sock.close()
            LOGGER.info('Закрытие сокета')
            sys.exit(0)

        if user_input == '!':
            self.p2p_dialog()
            return

        message = {
            ACTION: MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: self.name,
            DESTINATION: self.destination,
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
            if message[DESTINATION] == self.name:
                print(f'Вам: {message[ACCOUNT_NAME]}, '
                      f'содержание: {message.get(MESSAGE_TEXT)}')
            else:
                print(f'Всем: {message[ACCOUNT_NAME]}, '
                      f'содержание: {message.get(MESSAGE_TEXT)}')
        elif message == {RESPONSE: 200}:
            print('Успешное подключение к серверу')
        else:
            LOGGER.error(f'Получено некорректное сообщение {message}')

    def p2p_dialog(self):
        user_input = input("Введите имя получателя или оставьте поле пустым для общего чата: ")
        if user_input == '':
            self.destination = ALL
        else:
            self.destination = user_input
            self.mode = 'p2p'

        if self.destination == ALL:
            text = 'Введите сообщение ("!!!" для выхода, "!" для отправки личного сообщения) \n'
        else:
            text = f'Личное сообщение для {self.destination}("!!!" для выхода, "!" для изменения получателя) \n'
        print(text)

    def get_messages_wrapper(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.get_messages(loop))

    def send_messages_wrapper(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_messages(loop))

    async def get_messages(self, loop):
        while True:
            answer = await async_get_message(self.sock, loop)
            if self.mode == 'p2p' and answer[DESTINATION] == ALL:
                pass
            self.handle_server_message(answer)

    async def send_messages(self, loop):
        initial_message = self.create_presence()
        if self.destination == ALL:
            text = 'Введите сообщение ("!!!" для выхода, "!" для отправки личного сообщения) \n'
        else:
            text = f'Личное сообщение для {self.destination}("!!!" для выхода, "!" для изменения получателя) \n'
        print(text)

        await async_send_message(self.sock, loop, initial_message)

        while True:
            message = self.create_message()
            if message:
                await async_send_message(self.sock, loop, message)

    @log
    def main(self):
        try:
            send_thread = threading.Thread(target=self.send_messages_wrapper)
            listen_thread = threading.Thread(target=self.get_messages_wrapper)
            listen_thread.start()
            send_thread.start()

        except (ValueError, json.JSONDecodeError):
            LOGGER.error('Не удалось декодировать сообщение сервера.')
        except BrokenPipeError:
            LOGGER.error('Сервер разорвал соединение')
            sys.exit(1)


if __name__ == '__main__':
    client_sock = SocketClient()
    client_sock.main()
