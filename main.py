import requests
import lxml.html
import json

def main():
    URL = 'https://2ip.ru/'
    data = requests.get(URL).text
    html = lxml.lxml.fromstring(r)
    ip_address = html.xpath('//*[@id="d_clip_button"]').content
    print(ip_address)



if '__main__' == __name__:
    print('Start crawl...')
    main()
    print('End crawl. Done!')
