import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import settings
import re

class Mail():
    def __init__(self, subject, from_addr, to_addr, user='', password=''):
        self.subject = subject
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.user = user
        self.password = password
        self.__server = settings.HOST
        self.__port = settings.PORT

    def __create_message(self, rec):
        try:
            email = MIMEMultipart()
            email['Subject'] = self.subject
            email['From'] = self.from_addr
            email['To'] = rec
            return email
        except Exception as e:
            print(e)

    def __attach_IP(self, message, ip_text):
        BODY = f"{ip_text}"
        message.attach(MIMEText(BODY, 'plain', 'utf-8'))
        return message

    def send(self, text):
        server = smtplib.SMTP(self.__server, self.__port)
        if self.user or self.password:
            server.ehlo()
            server.starttls()
            server.login(self.user, self.password)
        for recipient in self.to_addr:
            message = self.__create_message(recipient)
            message = self.__attach_IP(message, text)

            server.sendmail(self.from_addr, recipient, message.as_string())
        server.quit()
