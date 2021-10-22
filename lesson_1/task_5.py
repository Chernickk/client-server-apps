import subprocess

# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
# преобразовать результаты из байтовового в строковый тип на кириллице.

ping_ya = subprocess.Popen(('ping', 'ya.ru'), stdout=subprocess.PIPE, encoding='utf-8')

for i, line in enumerate(ping_ya.stdout):
    ping_ya.kill() if i == 5 else print(line)
