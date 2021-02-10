import socket
import requests
import time
from os import path
from time import sleep
from multiprocessing import Process
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
        'args': ['-d', '-p', '10', '--on-count', '2']
    })
    process.start()

    while not check_pymultitor():
        sleep(1)

    return process


if __name__ == '__main__':

    start_time = time.time()
    process = execute_pymultitor()
    ip_list = []
    for i in range(20):
        res = requests.get('http://httpbin.org/ip', proxies={'http': '127.0.0.1:8080'}).json()
        print("%d) %s" % (i + 1, res['origin']))
        ip_list.append([res['origin']])

    end_time = time.time()
    for idx, ip in enumerate(ip_list):
        print(idx,"-번 ip)",ip)

    print("총",len(ip_list),"개 ip 확보 걸린 시간 ",end_time-start_time)


    process.terminate()
    process.join()
