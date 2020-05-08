import os

from pyquery import PyQuery as pq
from Spades_Team.crawler.instagram.crawler_ig_mp_v2 import make_dir,get_html



def main(each_region,each_target): #主程式  # 爬蟲 for Instagram
    headers = {
        'user_test-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'cookie': 'mid=XfiFQwALAAGQwcyYLlxLO_xkGrFB; fbm_124024574287414=base_domain=.instagram.com; shbid=16651; shbts=1581487025.8519735; rur=FTW; fbsr_124024574287414=KwK4lUDoQxVxJt2sc439xDwCWiAcvQTcifJJzMhK3AM.eyJ1c2VyX2lkIjoiMTAwMDAwNzc2NDkwMzMwIiwiY29kZSI6IkFRQTM4bHJxWFg5Q3BtWUtwZlVTTlVZZ3czRHNoWXFtNzdoU0VWaFRTRXU2SkFET3E5NXhfSFhJb1JPeE90eURZeTJHWEkxUHV4ZnV4bjNWY2doUW9BVE03a0ViaktGVm5uQUhUMzlWMWx4WGtnZXlNNXBzS3ItT1BheWZpdmNWLUNzbEF2MnkzRFdMdGxRNktpYjFmd0diNmRNTUw1ckdteXRHTzJEWFJ6RmVQcTFEQnlPTU1iQjlVX0NPekFZWmx6UlRUX2FjaUoyZXBaN256cUxOZFJFRVpLdjlmMVcwSWo5UUxrMVpFcUxLbi1XMnp6ZDlJc1VIeDcwNDJBWmR3NGFnTEoxY0FyaXBZTWRtYTFyYktVN2lMaTg2Mk8xWW9CVWphekFDeHZrenlVTzdSaTRxZnpiZkhFamsycHltRWhMUllQbWdQYlNKZUJlUkVtajlIdlcxIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUJWa1pCbGV6bkh1ZU9UWWlHZ2lBZWJaQW9oRnlpRmxSUEhubE9PQ0dnazg1ZzE5YlFEd2hrQ0N4SGpUb0g2UXJjMkVaQnJoUU5zcXV5WkFaQlpDb0VueVRnWkJVbXlmclBpMUtkbVEyS0ppQU5vSzdrT1h4VXNzWkNLMDcyWWRrQm1aQ0hnRGd0d2FySGdvbm5kczJRcGd6RFFEc05Bc1Z1elJZejZ6V3ZJam0iLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTU4MTQ4NzIxNH0; csrftoken=osIi7PQWy7fhNmyzNZMhhdgPhfZMLPgh; ds_user_id=4515140991; sessionid=4515140991%3Aid94nJfktYQEol%3A18;'}



    global search_tag
    # 設定 search_tag
    search_tag = each_region + each_target
    tag_url = 'https://zh.wikipedia.org/wiki/{0}旅遊景點列表'.format(each_region)

    # 建存檔資料
    path_dir = 'E:\\資策會-DB106\\專題\\wiki\\place'
    print(tag_url)
    make_dir(path_dir)

    # 加入停用 詞
    # 無函式 只能變成串列 於程式中阻擋
    stopword_set = set()
    with open('C:/Users/Big data/PycharmProjects/PyETL2/Spades_Team/jieba/stopword.txt', encoding='utf-8') as file:
        for each_stopword in file.read().split('\n'):
            stopword_set.add(each_stopword)

    html = get_html(tag_url, headers)
    doc = pq(html)
    items = doc('a').items()

    place_set = set()

    for wiki_place in items:
        wiki_place = wiki_place.text()
        if len(wiki_place) > 1 and wiki_place not in stopword_set:
            print(wiki_place)
            place_set.add(wiki_place)

    save_str = ''
    for each_place_set in place_set:
        save_str += each_place_set +'\n'


    # 存文字檔
    with open(path_dir + '/' + search_tag + '_wiki.txt', 'w', encoding='utf8') as f:
        f.write(save_str )








if __name__ == '__main__':

    tag_list_region = ['台北市','新北市','基隆市', '桃園市', '新竹市','新竹縣','宜蘭縣']  # 手動更改

    tag_list_target = ['景點']  # 手動更改

    for each_target in tag_list_target:
        for each_region in tag_list_region:
            print('開始爬:',each_region+each_target)
            main(each_region,each_target)

    print('Complete!!!!!!!!!!')