from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://betting.racingpost.com/horses/cards/")
bsObj = BeautifulSoup(html.read())
namelist=bsObj.select("a")
for i in namelist:
    print(i['href'])
