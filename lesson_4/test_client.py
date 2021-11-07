import time
import unittest

from lesson_3.client import create_request, analyze_response
from lesson_3.common.variables import ACTION, ACCOUNT_NAME, RESPONSE, \
    PRESENCE, TIME, USER, ERROR, PORT


class TestClient(unittest.TestCase):
    def test_normal_request(self):
        time_ = time.time()
        port = 7777
        account_name = 'Guest'

        normal_request = {
            ACTION: PRESENCE,
            TIME: time_,
            PORT: port,
            USER: {
                ACCOUNT_NAME: account_name
            }
        }

        request = create_request(port)
        request[TIME] = time_

        self.assertEqual(request, normal_request)

    def test_analyze_200(self):
        response = {RESPONSE: 200}
        result = analyze_response(response)
        self.assertEqual(result, '200 : OK')

    def test_analyze_400(self):
        response = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }
        result = analyze_response(response)
        self.assertIn('400', result)

    def test_analyze_incorrect(self):
        response = ''
        self.assertRaises(ValueError, analyze_response, response)


if __name__ == '__main__':
    unittest.main()
