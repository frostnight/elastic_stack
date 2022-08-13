import json
import traceback
import urllib.request
from xml.etree.ElementTree import ElementTree, fromstring

from elasticsearch import Elasticsearch, helpers


def get_api_key(key):
    with open('C:\\Users\\Justin-Laptop\\Desktop\\elastic_stack\\elastic_stack\\secrets.json', 'r') as f:
        json_data = json.load(f)
    return json_data.get(key)


api_key = get_api_key("SEOUL_PUBLIC_API_KEY")

es = Elasticsearch()

docs = []

for i in range(1, 21):
    iStart = (i-1)*1000 + 1
    iEnd = i*1000

    url = f"http://openapi.seoul.go.kr:8088/{api_key}/xml/TbPublicWifiInfo/{str(iStart)}/{str(iEnd)}/"
    response = urllib.request.urlopen(url)
    xml_str = response.read().decode('utf-8')

    tree = ElementTree(fromstring(xml_str))
    root = tree.getroot()

    for row in root.iter("row"):
        gu_nm = row.find('X_SWIFI_WRDOFC').text
        place_nm = row.find('X_SWIFI_MAIN_NM').text
        place_x = float(row.find('LAT').text)
        place_y = float(row.find('LNT').text)
        if place_y > 90 or place_y < -90:
            continue
        doc = {
            "_index": "seoul_wifi2",
            "_source": {
                "gu_nm": gu_nm,
                "place_nm": place_nm,
                "instl_xy": {
                    "lat": place_y,
                    "lon": place_x
                }
            }
        }
        docs.append(doc)
    print("END", iStart, "~", iEnd)
    res = helpers.bulk(es, docs)
print("END")
