# CREATED BY JOHN EARL COBAR

# lib imports
import requests
from time import sleep

# WORKER
def pinger_worker():
    print('Starting pinger')
    while True:
        while True:
            try:
                requests.get('https://free-to-keep.herokuapp.com/')
                break
            except Exception as e:
                print(e)
        sleep(1500)
