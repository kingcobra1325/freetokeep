# CREATED BY JOHN EARL COBAR

# lib imports
import traceback, logging, os, schedule
from os import environ
from PIL import Image
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

# custom imports
from Main.app_workers.f2k_email import send_email
from Main.database.database import free_game_db

################## INIT ##########################

email_sent = False
GOOGLE_CHROME_BIN = environ.get('GOOGLE_CHROME_BIN')
CHROMEDRIVER_PATH = environ.get('CHROMEDRIVER_PATH')

# SELENIUM DRIVER INIT
def parse_init(driver):
    driver.get('https://www.epicgames.com/store/en-US/free-games')
    sleep(30)
    print('Checking bundles first...')
    try:
        parse = driver.find_element_by_xpath('//a[starts-with(@href,"/store/en-US/bundle")]')
        print(parse)
        return parse
    except NoSuchElementException:
        print("Checking games")
        parse = driver.find_element_by_xpath('//a[starts-with(@href,"/store/en-US/product/")]')
        if parse == None:
            print("No Free to Keep games at the moment!")
            parse_init(driver)
        return parse

#################################################
##############  PARSE PROCESS ###################
#################################################

def egs_parse():

    print('Starting EGS parsing...')
    while True:
        try:
            global email_sent
            email_sent = False
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.binary_location = GOOGLE_CHROME_BIN
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=options)
            link = parse_init(driver)
            break
        except Exception as e:
            print(e)
            print('Restarting EGS parsing...')
    try:
        game_link = link.get_attribute('href')
        print(game_link)
        driver.get(game_link)
        sleep(3)
        game_name = driver.find_element_by_xpath('//h2[starts-with(@class,"NavigationVertical-subNavLabel_")]').text
        print(game_name)
        game_image = driver.find_element_by_xpath("//div[starts-with(@class,'Description-imageContainer')]").find_element_by_xpath('.//div').get_attribute('style').split('"')[1].split('?')[0]
        print(game_image)
        game_desc = driver.find_element_by_xpath("//div[starts-with(@class,'Description-description')]").text
        print(game_desc)
        free_till_raw = driver.find_element_by_xpath("//div[starts-with(@class,'PurchaseButton-priceCaption')]").find_element_by_xpath('.//span').text
        print(free_till_raw)
        free_game_db(game_link,game_name,game_image,game_desc,free_till_raw,source = "Epic Games Store")
        email_sent = True
    except (StaleElementReferenceException,NoSuchElementException):
        print('No other games at the moment!')
    driver.close()
    if email_sent == False:
        egs_parse()

# SCHEDULE_WORKER
schedule.every().thursday.at("23:05").do(egs_parse)

# WORKER
def egs_worker():
    print('Initializing Epic Games Store parsing system')
    while True:
        schedule.run_pending()
        # egs_parse()
        sleep(5)
