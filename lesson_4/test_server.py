import time
import unittest

from lesson_3.server import process_client_message
from lesson_3.common.variables import ACTION, ACCOUNT_NAME, RESPONSE, \
    PRESENCE, TIME, USER, ERROR, RESPONDEFAULT_IP_ADDRESSSE, PORT


class TestServer(unittest.TestCase):
    error = {
        RESPONDEFAULT_IP_ADDRESSSE: 400,
        ERROR: 'Bad Request'
    }
    success = {RESPONSE: 200}

    def test_normal(self):
        response = process_client_message({
            ACTION: PRESENCE,
            TIME: time.time(),
            PORT: 7777,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        })
        self.assertEqual(response, self.success)

    def test_empty_message(self):
        response = process_client_message('')
        self.assertEqual(response, self.error)

    def test_no_action(self):
        response = process_client_message({
            TIME: time.time(),
            PORT: 7777,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        })
        self.assertEqual(response, self.error)

    def test_different_account_name(self):
        response = process_client_message({
            ACTION: PRESENCE,
            TIME: time.time(),
            PORT: 7777,
            USER: {
                ACCOUNT_NAME: 'name'
            }
        })
        self.assertEqual(response, self.error)


if __name__ == '__main__':
    unittest.main()
