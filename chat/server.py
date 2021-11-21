"""Программа-сервер"""
import argparse
import asyncio
import select
import socket
import sys
import json
import time
from asyncio import sleep

from uuid import uuid4

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, ERROR, DEFAULT_PORT, MESSAGE, DEFAULT_IP_ADDRESS, DESTINATION, ALL, MESSAGE_TEXT
from common.utils import async_get_message, async_send_message
from errors import IncorrectDataError
from logs.server_log_config import LOGGER
from decos import log


class Client:
    def __init__(self, sock):
        self.name = f'Guest_{str(uuid4())[:8]}'
        self.socket = sock
        self.groups = []


class SocketServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.listen_address = None
        self.listen_port = None

        self.arg_parser()

        self.server.bind((self.listen_address, self.listen_port))
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.server.settimeout(0.1)
        self.server.listen(MAX_CONNECTIONS)

        self.clients = []
        self.messages = []

        self.main_loop = asyncio.get_event_loop()

    @log
    def arg_parser(self):
        """
        Парсер аргументов командной строки
        :return:
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
        parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
        arguments = parser.parse_args(sys.argv[1:])

        self.listen_address = arguments.addr
        self.listen_port = arguments.port

        if self.listen_port < 1024 or self.listen_port > 65535:
            LOGGER.critical('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)

    async def set_username(self, client, name):
        for user in self.clients:
            if user.name == name:
                await async_send_message(client.socket, self.main_loop, {
                    RESPONSE: 400,
                    ERROR: 'Пользователь с таким именем уже есть'
                })
        else:
            client.name = name
            await async_send_message(client.socket, self.main_loop, {RESPONSE: 200})

    async def add_message_to_queue(self, message):
        if DESTINATION in message and message[DESTINATION] == ALL:
            self.messages.append(message)
            LOGGER.info(f'сообщение от {message[ACCOUNT_NAME]} для всех: {message}')
        elif DESTINATION in message:
            if message[DESTINATION] in [user.name for user in self.clients]:
                self.messages.append(message)
                LOGGER.info(f'сообщение от {message[ACCOUNT_NAME]} для {message[DESTINATION]}: {message}')
            else:
                sender_name = message[ACCOUNT_NAME]
                sender = [user for user in self.clients if user.name == sender_name]
                if sender:
                    await async_send_message(sender[0].socket, self.main_loop, {
                        ACTION: MESSAGE,
                        TIME: time.time(),
                        DESTINATION: sender_name,
                        ACCOUNT_NAME: "SERVER",
                        MESSAGE_TEXT: "Пользователь с таким именем не найден",
                    })

    async def handle_client(self, client: Client):
        try:
            message = await async_get_message(client.socket, self.main_loop)
            if ACTION in message and message[ACTION] == PRESENCE and TIME in message and ACCOUNT_NAME in message:
                name = message[ACCOUNT_NAME]
                await self.set_username(client, name)

            elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and ACCOUNT_NAME in message:
                await self.add_message_to_queue(message)

            else:
                await async_send_message(client.socket, self.main_loop, {
                    RESPONSE: 400,
                    ERROR: 'Bad Request'
                })

        except (ValueError, json.JSONDecodeError):
            client.socket.close()
            raise IncorrectDataError

    async def accept_client(self):
        while True:
            client_sock, client_address = await self.main_loop.sock_accept(self.server)
            client = Client(client_sock)
            self.clients.append(client)

    async def handle_clients(self):
        while True:
            clients_sockets = [user.socket for user in self.clients]
            recv_ready_sockets, _, _ = select.select(clients_sockets, [], [], 0)
            recv_ready_clients = [user for user in self.clients if user.socket in recv_ready_sockets]
            if recv_ready_clients:
                for client in recv_ready_clients:
                    await self.handle_client(client)
            else:
                await sleep(0)

    async def send_messages(self):
        while True:
            if self.messages:
                message = self.messages.pop()
                if message[DESTINATION] == ALL:
                    for client in self.clients:
                        if client.name != message[ACCOUNT_NAME]:
                            try:
                                await async_send_message(client.socket, self.main_loop, message)
                            except:
                                LOGGER.info(f'Клиент {client.name} отключился от сервера.')
                                client.socket.close()
                                self.clients.remove(client)
                else:
                    recipient_name = message[DESTINATION]
                    recipient = [user for user in self.clients if user.name == recipient_name]
                    if recipient:
                        await async_send_message(recipient[0].socket, self.main_loop, message)
                    else:
                        sender_name = message[ACCOUNT_NAME]
                        sender = [user for user in self.clients if user.name == sender_name]
                        if sender:
                            await async_send_message(sender[0].socket, self.main_loop, {
                                ACTION: MESSAGE,
                                TIME: time.time(),
                                ACCOUNT_NAME: "SERVER",
                                MESSAGE_TEXT: f"Пользователь {recipient_name} отключился",
                            })
            else:
                await sleep(0)

    def run(self):
        self.main_loop.create_task(self.accept_client())
        self.main_loop.create_task(self.handle_clients())
        self.main_loop.create_task(self.send_messages())
        LOGGER.info('Сервер запущен')
        self.main_loop.run_forever()


if __name__ == '__main__':
    socket_server = SocketServer()
    socket_server.run()
