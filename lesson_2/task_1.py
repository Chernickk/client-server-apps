"""
TODO Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из
файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data —
и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
«Тип системы». Значения для этих столбцов также оформить в виде списка и поместить
в файл main_data (также для каждого файла);

b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать
получение данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;

c. Проверить работу программы через вызов функции write_to_csv().
"""

import re
import csv


def get_data_by_pattern(filename, header):
    with open(filename, 'r', encoding='1251') as f:
        return re.findall(f'\n{header}:\s+(.*)', f.read())[0]


def get_data():
    os_prod_list = [get_data_by_pattern(f'info_{i}.txt', 'Изготовитель системы') for i in range(1, 4)]
    os_name_list = [get_data_by_pattern(f'info_{i}.txt', 'Название ОС') for i in range(1, 4)]
    os_code_list = [get_data_by_pattern(f'info_{i}.txt', 'Код продукта') for i in range(1, 4)]
    os_type_list = [get_data_by_pattern(f'info_{i}.txt', 'Тип системы') for i in range(1, 4)]

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']

    result_text = list(map(list, zip(os_prod_list, os_name_list, os_code_list, os_type_list)))
    result_text.insert(0, headers)

    with open('main_data.txt', 'w') as f:
        for line in result_text:
            f.write(', '.join(line) + '\n')

    return result_text


def write_to_csv():
    data = get_data()
    with open('main_data.csv', 'w') as f:
        csv_writer = csv.writer(f)

        csv_writer.writerows(data)


write_to_csv()
