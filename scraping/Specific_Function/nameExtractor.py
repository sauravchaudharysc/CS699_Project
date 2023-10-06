import requests 
from bs4 import BeautifulSoup
res = requests.get("https://www.91mobiles.com/top-10-mobiles-in-india")

soup = BeautifulSoup(res.text,'html.parser')

title = soup.title.string
box = soup.find_all(class_="filter-grey-bar")

#List To Store All The Names of Phone on this Page
phoneName=[]
for x in box :
	if x.a == None :
		continue
	temp=x.a.getText().replace('\n','').lstrip().rstrip()
	phoneName.append(temp)
print(phoneName)



