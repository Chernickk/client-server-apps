import os
import subprocess
from uuid import uuid4
import sys
from time import sleep

PYTHON_PATH = sys.executable
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def get_subprocess(file_with_args):
    sleep(0.2)
    file_full_path = f"{PYTHON_PATH} {BASE_PATH}/{file_with_args}"
    args = ["gnome-terminal", "--disable-factory", "--", "bash", "-c", file_full_path]
    return subprocess.Popen(args, preexec_fn=os.setpgrp)


def run_server():
    get_subprocess('server.py 127.0.0.1 8888')


def run_n_clients(n):
    for i in range(n):
        client_name = str(uuid4())[:8]
        get_subprocess(f'client.py 127.0.0.1 8888 {client_name}')


if __name__ == '__main__':
    run_server()
    run_n_clients(5)