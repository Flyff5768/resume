import os
import json
import time
import random
import requests
from pyquery import PyQuery as pq
import datetime
#import Spades_Team.database.db_mongodb_docker as db_mongodb_docker
import db_mongodb_docker




def main(each_region, each_target): #主程式  # 爬蟲 for Instagram
    global headers
    headers = {
        'user_test-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}


    # step 1 : 設定 search_tag
    search_tag = each_region + each_target


    global path_dir
    path_dir = '/rawdata'
    path_dir = path_dir +'/%s' % (search_tag)
    make_dir(path_dir)


    # step2  : 取得歷史 data 及 has_next_page,end_cursor

    for page in range(1,100):

        tag_url = 'https://www.pixnet.net/mainpage/api/tags/{0}/feeds?page={1}&per_page=20&filter=articles&sort=related&refer=https%3A%2F%2Fwww.pixnet.net%2F'
        url = tag_url.format(search_tag, page)
        print('url =', url)

        json = get_html(url)
        get_analysis(json,path_dir,each_region,each_target)

        time_sleep = random.randint(0, 2)
        print('chang_page 休息', time_sleep, '秒')
        time.sleep(time_sleep)



def get_html(url): # 訪問網頁
    try:
        response = requests.get(url, headers)
        response.encoding = 'utf-8'

        HTTP_Status_Code =[200,401,404,500]
        if response.status_code in HTTP_Status_Code:
            #print(response.text)
            return response.text
        else:
            print('請求網頁源代碼錯誤, 錯誤狀態碼：', response.status_code)
            print(url)
            raise
    except Exception as e:
        print(e)
        time_sleep = 60 + float(random.randint(1, 4000)) / 100
        print('Crawler 休息', time_sleep, '秒')
        time.sleep(time_sleep)
        return get_html(url)

def get_analysis(data,path_dir,each_region,each_target):


    js_data = json.loads(data, encoding='utf-8')
    article_list = js_data['data']['feeds']

    # 讀取已爬過的log , 開紀錄shortcode文字檔
    path_record_article = path_dir + '/_record_article.txt'
    record_article_set = set()
    if os.path.exists(path_record_article):
        with open(path_record_article, 'r', encoding='utf8') as f:
            for each_record in f:
                record_article_set.add(each_record.replace('\n', ''))
    print('record_article_set :', len(record_article_set))


    for each_article in article_list :

        shortcode = each_article['member_uniqid']

        if shortcode not in record_article_set :

            global each_article_url,posting_time
            each_article_url = each_article['link']
            posting_time = datetime.datetime.fromtimestamp(each_article['created_at'])
            posting_time = posting_time.strftime("%Y-%m-%d %H:%M:%S")
            print(article_list.index(each_article)+1,'/',len(article_list),each_article_url)

            html_article = get_html(each_article_url)


            get_data(html_article,each_region,each_target)

            record_article_set.add(shortcode)

            # 存文字檔

            with open(path_record_article, 'a', encoding='utf8') as f:
                f.write(shortcode + '\n')

            data_count = len(record_article_set)
            time_sleep = random.randint(0, 2)
            print('已收集 : ',data_count,',Crawler 休息', time_sleep, '秒')
            time.sleep(time_sleep)


def replace_illegal_characters(string):
    list =['*','|','\\',':','\"','<','>','?','/','.',' ','-','.','[',']','。','＠','～','、','》','【','@','】','，','(',')','．','｜']
    for c in list:
        string = string.replace(c, '')

    return string


def make_dir(path_dir):
    list = path_dir.split('/')
    path_str = list[0]

    for each in list[1:]:
        path_str += "/" + each

        if not os.path.exists(path_str):
            os.mkdir(path_str)


def get_data(html,each_region,each_target):
    try:
        doc = pq(html)

        try:
            #標題
            items = doc('h2[itemprop="headline"]').items()
            for item in items:
                title = item.text()
                #print(title)
        except Exception as e:
            print(e)
            title = "NA"
            print(title)

        try:
            content = ''
            # 內文
            items = doc('div[id="article-content-inner"] p').items()
            for item in items:
                content += item.text().replace('-','')

            # print('content =', content)

        except Exception as e:
            print(e)
            content = 'NA'
            print(content)

        comment = 'NA'
        # print(comment)




        # 同整存檔內容
        global each_article_url,posting_time
        if each_target == '景點':
            save_data_dict = {'文章網址': each_article_url,
                              '發文時間': posting_time,
                              '標題': title,
                              '景點名稱': 'NA',
                              '文章內容': content,
                              '留言': comment,
                              '地址': 'NA',
                              '縣市': each_region}
        elif each_target == '美食':
            save_data_dict = {'文章網址': each_article_url,
                              '發文時間': posting_time,
                              '標題': title,
                              '餐廳名稱': 'NA',
                              '美食名稱': 'NA',
                              '文章內容': content,
                              '留言': comment,
                              '地址': 'NA',
                              '縣市': each_region}

        save_data_js = json.dumps(save_data_dict,ensure_ascii=False)

        # 建個別資料夾
        title = replace_illegal_characters(title)
        # path_dir_each = path_dir + '/' + title
        # os.mkdir(path_dir_each)
        # 存文字檔
        with open(path_dir + '/' + title + '.txt', 'a', encoding='utf8') as f:
            f.write(save_data_js + '\n-----\n')

        ## (選配)邊爬邊存mongo
        # if each_target == '景點':
        #     db_mongodb_docker.connect_mongodb("spades", "place")
        # elif each_target == '美食':
        #     db_mongodb_docker.connect_mongodb("spades", "food")
        #
        # db_mongodb_docker.mongodb_insert(json.loads(save_data_js))

        # #存照片
        # items = doc('link[rel="image_src"]').items()
        # img_url_list = []
        # for item in items:
        #     img_url_list.append(item.attr('href'))
        # for img_url_each in img_url_list :
        #
        #     request.urlretrieve(img_url_each,path_dir_each +'/'+ title +'---%s' %img_url_list.index(img_url_each) +'.jpg')

    except Exception as e:
        print(e)
        # 存文字檔
        with open('Exception.txt', 'a', encoding='utf8') as f:
            f.write(str(e)+'\n')
        pass


if __name__ == '__main__':

    tag_list_region = ['台北', '新北', '基隆', '桃園', '新竹', '宜蘭']  # 手動更改
    tag_list_target = ['景點', '美食']  # 手動更改

    for each_target in tag_list_target:
        for each_region in tag_list_region:
            print('開始爬:', each_region + each_target)
            main(each_region, each_target)

    print('Complete!!!!!!!!!!')
