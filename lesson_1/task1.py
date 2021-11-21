import subprocess
from random import randint


def ip_address():
    return '.'.join([str(randint(1, 255)) for _ in range(4)])


def host_ping(addresses):
    reachable = []
    unreachable = []
    for address in addresses:
        if subprocess.call(['ping', '-c', '1', address], stdout=subprocess.DEVNULL) == 0:
            print(f'{address} доступен')
            reachable.append(address)
        else:
            print(f'{address} недоступен')
            unreachable.append(address)

    return reachable, unreachable

if __name__ == '__main__':
    host_ping([ip_address() for i in range(3)])
