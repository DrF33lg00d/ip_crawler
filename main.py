import requests
import json
import settings
from my_mail import Mail


def main():
    url_ip = 'https://api.myip.com/'
    req = requests.get(url_ip)
    if req.status_code != 200:
        raise Exception(f'Error, status_code: {req.status_code}')
    ip = req.json().get('ip')
    if ip is None:
        raise Exception('IP not found.')

    need_send_mail = True
    try:
        with open('ip_log.json', 'r') as reader:
            ip_old = json.load(reader).get('ip')
            need_send_mail = ip_old is not None and ip_old != ip
    except Exception as e:
        print('No file found, create new one.')

    if need_send_mail:
        with open('ip_log.json', 'w') as f:
            json.dump({'ip': ip}, f, indent=4)
        text_mail = settings.text_of_mail.replace('%myip%', ip)
        message = Mail(
            subject=settings.subject_mail,
            from_addr=settings.send_from,
            to_addr=settings.send_to,
            user=settings.user,
            password=settings.password)
        message.send(text_mail)
    else:
        print('IP not changed.')


if '__main__' == __name__:
    main()
