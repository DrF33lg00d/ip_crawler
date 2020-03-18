import requests
import lxml.html
import json
import settings
from my_mail import Mail



def main():
    print('Start crawl...')
    URL = 'https://pr-cy.ru/browser-details/'
    r = requests.get(URL)
    data = r.text
    html = lxml.html.fromstring(data)
    ip_address = html.xpath('//table[@class="table"]//div[@class="ip"]/text()')
    text_mail = settings.text_of_mail.replace('%myip%', ip_address[0])
    print('End crawl. Done!')

    with open('ip_log.json', 'w') as f:
        json.dump(ip_address[0], f, indent=4)

    print('Creating mail...')
    message = Mail(
        subject=settings.subject_mail,
        from_addr=settings.send_from,
        to_addr=settings.send_to,
        user=settings.user,
        password=settings.password)
    message.send(text_mail)
    print('Message sent!')


if '__main__' == __name__:
    main()
