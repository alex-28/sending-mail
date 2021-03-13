import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser

base_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_path, 'email.ini')
config_parser = ConfigParser()
config_parser.read(config_path)

server = config_parser.get('smtp', 'server')
user = config_parser.get('smtp', 'user')
password = config_parser.get('smtp', 'password')

html = open('./index.html', 'r', encoding='UTF-8').read()
msg = MIMEMultipart('alternative')
msg.attach(MIMEText(html, 'html'))
msg['Subject'] = 'Subject...'
msg['From'] = user
smtpObj = smtplib.SMTP(server)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(user, password)
# https://tempail.com/ru/ - copy temp mail and test
smtpObj.sendmail(user, ['kudrezapsa@nedoz.com'], msg.as_string())
smtpObj.quit()
