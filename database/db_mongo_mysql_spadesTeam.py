import time
# need pip
from pymongo import MongoClient
import pymysql

def connect_mongodb(db_name,collection_name):
	global collection
	# connection
	conn = MongoClient("mongodb://admin:admin@192.168.1.137:27017") # 如果你只想連本機端的server你可以忽略，遠端的url填入: database://<user_name>:<user_password>@ds<xxxxxx>.mlab.com:<xxxxx>/<database_name>，請務必既的把腳括號的內容代換成自己的資料。
	db = conn[db_name]
	collection = db[collection_name]

def mongodb_find(condition={}):

	return collection.find(condition,{"_id":0})

def connect_mysql(host='192.168.1.137',user='root',passwd='root',database='spades'):
    global db,cursor

    #建立資料庫連線
    db = pymysql.connect(host=host,user=user,passwd=passwd,db=database,port=3306,charset='utf8')
    cursor= db.cursor()

    db.autocommit(True)

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

        print(err)



def main():

    mongo_place = 0
    mongo_food = 0

    #取景點
    connect_mongodb("spades", "place")
    for each in mongodb_find():
        #print(each)
        mongo_place += 1

    #取美食
    connect_mongodb("spades", "food")
    for each in mongodb_find():
        #print(each)
        mongo_food += 1


    print('mongo_place ',mongo_place)
    print('mongo_food ', mongo_food)

#================================================================================
    connect_mysql()
    mysql_place = 0
    mysql_food = 0

    # 取景點
    sql_str='select * from place'
    for each in mysql_select(sql_str):
        #print(each)
        mysql_place += 1

    # 取美食
    sql_str='select * from food'
    for each in mysql_select(sql_str):
        #print(each)
        mysql_food += 1

    print('mysql_place ', mysql_place)
    print('mysql_food ', mysql_food)



if __name__ == '__main__':
    time_start = time.time()
    main()
    db.close()
    cost_time = time.time() - time_start
    print(cost_time / 3600, '小時')
    print('Complete!!!!!!!!!!')