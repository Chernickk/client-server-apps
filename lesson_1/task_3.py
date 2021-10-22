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