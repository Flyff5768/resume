# pip uninstall tensorflow
# pip install tensorflow==1.14.0

# pip uninstall keras
# pip install keras==2.2.5

import os
import matplotlib.pyplot as plt
from keras.models import Sequential , load_model
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D,Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping
# from keras.backend import clear_session
import tensorflow as tf
graph = tf.get_default_graph()  # 功能：获取当前默认计算图。


import glob
from keras.preprocessing import image
from PIL import Image , ImageFile
import numpy as np

ImageFile.LOAD_TRUNCATED_IMAGES = True

def built_CNN_model(dir_path,model_save_name):

    # 指定圖片集路徑
    train_dir = dir_path + '/train'
    test_dir = dir_path + '/test'


    # 指定類別數
    num_classes = len(os.listdir(train_dir))

    ##模型設計##
    #模型初始化
    model = Sequential()

    #第一層 卷積層1
    model.add(Conv2D(filters=32, kernel_size=(3,3), input_shape=(150,150,3), activation='relu'))
    #第二層 池化層1
    model.add(MaxPooling2D(pool_size=(2,2)))
    #第三層 卷積層2
    model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu'))
    #第四層 池化層2
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.2))
    #第五層 卷積層3
    model.add(Conv2D(filters=128, kernel_size=(3,3), activation='relu'))
    #第六層 池化層3
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.2))
    #第七層 卷積層4
    model.add(Conv2D(filters=128, kernel_size=(3,3), activation='relu'))
    #第八層 池化層4
    model.add(MaxPooling2D(pool_size=(2,2)))
    #第九層 平坦層
    model.add(Flatten())
    #第十層 全連接層
    model.add(Dense(6272,activation='relu'))
    #第十一層 全連接層
    model.add(Dense(num_classes,activation='softmax'))

    # 顯示出模型摘要
    model.summary()


    estop = EarlyStopping(monitor='val_loss', patience=5)
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=1e-4), metrics=['accuracy'])

    # 將訓練的影像檔轉為批次量的張量
    train_datagen =  ImageDataGenerator(
        rescale=1./255, # 指定將影象像素縮放到 0~1 之間
                                         )
    test_datagen = ImageDataGenerator(rescale=1./255)
    # 訓練資料與測試資料
    # 分類超過兩類 使用 categorical, 若分類只有兩類使用 binary
    train_generator = train_datagen.flow_from_directory( train_dir,
                                                         target_size=(150, 150),
                                                         batch_size=50, #每一批次產生20個樣本
                                                         class_mode='categorical')
    print('=' * 30)
    print(train_generator.class_indices)
    print('=' * 30)

    validation_generator = test_datagen.flow_from_directory( test_dir,
                                                             target_size=(150, 150),
                                                             batch_size=50, #每一批次產生20個樣本
                                                             class_mode='categorical', )


    # 使用批量生成器 訓練模型
    H = model.fit_generator( train_generator,
                             verbose=2,
                             steps_per_epoch=30, # 一共訓練 100 次
                             epochs=100, # 每次訓練 30 回合
                             validation_data=validation_generator,
                             validation_steps=50,
                             callbacks=[estop] )
    model.save(model_save_name)


    # 顯示 acc 學習結果
    accuracy = H.history['acc']
    val_accuracy = H.history['val_acc']
    plt.plot(range(len(accuracy)), accuracy, marker='.', label='accuracy(training data)')
    plt.plot(range(len(val_accuracy)), val_accuracy, marker='.', label='val_accuracy(evaluation data)')
    plt.legend(loc='best')
    plt.grid()
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.show()
    # 顯示 loss 學習結果
    loss = H.history['loss']
    val_loss = H.history['val_loss']
    plt.plot(range(len(loss)), loss, marker='.', label='loss(training data)')
    plt.plot(range(len(val_loss)), val_loss, marker='.', label='val_loss(evaluation data)')
    plt.legend(loc='best')
    plt.grid()
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.show()

    print('=' * 30)
    print(train_generator.class_indices)
    print('=' * 30)



def load_CNN_model(model_path,pic_dir_path,pic_list=[]):
    # labels = {'古蹟': 0, '廟宇': 1, '登山': 2, '遊樂園': 3}
    labels = {'古蹟': 0, '台北101': 1, '海岸': 2, '淡水魚人碼頭': 3, '瀑布': 4, '燈塔': 5, '登山': 6, '紅毛城': 7, '遊樂園': 8}
    labels = {str(b): a for a, b in labels.items()}
    print('=' * 30)
    print("訓練的分類：", labels)
    print('=' * 30)

    with graph.as_default():
        '''
        你的预测的逻辑代码
        '''
        # 載入模型
        print(model_path)
        model = load_model(model_path)

        #model.summary()
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

            #將圖片轉為待測數據
            img = image.load_img(pic_dir_path + "/" + each_pic,target_size=(150,150))
            img = image.img_to_array(img)
            # print(img.shape)

            '''test_1'''
            img = np.expand_dims(img, axis=0)
            img = img/255

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

    # 模式切換
    # mode = 'built_model'
    mode = 'load_model'

    if mode == 'built_model':

        print('start')
        # 建模型
        built_CNN_model(dir_path="E:/資策會-DB106/專題/CNN",model_save_name = "CnnModelTrainPlace_v0.3.h5")

    elif mode == 'load_model':

        # load_CNN_model(model_path="E:/資策會-DB106/Python/PycharmProjects/Spades/Spades_Team/deep_learning/CnnModelTrainPlace_v0.6.h5",
        #                pic_dir_path="E:/資策會-DB106/專題/CNN/使用者上傳")

        load_CNN_model(
            model_path="E:/資策會-DB106/Python/PycharmProjects/Spades/Spades_Team/deep_learning/CnnModelTrainPlace_v0.6.h5",
            pic_dir_path="E:/資策會-DB106/專題/CNN/try")

#=====================================================
# model :  CnnModelTrainPlace_v0.1.h5
# 正確率: 0.42424242424242425
#
# model :  CnnModelTrainPlace_v0.1.h5
# 正確率: 0.5

#=====================================================
# v0.1 的 filters 加倍
# model :  CnnModelTrainPlace_v0.2.h5
# 正確率: 0.36363636363636365
#
# model :  CnnModelTrainPlace_v0.2.h5
# 正確率: 0.4777777777777778

#=====================================================
# v0.1 加兩層卷積層
# model :  CnnModelTrainPlace_v0.3.h5
# 正確率: 0.42424242424242425
#
# model :  CnnModelTrainPlace_v0.3.h5
# 正確率: 0.5666666666666667

#=====================================================
# v0.1 加六層卷積層
# model :  CnnModelTrainPlace_v0.4.h5
# 正確率: 0.45454545454545453
#
# model :  CnnModelTrainPlace_v0.4.h5
# 正確率: 0.5777777777777777

#=====================================================
# v0.1 的 不EarlyStopping
# model :  CnnModelTrainPlace_v0.5.h5
# 正確率: 0.48484848484848486
#
# model :  CnnModelTrainPlace_v0.5.h5
# 正確率: 0.6222222222222222

#=====================================================
# v0.1 的 不EarlyStopping  訓練 230 回合
# model :  CnnModelTrainPlace_v0.6.h5
# 正確率: 0.5454545454545454
#
# model :  CnnModelTrainPlace_v0.6.h5
# 正確率: 0.6555555555555556

#=====================================================
# v0.1 的 不EarlyStopping  訓練 330 回合 加六層卷積層
# model :  CnnModelTrainPlace_v0.7.h5
# 正確率: 0.5454545454545454
#
# model :  CnnModelTrainPlace_v0.7.h5
# 正確率: 0.6444444444444445

#=====================================================
# v0.1 的 不EarlyStopping  訓練 330 回合 加六層卷積層 資料增強增加學習樣本
# model :  CnnModelTrainPlace_v0.8.h5
# 正確率: 0.5454545454545454
#
# model :  CnnModelTrainPlace_v0.8.h5
# 正確率: 0.6777777777777778

#=====================================================
# v0.1 的 不EarlyStopping  訓練 660 回合 加八層卷積層 資料增強增加學習樣本

if __name__ == '__main__':

    main()
    print('Complete!!!!!!!!!!')
