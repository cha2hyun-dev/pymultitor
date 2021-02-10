import socket
import requests
import time
from os import path
from time import sleep
from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from importlib.machinery import SourceFileLoader
from selenium import webdriver

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
        'args': ['-d', '-p', '2', '--on-count', '1']
    })
    process.start()

    while not check_pymultitor():
        sleep(1)

    return process


def browser():  
    print("browser를 불러옵니다.")
    driver = webdriver.Chrome('./chromedriver')
    return driver

def test_func(link):
    print("test_func")
    driver = browser()
    driver.get(link)
    current_ip = socket.gethostbyname(socket.getfqdn())
    print(current_ip,"->",link, "success")

def multip():
    links = ["https://www.naver.com/", "https://m.naver.com/"]
    pool = Pool(processes=2)
    for i in range(0, len(links)):  
        pool.apply_async(test_func, args={links[i]})

    pool.close()
    pool.join()

if __name__ == '__main__':
    start_time = time.time()
    process = execute_pymultitor()
    ip_list = []
    for i in range(3):
        res = requests.get('http://httpbin.org/ip', proxies={'http': '127.0.0.1:8080'}).json()
        print("%d) %s" % (i + 1, res['origin']))
        ip_list.append([res['origin']])
        multip()

    end_time = time.time()
    for idx, ip in enumerate(ip_list):
        print(idx,"-번 ip)",ip)

    print("총",len(ip_list),"개 ip 확보 걸린 시간 ",end_time-start_time)
    process.terminate()
    process.join()
