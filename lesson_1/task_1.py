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
