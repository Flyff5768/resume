# pip install -U ckiptagger
# pip uninstall tensorflow
# pip install tensorflow==1.13.1
import Spades_Team.line.line_notify_message as line_notify
from ckiptagger import WS,POS,NER,construct_dictionary #「WS（斷詞）」、「POS（詞性標注）」及「NER（實體辨識）」
import time
import os
import logging
# sentence_list = ["傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。",
#                  "美國參議院針對今天總統布什所提名的勞工部長趙小蘭展開認可聽證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。",
#                   "",
#                   "土地公有政策?？還是土地婆有政策。.",
#                   "… 你確定嗎… 不要再騙了……",
#                   "最多容納59,000個人,或5.9萬人,再多就不行了.這是環評的結論.",
#                   "科長說:1,坪數對人數為1:3。2,可以再增加。"]
#
# ws = WS('.\data')
# pos = POS("./data")
# ner = NER("./data")
#
# word_sentence_list = ws(
#     sentence_list,
#     # sentence_segmentation = True, # To consider delimiters
#     # segment_delimiter_set = {",", "。", ":", "?", "!", ";"}), # This is the defualt set of delimiters
#     # recommend_dictionary = dictionary1, # words in this dictionary are encouraged
#     # coerce_dictionary = dictionary2, # words in this dictionary are forced
# )
#
# pos_sentence_list = pos(word_sentence_list)
#
# entity_sentence_list = ner(word_sentence_list, pos_sentence_list)
#
# print(word_s)
# 釋放記憶體(非必要)
# del ws
# del pos
# del ner



def ckiptagger(load_txt_path,save_path):
    ws = WS('.\data')
    time_start = time.time()
    # # 加入自定義 詞與其權重
    # word_customize_dict = {
    #     "今將": 1,
    #     "安樂": 1,
    # }
    #
    # # 將自訂義辭庫 轉成dict 在轉成ckiptagger自己的格式
    # word_Customize_ckiptaggerdictionary = construct_dictionary(word_customize_dict)

    # 加入停用 詞
    # 無函式 只能變成串列 於程式中阻擋
    stopword_set = set()
    with open('../jieba/stopword.txt', 'r' ,encoding='utf-8') as file:
        for each_stopword in file.read().split('\n'):
            stopword_set.add(each_stopword)


    with open(load_txt_path, 'r', encoding='utf8') as f:
        i = 0
        for txt_line in f:
            i += 1
            if i % 1000 == 0:
                logging.info("已處理 {0} ".format(i))
                cost_time = time.time() - time_start
                print('ckiptagger 花了', cost_time / 3600, '小時')

            sentence_list = []
            sentence_list.append(txt_line)
            # word_s = ws(sentence_list,coerce_dictionary = word_Customize_ckiptaggerdictionary,sentence_segmentation=True,segment_delimiter_set={'?', '？', '!', '！', '。', ',','，', ';', ':', '、'})
            word_s = ws(sentence_list,sentence_segmentation=True,segment_delimiter_set={'?', '？', '!', '！', '。', ',', '，', ';', ':', '、'})

            str_tmp = ''
            try:
                for each_word_list in word_s:
                    for each_word in each_word_list:

                        if len(each_word) > 1 and each_word not in stopword_set:
                            str_tmp += each_word + " "

            except Exception as e:
                print(e)
                continue

            # 斷詞結果存檔
            segSaveFile = save_path
            with open(segSaveFile, 'ab') as saveFile:
                saveFile.write(str_tmp.encode('utf-8')+'\n'.encode('utf-8'))


    cost_time = time.time() - time_start
    print('ckiptagger 花了',cost_time / 3600, '小時')
    print('save_path=',save_path)

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    ckiptagger(load_txt_path='../combin/raw_place.txt',save_path='./segDone_place.txt')
    ckiptagger(load_txt_path='../combin/raw_food.txt', save_path='./segDone_food.txt')





if __name__ == '__main__':
    main()
    print('Complete!!!!!!!!!!')
    line_notify.lineNotifyMessage(msg='combin_ig_txt Complete!!!!!!!!!!')










