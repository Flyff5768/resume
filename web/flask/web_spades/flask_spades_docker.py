# pip install flask
# pip3 install flask-bootstrap
# pip3 install flask-bootstrap4
# pip install flask-wtf Flask-SQLAlchemy

import time
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

# docker
import sys
sys.path.append('/code')
from transfer_learning_spades import load_transfer_model
from VGG16_spades import predict
from spades_recommend import place_recommend ,food_recommend
from route_plan import main as route_plan
from weather import weather
from db_mysql_docker import connect_mysql,mysql_select
from ELK import elasticsearch_spades

app = Flask(__name__) #建立 Flask 物件
# app.config['UPLOAD_FOLDER'] = upload_dir # user_test 上傳照片的存檔路徑
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

bootstrap = Bootstrap(app)   #建立 bootstrap 物件


@app.route('/')
def my_index_rebuild():
    return render_template('index.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/action_number.php',methods=['GET'])
def action_number():
    name = request.args.get('username')
    return render_template('load_pic.html',username = name)

@app.route('/recommend')
def my_index_new():
    return render_template('recommend.html')

@app.route('/hot_pot',methods=['GET','POST'])
def hot_pot():
    return render_template('hot_pot.html')

@app.route('/catogory',methods=['GET','POST'])
def catogory():
    return render_template('catogory.html')

@app.route('/keyword',methods=['GET','POST'])
def keyword():
    return render_template('keyword.html')

@app.route('/confirm',methods=['GET','POST'])
def confirm_new():
    return render_template('confirm_3.html')

@app.route('/aboutus',methods=['GET','POST'])
def aboutus():
    return render_template('aboutus.html')

@app.route('/upload',methods=['GET','POST'])
def action_load_pic():
    global filenames, upload_dir,place_filenames,food_filenames,userdate,usergo

    # docker
    # user_test 上傳照片的存檔路徑
    upload_dir = r'/code/flask/web_spades'

    print(request.method)
    if request.method == 'POST':
        userdate = request.form['userdate']
        usergo = request.form['usergo']
        print(userdate)
        print(usergo)
        uploaded_place_files = request.files.getlist("place")
        uploaded_food_files = request.files.getlist("food")
        filenames = []
        place_filenames = []
        food_filenames = []

        for file in uploaded_place_files:
            filename = file.filename
            file.save(upload_dir + "/static/" + filename)
            place_filenames.append(filename)
            filenames.append(filename)

        for file in uploaded_food_files:
            filename = file.filename
            file.save(upload_dir + "/static/" + filename)
            food_filenames.append(filename)
            filenames.append(filename)



    print('filenames',filenames)
    return render_template('confirm.html',filenames=filenames)


@app.route('/travel_plan',methods=['GET','POST'])
def travel_plan():
    time_start = time.time()

    # docker
    pred_place_dict = load_transfer_model(model_path=r"/code/mode_iv3LeafFinetune_15.h5",
                                          pic_dir_path=upload_dir + "/static", pic_list=place_filenames)
    pred_food_dict = predict(pic_dir_path=upload_dir + "/static", pic_list=food_filenames)
    print('pred_place_dict ', pred_place_dict)
    print('pred_food_dict ', pred_food_dict)

    '''
    照片分析完成 進 類別推薦 模型 程式撰寫區
    '''

    place_recommend_list = place_recommend(pred_place_dict)
    food_recommend_list = food_recommend(pred_food_dict)
    print('place_recommend_list ', place_recommend_list)
    print('food_recommend_list ', food_recommend_list)

    '''
    得到 地點 進 路線規劃 模型 程式撰寫區
    '''
    start_place_list = [usergo]
    final_list , travel_suggest = route_plan(place_recommend_list=start_place_list+place_recommend_list,food_recommend_list = food_recommend_list)
    basic_data = {'出發日期': userdate, '旅遊天數':'1天'}
    # final_list = [{'出發': " '台北車站'", '到達': " 'Papa Vito'", '距離': " '11.1'", '交通時間': Decimal('0.4'),
    #                '停留時間': Decimal('0.6'), '交通+停留時間': Decimal('1.0'), '累積時間': Decimal('1.0'),
    #                '離開時間': datetime.datetime(2020, 5, 15, 9, 0)},
    #               {'出發': " 'Papa Vito'", '到達': " '淡水港燈塔'", '距離': " '16.6", '交通時間': Decimal('0.7'),
    #                '停留時間': Decimal('0.0'), '交通+停留時間': Decimal('0.7'), '累積時間': Decimal('1.1'),
    #                '離開時間': datetime.datetime(2020, 5, 15, 9, 42)}]
    # travel_suggest = '行程有點少, 請考慮增加景點'

    print(final_list)
    print(travel_suggest)

    weather_dict = weather()
    print(weather_dict)

    cost_time = time.time() - time_start
    print(cost_time,'秒')

    # brief = {'date':'2020/5/22',
    #          'days':1
    #          }

    #return render_template('recommand.html', final_list=final_list, travel_suggest=travel_suggest,
    #                       weather_dict=weather_dict, start_place_list=start_place_list, basic_data=basic_data)
    return render_template('recommend.html', final_list=final_list, travel_suggest=travel_suggest,
                           weather_dict=weather_dict, start_place_list=start_place_list, basic_data=basic_data)


def select_sql(table,orderby):
    place_list = []
    connect_mysql()
    sql_str = 'SELECT * FROM {} ORDER BY {} DESC LIMIT 8'.format(table,orderby)
    tmp = mysql_select(sql_str)
    for each in tmp:
        place_list.append(each[0])

    return place_list

def elasticsearch_search(query_str):
    place_list = []
    place_dict = {}
    elasticsearch_spades.connect_elasticsearch()
    for one in elasticsearch_spades.elasticsearch_search(index='place_clean_v1', size=500, query_body={"query": {"match": {'文章內容': query_str}}}):
        # print(one['_source']['景點名稱'], 'score', one['_score'])
        if one['_source']['景點名稱'] not in place_dict:
            place_dict[one['_source']['景點名稱']] = 1
        else:
            place_dict[one['_source']['景點名稱']] += 1

    tmp_list = sorted(place_dict.items(), key=lambda d: d[1], reverse=True)
    for i in range(0, 8): place_list.append(tmp_list[i][0])

    return place_list

@app.route('/keyword2',methods=['GET','POST'])
def keyword2():
    if request.method == 'POST':
        keyword = request.form['userkeyword']
        print(keyword)

    return render_template('keyword.html',place_list=elasticsearch_search(keyword))


@app.route('/Parent_child',methods=['GET','POST'])
def Parent_child():
    return render_template('catogory.html',place_list=select_sql('Parent_child_score','score'))

@app.route('/Couple',methods=['GET','POST'])
def Couple():
    return render_template('catogory.html',place_list=select_sql('Couple_score','score'))

@app.route('/Old_and_young',methods=['GET','POST'])
def Old_and_young():
    return render_template('catogory.html',place_list=select_sql('Old_and_young_score','score'))

@app.route('/friend',methods=['GET','POST'])
def friend():
    return render_template('catogory.html',place_list=select_sql('friend_score','score'))


#======================================================================================


@app.route('/keelung_hot',methods=['GET','POST'])
def keelung_hot():
    return render_template('hot_pot.html',place_list=select_sql('keelung_hot','"count(attractions)"'))

@app.route('/taipei_hot',methods=['GET','POST'])
def taipei_hot():
    return render_template('hot_pot.html',place_list=select_sql('taipei_hot','"count(attractions)"'))

@app.route('/new_taipei_hot',methods=['GET','POST'])
def new_taipei_hot():
    return render_template('hot_pot.html',place_list=select_sql('new_taipei_hot','"count(attractions)"'))

@app.route('/taoyuan_hot',methods=['GET','POST'])
def taoyuan_hot():
    return render_template('hot_pot.html',place_list=select_sql('taoyuan_hot','"count(attractions)"'))

@app.route('/hsinchu_hot',methods=['GET','POST'])
def hsinchu_hot():
    return render_template('hot_pot.html',place_list=select_sql('hsinchu_hot','"count(attractions)"'))

@app.route('/yilan_hot',methods=['GET','POST'])
def yilan_hot():
    return render_template('hot_pot.html',place_list=select_sql('yilan_hot','"count(attractions)"'))





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)