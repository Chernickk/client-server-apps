from tabulate import tabulate
from task1 import host_ping


def host_range_ping_tab(ip_address):
    ip_without_last_octet = '.'.join(ip_address.split('.')[:-1])
    ip_list = [f'{ip_without_last_octet}.{i}' for i in range(1, 255)]

    reachable, unreachable = host_ping(ip_list)

    table_list = []
    for _ in range(max(len(reachable), len(unreachable))):
        reachable_ip = reachable.pop() if reachable else ''
        unreachable_ip = unreachable.pop() if unreachable else ''
        table_list.append((reachable_ip, unreachable_ip))

    headers = ['reachable', 'unreachable']

    print(tabulate(table_list, headers=headers))


if __name__ == '__main__':
    host_range_ping_tab('192.168.1.1')