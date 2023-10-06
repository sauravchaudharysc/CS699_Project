import requests 
from bs4 import BeautifulSoup
res = requests.get("https://www.91mobiles.com/top-10-mobiles-in-india")

soup = BeautifulSoup(res.text,'html.parser')

title = soup.title.string
box = soup.find_all(class_="price price_padding")
price = [ x.getText() for x in box ]
print(price)