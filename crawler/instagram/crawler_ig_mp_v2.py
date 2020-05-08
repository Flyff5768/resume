import os
import json
import time
import random
import datetime
import multiprocessing as mp
import Spades_Team.line.line_notify_message as line_notify
# pip
import requests
from pyquery import PyQuery as pq


def main(each_region, each_target):  # 主程式  # 爬蟲 for Instagram
    headers = {
        'user_test-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'cookie': 'mid=XfiFQwALAAGQwcyYLlxLO_xkGrFB; fbm_124024574287414=base_domain=.instagram.com; shbid=16651; shbts=1581487025.8519735; rur=FTW; fbsr_124024574287414=KwK4lUDoQxVxJt2sc439xDwCWiAcvQTcifJJzMhK3AM.eyJ1c2VyX2lkIjoiMTAwMDAwNzc2NDkwMzMwIiwiY29kZSI6IkFRQTM4bHJxWFg5Q3BtWUtwZlVTTlVZZ3czRHNoWXFtNzdoU0VWaFRTRXU2SkFET3E5NXhfSFhJb1JPeE90eURZeTJHWEkxUHV4ZnV4bjNWY2doUW9BVE03a0ViaktGVm5uQUhUMzlWMWx4WGtnZXlNNXBzS3ItT1BheWZpdmNWLUNzbEF2MnkzRFdMdGxRNktpYjFmd0diNmRNTUw1ckdteXRHTzJEWFJ6RmVQcTFEQnlPTU1iQjlVX0NPekFZWmx6UlRUX2FjaUoyZXBaN256cUxOZFJFRVpLdjlmMVcwSWo5UUxrMVpFcUxLbi1XMnp6ZDlJc1VIeDcwNDJBWmR3NGFnTEoxY0FyaXBZTWRtYTFyYktVN2lMaTg2Mk8xWW9CVWphekFDeHZrenlVTzdSaTRxZnpiZkhFamsycHltRWhMUllQbWdQYlNKZUJlUkVtajlIdlcxIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUJWa1pCbGV6bkh1ZU9UWWlHZ2lBZWJaQW9oRnlpRmxSUEhubE9PQ0dnazg1ZzE5YlFEd2hrQ0N4SGpUb0g2UXJjMkVaQnJoUU5zcXV5WkFaQlpDb0VueVRnWkJVbXlmclBpMUtkbVEyS0ppQU5vSzdrT1h4VXNzWkNLMDcyWWRrQm1aQ0hnRGd0d2FySGdvbm5kczJRcGd6RFFEc05Bc1Z1elJZejZ6V3ZJam0iLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTU4MTQ4NzIxNH0; csrftoken=osIi7PQWy7fhNmyzNZMhhdgPhfZMLPgh; ds_user_id=4515140991; sessionid=4515140991%3Aid94nJfktYQEol%3A18;'}

    end_cursor = ''
    has_next_page = True

    global search_tag
    # 設定 search_tag
    search_tag = each_region + each_target
    tag_url = 'https://www.instagram.com/explore/tags/{0}/'.format(search_tag)

    # 建存檔資料
    path_dir = 'E:\\資策會-DB106\\專題\\Instagram\\All\\{0}'.format(search_tag)
    make_dir(path_dir)

    # 讀取已爬過的log , 開紀錄shortcode文字檔
    path_record_article = path_dir + '\\_record_article.txt'
    record_article_set = set()
    if os.path.exists(path_record_article):
        with open(path_record_article, 'r', encoding='utf8') as f:
            for each_record in f:
                record_article_set.add(each_record.replace('\n', ''))
    print('record_article_set :', len(record_article_set))

    path_record_page = path_dir + '\\_record_page.txt'
    record_article_page = ''
    if os.path.exists(path_record_page):
        with open(path_record_page, 'r', encoding='utf8') as f:
            record_article_page = f.read()
    print('record_article_page :', len(record_article_page))

    # multiprocessing
    # crawler任務佇列
    task_queue_crawler = mp.JoinableQueue()
    # record_article任務佇列
    task_queue_record_article = mp.JoinableQueue()
    # 建立多執行緒
    start_multiprocessing(task_queue_crawler=task_queue_crawler,
                          task_queue_record_article=task_queue_record_article,
                          path_dir=path_dir,
                          path_record_article=path_record_article,
                          headers=headers,
                          each_region=each_region,
                          each_target=each_target)

    # step 3 : 取得search_tag首頁data 及 has_next_page,end_cursor
    if end_cursor == '':
        # 訪問Instagram 取得 html
        html = get_html(tag_url, headers)
        has_next_page, end_cursor, record_list = get_analysis(html, 'html')
        record_article_set = put_task_queue_crawler(task_queue_crawler, record_list, record_article_set)

    # step  : 取得歷史 data 及 has_next_page,end_cursor
    while has_next_page:
        url = 'https://www.instagram.com/graphql/query/?query_hash=bd33792e9f52a56ae8fa0985521d141d&variables=%7B%22tag_name%22%3A%22{0}%22%2C%22first%22%3A50%2C%22after%22%3A%22{1}%22%7D'
        url = url.format(search_tag, end_cursor)
        print('next url =', url)

        json = get_html(url, headers)

        try:
            has_next_page, end_cursor, record_list = get_analysis(json, 'json')
            record_article_set = put_task_queue_crawler(task_queue_crawler, record_list, record_article_set)
        except Exception as e:
            print('Exception =', e)
            print(json)

        # print('start_multiprocessing')
        task_queue_crawler.join()  # 確定任務佇列 處理完主程式才離開(主程式結束 任務佇列會繼續
        task_queue_record_article.join()
        # print('exit_multiprocessing')

        data_count = len(record_article_set)
        print('已收集 : ', data_count)
        time_sleep = random.randint(1, 5)
        print('chang_page 休息', time_sleep, '秒')
        time.sleep(time_sleep)

        # while task_queue_crawler.qsize() > 300 :
        #     time.sleep(300)

    # 確認爬完 在換下一個地方搜尋
    # task_queue_crawler.join()  # 確定任務佇列 處理完主程式才離開(主程式結束 任務佇列會繼續
    # task_queue_record_article.join()


def get_html(url, headers):  # 訪問網頁
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        HTTP_Status_Code = [200, 401, 404, 429]
        if response.status_code in HTTP_Status_Code:
            # print(response.status_code)
            # print(response.text)
            return response.text
        else:
            print('請求網頁源代碼錯誤, 錯誤狀態碼：', response.status_code)
            print(url)
            raise
    except Exception as e:
        print('Exception =', e)
        time_sleep = 60 + float(random.randint(1, 4000)) / 100
        print('Crawler 休息', time_sleep, '秒', '---url:', url)
        time.sleep(time_sleep)
        return get_html(url, headers)


def put_task_queue_crawler(task_queue_crawler, record_list, record_article_set):
    for each_record in record_list:
        if each_record not in record_article_set:
            task = [record_list.index(each_record) + 1, len(record_list), each_record]
            task_queue_crawler.put(task)  # 放進_任務佇列
            record_article_set.add(each_record)

            # line 通知 進度
            global search_tag
            data_count = len(record_article_set)
            if data_count % 20000 == 0: line_notify.lineNotifyMessage(msg=str(search_tag) + ' 已收集: ' + str(data_count))

    return record_article_set


def get_analysis(data, data_format):
    if data_format == 'html':
        doc = pq(data)
        article_count = doc('meta[name="description"]')
        print(article_count.attr('content'))
        items = doc('script[type="text/javascript"]').items()
        for item in items:
            if item.text().strip().startswith('window._sharedData'):
                js_data = json.loads(item.text()[21:-1], encoding='utf-8')
                article_list = js_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media'][
                    'edges']
                global end_cursor, has_next_page
                has_next_page = bool(
                    js_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info'][
                        'has_next_page'])
                end_cursor = \
                js_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info'][
                    'end_cursor']

    elif data_format == 'json':

        js_data = json.loads(data, encoding='utf-8')
        article_list = js_data['data']['hashtag']['edge_hashtag_to_media']['edges']
        has_next_page = bool(js_data['data']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page'])
        end_cursor = js_data['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']

    print('next_has_next_page =', has_next_page)
    print('next_end_cursor =', end_cursor)

    shortcode_list = [each_article['node']['shortcode'] for each_article in article_list]

    return has_next_page, end_cursor, shortcode_list


def start_multiprocessing(task_queue_crawler, task_queue_record_article, path_dir, path_record_article, headers,
                          each_region, each_target):
    for i in range(0, 3):
        # 爬蟲工作程序
        worker = mp.Process(target=crawler_multiprocessing, args=(
        i, task_queue_crawler, path_dir, task_queue_record_article, headers, each_region, each_target))
        worker.daemon = True
        worker.start()

    # 存 record_article 工作程序
    worker_record_articl = mp.Process(target=record_article_multiprocessing,
                                      args=(task_queue_record_article, path_record_article))
    worker_record_articl.daemon = True
    worker_record_articl.start()


def crawler_multiprocessing(worker_id, task_queue_crawler, path_dir, task_queue_record_article, headers, each_region,
                            each_target):
    while True:

        task_list_get = task_queue_crawler.get()
        print('id =', worker_id, ',stard_task-----', task_list_get[0], '/', task_list_get[1], '/',
              task_queue_crawler.qsize())
        shortcode = task_list_get[2]

        global each_article_url
        each_article_url = 'https://www.instagram.com/p/' + shortcode + '/'

        html_article = get_html(each_article_url, headers)
        post_time = get_data(html_article, path_dir, each_region, each_target)

        if post_time == None:
            line_notify.lineNotifyMessage(
                msg='id =' + str(worker_id) + '\n' + str(each_article_url) + '\npost_time = ' + str(post_time))
            break
        else:
            task_queue_record_article.put(shortcode)  # 放進_任務佇列

            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            time_sleep = random.randint(1, 3)
            print('id =', worker_id, ',done_task------', task_list_get[0], '/', task_list_get[1], '/',
                  task_queue_crawler.qsize(), ',休息', time_sleep, '秒', now_time, each_article_url, '發文時間:', post_time)
            time.sleep(time_sleep)
            task_queue_crawler.task_done()


def record_article_multiprocessing(task_queue_record_article, path_record_article):
    while True:
        record_article = task_queue_record_article.get()
        # 存文字檔
        with open(path_record_article, 'a', encoding='utf8') as f:
            f.write(record_article + '\n')

        task_queue_record_article.task_done()


def replace_illegal_characters(string):
    list = ['*', '|', '\\', ':', '\"', '<', '>', '?', '/', '.', ' ', '-', '.', '[', ']', '。', '＠', '～', '、', '》', '【',
            '@', '】', '，', '(', ')', '．', '｜']
    for c in list:
        string = string.replace(c, '')

    return string


def make_dir(path_dir):
    # 將路徑切割 一層一層 建資料夾
    list = path_dir.split('\\')
    path_str = list[0]
    for each in list[1:]:
        path_str += "\\" + each
        if not os.path.exists(path_str):
            os.mkdir(path_str)


def get_data(html, path_dir, each_region, each_target):
    try:
        doc = pq(html)
        items = doc('script[type="text/javascript"]').items()
        for item in items:
            if item.text().strip().startswith('window.__additionalDataLoaded'):
                try:
                    js_data = json.loads(item.text()[48:-2], encoding='utf-8')
                    print(item.text()[48:-2])
                except:
                    break
                try:
                    # 標題
                    title = js_data["graphql"]["shortcode_media"]["location"]['name']
                    # print(title)
                except:
                    title = "NA"
                    print('title:', title)

                try:
                    # 內文
                    content = js_data["graphql"]["shortcode_media"]["edge_media_to_caption"]['edges'][0]['node'][
                        'text'].replace('-', '')
                    # print(content)
                except:
                    content = 'NA'
                    print('content:', content)

                try:
                    # 留言
                    comment_times = len(js_data["graphql"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"])
                    comment_list = js_data["graphql"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"]
                    comment = ''

                    for each_comment in comment_list:
                        comment += each_comment["node"]["text"]

                        comment_son_list = each_comment["node"]["edge_threaded_comments"]["edges"]
                        for each_comment_son in comment_son_list:
                            each_comment_son_clean = each_comment_son["node"]["text"].replace('\n', '')
                            comment += '\n    ' + each_comment_son_clean + '\n'
                except:
                    comment = 'NA'
                    print('comment:', comment)

                try:
                    # 發言時間 Unix timestamp
                    unix_timestamp = js_data["graphql"]["shortcode_media"]["taken_at_timestamp"]
                    posting_time = datetime.datetime.fromtimestamp(unix_timestamp)
                    posting_time = posting_time.strftime("%Y-%m-%d %H:%M:%S")
                    # print(posting_time)
                    # print(type(posting_time))
                except:
                    posting_time = 'NA'
                    print('posting_time:', comment)

                if each_target == '景點':
                    save_data_dict = {'文章網址': each_article_url,
                                      '發文時間': posting_time,
                                      '標題': title,
                                      '景點名稱': title,
                                      '文章內容': content,
                                      '留言': comment,
                                      '地址': 'NA',
                                      '縣市': each_region}
                elif each_target == '美食':
                    save_data_dict = {'文章網址': each_article_url,
                                      '發文時間': posting_time,
                                      '標題': title,
                                      '餐廳名稱': title,
                                      '美食名稱': 'NA',
                                      '文章內容': content,
                                      '留言': comment,
                                      '地址': 'NA',
                                      '縣市': each_region}

                save_data_js = json.dumps(save_data_dict, ensure_ascii=False)

                # save_data_js = json.loads(save_data_js, encoding='utf-8')
                # print(save_data_js['文章網址'])
                # print(save_data_js['發文時間'])
                # print(save_data_js['標題'])
                # print(save_data_js['景點名稱'])
                # print(save_data_js['文章內容'])
                # print(save_data_js['留言'])
                # print(save_data_js['地址'])
                # print(save_data_js['縣市'])

                # 建個別資料夾
                title = replace_illegal_characters(title)
                # path_dir_each = path_dir + '/' + title
                # os.mkdir(path_dir_each)
                # 存文字檔
                with open(path_dir + '/' + title + '.txt', 'a', encoding='utf8') as f:
                    f.write(save_data_js + '\n-----\n')

                # #存照片
                # try :
                #     img_url_list = js_data["graphql"]["shortcode_media"]['edge_sidecar_to_children']['edges']
                #     for img_url_each in img_url_list :
                #         img_url = img_url_each['node']['display_url']
                #         #print(img_url_list.index(img_url_each))
                #         request.urlretrieve(img_url,path_dir_each +'/'+ title +'---%s' %img_url_list.index(img_url_each) +'.jpg')
                # except :
                #      collect_Exception(e)
                #     img_url = js_data["graphql"]["shortcode_media"]['display_url']
                #     request.urlretrieve(img_url,path_dir_each + '/' + title + '.jpg')

        return posting_time
    except Exception as e:
        print(e)


# def collect_Exception(e,url=''):
#     path = './{0}_Exception.txt'.format(os.path.basename(__file__).replace('.py', ''))
#     time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     save_Exception_dict = {"time":time,"Exception":str(e),"url":url}
#     js_data_Exception = json.dumps(save_Exception_dict)
#     # 存文字檔
#     with open(path, 'a', encoding='utf8') as f:
#         f.write( js_data_Exception + '\n')


if __name__ == '__main__':

    tag_list_region = ['台北', '新北', '基隆', '桃園', '新竹', '宜蘭']  # 手動更改
    # tag_list_region = ['桃園', '新竹','宜蘭']  # 手動更改
    tag_list_target = ['景點', '美食']  # 手動更改

    for each_target in tag_list_target:
        for each_region in tag_list_region:
            print('開始爬:', each_region + each_target)
            line_notify.lineNotifyMessage(msg='開始爬:{0}{1}'.format(each_region, each_target))
            main(each_region, each_target)

    print('Complete!!!!!!!!!!')


