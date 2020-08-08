import random
import requests
import lxml.html
from bs4 import BeautifulSoup

UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
       "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
       "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
       )


def reverseAddress(latitude: str, longitude: str):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive',
               'User-Agent': UAS[random.randrange(len(UAS))]}
    url = 'https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?apiKey=t3ojEdX3-0ZlaVzNXSk0REUYe7emfrcl-GIjoZmLcjc&mode=retrieveAddresses&prox='
    url = url + str(latitude) + ',' + str(longitude)
    response = requests.get(url, headers=headers)
    data = response.json()
    near_Address = data['Response']['View'][0]['Result']
    for Result in near_Address:
        if 'Street' in Result['Location']['Address'].keys():
            near_Address = Result['Location']['Address']
            break
    return near_Address


def cleanContact(arrayCont):
    clean= set()
    for it in arrayCont:
        tmp= it.strip()
        if len(tmp)>1:
            clean.add(tmp)
    return '/ '.join(clean)
#print( reverseAddress(4.607478241760199,-74.10118935600482))
# print(get_totalPropertiesCountBs4('https://www.metrocuadrado.com/venta/bogota/'))
