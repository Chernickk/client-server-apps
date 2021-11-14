"""Программа-сервер"""
import argparse
import asyncio
import select
import socket
import sys
import json

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER, DEFAULT_IP_ADDRESS
from common.utils import async_get_message, async_send_message
from errors import IncorrectDataError
from logs.server_log_config import LOGGER
from decos import log


class SocketServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.listen_address = None
        self.listen_port = None

        self.arg_parser()

        self.server.bind((self.listen_address, self.listen_port))
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.settimeout(0.2)
        self.server.listen(MAX_CONNECTIONS)

        self.clients = {}
        self.messages = []

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

    async def handle_client(self, client):
        try:
            message = await async_get_message(client)
            if ACTION in message and message[ACTION] == PRESENCE and TIME in message and ACCOUNT_NAME in message:
                self.clients[client] = message[ACCOUNT_NAME]
                await async_send_message(client, {RESPONSE: 200})
                return

            elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and ACCOUNT_NAME in message:
                self.messages.append(message)
                LOGGER.info(f'сообщение от клиента: {message}')
                return
            else:
                await async_send_message(client, {
                    RESPONSE: 400,
                    ERROR: 'Bad Request'
                })

        except (ValueError, json.JSONDecodeError):
            client.close()
            raise IncorrectDataError

    async def run_server(self):
        loop = asyncio.get_event_loop()

        while True:
            try:
                client, client_address = await loop.sock_accept(self.server)
                self.clients[client] = 'Guest'
            except OSError:
                pass

            recv_ready = []
            send_ready = []

            if self.clients:
                recv_ready, send_ready, _ = select.select(self.clients.keys(), self.clients.keys(), [], 0)

            for client_with_message in recv_ready:
                try:
                    await self.handle_client(client_with_message)
                except:
                    LOGGER.info(f'Клиент {self.clients[client_with_message]} отключился')
                    del self.clients[client_with_message]

            if self.messages and send_ready:
                message = self.messages.pop()
                for client in send_ready:
                    try:
                        await async_send_message(client, message)
                    except:
                        LOGGER.info(f'Клиент {self.clients[client]} отключился от сервера.')
                        client.close()
                        del self.clients[client]

    def run(self):

        LOGGER.info('Сервер запущен')
        asyncio.run(self.run_server())


if __name__ == '__main__':
    socket_server = SocketServer()
    socket_server.run()
