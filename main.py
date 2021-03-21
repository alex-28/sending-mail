import smtplib
import os
import csv
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA = 'data'
TEMPLATE = 'template'
SERVER = 'server'
USER = 'user'
PASSWORD = 'password'


def get_data_from_config(path):
    config_path = os.path.join(BASE_PATH, path)
    config_parser = ConfigParser()
    config_parser.read(config_path)

    return {
        SERVER: config_parser.get('smtp', SERVER),
        USER: config_parser.get('smtp', USER),
        PASSWORD: config_parser.get('smtp', PASSWORD)
    }


def get_csv_data(path):
    csv_path = os.path.join(BASE_PATH, path)
    data = []
    with open(csv_path, 'r', encoding='UTF-8') as file_obj:
        reader = csv.DictReader(file_obj, delimiter=',')
        data = [line for line in reader]
    return data


def get_template(path, item):
    html_path = os.path.join(BASE_PATH, path)
    html = ''
    with open(html_path, 'r', encoding='UTF-8') as file_obj:
        html = file_obj.read()
    for key in item.keys():
        html = html.replace('{' + key + '}', item[key])
    return html


def get_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-template', '-t')
    parser.add_argument('-data', '-d')
    args = parser.parse_args()

    return {
        TEMPLATE: args.template,
        DATA: args.data
    }


args = get_command_line_arguments()
csv_data = get_csv_data(args[DATA])

config = get_data_from_config('./email.ini')
user = config[USER]

smtpObj = smtplib.SMTP(config[SERVER])
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(user, config[PASSWORD])

for item in csv_data:
    html = get_template(args[TEMPLATE], item)
    msg = MIMEMultipart('alternative')
    msg.attach(MIMEText(html, 'html'))
    msg['Subject'] = 'Hello. It`s me'
    msg['From'] = user
    # https://tempail.com/ru/ - copy temp mail and test
    smtpObj.sendmail(user, item['email'], msg.as_string())

smtpObj.quit()
