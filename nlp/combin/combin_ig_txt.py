import os
import time
import json
import Spades_Team.line.line_notify_message as line_notify
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


dir_path = 'E:\資策會-DB106\專題\Instagram\All'
# dir_path = 'E:\資策會-DB106\專題\Pixnet\All'
dir_list =  os.listdir(dir_path)
txt = ''



time_start = time.time()
i = 0
for each_dir in os.listdir(dir_path):
    if '景點' in each_dir:
        save_file_name = 'raw_place.txt'
    elif '美食' in each_dir:
        save_file_name = 'raw_food.txt'

    # print(each_dir)
    temp_str = ''
    dir_path_play_food = dir_path + "/" + each_dir
    for each_txt in os.listdir(dir_path_play_food):
        if '_record_article.txt' != each_txt:
            i += 1
            if i % 50000 == 0:
                logging.info("已處理 {0} ".format(i))
                cost_time = time.time() - time_start
                print('combin 花了', cost_time / 3600, '小時')

            # print(each_txt)
            with open(dir_path_play_food + '/' + each_txt, 'r', encoding='utf8') as f:
                try:
                    read_txt = f.read()
                    for each_article in read_txt.split('\n-----'):
                        if each_article != '\n':
                            each_article = json.loads(each_article)
                            # print(txt)
                            for each_line in each_article["文章內容"].split('\n'):
                                if len(each_line) >1 and '#' not in each_line:
                                    temp_str += each_line


                except Exception as e:
                    print(e)
                    # print(read_txt)
                    pass


    with open('./'+save_file_name,'a',encoding='utf8') as f:
        f.write(temp_str + '\n')




cost_time =time.time() - time_start
print(cost_time/3600,'小時')
print('Complete!!!!!!!!!!')

line_notify.lineNotifyMessage(msg='combin_ig_txt Complete!!!!!!!!!!')
