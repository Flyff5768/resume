# pip install elasticsearch


from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch(hosts="192.168.1.137")

'''
index 引數代表了索引名稱，
doc_type 代表了文件型別，
body 則代表了文件具體內容，
id 則是資料的唯一標識 ID
'''

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}

res = es.index(index="test-index", id=2, body=doc)

print('res',res)
print("res['result']",res['result'])

res = es.get(index="test-index", id=2)
print('res',res)
print("res['_source']",res['_source'])


es.indices.refresh(index="test-index")

print(es.count(index="test-index"))

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])

print('res',res)

for hit in res['hits']['hits']:
    print(hit)
    print(hit["_source"])
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
    print('=' * 200)








