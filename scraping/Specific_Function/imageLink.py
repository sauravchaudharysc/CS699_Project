import requests 
from bs4 import BeautifulSoup
res = requests.get("https://www.91mobiles.com/top-10-mobiles-in-india")

soup = BeautifulSoup(res.text,'html.parser')


ImageLink=[]

title = soup.title.string
box = soup.find_all(class_="finder_pro_image fimage gaclick")

for desc in box:
	if desc.get('src')!= None:
		src_value = desc.get('src')
	else :
		src_value = desc.get('data-src')	
	ImageLink.append(src_value.replace('//',''))
	
print(ImageLink)
