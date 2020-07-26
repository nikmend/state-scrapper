import requests
import lxml.html

def get_totalPropertiesCount(url:str):
    response = requests.get(url)
    tree = lxml.html.fromstring(response.text)
    totalNewPropertiesCount = tree.cssselect('#total-new-properties-count-list')
    totalUsedPropertiesCount = tree.cssselect('#total-used-properties-count-list')
    return totalNewPropertiesCount,  totalUsedPropertiesCount

print( get_totalPropertiesCount('https://www.metrocuadrado.com/venta/bogota/'))