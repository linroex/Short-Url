import csv
import requests

from requests.auth import HTTPBasicAuth

API_URL = 'https://api.mailgun.net/v3'
API_KEY = 'key-80tmpp2v51qj6jd234d4g7hhqkrmtrf1'
DOMAIN = 'ntust.me'
SENDER = 'no-reply@ntust.me'

def get_random_password(length):
    from random import choice
    from string import ascii_uppercase

    return ''.join([choice(ascii_uppercase) for c in range(length)])

def appliers_handler(appliers_file):

    with open(appliers_file, encoding='utf8') as f:
        f.readline()
        appliers = csv.reader(f)

        for applier in appliers:
            # login = applier[2]
            email = applier[3]
            # password = get_random_password(8)
            
            send_verify_mail(email)

def add_smtp_credentials(login, password):
    return requests.post(
        '{API_URL}/domains/{DOMAIN}/credentials'.format(API_URL=API_URL, DOMAIN=DOMAIN), 
        auth = HTTPBasicAuth('api', API_KEY), 
        data = {
        'login': login,
        'password': password
    })

def send_verify_mail(receiver):
    subject = 'NTUST.ME 電子信箱申請確認信'
    content = open('verify_mail.html', encoding='utf-8').read()

    return requests.post(
        '{API_URL}/domains/{DOMAIN}/credentials'.format(API_URL=API_URL, DOMAIN=DOMAIN),
        auth=("api", API_KEY),
        data={"from": SENDER,
            "to": receiver,
            "subject": subject,
            "html": content,
            "o:tracking-opens":True})

def add_forward_route():
    pass

def main():
    appliers_handler('/Users/linroex/Downloads/NTUST.ME 信箱封測申請-report.csv')

if __name__ == '__main__':
    main()