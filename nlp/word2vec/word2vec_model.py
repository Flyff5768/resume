import time

import os

#pip
from gensim.models import word2vec


def built_model(txt_path):

    # 建模型
    time_start = time.time()
    sentences = word2vec.LineSentence(txt_path)
    model = word2vec.Word2Vec(sentences, size=300, iter=100, sg=0, workers=3)

    model.save("./word2vec_model_words{0}.model".format(model.corpus_total_words))

    print(model.corpus_total_words)
    cost_time = time.time() - time_start
    print('built_model 花了', cost_time / 3600, '小時')


def load_model(model_path,test_words_list):
    # load 模型
    model = word2vec.Word2Vec.load(model_path)
    time.sleep(3)
    for each_word in test_words_list:

        print('{0}_{1} :'.format(each_word,model_path.split('_')[-1]))
        try:
            each_word_similar_list = model.most_similar(each_word,topn=20)

            print(each_word_similar_list)

        except KeyError as e:
            # print(e)
            print('Sorry word {0} not in vocabulary'.format(each_word))

def main():

    # 模式切換
    # mode = 'built_model'
    mode = 'load_model'

    if mode == 'built_model':

        print('start')
        # 建模型
        # built_model(txt_path="C:\\Users\Big data\PycharmProjects\PyETL2\Spades_Team\segDone_spades_v4.txt")#純維基
        built_model(txt_path=r"C:\Users\Big data\PycharmProjects\Spades\Spades_Team/nlp\ckiptagger/segDone_food.txt")

    elif mode == 'load_model':

        Tag_place_dict = {
            "室內": ["百貨", "藝術", "寺廟", "觀光工廠"],
            "室外": ["公園", "夜市", "古蹟", "老街", "運動", "農場", "登山", "遊樂園", "生態之旅"]
        }

        # load_model(model_path="./word2vec_model_words57876037_v2_pureIG.model",
        #            test_words_list=Tag_place_dict["室內"])
        # load_model(model_path="./word2vec_model_words238655291_v3_IgWiki.model",
        #            test_words_list=Tag_place_dict["室內"])
        # load_model(model_path="./word2vec_model_words180777485_v4_pureWiki.model",
        #            test_words_list=Tag_place_dict["室內"])
        # load_model(model_path="./word2vec_model_words8889372_v5_pureplace.model",
        #            test_words_list=Tag_place_dict["室內"])
        # load_model(model_path="./word2vec_model_words16073689_v6_purefood.model",
        #            test_words_list=Tag_place_dict["室內"])

        load_model(model_path="./word2vec_model_words8889372_v5_pureplace.model",
                   test_words_list=Tag_place_dict["室內"])

        load_model(model_path="./word2vec_model_words8889372_v5_pureplace.model",
                   test_words_list=Tag_place_dict["室外"])















if __name__ == '__main__':

    main()
    print('Complete!!!!!!!!!!')