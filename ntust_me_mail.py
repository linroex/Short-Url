import csv
import requests

from requests.auth import HTTPBasicAuth
from Config import config

def generate_verify_token(email):
    import hashlib
    from time import time

    return hashlib.sha224((email + str(time()) + config['secret']).encode('utf8')).hexdigest()

def get_random_password(length):
    from random import choice
    from string import ascii_uppercase

    return ''.join([choice(ascii_uppercase) for c in range(length)])

def add_smtp_credentials(login, password):
    return requests.post(
        '{API_URL}/domains/{DOMAIN}/credentials'.format(API_URL=config['API_URL'], DOMAIN=config['DOMAIN']), 
        auth = HTTPBasicAuth('api', config['API_KEY']), 
        data = {
        'login': login,
        'password': password
    })

def send_verify_mail(receiver, name, token):
    subject = 'NTUST.ME 電子信箱申請確認信'
    content = open('verify_mail.html', encoding='utf-8').read().replace('{{name}}', name).replace('{{token}}', token)

    return requests.post(
        '{API_URL}/{DOMAIN}/messages'.format(API_URL=config['API_URL'], DOMAIN=config['DOMAIN']),
        auth=("api", config['API_KEY']),
        data={"from": config['SENDER'],
            "to": receiver,
            "subject": subject,
            "html": content,
            "o:tracking-opens":True})

def add_forward_route():
    pass

def main():
    with open('/Users/linroex/Downloads/NTUST.ME 信箱封測申請-report.csv', encoding='utf8') as f:
        f.readline()
        appliers = csv.reader(f)

        for applier in appliers:
            name = applier[1]
            email = applier[3]
            token = generate_verify_token(email)
            
            send_verify_mail(email, name, token)
            exit()

if __name__ == '__main__':
    main()