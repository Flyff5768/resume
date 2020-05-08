# pip install snownlp
from snownlp import SnowNLP
import random

import time

'''local'''
from Spades_Team.ELK import elasticsearch_spades
from Spades_Team.nlp.word_judgment import word_judgment_Chinese
from Spades_Team.database.db_mysql import connect_mysql,mysql_create_table,mysql_insert_into,mysql_select

'''docker'''
# from ELK import elasticsearch_spades
# from word_judgment import word_judgment_Chinese
# from db_mysql_docker import connect_mysql,mysql_create_table,mysql_insert_into,mysql_select



place_labels_dict = {'古蹟': ['華山1914文化創意產業園區','國立故宮博物院','梁實秋故居'],
                     '海岸': ['淺水灣海濱公園','石門洞','深澳岬角'],
                     '瀑布': ['青山瀑布','十分瀑布','銀河瀑布'],
                     '燈塔': ['淡水港燈塔','富貴角燈塔','三貂角燈塔'],
                     '登山': ['金面山步道','頂山石梯嶺步道','南港山縱走親山步道'],
                     '遊樂園': ['臺北市兒童新樂園','野柳海洋世界',],
                     '淡水魚人碼頭': ['淡水魚人碼頭'],
                     '台北101': ['台北101'],
                     '紅毛城': ['紅毛城']}


food_labels_dict = {'pizza': ['Gusto Pizza','初宅 ONE HOUSE PIZZA','Papa Vito'],
                   'hot_pot': ['元和屋日式海鮮火鍋','木蘭閣','碼頭老火鍋'],
                   'ice_cream': ['永富冰淇淋','冰淇淋機場','Double V'],
                   'burrito':['NALAs Mexican Food','Macho Tacos 瑪丘墨式餅舖','Macho Tacos 瑪丘墨式餅舖 '],
                   'rotisserie':['樂軒和牛專門店','京昌園日本本格燒肉餐廳','樂軒松阪亭']}

'''從elasticsearch 拉目標類別 文章並依序進snownlp 評分 最後加總'''
def elasticsearch_feat_snowNLP(each_label):
    elasticsearch_spades.connect_elasticsearch()
    # labels = ['古蹟', '海岸', '瀑布', '燈塔', '登山', '遊樂園', '火鍋', '燒烤']
    # for each_label in labels:
    query_str =  each_label
    # print('query_str', query_str)
    place_list = []
    '''初步找出這類別有哪些推薦景點'''
    for one in elasticsearch_spades.elasticsearch_search(index='place_clean_v1', size=100, query_body={"query": {"match": {'文章內容': query_str}}}):
        # print(one['_source']['景點名稱'], 'score', one['_score'])

        if one['_source']['景點名稱'] not in place_list: place_list.append(one['_source']['景點名稱'])

    '''將這些景點的文章統整'''
    place_article_dict = {}
    for each_place in place_list :
        for two in elasticsearch_spades.elasticsearch_search(index='place_clean_v1', size=100,
                                                         query_body={"query": {"match": {'景點名稱': each_place}}}):

            # if each_place not in place_article_dict:
            #     place_article_dict[each_place] = two['_source']['文章內容']
            # else:
            #     place_article_dict[each_place] += two['_source']['文章內容']


            '''將文章內容只留中文 後 進 snowNLP '''
            Chinese_article= word_judgment_Chinese(two['_source']['文章內容'])
            if len(Chinese_article) == 0 :
                s_senti = 0
            else:
                try:
                    s = SnowNLP(word_judgment_Chinese(two['_source']['文章內容']))
                    s_senti = round(s.sentiments, 2)
                except:
                    print(word_judgment_Chinese(two['_source']['文章內容']))
                    s_senti = 0

            if each_place not in place_article_dict:
                place_article_dict[each_place] = s_senti
            else:
                place_article_dict[each_place] += s_senti






        # print(two)
        # print(two['_source']['文章內容'])
        # print('='*500)

    return place_article_dict

'''設定 收尋 類別 及 存進 mysql'''
def search_and_mysql(target_dict):
    for each_target in target_dict.items():
        # print(each_target)
        # print(each_target[0])
        # print(each_target[1])
        dict_tmp = elasticsearch_feat_snowNLP('台北 '+each_target[0])
        # print(dict_tmp)
        for each in dict_tmp.items():
            # print(each[0])
            # print(each[1])
            connect_mysql()
            sql_table_name = each_target[1]+'_score'  # mysql table 名稱
            sql_str = '''
                     CREATE TABLE IF NOT EXISTS {}(
                     place varchar(50) 	PRIMARY KEY,
                     score	float);
                     '''.format(sql_table_name)
            mysql_create_table(sql_str)
            sql_str = 'insert into {}(place,score) values(\'{}\',{});'.format(sql_table_name,each[0], each[1])
            mysql_insert_into(sql_str)
            # print('=' * 1000)


def place_recommend(pred_place_dict):
    place_recommend_list = []
    target_dict = {'古蹟': 'Historic',
                   '海岸': 'coastal',
                   '瀑布': 'waterfall',
                   '燈塔': 'Lighthouse',
                   '登山': 'Mountaineering',
                   '遊樂園': 'amusement_park',
                   '親子': 'Parent_child',
                   '情侶': 'Couple',
                   '老少咸宜': 'Old_and_young',
                   '朋友': 'friend'}

    connect_mysql()
    for each_place in pred_place_dict.items():

        '''手動推薦'''
        #place_recommend_list.append(place_labels_dict[each_place[0]][random.randint(0, len(place_labels_dict[each_place[0]])-1)])

        '''spades 推薦'''
        if each_place[0] == '台北101':
            place_recommend_list.append('台北101')
        elif each_place[0] == '紅毛城':
            place_recommend_list.append('紅毛城')
        elif each_place[0] == '淡水漁人碼頭':
            place_recommend_list.append('淡水漁人碼頭')
        else:
            sql_str='SELECT * FROM {} ORDER BY score DESC LIMIT 3'.format(target_dict[each_place[0]]+'_score')
            # print('sql_str',sql_str)
            # print('mysql_select(sql_str)',mysql_select(sql_str))
            tmp = mysql_select(sql_str)
            # print(tmp)
            # print(tmp[random.randint(0, len(tmp)-1)][0])
            place_recommend_list.append(tmp[random.randint(0, len(tmp)-1)][0])

    return place_recommend_list


def food_recommend(pred_food_dict):
    food_recommend_list = []
    target_dict = {'披薩': 'pizza',
                   '火鍋': 'hot_pot',
                   '冰淇淋': 'ice_cream',
                   '墨西哥捲餅': 'burrito',
                   '燒烤': 'rotisserie',
                   }

    connect_mysql()
    for each_food in pred_food_dict.items():

        '''手動推薦'''
        #food_recommend_list.append(food_labels_dict[each_food[0]][random.randint(0, len(food_labels_dict[each_food[0]]) - 1)])

        '''spades 推薦'''
        sql_str = 'SELECT * FROM {} ORDER BY score DESC LIMIT 3'.format(each_food[0] + '_score')
        # print('sql_str',sql_str)
        # print('mysql_select(sql_str)',mysql_select(sql_str))
        tmp = mysql_select(sql_str)
        # print(tmp)
        # print(tmp[random.randint(0, len(tmp)-1)][0])
        food_recommend_list.append(tmp[random.randint(0, len(tmp) - 1)][0])

    return food_recommend_list



def main():
    # pred_place_dict = {'古蹟': 1, '台北101': 3, '紅毛城': 1, '海岸': 1, '燈塔': 1, '瀑布': 1,'淡水漁人碼頭':1}
    # pred_food_dict = {'pizza': 1, 'hot_pot': 1, 'ice_cream': 1, 'burrito': 1, 'rotisserie': 1}
    #
    #
    # print(place_recommend(pred_place_dict))
    # print(food_recommend(pred_food_dict))
    #==================================================================================================================

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

    # search_and_mysql(target_dict)
    # ==================================================================================================================

    search_tag = '台北 甜點'
    tag_dict = elasticsearch_feat_snowNLP(search_tag)
    print()

    tag_dict_list = sorted(tag_dict.items(), key=lambda d: d[1], reverse=True)
    # print (tag_dict_list)
    print("共", len(tag_dict_list), '個 Tag')
    print(search_tag)
    for i in range(1, len(tag_dict_list)):
        print('第', i, '名 :', tag_dict_list[i - 1][0], tag_dict_list[i - 1][1])



if __name__ == '__main__':

    time_start = time.time()
    main()
    cost_time = time.time() - time_start
    print(cost_time , '秒')
    print('Complete!!!!!!!!!!')
