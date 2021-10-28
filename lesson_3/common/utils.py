"""Утилиты"""
import asyncio
import json
from common.variables import MAX_PACKAGE_LENGTH, ENCODING


async def async_get_message(client):
    '''
    Утилита приёма и декодирования сообщения
    принимает байты выдаёт словарь, если приняточто-то другое отдаёт ошибку значения
    :param client:
    :return:
    '''
    loop = asyncio.get_event_loop()

    encoded_response = await loop.sock_recv(client, MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


async def async_send_message(sock, message):
    """
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его
    :param sock:
    :param message:
    :return:
    """
    loop = asyncio.get_event_loop()

    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    await loop.sock_sendall(sock, encoded_message)
