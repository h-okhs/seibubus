# coding: UTF-8
import requests
import re
from bs4 import BeautifulSoup

url = "http://transfer.navitime.biz/seibubus-dia/pc/location/BusLocationResult?startId=00110168&goalId=00110123"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"}
res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.content, "lxml")

plots = soup.select("ul#resultList li")
print(plots)

for plot in plots:
  try:
    plotsoup = BeautifulSoup(plot, "lxml")
    courseName = plotsoup.find_all("div", class_="courseName").pop(0).replace('＜', '').replace('＞', '')
    departuretime = plotsoup.find_all("div", text=re.compile("発車まで")).pop(0).replace(' ', '')

    print(courseName)
    print(departuretime)
  except:
    pass

