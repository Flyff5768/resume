# import
import os
import json
import time
# need pip
from pymongo import MongoClient
#from bson.objectid import ObjectId #這東西再透過ObjectID去尋找的時候會用到


def connect_mongodb(db_name,collection_name,host='192.168.1.137'):
	global collection
	# connection
	conn = MongoClient("mongodb://admin:admin@{}:27017".format(host)) # 如果你只想連本機端的server你可以忽略，遠端的url填入: database://<user_name>:<user_password>@ds<xxxxxx>.mlab.com:<xxxxx>/<database_name>，請務必既的把腳括號的內容代換成自己的資料。
	db = conn[db_name]
	collection = db[collection_name]

	# collection.remove({})

def mongodb_insert(json):

	collection.insert(json)

def mongodb_find(condition={},limit=0):

	if limit == 0:
		return collection.find(condition, {"_id": 0}, no_cursor_timeout=True)
	else:
		return collection.find(condition,{"_id":0},no_cursor_timeout=True).limit(limit)

def mongodb_findOne(condition={}):

	return collection.find_one(condition,{"_id":0})

def insert_crawler_dir(dir_path):
	i = 0

	for each_dir in os.listdir(dir_path):
		if '景點' in each_dir:
			connect_mongodb("spades", "place")
		elif '美食' in each_dir:
			connect_mongodb("spades", "food")
		elif '住宿' in each_dir:
			connect_mongodb("spades", "hotel")

		# print(each_dir)
		dir_path_play_food = dir_path + "/" + each_dir
		for each_txt in os.listdir(dir_path_play_food):
			if '_record_article.txt' != each_txt:
				# print(each_txt)
				with open(dir_path_play_food + '/' + each_txt, 'r', encoding='utf8') as f:
					try:
						for txt in f.read().split('\n-----'):
							if txt != '\n':
								try:
									txt = json.loads(txt)
									# print(txt)
									mongodb_insert(txt)
								except:
									pass
								i += 1
								if i % 2000 == 0: print(i)
					except:
						pass

def mongodb_summary():
	print('collection:',collection)
	print('collection count:',collection.count())

def mongodb_remove(condition={}):
	collection.remove(condition)

def mongodb_remove(condition={}):
	collection.remove(condition)

def main():

	insert_crawler_dir(r'E:\資策會-DB106\專題\大家爬蟲資料\all')

	connect_mongodb("spades", "place")
	mongodb_summary()
	# mongodb_remove()

	connect_mongodb("spades", "food")
	mongodb_summary()
	# mongodb_remove()

	connect_mongodb("spades", "hotel")
	mongodb_summary()


# mongodb_remove()

# # test if connection success
# collection.stats  # 如果沒有error，你就連線成功了。
# print(collection.stats)


if __name__ == '__main__':
	time_start = time.time()
	main()
	cost_time = time.time() - time_start
	print(cost_time / 3600, '小時')
	print('Complete!!!!!!!!!!')
