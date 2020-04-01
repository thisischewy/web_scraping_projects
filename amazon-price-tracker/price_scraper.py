import requests
from bs4 import BeautifulSoup
import smtplib
import time

# URL = 'https://www.amazon.com/Anti-pm2-5-Personal-Breathable-Comfortable-Completed/dp/B086HNNYRH/ref=sxbs_sxwds-stvp?cv_ct_cx=kf94+mask&keywords=kf94+mask&pd_rd_i=B086HNNYRH&pd_rd_r=f0e3927e-72c4-4169-9e41-3394c23a800a&pd_rd_w=YG0bZ&pd_rd_wg=0eG34&pf_rd_p=967d8720-e4cf-4d5d-9da3-53f47ca634a3&pf_rd_r=BGXW6YT30SYYEERBP0C0&psc=1&qid=1585756300&sr=1-3-dd5817a1-1ba7-46c2-8996-f96e7b0f409c'
URL = 'https://www.amazon.com/ASUS-GeForce-Overclocked-Graphics-ROG-STRIX-RTX-2080-O11G/dp/B07HY6QWXN/ref=sr_1_1?keywords=asus+2080ti&qid=1585756279&sr=8-1'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36}'}
PRICE = 1000
# PRICE = 20


def get_price():
    page = requests.get(URL, headers=HEADERS)
    # soup = BeautifulSoup(page.content, 'html.parser')
    soup = BeautifulSoup(page.text, 'lxml')
    title = soup.find(id='productTitle').text
    price = soup.find(id='priceblock_ourprice').text

    price.strip()
    price = price.replace(',', '')
    price = float(price[1:])
    print(title.strip())
    print(price)

    if price < PRICE:
        send_email()


def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('Your email here', 'Your password')

    subject = 'Price went down!'
    body = 'Product link https://www.amazon.com/ASUS-GeForce-Overclocked-Graphics-ROG-STRIX-RTX-2080-O11G/dp/B07HY6QWXN/ref=sr_1_1?keywords=asus+2080ti&qid=1585756279&sr=8-1'
    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail('add FROM email', 'add TO email', msg)

    print('Email sent!')

    server.quit()



if __name__ == '__main__':
    while(True):
        get_price()
        time.sleep(600)


