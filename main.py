import requests
import lxml.html
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import settings
import time

def send_email(subject, to_addr, from_addr, body_text):
    """
    Send an email
    """
    message = MIMEMultipart()
    message['From'] = from_addr
    message['To'] = to_addr
    message['Subject'] = subject
    BODY = "\r\n".join((
        "From: %s" % from_addr,
        "To: %s" % to_addr,
        "Subject: %s" % subject ,
        "",
        body_text
    ))
    message.attach(MIMEText(BODY, 'plain', 'utf-8'))
    session = smtplib.SMTP(settings.HOST, settings.PORT)
    session.set_debuglevel(True)
    session.starttls()
    session.login(settings.user, settings.password)
    text = message.as_string()
    session.sendmail(from_addr, to_addr, text)
    session.quit()





def main():
    print('Start crawl...')
    URL = 'https://pr-cy.ru/browser-details/'
    r = requests.get(URL)
    data = r.text
    html = lxml.html.fromstring(data)
    ip_address = html.xpath('//table[@class="table"]//div[@class="ip"]/text()')
    print('End crawl. Done!')

    with open('ip_log.json', 'w') as f:
        json.dump(ip_address, f, indent=4)

    while True:
        try:
            print('Trying to sent mail...')
            send_email(settings.subject_mail, settings.send_to, settings.send_from, ip_address[0])
            print('Mail Sent')
            break
        except Exception as e:
            print('kekeke))')
            time.sleep(2)








if '__main__' == __name__:
    main()
