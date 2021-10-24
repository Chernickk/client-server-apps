"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;

b. Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""

import json


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json', 'r+') as f:
        result = json.loads(f.read())

        result['orders'].append(
            {
                'item': item,
                'quantity': quantity,
                'price': price,
                'buyer': buyer,
                'date': date
            }
        )

        f.seek(0)
        json.dump(result, f)


write_order_to_json('item', 5, 500, 'Vasya', '22.22.22')
