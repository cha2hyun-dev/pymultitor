import socket
import requests
from os import path
from time import sleep
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from importlib.machinery import SourceFileLoader

__folder__ = path.dirname(__file__)


def check_pymultitor(address='127.0.0.1', port=8080):
    s = socket.socket()
    try:
        s.connect((address, port))
        return True
    except socket.error:
        return False


def execute_pymultitor():
    pymultitor_path = path.abspath(path.join(__folder__, '..', '..', 'pymultitor.py'))
    pymultitor_module = SourceFileLoader('pymultitor', pymultitor_path).load_module("pymultitor")
    process = Process(target=pymultitor_module.main, kwargs={
        'args': ['-d', '-p', '3', '--on-count', '1']
    })
    process.start()

    while not check_pymultitor():
        sleep(1)

    return process


def iter_credentials(size=0):
    with open(path.join(__folder__, 'john.txt')) as credentials_file:
        credentials = credentials_file.readlines()
        for i, credentials in enumerate(credentials):
            if size and i >= size:
                break
            yield credentials.rstrip('\n').split(':')


def auth():
    res = requests.get('http://httpbin.org/ip', proxies={'http': '127.0.0.1:8080'}).json()
    current_ip = res['origin']
    print(current_ip)
    return current_ip

def callback():
    print("...ok")


if __name__ == '__main__':
    process = execute_pymultitor()

    username = 'test'
    pool = ThreadPool(5)
    ip_list = []
    for i in range(3):
        ip_list.append(pool.apply_async(auth, callback=callback))
    pool.close()
    pool.join()

    process.terminate()
    process.join()
    print(ip_list)
