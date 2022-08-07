from elasticsearch import Elasticsearch

es = Elasticsearch()

doc = {"name": "kim", "age": 35}
res = es.index(index='test_index', document=doc)
print(res)

query = {
    "term": {
        "DestCityName": "Seoul"
    }
}

res = es.search(index='kibana_sample_data_flights', query=query, size=1)
print(res)
