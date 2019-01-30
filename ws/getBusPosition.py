# coding: UTF-8
import urllib3
import re
from bs4 import BeautifulSoup

url = "http://transfer.navitime.biz/seibubus-dia/pc/location/BusLocationResult?startId=00110168&goalId=00110123"

http = urllib3.PoolManager()
html = http.request('GET', url)

soup = BeautifulSoup(html.data, "html.parser")

plots = soup.find_all("li", id=re.compile("plot"))

print(plots.pop(0).find_all("div", class_="courseName"))

for plot in plots:
  try:
    plotsoup = BeautifulSoup(plot, "html.parser")
    courseName = plotsoup.find_all("div", class_="courseName").pop(0).replace('＜', '').replace('＞', '')
    departuretime = plotsoup.find_all("div", text=re.compile("発車まで")).pop(0).replace(' ', '')

    print(courseName)
    print(departuretime)
  except:
    pass

