# CREATED BY JOHN EARL COBAR

# lib imports
import smtplib
from os import environ
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

################## INIT ##########################

sender_email = environ['SENDER_EMAIL']
sender_pw = environ['SENDER_PW']

#################################################
##############  SENDING PROCESS #################
#################################################

def send_email(game_link,game_name,game_image,game_desc,free_till,source,email_list):

    for to in email_list:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'{game_name} is now Free to Keep!'
        msg['To'] = to
        msg['From'] = sender_email

        # EMAIL CONTENT
        html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
         <head>
          <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
          <title>""" + game_name + """- Free to Keep Game Available!</title>
          <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        </head>
        <body style="background-color:black;color:white">
        <img src=""" + game_image + """ style="width: 324px; height: 151px; overflow: hidden; display: block;
        margin-left: auto;
        margin-right: auto;
        width: 75%;"></img>
        <h2 style="text-align:center">""" +  game_name + """ is now available for Free!</h2>
        <h4>From the """ + source + """
        <p>""" + game_desc + """</p>
        <br>
        <p>The Game is free until """ + free_till + """</p>
        <br>
        </h4>
        <h1 style="text-align:center"><a href=""" + f'"{game_link}"' + """>Grab it Now!</a></h1>
        </body>
        </html>
                        """
        msg.attach(MIMEText(html,'html'))

        # ZOHOMAIL
        with smtplib.SMTP('smtp.zoho.com', 587) as mail:
            mail.ehlo()
            mail.starttls()
            mail.login(sender_email,sender_pw)
            mail.sendmail(msg['From'], msg['To'], msg.as_string())
            print(f'Email successfully sent to {to}')
