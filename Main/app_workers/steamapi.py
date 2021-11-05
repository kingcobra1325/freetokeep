# CREATED BY JOHN EARL COBAR

# lib imports
import requests, json, timeit, traceback, logging, os, dropbox
from itertools import cycle
from time import sleep
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from dropbox.exceptions import ApiError
from json.decoder import JSONDecodeError

# custom imports
from Main.app_workers.f2k_email import send_email
from Main.database.database import free_game_db

################## INIT ##########################

dbx_token = os.environ['DROPBOX_TOKEN']
dbx = dropbox.Dropbox(dbx_token)

#################################################
###############  STEAM JSON #####################
#################################################

def update_steam_json(gamelist=None):
    if not gamelist:
        print('Creating new Steam API game list!')
        gamelist = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/').json()
    with open('steam-game-list.json', 'w') as data:
        json.dump(gamelist, data)
    with open('steam-game-list.json', 'rb') as data:
        dbx.files_upload(data.read(),'/steam_game_list.json',dropbox.files.WriteMode.overwrite)
    return gamelist

#################################################
#############  PARSE PROCESS ####################
#################################################

def steam_parse(gameappid):
    valid = False
    retry = 0
    while True:
        try:
            sleep(2)
            r = requests.get(f'http://store.steampowered.com/api/appdetails?appids={gameappid}').json()[f'{gameappid}']
            valid = True
            break
        except Exception as e:
            print(f'{gameappid} App ID')
            print(e)
            if retry < 100:
                retry+=1
                print(f'Error parsing. Retrying... (Attempt:{retry})')
            else:
                print(f'Skipping {gameappid}  App ID')
                break
    if valid:
        if r['success']:
            if r['data']['type'] == 'game':
                try:
                    discount = r['data']['price_overview']['discount_percent']
                    if discount == 100:
                        game_link =  f'https://store.steampowered.com/app/{gameappid}'
                        game_name = r['data']['name']
                        game_desc = r['data']['about_the_game']
                        game_image = r['data']['header_image']
                        free_till_raw = BeautifulSoup(requests.get(f'https://store.steampowered.com/app/{gameappid}').text,features="lxml").find('p',class_='game_purchase_discount_quantity').text.split('\t')[0]
                        print(f'{game_link}\n{game_name}\n{game_desc}\n{game_image}\n{free_till_raw}')
                        free_game_db(game_link,game_name,game_image,game_desc,free_till_raw,source = "Steam Store")
                except KeyError:
                    pass
                except AttributeError as e:
                    print(f'{e}: Error for Steam Game ID {gameappid}')

# WORKER
def steam_worker():

    while True:
        i = 0
        print('Starting steam API parsing')

        #####################
        # CHECKING IF STEAM ONLINE FILE EXISTS
        #####################
        try:
            x = dbx.files_download_to_file('steam-game-list.json','/steam_game_list.json')
        except (ApiError,AttributeError):
            print('No existing Steam Game list found!')
            try:
                os.remove('steam-game-list.json')
            except FileNotFoundError:
                pass
        #####################
        # CREATE OR LOAD STEAM FILE
        #####################
        try:
            if os.path.getsize('steam-game-list.json') > 27:
                print('Loading existing Steam API game list!')
                gamelist = json.loads(open('steam-game-list.json').read())
            else:
                gamelist = update_steam_json()
        except FileNotFoundError:
            gamelist = update_steam_json()
        while os.path.getsize('steam-game-list.json') > 27:
            try:
                game_data = gamelist['applist']['apps'].pop()
            except IndexError:
                update_steam_json(gamelist)
                break
            gameappid = game_data['appid']
            steam_parse(gameappid)
            i+=1
            if (i % 1000) == 0:
                steam_games_remaining = len(gamelist['applist']['apps'])
                update_steam_json(gamelist)
        os.remove('steam-game-list.json')
        print('Steam Store parsing complete! Restarting....')

# TEST
def test():
    r = requests.get(f'http://store.steampowered.com/api/appdetails?appids=1076280').json()[f'1076280']
    game_link =  f'https://store.steampowered.com/app/1076280'
    game_name = r['data']['name']
    game_desc = r['data']['about_the_game']
    game_image = r['data']['header_image']
    free_till_raw = BeautifulSoup(requests.get('https://store.steampowered.com/app/1076280').text,features="lxml").find('p',class_='game_purchase_discount_quantity').text.split('\t')[0]
    free_game_db(game_link,game_name,game_image,game_desc,free_till_raw,source = "Steam Store")
