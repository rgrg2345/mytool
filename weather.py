# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re,requests
import sys,datetime


reload(sys)
sys.setdefaultencoding('utf8')

#because it is fixed, so const it
static_url='http://www.cwb.gov.tw/V7/forecast/week/week.htm'
def padding(s,n=-1):
  padlen=10
  if n==-2:
    cnt=round(len(s)/1.5)
  elif n!=-1:
    cnt=padlen-n
  else:
    cnt=len(s)
  s+=" "*int(padlen-cnt)

  return s

class Weather:
  def __init__(self,searchtag="臺北市"):
    self.tag=searchtag.lower()
    self.city=self.tag
    self.code=""
    self.printout=False

  def query(self):
    res=requests.get(static_url)
    res.encoding=('utf-8')
    code = BeautifulSoup(res.text,"html.parser")
    return code
  def extractData(self,item):
    #initialize list
    #temp 0:day , 1:night
    tempData=[['0~0' for j in range(7)]for i in range(2)]
    typeData=[['0~0' for j in range(7)]for i in range(2)]

    cnt,tcnt=0,0
    item=BeautifulSoup(item,"html.parser")
    for temp in item.select('td'):
      if re.search('上|天',str(temp)):
        continue
      data=re.search('[0-9]{1,3}.+[0-9]{1,3}',str(temp.text))
      if data:
        tempData[cnt/7][cnt%7]=data.group()
        cnt+=1
      tdata=None
      tdata=re.search('(?:title=").+',str(temp))
      if tdata:
        s=tdata.group()
        typeData[tcnt/7][tcnt%7]=s[7:len(s)-8]
        tcnt+=1
    return tempData,typeData
  def constructData(self,data,tdata):
    #init data with city name
    self.tData=padding(self.city,4)

    week=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    wod=datetime.datetime.now().weekday()
    cnt=0
    while cnt <7:
      self.tData+=padding(str(week[(wod+cnt)%7]))
      cnt+=1
    self.tData+=str('\n')
    for i in range(2):
      self.tData+=padding((str('Night' if i%2==1 else 'Day')))
      for j in range(7):
        self.tData+=padding(str(data[i][j]))
      self.tData+=str('\n')
      self.tData+=padding('')
      for j in range(7):
        self.tData+=padding(tdata[i][j],-2)
      self.tData+=str('\n')
  def setcity(self,city):
    self.city=self.tag=city
    self.tData=""
    self.tData=padding(self.tag,-2)
    self.printout=False

  def cityweather(self):
    if self.code=="":
      self.code=self.query()
    parser=self.code.select('tr')
    data,i,s=[],0,""
    while i<len(parser)-1:
      m=re.search('星期一',str(parser[i]))
      if not m:
        s=str(parser[i])+str(parser[i+1])
        data.append(s)
        i=i+2
      else:
        i=i+1

    #initial list
    citys=[""]

    for item in data:
      if self.tag=="all":
        citys[0]=BeautifulSoup(item,"html.parser").select('th')[0].text
        self.city=citys[0]
      else:
        citys=re.findall('%s'%self.tag,item)
      for city in citys:
        city=BeautifulSoup(item,"html.parser").select('th')[0].text
        self.city=city

        data,tdata=self.extractData(item)
        self.constructData(data,tdata)
        print self.tData
        self.printout=True

    if not self.printout:
      print 'Cannot\' find %s\'s weather data'%self.tag
if len(sys.argv)<2:
  w=Weather()
else:
  w=Weather(sys.argv[1])
w.cityweather()
if len(sys.argv)>2:
  cnt=0
  while cnt<len(sys.argv)-2:
    w.setcity(sys.argv[2+cnt])
    w.cityweather()
    cnt+=1


