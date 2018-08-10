from flask import Flask, render_template, jsonify
from bs4 import BeautifulSoup
import lxml, requests
import re
import json
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:wldk77@localhost/welfare'
db = SQLAlchemy(app)

class Lecture(db.Model):
    lecture_name = db.Column(db.String(300), primary_key=True)
    lecture_comp = db.Column(db.String(300), unique=False)
    lecture_area = db.Column(db.String(300), unique=False)
    lecture_call = db.Column(db.String(300), unique=False)
    lecture_fee = db.Column(db.String(300), unique=False)
    lecture_pay = db.Column(db.String(300), unique=False)
    lecture_term = db.Column(db.String(300), unique=False)
    lecture_time = db.Column(db.String(300), unique=False)
    lecture_num = db.Column(db.String(300), unique=False)
    support_qua = db.Column(db.String(5000), unique=False)
    support_dcm = db.Column(db.String(5000), unique=False)
    support_intro = db.Column(db.String(10000), unique=False)
    support_content = db.Column(db.String(10000), unique=False)
    support_course = db.Column(db.String(10000), unique=False)
    support_cer = db.Column(db.String(3000), unique=False)
    support_teacher = db.Column(db.String(3000), unique=False)

    def __init__(self, lecture_name, lecture_comp, lecture_area, lecture_call, lecture_fee, lecture_pay, lecture_term, lecture_time, lecture_num,
                 support_qua, support_dcm, support_intro, support_content, support_course, support_cer, support_teacher):
        self.lecture_name = lecture_name
        self.lecture_comp = lecture_comp
        self.lecture_area = lecture_area
        self.lecture_call = lecture_call
        self.lecture_fee = lecture_fee
        self.lecture_pay = lecture_pay
        self.lecture_term = lecture_term
        self.lecture_time = lecture_time
        self.lecture_num = lecture_num
        self.support_qua = support_qua
        self.support_dcm = support_dcm
        self.support_intro = support_intro
        self.support_content = support_content
        self.support_course = support_course
        self.support_cer = support_cer
        self.support_teacher = support_teacher

    def __repr__(self):
        return '<Lecture %r>' % self.lecture_name

lecture = {
    'lecture_name': '',
    'lecture_comp': '',
    'lecture_area': '',
    'lecture_call': '',
    'lecture_fee': '',
    'lecture_pay': '',
    'lecture_term': '',
    'lecture_time': '',
    'lecture_num': ''
}

support = {
    'support_qua':'',
    'support_dcm':'',
    'support_intro':'',
    'support_content':'',
    'support_course':'',
    'support_cer':'',
    'support_teacher':''
}

lecture_result = []
lecture_result2 = []


@app.route('/')
def home():
    str = 'This is main'

    req = requests.get('http://www.gukbi.com/Course/?Category=1')
    soup = BeautifulSoup(req.content,'lxml')
    content_list = []
    join_uri = 'http://www.gukbi.com/Course/'


    find_list=[]
    find_list2=[]
    for name in soup.find_all('p', {'style': 'line-height:145%;'}):
        for lis,lis2 in zip(name.find_all('b'), name.find_all('a')):
            find_list.append(lis)
            find_list2.append(lis2)

    #cut
    find_list = find_list[:30]
    find_list2 = find_list2[:30]

    #find and compare contents
    for lis, lis2 in zip(find_list, find_list2):
        href = lis2['href']
        req_content = requests.get(join_uri + href)
        soup = BeautifulSoup(req_content.content, 'lxml')

        #게시물 타이틀 쪽
        list = soup.find_all('p', {'style': 'margin-right:5; margin-left:5;'})
        # 지원자격, 등록시구비서류, 과정소개, 교육내용, 수료 후 진로, 관련자격증, 강사소개 => support_dict
        list2 = soup.find_all('p', {'style': 'line-height:145%; margin-right:5; margin-left:5;'})

        lecture_content = []
        lecture_content2 = []

        for lis in list:
            lecture_content.append(lis.text)
        for lis2 in list2:
            lecture_content2.append(lis2.text)

        sub_string = "\r\n|\xa0"
        for num, k in zip(range(0, len(lecture_content)), lecture.keys()):
            lecture_content[num] = re.sub(sub_string, "", lecture_content[num])
            lecture_content[num] = " ".join(lecture_content[num].split())
            lecture[k] = lecture_content[num]
            lecture_result.append(lecture)

        for num, k in zip(range(0, len(lecture_content2)), support.keys()):
            lecture_content2[num] = " ".join(lecture_content2[num].split())
            support[k] = lecture_content2[num]
            lecture_result2.append(support)

        # lecture_db = Lecture(lecture['lecture_name'], lecture['lecture_comp'], lecture['lecture_area'],
        #                       lecture['lecture_call'], lecture['lecture_fee'], lecture['lecture_pay'],
        #              lecture['lecture_term'],lecture['lecture_time'],lecture['lecture_num'],
        #                       support['support_qua'],support['support_dcm'],support['support_intro'],support['support_content'],
        #          support['support_course'],support['support_cer'],support['support_teacher'])

        #db.session.add(lecture_db)
    #db.session.commit()


    return 'hello'

@app.route('/<areas>', methods=['GET'])
def area_db(areas):
    area_lecture = Lecture.query.filter(Lecture.lecture_area.contains(areas)).all()
    if area_lecture:
        list =[]
        for lectures in area_lecture:
            all_lect_dic = {
                'lecture_name': lectures.lecture_name,
                'lecture_comp': lectures.lecture_comp,
                'lecture_area': lectures.lecture_area,
                'lecture_call': lectures.lecture_call,
                'lecture_fee': lectures.lecture_fee,
                'lecture_pay': lectures.lecture_pay,
                'lecture_term': lectures.lecture_term,
                'lecture_time': lectures.lecture_time,
                'lecture_num': lectures.lecture_num,
                'support_qua': lectures.support_qua,
                'support_dcm': lectures.support_dcm,
                'support_intro': lectures.support_intro,
                'support_content': lectures.support_content,
                'support_course': lectures.support_course,
                'support_cer': lectures.support_cer,
                'support_teacher': lectures.support_teacher
            }
            list.append(all_lect_dic)
        return json.dumps(list, ensure_ascii=False)
    else:
        return ''

@app.route('/all', methods=['GET'])
def all_db():
    list = []
    for lectures in Lecture.query.all():
        all_lect_dic = {
            'lecture_name': lectures.lecture_name,
            'lecture_comp': lectures.lecture_comp,
            'lecture_area': lectures.lecture_area,
            'lecture_call': lectures.lecture_call,
            'lecture_fee': lectures.lecture_fee,
            'lecture_pay': lectures.lecture_pay,
            'lecture_term': lectures.lecture_term,
            'lecture_time': lectures.lecture_time,
            'lecture_num': lectures.lecture_num,
            'support_qua': lectures.support_qua,
            'support_dcm': lectures.support_dcm,
            'support_intro': lectures.support_intro,
            'support_content': lectures.support_content,
            'support_course': lectures.support_course,
            'support_cer': lectures.support_cer,
            'support_teacher': lectures.support_teacher
        }
        list.append(all_lect_dic)
    return json.dumps(list, ensure_ascii=False)

if __name__ == '__main__':
    app.run()
