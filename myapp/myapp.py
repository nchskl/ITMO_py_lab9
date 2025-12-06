from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from datetime import datetime

from models import *

from utils.currencies_api import get_currencies

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

tpl_index = env.get_template("index.html")
tpl_currencies = env.get_template("currencies.html")
tpl_users = env.get_template("users.html")
tpl_user_detail = env.get_template("user_detail.html")
tpl_author = env.get_template("author.html")

main_author = Author('Vyacheslav Fedorov', 'P3120')
app = App('CurrenciesListApp', '1.0.0', main_author.name)

users = [User(504485, 'Fedorov V'),
         User(505301, 'Shanin I'),
         User(504634, 'Halilov Ch'),
         User(504695, 'Karelina M')]

currencies = []
user_currencies = []


def load_currencies():
    global currencies
    try:
        currencies_data = get_currencies()

        currencies = []


        for data in currencies_data:
            print(data)
            try:
                currency = Currency(
                    cid=data['id'],
                    num_code=data['num_code'],
                    char_code=data['char_code'],
                    name=data['name'],
                    value=data['value'],
                    nominal=data['nominal'],
                )
                currencies.append(currency)
            except Exception as e:
                print(f'Ошибка создания валюты {data.get("char_code", "unknown")}: {e}')
                continue

            print(f'Загружено {len(currencies)} валют из API.')

            currencies.sort(key=lambda c: c.char_code)

    except Exception as e:
        print(f'Ошибка загрузки валют: {e}')
        return False
    return True

def get_user_by_id(user_id):
    for user in users:
        if int(user.uid) == int(user_id):
            return user
    return None

def get_currency_by_id(currency_id):
    for currency in currencies:
        if currency.cid == currency_id:
            return currency
    return None

def get_currency_by_char_code(char_code):
    for currency in currencies:
        if currency.char_code == char_code:
            return currency
    return None

def get_user_subscriptions(user_id):
    return [uc for uc in user_currencies if uc.user_id == user_id]

def get_subscribed_currencies(user_id):
    subscriptions = get_user_subscriptions(user_id)
    subscribed_currencies = []
    for sub in subscriptions:
        currency = get_currency_by_id(sub.currency_id)
        if currency:
            subscribed_currencies.append(currency)
    return subscribed_currencies

def get_available_currencies(user_id):
    subscribed_ids = [sub.currency_id for sub in get_user_subscriptions(user_id)]
    return [currency for currency in currencies if currency.cid not in subscribed_ids]

def subscribe_user_to_currency(user_id, currency_id):
    for uc in user_currencies:
        if uc.user_id == user_id and uc.currency_id == currency_id:
            return False
    new_id = max([uc.id for uc in user_currencies], default=0) + 1
    user_currencies.append(UserCurrency(new_id, user_id, currency_id))
    return True

def unsubscribe_user_from_currency(user_id, currency_id):
    global user_currencies
    initial_length = len(user_currencies)
    user_currencies = [
        uc for uc in user_currencies
        if not (uc.user_id == user_id and uc.currency_id == currency_id)
    ]
    return len(user_currencies) < initial_length

load_currencies()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _render_error(self, code, message):
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{code} - {message}</title>
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>{code} - {message}</h1>
            <p><a href="/users">Вернуться к списку пользователей</a></p>
        </body>
        </html>
        """
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        navigation = [
            {'caption': 'Главная', 'href': '/'},
            {'caption': 'Валюты', 'href': '/currencies'},
            {'caption': 'Пользователи', 'href': '/users'},
            {'caption': 'Об авторе', 'href': '/author'}
        ]

        try:
            if path == '/':
                html = tpl_index.render(myapp=app.name,
                                        version=app.version,
                                        author=main_author.name,
                                        group=main_author.group,
                                        navigation=navigation,
                                        total_currencies=len(currencies),
                                        total_users=len(users),
                                        api_type='JSON API ЦБ РФ')

            elif path == '/currencies':
                update_requested = "update" in query_params

                success = load_currencies()
                show_message = success if update_requested else None

                last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                html = tpl_currencies.render(
                    currencies=currencies,
                    navigation=navigation,
                    last_update=last_update,
                    total=len(currencies),
                    load_success=success
                )

            elif path == '/users':
                html = tpl_users.render(
                    users=users,
                    navigation=navigation,
                    total=len(users)
                )

            elif path == '/user':
                user_id = int(query_params.get('id', [0])[0])
                user = get_user_by_id(user_id)

                if user:
                    subscribed = get_subscribed_currencies(user_id)
                    available = get_available_currencies(user_id)

                    html = tpl_user_detail.render(
                        user=user,
                        subscribed_currencies=subscribed,
                        available_currencies=available,
                        navigation=navigation,
                        total_subscribed=len(subscribed),
                        total_available=len(available)
                    )
                else:
                    self._render_error(404, "Пользователь не найден")
                    return

            elif path == '/author':
                # Страница об авторе
                html = tpl_author.render(
                    author=main_author,
                    app=app,
                    navigation=navigation,
                    api_url="https://www.cbr-xml-daily.ru/daily_json.js"
                )

            elif path == '/update':
                # Обновление курсов валют
                success = load_currencies()
                if success:
                    self.send_response(302)
                    self.send_header("Location", "/currencies?updated=1")
                    self.end_headers()
                    return
                else:
                    self.send_response(302)
                    self.send_header("Location", "/currencies?updated=2")
                    self.end_headers()
                    return

            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found')
                return

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        except Exception as e:
            self._render_error(500, f'Внутренняя ошибка сервера: {e}')


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('server is running an http://localhost:8080/')
    httpd.serve_forever()