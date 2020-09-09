# -*- coding: utf-8 -*-
#from translator import read_csv
import re
from general import makestr,General_Option
from aip.nlp import AipNlp
import time
import redis
class label_response():
    def __init__(self,response):
        l=[]
        for dic in response['item']['lv1_tag_list']:
            l.append(dic['tag'])
        lv1_labellist = l

        l=[]
        for dic in response['item']['lv2_tag_list']:
            l.append(dic['tag'])
        lv2_labellist = l
        self.lable_dic={}
        self.lable_dic['lv1']=lv1_labellist
        self.lable_dic['lv2']=lv2_labellist

    def get_lable_dic(self):
        return self.lable_dic

def baidu_chdes_to_label(domain_chdes_dic):
    # 这个是百度开放平台的应用号以及密钥，如果用完次数可申请新的号
    # 换成新的参数继续使用
    APP_ID = '21968853'
    API_KEY = 'rdYDK2no7czNhfpDHh2qn345'
    SECRET_KEY = 'WAwfYzmfzmRLwUHcc0bGqpeUSg8rjPzZ'

    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    for domain in domain_chdes_dic.keys():  # 针对redis 数据库0中有很多请求的域名的时候进行多个域名的查询
        f = 1
        times = 1
        chdes = domain_chdes_dic[domain]
        chstr = makestr(re.findall(r'[\u4e00-\u9fa5，。？！；、]+', chdes))
        title = domain
        if title == '' or chstr == "":
            print('分类请求为空值，请检查输入')
            return 1
        content = chstr
        while (f):
            try:
                response = client.topic(title, content)
            except:
                print(domain + " 分类请求错误，准备重试")
                continue
            try:
                Response = label_response(response)
                redi = redis.Redis(host='127.0.0.1', db=3)
                redi.set(domain, str(Response.get_lable_dic()))
                print("domain: " + domain + " tags:" + str(Response.get_lable_dic()))
                f = 0
                # 成功之后就靠f=0退出循环，进行下一个域名的查询
            except:
                times += 1
                if times > 20:
                    print("重试次数过多，请检查输入！")
                    return 1
                print(domain + " 分类请求超时，准备重试第%d次" % (times))


def chdes_to_label(domain_chdes_dic,global_option):
    #要加文章分类的api的话在这里加
    if global_option.label_api=="baidu":
        baidu_chdes_to_label(domain_chdes_dic)
    if global_option.label_api=='demo':
        pass

if __name__=="__main__":
    domain_chdes_dic={'www.baidu.com':'百度是一家做搜索引擎的公司，有人工智能，输入法，浏览器等业务'}
    global_option=General_Option()
    chdes_to_label(domain_chdes_dic,General_Option)
