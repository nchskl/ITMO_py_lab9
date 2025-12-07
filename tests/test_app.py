import unittest
import threading
import time
import http.client

from http.server import HTTPServer
from myapp.myapp import SimpleHTTPRequestHandler, get_currencies, currencies, users


HOST = "localhost"
PORT = 8081  # тестовый порт чтобы не мешать реальному


def start_test_server():
    server = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.2)  # ждём запуск
    return server


class MyAppHttpTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = start_test_server()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def http_get(self, path):
        conn = http.client.HTTPConnection(HOST, PORT)
        conn.request("GET", path)
        return conn.getresponse()

    def test_index_page(self):
        resp = self.http_get("/")
        data = resp.read().decode("utf-8")
        self.assertIn("Пользователи", data)

    def test_currencies_route(self):
        resp = self.http_get("/currencies")
        text = resp.read().decode("utf-8")
        self.assertIn("EUR", text)

    def test_users_route(self):
        resp = self.http_get("/users")
        text = resp.read().decode("utf-8")

        # проверяем, что хотя бы один пользователь есть
        for u in users:
            self.assertIn(u["username"], text)


if __name__ == "__main__":
    unittest.main()
