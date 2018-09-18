from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup
import lxml, requests
import re
import json
import csv
import os
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#using postgres
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:wldk77@localhost/welfare'
#using mysql and localhost DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wldk777@/welfare'
#using Paas-Ta DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://7393b54eb5c4b604:2209231408e05cd0@133.186.153.136:3306/op_53f846df_6641_414c_8be6_bb986bd54383'
db = SQLAlchemy(app)


class Lecture(db.Model):
    lecture_name = db.Column(db.VARCHAR(150), primary_key=True)
    lecture_comp = db.Column(db.Text, unique=False)
    lecture_area = db.Column(db.Text, unique=False)
    lecture_call = db.Column(db.Text, unique=False)
    lecture_fee = db.Column(db.Text, unique=False)
    lecture_pay = db.Column(db.Text, unique=False)
    lecture_term = db.Column(db.Text, unique=False)
    lecture_time = db.Column(db.Text, unique=False)
    lecture_num = db.Column(db.Text, unique=False)
    support_qua = db.Column(db.Text, unique=False)
    support_dcm = db.Column(db.Text, unique=False)
    support_intro = db.Column(db.Text, unique=False)
    support_content = db.Column(db.Text, unique=False)
    support_course = db.Column(db.Text, unique=False)
    support_cer = db.Column(db.Text, unique=False)
    support_teacher = db.Column(db.Text, unique=False)
    employ= db.Column(db.VARCHAR(5), primary_key=True)


    def __init__(self, lecture_name, lecture_comp, lecture_area, lecture_call, lecture_fee, lecture_pay, lecture_term, lecture_time, lecture_num,
                 support_qua, support_dcm, support_intro, support_content, support_course, support_cer, support_teacher, employ):
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
        self.employ = employ
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
    'support_teacher':'',
    'employ':''
}

lecture_result = []
lecture_result2 = []
@app.route('/dbdb')
def dbdb():
    db.session.remove()
    db.drop_all()
    db.create_all()
    return ''


@app.route('/hrd_db')
def hrd_db():
    req_url = 'https://ps.korchamhrd.net/education/professionalSkillEduList.do?rootMenuId=110&menuId=113&mojip_cd=111001'
    req = requests.get(req_url)
    soup = BeautifulSoup(req.content, 'lxml')

    join_url = 'https://ps.korchamhrd.net/education/professionalSkillEduDetail.do?rootMenuId=110&menuId=113&gaebalwon_cd=01000&gwajeong_no='

    #전체페이지에서 목록
    code_list = []
    hrd_name_list = []
    for name in soup.find_all('td', {'left'}):
        page = name.find('a')['href']
        page_code = page[31:39]
        hrd_name = name.find('a').contents[0]
        code_list.append(page_code)
        hrd_name_list.append(hrd_name)

    all_list = []
    title_name_list = []
    content_list = []
    #개별페이지
    for code in code_list:
        req_content = requests.get(join_url + code)
        soup = BeautifulSoup(req_content.content, 'lxml')
        #content = soup.find_all('th', {'scope': 'row'})
        #개별페이지의 모든 속성[0] 교육기관 [1] 교육기간 ~~

        title = soup.find('div', {'class':'tit'})
        title_name = title.find('h2')
        title_name_list.append(title_name)

        sub_string = "\n"
        for c in soup.find_all('tr'):
            #restring[0], restring[1]으로 속성값 적용
            re_string = re.sub(sub_string, "", c.get_text())
            content_list.append(re_string)
        all_list.append(content_list)

    print(all_list[0])

    return 'hrd_db save'

@app.route('/')
def home():
    str = 'This is main'
    # db생성 함수
    #db.create_all()
    req_url_1 = 'http://www.gukbi.com/Course/?Category=1'
    req_url = 'http://www.gukbi.com/Search/?Query=%EB%B6%80%EC%82%B0'
    req = requests.get(req_url)
    soup = BeautifulSoup(req.content,'lxml')
    content_list = []
    join_uri = 'http://www.gukbi.com/Course/'

    #일반교육과정을 위한 크롤링
    href_list = []
    for name_n in soup.find_all('td', {'width': '345'}):
        for lis in name_n.find_all('a'):
            href_list.append(lis)

    for lis in href_list:
        href = lis['href']
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
            if ("실직자" in lecture['lecture_name']):
                result = re.sub("[\[].*?[\]]", "", lecture['lecture_name'])
                support['employ'] = "실직자"
                lecture['lecture_name'] = result.lstrip()
            elif ("재직자" in lecture['lecture_name'] or "일반" in lecture['lecture_name'] ):
                result = re.sub("[\[].*?[\]]", "", lecture['lecture_name'])
                support['employ'] = "재직자"
                lecture['lecture_name'] = result.lstrip()
            lecture_result.append(lecture)

        #
        # if("실직자" in lecture['lecture_name']):
        #     result = re.sub("[\[].*?[\]]", "", lecture['lecture_name'])
        #     lecture['lecture_name'] = result
        # elif (lecture['lecture_name'].find('재직자')):
        #     result = re.sub("[\[].*?[\]]", "", lecture['lecture_name'])
        #     lecture['lecture_name'] = result


        for num, k in zip(range(0, len(lecture_content2)), support.keys()):
            lecture_content2[num] = " ".join(lecture_content2[num].split())
            support[k] = lecture_content2[num]
            lecture_result2.append(support)

    #
    # ##top교육과정을 위한 크롤링
    # find_list=[]
    # find_list2=[]
    # for name in soup.find_all('p', {'style': 'line-height:145%;'}):
    #     for lis,lis2 in zip(name.find_all('b'), name.find_all('a')):
    #         find_list.append(lis)
    #         find_list2.append(lis2)
    #
    # #cut (국비지원top교육과정목록 , top아닌 교육과정과는 다름)
    # find_list = find_list[:2]
    # find_list2 = find_list2[:2]
    #
    # #find and compare contents
    # for lis, lis2 in zip(find_list, find_list2):
    #     href = lis2['href']
    #     req_content = requests.get(join_uri + href)
    #     soup = BeautifulSoup(req_content.content, 'lxml')
    #
    #     #게시물 타이틀 쪽
    #     list = soup.find_all('p', {'style': 'margin-right:5; margin-left:5;'})
    #     # 지원자격, 등록시구비서류, 과정소개, 교육내용, 수료 후 진로, 관련자격증, 강사소개 => support_dict
    #     list2 = soup.find_all('p', {'style': 'line-height:145%; margin-right:5; margin-left:5;'})
    #
    #     lecture_content = []
    #     lecture_content2 = []
    #
    #     for lis in list:
    #         lecture_content.append(lis.text)
    #     for lis2 in list2:
    #         lecture_content2.append(lis2.text)
    #
    #     sub_string = "\r\n|\xa0"
    #     for num, k in zip(range(0, len(lecture_content)), lecture.keys()):
    #         lecture_content[num] = re.sub(sub_string, "", lecture_content[num])
    #         lecture_content[num] = " ".join(lecture_content[num].split())
    #         lecture[k] = lecture_content[num]
    #         lecture_result.append(lecture)
    #
    #     for num, k in zip(range(0, len(lecture_content2)), support.keys()):
    #         lecture_content2[num] = " ".join(lecture_content2[num].split())
    #         support[k] = lecture_content2[num]
    #         lecture_result2.append(support)

        lecture_db = Lecture(lecture['lecture_name'], lecture['lecture_comp'], lecture['lecture_area'],
                                lecture['lecture_call'], lecture['lecture_fee'], lecture['lecture_pay'],
                       lecture['lecture_term'],lecture['lecture_time'],lecture['lecture_num'],
                                support['support_qua'],support['support_dcm'],support['support_intro'],support['support_content'],
                   support['support_course'],support['support_cer'],support['support_teacher'],support['employ'])

        db.session.add(lecture_db)
    db.session.commit()
    return 'hello'




#주소 url 형식: /search?lecture_name=sdhajskdhakjsdhsakjhsajkdhas
@app.route('/search', methods=['GET'])
def lecture_name_db():
    lecture_name = request.args.get('lecture_name')
    area_lecture = Lecture.query.filter(Lecture.lecture_name.contains(lecture_name)).all()
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
                'support_teacher': lectures.support_teacher,
                'employ': lectures.employ
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
            'support_teacher': lectures.support_teacher,
            'employ': lectures.employ
        }
        list.append(all_lect_dic)
    return json.dumps(list, ensure_ascii=False)


@app.route('/all_gukbi', methods=['GET'])
def all_pusan():
    area_lecture = Lecture.query.filter(Lecture.lecture_area.contains("부산")).all()
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


#
# if __name__ == '__main__':
#     app.run()




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
