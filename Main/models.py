# CREATED BY JOHN EARL COBAR

# lib imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import datetime

################## INIT ##########################

base = declarative_base()

#################################################
###############  SQL MODELS #####################
#################################################

# GAMES
class Games(base):

    __tablename__ = 'Games'
    Link = Column(String, primary_key=True)
    Name = Column(String)
    Image = Column(String)
    Desc = Column(String)
    Till = Column(String)
    Source = Column(String)

    ##### additional info ########
    date_added = Column(DateTime, default=datetime.datetime.utcnow)

# EMAILS
class Emails(base):

    __tablename__ = 'Emails'
    Email = Column(String, primary_key=True)

    ##### additional info ########
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
