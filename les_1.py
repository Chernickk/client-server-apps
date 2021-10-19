import subprocess

import chardet

# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате
# и проверить тип и содержание соответствующих переменных.
# Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных.

words = ['разработка',
         'сокет',
         'декоратор']
unicode_words = ('\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0',
                 '\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82',
                 '\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80')

[print(f'{word}, type {type(word)}') for word in words]
[print(f'{word}, type {type(word)}') for word in unicode_words]

# 2. Каждое из слов «class», «function», «method» записать в байтовом типе
# без преобразования в последовательность кодов (не используя методы encode и decode)
# и определить тип, содержимое и длину соответствующих переменных.

bytes_words = [b'class',
               b'function',
               b'method']

[print(f'{word}, type {type(word)}, length {len(word)}') for word in bytes_words]

# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

words_to_bytes = ['attribute',
                  'класс',
                  'функция',
                  'type']

for word in words_to_bytes:
    try:
        bytes(word, encoding='utf-8')
    except TypeError:
        print(f'{word} невозможно записать в байтовом типе')

"""
    невозможно записать в виде b'word' слова в русской раскладке
"""

# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления
# в байтовое и выполнить обратное преобразование (используя методы encode и decode).

encode_decode_words = ['разработка',
                       'администрирование',
                       'protocol',
                       'standard']

encoded_words = [word.encode('utf-8') for word in encode_decode_words]
print(encoded_words)

decoded_words = [word.decode('utf-8') for word in encoded_words]
print(decoded_words)

# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
# преобразовать результаты из байтовового в строковый тип на кириллице.

ping_ya = subprocess.Popen(('ping', 'ya.ru'), stdout=subprocess.PIPE, encoding='utf-8')

for i, line in enumerate(ping_ya.stdout):
    ping_ya.kill() if i == 5 else print(line)


# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование»,
# «сокет», «декоратор». Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.

with open('test_file.txt', 'w') as f:
    for line in ['сетевое программирование', 'сокет', 'декоратор']:
        f.write(f'{line}\n')

with open('test_file.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line, end='')


