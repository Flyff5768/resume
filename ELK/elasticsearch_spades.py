# pip install elasticsearch

import time
from datetime import datetime
from elasticsearch import Elasticsearch


def connect_elasticsearch(host='192.168.1.137'):
    global es
    # IP 要改
    es = Elasticsearch(hosts=host,timeout=30)
    # es = Elasticsearch(hosts="107.167.187.84", timeout=30)

def elasticsearch_insert(index,doc_type,body):
    '''
    index 引數代表了索引名稱，
    doc_type 代表了文件型別，
    body 則代表了文件具體內容，
    id 則是資料的唯一標識 ID
    '''

    # doc = {
    #     'author': 'kimchy',
    #     'text': 'Elasticsearch: cool. bonsai cool.',
    #     'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    # }
    # res = es.index(index="test-index", id=2, body=doc)

    if 'timestamp' not in  body:
        body['insert_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        es.index(index=index,doc_type=doc_type, body=body)
    except Exception as err:
        print(err)
        connect_elasticsearch()
        time.sleep(10)
        elasticsearch_insert(index=index,doc_type=doc_type, body=body)


def elasticsearch_get(index,doc_type,id,body_json):

    res = es.get(index="test-index", id=2)
    print('res',res)
    print("res['_source']",res['_source'])

def elasticsearch_search(index,query_body,size=50):
    # body = {"query": {"match": {'酒店地址': '台北'}}}

    es.indices.refresh(index=index)
    res = es.search(index=index,size=size, body=query_body)

    return res['hits']['hits']


def elasticsearch_count(index):

    return es.count(index=index)



''' 將時間 parse 成時間物件 才能進 kibana '''
def kibana_strptime(parse_str):

    try:
        parse_str = time.strptime(parse_str, "%Y-%m-%d %H:%M:%S")
        # parse 完的樣子
        # time.struct_time(tm_year=2018, tm_mon=7, tm_mday=15, tm_hour=18, tm_min=40, tm_sec=35, tm_wday=6, tm_yday=196, tm_isdst=-1)
    except:
        try:
            parse_str = time.strptime(parse_str, "%Y-%m-%d")
            # parse 完的樣子
            # time.struct_time(tm_year=2009, tm_mon=8, tm_mday=21, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=4, tm_yday=233, tm_isdst=-1)
        except:
            # print('each',each) # each {'文章網址': 'http://place.qyer.com/poi/V2UJZlFmBz5TbVI3Cm0/', '發文時間': '2020-03-0', '標題': '齊東詩舍', '評分': '0.0', '景點名稱': '齊東詩舍', '文章內容': '福德宫建于乾隆六年，用于供奉土地公，后经过多次整修已成为当地最大的土地庙之一。', '留言': 'NA', '地址': '115台湾台北市南港区中坡南路51号号(查看地图)', '縣市': '台北市'}
            # print("each['發文時間']",each['發文時間']) # each['發文時間'] 2020-03-0
            parse_str = 'err_time_format'

    return parse_str

def main():

    es_index = "place_clean_v1"
    connect_elasticsearch()

    # print(elasticsearch_count(es_index))
    '''測試收尋時間'''

    time_start = time.time()
    query_str = '臭豆腐'
    doc_data =  elasticsearch_search(index=es_index, size= 1 ,query_body={"query": {"match": {'文章內容': query_str}}})
    print(doc_data)

    cost_time = time.time() - time_start
    print('收尋時間: {} 秒'.format(round(cost_time, 2)))

if __name__ == '__main__':
    # time_start = time.time()
    main()
    # cost_time = time.time() - time_start
    # print(round(cost_time,2), '秒')
    # print('Complete!!!!!!!!!!')
