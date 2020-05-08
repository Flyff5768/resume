# --- page.91
# coding: utf - 8
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np
import os
import tensorflow as tf
graph = tf.get_default_graph()  # 功能：获取当前默认计算图。
# 載入 VGG16
model = VGG16(weights='imagenet')
# 顯示出模型摘要
#model.summary()

# 辨識
def predict(pic_dir_path,pic_list=[],rank=1):

    food_classification_dict = {}

    if len(pic_list) == 0:
        temp_pic_list = os.listdir(pic_dir_path)
    elif len(pic_list) != 0:
        temp_pic_list = pic_list
    with graph.as_default():
        '''
        你的预测的逻辑代码
        '''
        for each_pic in temp_pic_list:

            img = image.load_img(pic_dir_path + "/" + each_pic, target_size=(224, 224))
            x = image.img_to_array(img)
            #print(x.shape)   # (224, 224, 3)

            # 在x array 的第 0 維新增一個資料(np.expand_dims 用於擴充維度 )
            x = np.expand_dims(x, axis=0)
            #print(x.shape)   # (1, 224, 224, 3)

            # 預測圖片 # 轉換成 VGG16 可以讀的格式
            preds = model.predict(preprocess_input(x))
            #print(preds.shape)   # (1, 1000)

            # rank 取前幾名排序
            results = decode_predictions(preds, top=rank)[0]

            # 將預測結果存為dict 並 記錄次數
            if results[0][1] in food_classification_dict:
                food_classification_dict[results[0][1]] += 1
            else:
                food_classification_dict[results[0][1]] = 1

    print(food_classification_dict)
    return food_classification_dict

def main():
    predict(pic_dir_path=r'E:\資策會-DB106\Python\PycharmProjects\Spades\Spades_Team\deep_learning\user_test')


if __name__ == '__main__':
    main()
    print('Complete!!!!!!!!!!')

