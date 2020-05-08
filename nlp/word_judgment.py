


'''保留中文 數字 大寫英文 小寫英文'''
def word_judgment(txt_target):
    filter_str = ''
    for each_word in txt_target:

        if (each_word >= u'\u4e00' and each_word <= u'\u9fa5') or (
                each_word >= u'\u0030' and each_word <= u'\u0039') or (
                each_word >= u'\u0041' and each_word <= u'\u005a') or (
                each_word >= u'\u0061' and each_word <= u'\u007a') or (each_word == '#'):

            filter_str += each_word
    return filter_str
'''保留中文'''
def word_judgment_Chinese(txt_target):
    filter_str = ''
    for each_word in txt_target:
        if (each_word >= u'\u4e00' and each_word <= u'\u9fa5') :

            filter_str += each_word
    return filter_str

'''數字 '''
def word_judgment_number(txt_target):
    filter_str = ''
    for each_word in txt_target:
        if (each_word >= u'\u0030' and each_word <= u'\u0039') :

            filter_str += each_word
    return filter_str

'''大寫英文'''
def word_judgment_Capital_English(txt_target):
    filter_str = ''
    for each_word in txt_target:
        if (each_word >= u'\u0041' and each_word <= u'\u005a') :

            filter_str += each_word
    return filter_str

'''小寫英文'''
def word_judgment_Lower_case_english(txt_target):
    filter_str = ''
    for each_word in txt_target:
        if (each_word >= u'\u0061' and each_word <= u'\u007a') :

            filter_str += each_word
    return filter_str

def main():
    txt = '我是中文 IAM am english @@@@0123456789 #'
    print(word_judgment(txt))
    print(word_judgment_Chinese(txt))
    print(word_judgment_number(txt))
    print(word_judgment_Capital_English(txt))
    print(word_judgment_Lower_case_english(txt))







if __name__ == '__main__':

    main()
