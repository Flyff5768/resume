import time
from datetime import datetime

from Spades_Team.database import db_mongodb
from Spades_Team.ELK import elasticsearch_spades



'''排除 沒發文時間 沒景點名稱 '''
def place_clean(db_name,collection_name):

    '''連線設定'''

    # 連線 mongodb
    db_mongodb.connect_mongodb(db_name, collection_name)

    mongo_count = 0
    es_count = 0
    err_time_format = 0
    store_list = []

    for each in db_mongodb.mongodb_find():

        '''排除 沒發文時間 沒景點名稱 '''
        try:
            if each['發文時間'] == 'NA' or each['景點名稱'] == 'NA':
                continue
        except:
            continue


        store_list.append(each)
        mongo_count += 1
        es_count += 1
        if es_count % 10000 == 0: print(es_count)


    print('mongo_count', mongo_count)
    print('es_count', es_count)
    print('err_time_format', err_time_format)

    return store_list



'''將爬的景點資料清洗 並另存'''
def main():
    # hotel place food

    '''連線設定'''
    db_name = 'spades'
    source_collection_name = "place"
    store_collection_name = "place_clean_v1"


    '''排除 沒發文時間 沒景點名稱 將 發文時間 parse 成時間物件'''
    # clean_place =  place_clean(db_name=db_name, collection_name=source_collection_name)

    '''另存進新的 collection'''
    # db_mongodb.connect_mongodb(db_name,store_collection_name)
    # for doc in clean_place:
    #     db_mongodb.mongodb_insert(doc)

    '''存進 elasticsearch'''
    # 連線 elasticsearch
    elasticsearch_spades.connect_elasticsearch()
    es_index = store_collection_name
    es_doc_type = store_collection_name

    es_count = 0
    err_time_format = 0
    db_mongodb.connect_mongodb(db_name, store_collection_name)
    mongo = db_mongodb.mongodb_find()
    for each in mongo:

        ''' 將 發文時間 parse 成時間物件 '''
        kibana_time = elasticsearch_spades.kibana_strptime(each['發文時間'])
        if kibana_time != 'err_time_format':
            each['發文時間'] = kibana_time
            each['timestamp'] = kibana_time
            # print(each)
            # print(type(each))
            elasticsearch_spades.elasticsearch_insert(index=es_index, doc_type=es_doc_type, body=each)
            es_count += 1
            if es_count % 5000 == 0: print(es_count)
        else:
            err_time_format += 1


    print('es_count', es_count)
    print('err_time_format', err_time_format)





if __name__ == '__main__':
    # try:
    time_start = time.time()
    main()
    cost_time = time.time() - time_start
    print(cost_time / 3600, '小時')
    print('Complete!!!!!!!!!!')
    # except:
    #     lineNotifyMessage()
