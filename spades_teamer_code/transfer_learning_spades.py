# --coding:utf-8--

from keras.preprocessing import image
import numpy as np
from PIL import Image
import os
from keras.models import load_model
import tensorflow as tf
graph = tf.get_default_graph()  # 功能：获取当前默认计算图。

def read_image(img_path):
    try:
        img = image.load_img(img_path, target_size=(299, 299))
    except Exception as e:
        print(img_path, e)

    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img/255


def draw_save(img_path, label, img_test, out='tmp/'):
    img = Image.open(img_path)
    os.makedirs(os.path.join(out, label), exist_ok=True)
    if img is None: return None

    img.save(os.path.join(out, label, img_test))



def load_transfer_model(model_path,pic_dir_path,pic_list=[]):
    labels = {'古蹟': 0, '台北101': 1, '海岸': 2, '淡水漁人碼頭': 3, '瀑布': 4, '燈塔': 5, '登山': 6, '紅毛城': 7, '遊樂園': 8}
    labels = {str(v): k for k, v in labels.items()}

    with graph.as_default():
        model = load_model(model_path)  # 辨識景點

        correct_predict = 0
        error_predict = 0

        pred_dict = {}
        place_classification_dict = {}
        print('=' * 100)

        if len(pic_list) == 0:
            temp_pic_list = os.listdir(pic_dir_path)
        elif len(pic_list) != 0:
            temp_pic_list = pic_list

        for each_pic in temp_pic_list:

            # 將圖片轉為待測數據
            img = image.load_img(pic_dir_path + "/" + each_pic, target_size=(299, 299))
            img = image.img_to_array(img)
            # print(img.shape)

            '''test_1'''
            img = np.expand_dims(img, axis=0)
            img = img / 255

            pred = model.predict(img)[0]

            index = np.argmax(pred)
            pred_dict[each_pic] = labels[str(index)]

            # 將預測結果存為dict 並 記錄次數
            if labels[str(index)] in place_classification_dict:
                place_classification_dict[labels[str(index)]] += 1
            else:
                place_classification_dict[labels[str(index)]] = 1

            # print('=' * 30)
            # print(pred)
            # print("實際:",each_pic)
            # print("預測:",labels[str(index)], pred[index])

            if labels[str(index)] in each_pic:
                correct_predict += 1
            else:
                error_predict += 1

            # plt.figure()
            # im = Image.open(pic_dir_path + "/" + each_pic)
            # im_list = np.asarray(im)
            # # plt.title("file:{0}/nPredict:{1}".format(pic_path.split("/")[-1].split(".")[0],labels[pred[0]]))
            # plt.axis("off")
            # plt.imshow(im_list)
            # plt.show()

        print("model : ", model_path.split("/")[-1])
        print("正確率:", correct_predict / (correct_predict + error_predict))
        print(pred_dict)

        return place_classification_dict





def main():
    load_transfer_model(model_path=r"E:\資策會-DB106\Python\PycharmProjects\Spades\Spades_Team\spades_teamer_code/mode_iv3LeafFinetune_15.h5",
                       pic_dir_path=r"E:/資策會-DB106/專題/CNN/使用者上傳")

    load_transfer_model(
        model_path=r"E:\資策會-DB106\Python\PycharmProjects\Spades\Spades_Team\spades_teamer_code/mode_iv3LeafFinetune_15.h5",
        pic_dir_path=r"E:/資策會-DB106/專題/CNN/try")



if __name__ == '__main__':

    main()
    print('Complete!!!!!!!!!!')
