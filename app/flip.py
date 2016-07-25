import requests
from bs4 import BeautifulSoup
request = requests.get("http://www.flipkart.com/search").text
soup = BeautifulSoup(request, "lxml")
