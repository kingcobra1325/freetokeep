# CREATED BY JOHN EARL COBAR

# lib imports
import requests
from time import sleep

# WORKER
def pinger_worker():
    print('Starting pinger')
    while True:
        requests.get('https://free-to-keep.herokuapp.com/')
        sleep(1500)
