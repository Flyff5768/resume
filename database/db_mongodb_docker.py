#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# import
import os
import json
import time
import sys
# need pip
from pymongo import MongoClient
#from bson.objectid import ObjectId #這東西再透過ObjectID去尋找的時候會用到


def connect_mongodb(db_name,collection_name):
	global collection

	connect_success = False
	while connect_success == False:
		try:
			# connection
			MongoClient()
			conn = MongoClient("mongodb://admin:admin@mongo:27017") # 如果你只想連本機端的server你可以忽略，遠端的url填入: database://<user_name>:<user_password>@ds<xxxxxx>.mlab.com:<xxxxx>/<database_name>，請務必既的把腳括號的內容代換成自己的資料。
			db = conn[db_name]
			collection = db[collection_name]

			connect_success = True

		except Exception as err:
			print('Defact Function:', sys._getframe().f_code.co_name)
			print(err)
			time.sleep(5)



	# collection.remove({})

def mongodb_authentication(db,username,passwd):
	collection.auth(username,passwd)

def mongodb_insert(json):

	collection.insert(json)

def mongodb_find(condition={}):

	return collection.find(condition,{"_id":0})

def mongodb_findOne(condition={}):

	return collection.find_one(condition,{"_id":0})

def mongodb_summary():
	print('collection:',collection)
	print('collection count:',collection.count())

def mongodb_remove(condition={}):
	collection.remove(condition)


def main():

	i = 0
	dir_path = '/rawdata'
	# print(os.listdir(dir_path))
	for each_dir in os.listdir(dir_path):
		if '景點' in each_dir:
			connect_mongodb("spades", "place")
		elif '美食' in each_dir:
			connect_mongodb("spades", "food")
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
							mongodb_insert(txt)
							i += 1

	connect_mongodb("spades", "place")
	mongodb_summary()
	# mongodb_remove()

	connect_mongodb("spades", "food")
	mongodb_summary()
	# mongodb_remove()

	print(i)


# # test if connection success
# collection.stats  # 如果沒有error，你就連線成功了。
# print(collection.stats)


if __name__ == '__main__':

    main()
    print('Complete!!!!!!!!!!')
