import requests 
from bs4 import BeautifulSoup
res = requests.get("https://www.91mobiles.com/top-10-mobiles-in-india")

soup = BeautifulSoup(res.text,'html.parser')


Performance =[]
Display =[]
Camera =[]
Battery =[]
	

title = soup.title.string
box = soup.find_all(class_="filter-grey-bar filter_gray_bar_margin grey_bar_custpage")

for boxe in box:
	sub_box = boxe.find_all(class_="left specs_li")
	for x in sub_box:
		ans=x.getText()
		if 'Performance' in ans:
			LI=[]
			for a in x.find_all("label"):
				LI.append(a.getText())
			Performance.append(LI)
		if 'Display' in ans:
			LI=[]
			for a in x.find_all("label"):
				LI.append(a.getText())
			Display.append(LI)	
		if 'Camera' in ans:
			LI=[]
			for a in x.find_all("label"):
				LI.append(a.getText())
			Camera.append(LI)	
		if 'Battery' in ans:
			LI=[]
			for a in x.find_all("label"):
				LI.append(a.getText())					
			Battery.append(LI)

print(Performance[0])
print(Display[0])
print(Camera[0])
print(Battery[0])
