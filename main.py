import requests
import lxml.html
import json
import settings
from my_mail import Mail


def get_ip_from_myip():
    url = 'https://api.myip.com'
    data = requests.get(url)
    if data.status_code != 200:
        return ''
    return data.json().get('ip')


def get_ip_from_prcy():
    url = 'https://pr-cy.ru/browser-details/'
    r = requests.get(url)
    if r.status_code != 200:
        return ''
    data = r.text
    html = lxml.html.fromstring(data)
    ip_address = html.xpath('//table[@class="table"]//div[@class="ip"]/text()')
    return ip_address


def main():
    funcs = [get_ip_from_myip, get_ip_from_prcy]
    ip_address = ''
    print('Start crawl...')
    for get_ip in funcs:
        if not ip_address:
            ip_address = get_ip()
    print('End crawl. Done!')

    if ip_address:
        with open('ip_log.json', 'w') as f:
            json.dump(ip_address, f, indent=4)

        print('Creating mail...')
        text_mail = settings.text_of_mail.replace('%myip%', ip_address)
        message = Mail(
            subject=settings.subject_mail,
            from_addr=settings.send_from,
            to_addr=settings.send_to,
            user=settings.user,
            password=settings.password)
        message.send(text_mail)
        print('Message sent!')
    else:
        print('Can\'t crawl your IP, sorry :c')


if '__main__' == __name__:
    main()
