# CREATED BY JOHN EARL COBAR

# lib imports
import os, schedule
from time import sleep
from sqlalchemy import create_engine, Column, String, DateTime, asc, desc, exists
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.pool import NullPool

# custom imports
from Main.models import Games, Emails, base
from Main.app_workers.date_extractor import date_extractor
from Main.app_workers.f2k_email import send_email

################## INIT ##########################

DATABASE_URL = os.environ['DATABASE_URL']

def session_init():
    while True:
        try:
            db = create_engine(DATABASE_URL, poolclass=NullPool)
            Session = sessionmaker(db)
            session = Session()
            base.metadata.create_all(db)
            return session,db
        except OperationalError as e:
            print(e)
            print('Database connection error. Retrying....')

#################################################
############  EMAIL FUNCTIONS ###################
#################################################

#CREATE
def register_email(email):
    session,db = session_init()
    while True:
        try:
            if session.query(exists().where(Emails.Email==email)).scalar():
                return None
            add_email = Emails(Email=email)
            session.add(add_email)
            session.commit()
            print(f'{email} successfully registered to database')
            session.close()
            db.dispose()
            return True
            break
        except OperationalError as e:
            print(e)
            print('Database connection error. Retrying....')

#READ
def fetch_emails():
    session,db = session_init()
    while True:
        try:
            return [x.Email for x in session.query(Emails).all()]
            session.close()
            db.dispose()
            break
        except OperationalError as e:
            print(e)
            print('Database connection error. Retrying....')

#DELETE
def delete_email(delete):
    session,db = session_init()
    while True:
        try:
            email_for_deletion = session.query(Emails).filter_by(Email=delete).first()
            if email_for_deletion:
                print(f'Email {email_for_deletion.Email} found. Deleting....')
                session.delete(email_for_deletion)
                session.commit()
                print('Deletion successful')
                session.close()
                db.dispose()
                return True
                break
            else:
                print('Email cannot be found on the database')
                return False
        except OperationalError as e:
            print(e)
            print('Database connection error. Retrying....')

#TEST CREATE
def test_input_email():
    while True:
        print('Register Email:')
        email = input()
        register_email(email)

#TEST READ
def test_email_check():
    session,db = session_init()
    if session.query(exists().where(Emails.Email=='sigmail.com')).scalar():
        print('Its here!')
    else:
        print('Nah')

#################################################
#############  GAME FUNCTIONS ###################
#################################################

#CREATE
def free_game_create(game_link,game_name,game_image,game_desc,free_till,source):
    session,db = session_init()
    while True:
        try:
            free_game = Games(Link=game_link,
                      Name=game_name,
                      Image=game_image,
                      Desc=game_desc,
                      Till=free_till,
                      Source=source)
            session.add(free_game)
            session.commit()
            session.close()
            db.dispose()
            send_email(game_link,game_name,game_image,game_desc,free_till,source,email_list=fetch_emails())
            break
        except OperationalError as e:
            print(e)
            print('Database connection error. Retrying....')
#READ
def free_game_db(game_link,game_name,game_image,game_desc,free_till_raw,source):
    session,db = session_init()
    while True:
        try:
            free_game = session.query(Games).filter_by(Link=game_link).first()
            session.close()
            db.dispose()
            break
        except OperationalError as e:
            print(e)
            print('Database connection error. Retrying....')
    free_till = date_extractor(free_till_raw,source)

    if not free_game:
        print(f'Free Game {game_name} is new. Sending emails now....')
        free_game_create(game_link,game_name,game_image,game_desc,free_till,source)
        return True
    elif free_game.Source != source:
        print(f'Free Game {game_name} is free on {source} but it was also free on {free_game.Source}. Sending emails now....')
        free_game_create(game_link,game_name,game_image,game_desc,free_till,source)
        return True
    else:
        print(f'{free_game.Name} from {free_game.Source} has already been parsed and emails has been sent!')
        return False

#READ_LIST
def list_game_db():
    session,db = session_init()
    while True:
        try:
            return [x for x in session.query(Games).order_by(desc(Games.date_added)).all()]
            session.close()
            db.dispose()
            break
        except Exception as e:
            print(e)
            print('Database connection error. Retrying....')

#DELETE
def delete_game(game_link):
    session,db = session_init()
    while True:
        try:
            game_for_deletion = session.query(Games).filter_by(Link=game_link).first()
            if game_for_deletion:
                print(f'{game_for_deletion.Name} {game_for_deletion.Link} found. Deleting....')
                session.delete(game_for_deletion)
                session.commit()
                print('Deletion successful')
                session.close()
                db.dispose()
                break
            else:
                print('Game cannot be found the database')
                break
        except OperationalError as e:
            print(e)
            print('Database connection error. Retrying....')

#################################################
#############  AUX FUNCTIONS ####################
#################################################

#DESC Shortener
def cleaner_desc(Games):
    UpdatedGames = []
    for game in Games:
        for section in game.Desc.split("<br>"):
            try:
                if section[0] != '<' and section[-1] != '>':
                    game.Desc = section
                    UpdatedGames.append(game)
                    break
            except IndexError:
                break
    return UpdatedGames

#################################################
############  EXPIRY FUNCTIONS ##################
#################################################

#PROCESS
def expiry_check():
    session,db = session_init()
    while True:
        try:
            print('Running expiry checker...')
            current_date = date(datetime.now().year,datetime.now().month,datetime.now().day)
            print(f'Current Date(HK): {current_date}\n')
            for check_game in session.query(Games).all():
                raw_date = check_game.Till.split('/')
                expiry_date = date(int(raw_date[2]),int(raw_date[0]),int(raw_date[1]))
                print(f'{check_game.Name} {expiry_date}')
                if current_date > expiry_date:
                    print('Game has expired\n')
                    delete_game(check_game.Link)
                else:
                    print('Game has yet to expire\n')
            session.close()
            db.dispose()
            break
        except OperationalError as e:
            print('Database connection error. Retrying....')

#SCHEDULE_WORKER
schedule.every().day.at("01:00").do(expiry_check)

#WORKER
def expiry_worker():
    print('Initializing expiry checker')
    while True:
        schedule.run_pending()
        sleep(5)
