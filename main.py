import requests
from bs4 import BeautifulSoup
from pprint import pprint
import smtplib
import os
from dotenv import load_dotenv
import lxml
# This is a small project where i use Web Scrapping to track the desirable price for an item that I want to buy
# and wait for it price being modified
# Tech: use SMTP to alert myself via email

load_dotenv()
user = os.getenv('USER')
password = os.getenv('PASSWORD')
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language":"en-US,en;q=0.9",
}
link_product = "https://www.amazon.com/dp/B01N5M3752/ref=nav_ya_signin?pd_rd_i=B01N5M3752&pd_rd_w=DxxZQ&content-id=amzn1.sym.eb7c1ac5-7c51-4df5-ba34-ca810f1f119a&pf_rd_p=eb7c1ac5-7c51-4df5-ba34-ca810f1f119a&pf_rd_r=9SQBRHP5GDPP2J6VCWA5&pd_rd_wg=ZWFxM&pd_rd_r=4f67b603-9e0a-4844-8487-e8e24e04455d&s=home-garden&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw&claim_type=MobileNumber&new_account=1&th=1"
response = requests.get(url= link_product, headers= headers)
content = response.text
pprint(response.status_code)
soup = BeautifulSoup(content, "lxml")
#Get the price of the item :
data_row = soup.select_one(selector=".a-price-whole")
item_price = data_row.getText().split(".")[0]
#Get the item name :
title_row = soup.select_one(selector="#productTitle")
item_name = title_row.getText()
#Set up target price :3
target_price = 215
#set up SMTP
if int(item_price) >= target_price :
    message = f"{item_name}is now ${item_price}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection :
        connection.starttls()
        connection.login(user=user, password=password)
        connection.sendmail(from_addr=user, to_addrs=user,msg=f"Subject:AMAZON PRICE ALERT\n\n"
                                                              f"{message}\n{link_product}")

