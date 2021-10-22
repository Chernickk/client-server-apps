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
