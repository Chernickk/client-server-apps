# 2. TODO Каждое из слов «class», «function», «method» записать в байтовом типе
#  без преобразования в последовательность кодов (не используя методы encode и decode)
#  и определить тип, содержимое и длину соответствующих переменных.

bytes_words = [b'class',
               b'function',
               b'method']

[print(f'{word}, type {type(word)}, length {len(word)}') for word in bytes_words]
