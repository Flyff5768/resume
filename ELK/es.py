# pip install elasticsearch

import time
from elasticsearch import Elasticsearch




def connect_elasticsearch():
    global es

    es = Elasticsearch(hosts="192.168.1.137",timeout=30)


def elasticsearch_search(index,query_body,size=50):
    # {"query": {"match": {'酒店地址': '台北'}}}

    es.indices.refresh(index=index)
    res = es.search(index=index,size=size, body=query_body)

    return res['hits']['hits']





'''從elasticsearch 拉目標類別 文章並依序進snownlp 評分 最後加總'''
def elasticsearch_place(each_label):
    connect_elasticsearch()
    query_str =  each_label
    place_list = []
    '''初步找出這類別有哪些推薦景點'''
    for one in elasticsearch_search(index='place_clean_v1', size=50, query_body={"query": {"match": {'文章內容': query_str}}}):

        if one['_source']['景點名稱'] not in place_list: place_list.append(one['_source']['景點名稱'])

    '''將這些景點的文章統整'''
    place_article_dict = {}
    for each_place in place_list :
        for two in elasticsearch_search(index='place_clean_v1', size=100,
                                                         query_body={"query": {"match": {'景點名稱': each_place}}}):

            # if each_place not in place_article_dict:
            #     place_article_dict[each_place] = two['_source']['文章內容']
            # else:
            #     place_article_dict[each_place] += two['_source']['文章內容']


            '''將文章內容只留中文 後 進 snowNLP '''
            article= two['_source']['文章內容']

            if each_place not in place_article_dict:
                place_article_dict[each_place] = article
            else:
                place_article_dict[each_place] += article


    return place_article_dict


def main():
    target_dict = {'古蹟': 'Historic',
                   '海岸': 'coastal',
                   '瀑布': 'waterfall',
                   '燈塔': 'Lighthouse',
                   '登山': 'Mountaineering',
                   '遊樂園': 'amusement_park',
                   '披薩': 'pizza',
                   '火鍋': 'hot_pot',
                   '冰淇淋': 'ice_cream',
                   '墨西哥捲餅': 'burrito',
                   '燒烤': 'rotisserie',
                   '親子': 'Parent_child',
                   '情侶': 'Couple',
                   '老少咸宜': 'Old_and_young',
                   '朋友': 'friend'}



    dict_tmp = elasticsearch_place('台北 '+target_dict['古蹟'])

    print(dict_tmp)



    '''
    {'地點1':'分數','地點2':'分數','地點3':'分數'}
    '''





if __name__ == '__main__':
    time_start = time.time()
    main()
    cost_time = time.time() - time_start
    print(cost_time / 3600, '小時')
    print('Complete!!!!!!!!!!')
