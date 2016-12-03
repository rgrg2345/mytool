#encoding utf-8
import requests
import re
from sys import argv

def get_dns_info(url):
  #url='http://p.eagate.573.jp/game/jubeat/qubell/p/playdata/index.html'
  m=re.search('(?:http).{3,4}www.+',url)
  if not m:
    m=re.search('(?:www).+',url)
    if not m:
      url=str('https://www.')+url
    else:
      url=str('https://')+url
  resp=requests.get(url,stream=True)
  (ip,port)=resp.raw._connection.sock.getpeername()
  if len(argv)<3:
    print ip+','+str(port)
  elif str(argv[2])=='0':#ip
    print ip
  else:
    print port
  #print '{}'.format(ip).format(port)
if __name__=='__main__':
  get_dns_info(argv[1])
