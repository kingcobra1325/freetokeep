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
from Main.app_workers.date_extractor import expiry_default

################## INIT ##########################



f2p_list = [
            'https://www.epicgames.com/store/en-US/p/fortnite',
            'https://www.epicgames.com/store/en-US/p/rocket-league',
            'https://www.epicgames.com/store/en-US/p/scavengers',
            'https://www.epicgames.com/store/en-US/p/rogue-company',
            'https://www.epicgames.com/store/en-US/p/idle-champions-of-the-forgotten-realms',
            'https://www.epicgames.com/store/en-US/p/dauntless',
            'https://www.epicgames.com/store/en-US/p/paladins',
            'https://www.epicgames.com/store/en-US/p/trackmania',
            'https://www.epicgames.com/store/en-US/p/smite',
            'https://www.epicgames.com/store/en-US/p/world-of-warships',
            'https://www.epicgames.com/store/en-US/p/spellbreak',
            'https://www.epicgames.com/store/en-US/p/heroes-and-generals-wwii',
            'https://www.epicgames.com/store/en-US/p/crsed-f-o-a-d',
            'https://www.epicgames.com/store/en-US/p/auto-chess',
            'https://www.epicgames.com/store/en-US/p/path-of-exile',
            'https://www.epicgames.com/store/en-US/p/magic-legends',
            'https://www.epicgames.com/store/en-US/p/mtg-arena',
            'https://www.epicgames.com/store/en-US/p/diabotical',
            'https://www.epicgames.com/store/en-US/p/neverwinter',
            'https://www.epicgames.com/store/en-US/p/star-trek-online',
            'https://www.epicgames.com/store/en-US/p/primordials-battle-of-gods',
            'https://www.epicgames.com/store/en-US/p/might-and-magic-chess-royale',
            'https://www.epicgames.com/store/en-US/p/hyper-scape',
            'https://www.epicgames.com/store/en-US/p/thecycle',
            'https://www.epicgames.com/store/en-US/p/battle-breakers',
            'https://www.epicgames.com/store/en-US/p/spellforce-3-versus',
            'https://www.epicgames.com/store/en-US/p/sludge-life',
            'https://www.epicgames.com/store/en-US/p/thimbleweed-park--delores',
            'https://www.epicgames.com/store/en-US/p/3-out-of-10-season-2',
            'https://www.epicgames.com/store/en-US/p/genshin-impact',
            'https://www.epicgames.com/store/en-US/p/unmetal--demo',
            'https://www.epicgames.com/store/en-US/p/aeterna-noctis--demo',
            'https://www.epicgames.com/store/en-US/p/knockout-city--trial',
            'https://www.epicgames.com/store/en-US/p/football-manager-2021--demo',
            'https://www.epicgames.com/store/en-US/p/bonfire-peaks',
            'https://www.epicgames.com/store/en-US/p/animation-throwdown-the-quest-for-cards',
            'https://www.epicgames.com/store/en-US/p/phantasy-star-online-2',
            'https://www.epicgames.com/store/en-US/p/eve-online',
            'https://www.epicgames.com/store/en-US/p/warframe',
            'https://www.epicgames.com/store/en-US/p/warface',
            'https://www.epicgames.com/store/en-US/p/core',
            'https://www.epicgames.com/store/en-US/p/crayta',
            'https://www.epicgames.com/store/en-US/p/league-of-legends',
            'https://www.epicgames.com/store/en-US/p/teamfight-tactics',
            'https://www.epicgames.com/store/en-US/p/legends-of-runeterra',
            'https://www.epicgames.com/store/en-US/p/valorant',
            'https://www.epicgames.com/store/en-US/p/ghost-recon-breakpoint--free-trial'

]

email_sent = False

# BINARY INIT
if environ.get('DEPLOYED'):
    GOOGLE_CHROME_BIN = environ.get('GOOGLE_CHROME_BIN')
    CHROMEDRIVER_PATH = environ.get('CHROMEDRIVER_PATH')
else:
    GOOGLE_CHROME_BIN = 'C:\Pysourcecodes\chromium\chrome.exe'
    CHROMEDRIVER_PATH = 'C:\Pysourcecodes\chromium\chromedriver'

# SELENIUM DRIVER INIT
def parse_init(driver):
    driver.get('https://www.epicgames.com/store/en-US/free-games')
    sleep(20)
    parse_list = []
    # check bundle first
    for bundles in driver.find_elements_by_xpath('//a[starts-with(@href,"/store/en-US/bundle")]'):
        parse_list.append(bundles)
    # check games
    for items in driver.find_elements_by_xpath('//a[starts-with(@href,"/store/en-US/p/")]'):
        parse_list.append(items)
    if parse_list == None:
        print("No Free to Keep games at the moment!")
        parse_init(driver)
    return parse_list

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
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--log-level=3")
            options.binary_location = GOOGLE_CHROME_BIN
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=options)
            list_link = parse_init(driver)
            check_link_list = []
            for link in list_link:
                if link:
                    check_link_list.append(link.text)
            break
        except Exception as e:
            print(e)
            print('Restarting EGS parsing...')
    for check_link in check_link_list:
        try:
            # Cycle thru WebElements
            for parse_link in parse_init(driver):
                if check_link == parse_link.text:
                    href_link = parse_link.get_attribute('href')
                    print(f'CURRENTLY CHECKING LINK:{href_link}')
                    if not f2p_list.count(href_link):
                        link = parse_link
            raw_time = link.find_elements_by_xpath(".//time")
            if raw_time:
                free_till_raw = link.find_elements_by_xpath(".//time")[0].text
            else:
                free_till_raw = expiry_default()
            # print('Test 1 Successful')
            game_link = link.get_attribute('href')
            driver.get(game_link)
            sleep(3)
            if driver.find_element_by_xpath("//button[starts-with(@data-testid,'purchase-cta-button')]").text == 'GET':
                print(game_link)
                name_list = driver.find_elements_by_xpath("//div[starts-with(@data-component,'PDPTitleHeader')]")
                while True:
                    name_temp = name_list.pop(0).text
                    if name_temp:
                        game_name = name_temp
                        break
                if not game_name:
                    game_name_raw = driver.find_elements_by_xpath("//div[starts-with(@class,'SubPageHeader')]")
                    if not game_name_raw:
                        game_name = driver.find_element_by_xpath("//h1[contains(@class,'MarkdownHeading')]").text
                    else:
                        # print('Test 3 Successful')
                        game_name = game_name_raw[1].find_elements_by_xpath(".//h3")[1].text

                print(game_name)
                image_addr = driver.find_element_by_xpath("//div[starts-with(@data-component,'PDPSidebarLogo')]//img[starts-with(@data-component,'FallbackImage')]")
                if image_addr:
                    game_image = image_addr.get_attribute('src').split('?')[0]
                else:
                    game_image = driver.find_element_by_xpath("//div[contains(@class,'AspectRatioContainer__content')]/div/div").get_attribute('style').split('"')[1].split('?')[0]
                print(game_image)
                desc_addr = driver.find_elements_by_xpath("//div[starts-with(@data-component,'MarkdownParagraph')]")
                if desc_addr:
                    game_desc = desc_addr[0].text
                else:
                    game_desc = driver.find_element_by_xpath("//div[contains(@class,'imageContainerSimple')]/following-sibling::div/div").text
                print(game_desc)
                print(free_till_raw)
                free_game_db(game_link,game_name,game_image,game_desc,free_till_raw,source = "Epic Games Store")
                email_sent = True
            else:
                print(f'Its currently not FREE: {game_link}')
        except (StaleElementReferenceException,NoSuchElementException,IndexError) as e:
            print(f'Not a valid free to keep game!: {e}')
    driver.close()
    if email_sent == False:
        egs_parse()

# RUN PARSE AT INIT
print('Running INIT Parse')
egs_parse()

# SCHEDULE_WORKER
schedule.every().day.at("23:05").do(egs_parse)

# WORKER
def egs_worker():
    print('Initializing Epic Games Store parsing system')
    print(GOOGLE_CHROME_BIN)
    print(CHROMEDRIVER_PATH)
    while True:
        schedule.run_pending()
        sleep(5)
