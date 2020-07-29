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


def get_totalPropertiesCount(url: str):
    ua = UAS[random.randrange(len(UAS))]
    headers = {'user-agent': ua}
    response = requests.get(url, headers=headers)
    tree = lxml.html.fromstring(response.text)
    print(response.text)
    totalNewPropertiesCount = tree.cssselect('#total-new-properties-count-list')
    totalUsedPropertiesCount = tree.cssselect('#total-used-properties-count-list')
    return totalNewPropertiesCount, totalUsedPropertiesCount


def get_totalPropertiesCountBs4(url: str):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive',
               'User-Agent': UAS[random.randrange(len(UAS))]}
    response = requests.get(url, headers=headers)
    print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    totalNewPropertiesCount = soup.select('#total-new-properties-count-list')
    totalUsedPropertiesCount = soup.select('#total-used-properties-count-list')
    return totalNewPropertiesCount, totalUsedPropertiesCount


#print(get_totalPropertiesCountBs4('https://www.metrocuadrado.com/venta/bogota/'))
