# CREATED BY JOHN EARL COBAR

# lib imports
from re import compile
from calendar import month_abbr
from datetime import datetime, timedelta

################ REGEX INIT ########################

steam_extractor = compile(r'(\b\d+ \w\w\w\b|\b\w\w\w \d+\b)')
egs_extractor = compile(r'\d+/\d+/\d+')

############### CURRENT DATE #######################

currentMonth = datetime.now().month
currentYear = datetime.now().year

#################################################
#############  DATE EXTRACTOR ###################
#################################################

def date_extractor(input_date,source):
    if source == "Steam Store":
        raw_date = steam_extractor.findall(input_date)[0].split(" ")
        if raw_date[0].isnumeric():
            day = raw_date[0]
            raw_month = raw_date[1]
        elif raw_date[1].isnumeric():
            raw_month = raw_date[0]
            day = raw_date[1]
        month = [x[0] for x in enumerate(month_abbr) if raw_month == x[1]][0]
        if (raw_date[1] == 'Jan') and (currentMonth == 12):
            year = currentYear + 1
        else:
            year = currentYear
        return f'{month}/{day}/{year}'
    elif source == "" "Epic Games Store":
        raw_date = input_date.split(" ")
        raw_month = raw_date[0]
        day = raw_date[1]
        month = [x[0] for x in enumerate(month_abbr) if raw_month == x[1]][0]
        if (raw_date[1] == 'Jan') and (currentMonth == 12):
            year = currentYear + 1
        else:
            year = currentYear
        return f'{month}/{day}/{year}'
    else:
        print('Valid source not specified')

def expiry_default():
    raw_current = datetime.now() + timedelta(days=14)
    raw_month = raw_current.month
    date = raw_current.day
    month = [x[1] for x in enumerate(month_abbr) if raw_month == x[0]][0]
    return f'{month} {date}'
