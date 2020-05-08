# import
import os
import json
import sys
import time
from word_judgment import word_judgment
# pip
import pymysql


def connect_mysql(host='172.28.0.4',user='root',passwd='root',database='spades'):
    global db,cursor

    connect_success = False
    while connect_success == False:

        try:
            #建立資料庫連線
            db = pymysql.connect(host=host,user=user,passwd=passwd,db=database,port=3306,charset='utf8')
            cursor= db.cursor()

            db.autocommit(True)
            connect_success = True

        except Exception as err:
            print('Defact Function:', sys._getframe().f_code.co_name)
            print(err)
            time.sleep(5)


def mysql_create_table(sql_str):
    # create table
    try :
        # example
        # sql_str = '''
        #         CREATE TABLE IF NOT EXISTS place(
        #         article_url 		varchar(100) 	PRIMARY KEY,
        #         article_post_time	DATETIME,
        #         article_title		varchar(100),
        #         place_name			varchar(100),
        #         article_content		varchar(100),
        #         article_comment		varchar(100),
        #         place_address		varchar(100),
        #         place_county        char(10));
        #         '''

        cursor.execute(sql_str)

    except Exception as err:
        print('Defact Function:',sys._getframe().f_code.co_name)
        print(err)

def mysql_insert_into(sql_str):

    try :
        # example
        #sql_str='insert into product(name,price) values(\'{}\',{});'.format('Nokia 7',7000)
        cursor.execute(sql_str)

    except Exception as err:
        print('Defact Function:',sys._getframe().f_code.co_name)
        print(err)

def mysql_insert_into_place(article_url,article_post_time,article_title,place_name,article_content, article_comment, place_address, place_county):
    try :
        sql_str='''insert into place(article_url,article_post_time,article_title,place_name,article_content, article_comment, place_address, place_county) 
                    values(\'{0}\',
                    \'{1}\',
                    \'{2}\',
                    \'{3}\',
                    \'{4}\',
                    \'{5}\',
                    \'{6}\',
                    \'{7}\');'''.format(article_url,article_post_time,article_title,place_name,article_content,article_comment,place_address,place_county)
        cursor.execute(sql_str)
    except Exception as err:
        print('Defact Function:',sys._getframe().f_code.co_name)
        print(err)
        print(sql_str)

def mysql_insert_into_food(article_url,article_post_time,article_title,restaurant_name,food_name,article_content,article_comment,place_address,place_county):
    try:
        sql_str = '''insert into food(article_url,
					article_post_time,
                    article_title,
                    restaurant_name,
                    food_name,
                    article_content,
                    article_comment,
                    place_address,
                    place_county) 
                values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\');'''.format(article_url, article_post_time,article_title, restaurant_name,food_name, article_content,article_comment, place_address,place_county)
        cursor.execute(sql_str)
    except Exception as err:
        print('Defact Function:', sys._getframe().f_code.co_name)
        print(err)
        print(sql_str)

def insert_crawler_dir(dir_path):
    sql_str = '''CREATE TABLE IF NOT EXISTS place(
    article_url 		TEXT ,
    article_post_time	TEXT,
    article_title		TEXT,
    place_name			TEXT,
    article_content		MEDIUMTEXT ,
    article_comment		TEXT,
    place_address		TEXT,
    place_county        TEXT);'''
    mysql_create_table(sql_str)

    sql_str = '''CREATE TABLE IF NOT EXISTS food(
    article_url 		TEXT ,
    article_post_time	TEXT,
    article_title		TEXT,
    restaurant_name		TEXT,
    food_name			TEXT,
    article_content		MEDIUMTEXT ,
    article_comment		TEXT,
    place_address		TEXT,
    place_county        TEXT);'''
    mysql_create_table(sql_str)

    place_count = 0
    food_count = 0

    for each_dir in os.listdir(dir_path):

        # print(each_dir)
        dir_path_play_food = dir_path + "/" + each_dir
        for each_txt in os.listdir(dir_path_play_food):
            if '_record_article.txt' != each_txt:
                # print(each_txt)
                with open(dir_path_play_food + '/' + each_txt, 'r', encoding='utf8') as f:
                    for txt in f.read().split('\n-----'):
                        if txt != '\n':
                            txt = json.loads(txt)
                            # print(txt)
                            if '景點' in each_dir:
                                place_count += 1
                                mysql_insert_into_place(article_url=txt['文章網址'],
                                                        article_post_time=txt['發文時間'],
                                                        article_title=word_judgment(txt['標題']),
                                                        place_name=word_judgment(txt['景點名稱']),
                                                        article_content=word_judgment(txt['文章內容']),
                                                        article_comment=word_judgment(txt['留言']),
                                                        place_address=txt['地址'],
                                                        place_county=txt['縣市'])
                            elif '美食' in each_dir:
                                food_count += 1
                                mysql_insert_into_food(article_url=txt['文章網址'],
                                                       article_post_time=txt['發文時間'],
                                                       article_title=word_judgment(txt['標題']),
                                                       restaurant_name=word_judgment(txt['餐廳名稱']),
                                                       food_name=word_judgment(txt['美食名稱']),
                                                       article_content=word_judgment(txt['文章內容']),
                                                       article_comment=word_judgment(txt['留言']),
                                                       place_address=txt['地址'],
                                                       place_county=txt['縣市'])
    print('dir_path :', dir_path)
    print('place_count :',place_count)
    print('food_count :', food_count)
    print('total_count :', place_count + food_count)

def mysql_select(sql_str):

    try :
        # example
        # sql_str='select * from product'
        cursor.execute(sql_str)

        # print(cursor.rowcount)        #筆數
        # datarows=cursor.fetchall()
        # for r in datarows:
        #     print(r)

        return cursor.fetchall()

    except Exception as err:
        print('Defact Function:', sys._getframe().f_code.co_name)
        print(err)

def mysql_drop(sql_str):

    try :
        # example
        #sql_str='DROP TABLE food2;'
        cursor.execute(sql_str)

    except Exception as err:
        print('Defact Function:', sys._getframe().f_code.co_name)
        print(err)




def main():

    connect_mysql()

    insert_crawler_dir(dir_path = '/rawdata')


    # sql_str = 'drop table place;'
    # mysql_drop(sql_str)
    # sql_str = 'drop table food;'
    # mysql_drop(sql_str)

if __name__ == '__main__':

    main()
    db.close()
    print('Complete!!!!!!!!!!')