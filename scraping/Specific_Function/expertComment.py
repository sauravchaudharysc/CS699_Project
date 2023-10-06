import requests 
from bs4 import BeautifulSoup
res = requests.get("https://www.91mobiles.com/top-10-mobiles-in-india")

soup = BeautifulSoup(res.text,'html.parser')


ExpertComment=[]

title = soup.title.string
box = soup.find_all(class_="exp_comnt_pnl")
for desc in box:
	temp = desc.getText().splitlines()
	ExpertComment.append(temp[2].lstrip().rstrip())
print(ExpertComment)
