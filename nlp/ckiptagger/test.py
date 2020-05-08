# pip install -U ckiptagger
# pip install tensorflow==1.13.1
from ckiptagger import WS , construct_dictionary

sentence_list = ["傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。"]

ws = WS('.\data')

word_s = ws(sentence_list,
            sentence_segmentation=True,
            segment_delimiter_set={'?', '？', '!', '！', '。', ',',
                                   '，', ';', ':', '、'})
print(word_s)


word_to_weight2 = {
    "今將": 1,
    "安樂": 1,
  }

dictionary2 = construct_dictionary(word_to_weight2)


word_s2 = ws(sentence_list,
            coerce_dictionary = dictionary2,
            sentence_segmentation=True,
            segment_delimiter_set={'?', '？', '!', '！', '。', ',',
                                   '，', ';', ':', '、'})

print(word_s2)












