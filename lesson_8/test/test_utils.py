import asyncio
import json
import time
import socket
import unittest

from lesson_6.common.utils import async_get_message, async_send_message
from lesson_6.common.variables import ACTION, ACCOUNT_NAME, RESPONSE, \
    PRESENCE, TIME, USER, ERROR, RESPONDEFAULT_IP_ADDRESSSE, PORT, ENCODING


class TestSocket:
    '''
    Тестовый класс для тестирования отправки и получения,
    при создании требует словарь, который будет прогонятся
    через тестовую функцию
    '''
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        """
        Тестовая функция отправки, корретно  кодирует сообщение,
        так-же сохраняет то, что должно быть отправлено в сокет.
        message_to_send - то, что отправляем в сокет
        :param message_to_send:
        :return:
        """
        json_test_message = json.dumps(self.test_dict)
        # кодирует сообщение
        self.encoded_message = json_test_message.encode(ENCODING)
        # сохраняем что должно было отправлено в сокет
        self.received_message = message_to_send

    def recv(self, max_len):
        """
        Получаем данные из сокета
        :param max_len:
        :return:
        """
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    '''
    Тестовый класс, собственно выполняющий тестирование.
    '''
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_get_message(self):
        """
        Тест функции приёма сообщения
        :return:
        """
        loop = asyncio.get_event_loop()

        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        # тест корректной расшифровки корректного словаря
        self.assertEqual(loop.run_until_complete(async_get_message(test_sock_ok)), self.test_dict_recv_ok)
        # тест корректной расшифровки ошибочного словаря
        self.assertEqual(loop.run_until_complete(async_get_message(test_sock_err)), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
