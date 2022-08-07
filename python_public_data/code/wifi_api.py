import json
import urllib.request
from xml.etree.ElementTree import ElementTree, fromstring

from elasticsearch import Elasticsearch


def get_api_key(key):
    with open('C:\\Users\\Justin-Laptop\\Desktop\\elastic_stack\\elastic_stack\\secrets.json', 'r') as f:
        json_data = json.load(f)
    return json_data.get(key)


api_key = get_api_key("SEOUL_PUBLIC_API_KEY")
# url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/TbPublicWifiInfo/1/5/"
# response = urllib.request.urlopen(url)
# json_str = response.read().decode('utf-8')
# data = json.loads(json_str)
# print(json.dumps(data, indent=4, ensure_ascii=False))

es = Elasticsearch()

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
        doc = {
            "gu_nm": gu_nm,
            "place_nm": place_nm,
            "instl_xy": {
                "lat": place_y,
                "lon": place_x
            }
        }
        res = es.index(index="seoul_wifi", doc_type="_doc", document=doc)
    print("END", iStart, "~", iEnd)
print("END")
