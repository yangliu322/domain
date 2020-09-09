import redis


# 传入列表，返回前字符串列表合并为字符串
def makestr(wordlist):
    enstr = ''
    for word in wordlist:
        enstr += word
        enstr += "%"
    return enstr[:-1]


# 从redis中提取出不同key对应的值
def Get_str_from_redis(key, host='127.0.0.1', port='6379', db=0):
    red = redis.Redis(host=host, port=port, db=db)
    return red.get(key).decode('utf-8')


# 全局选项对象,在此对象中定义浏览器以及翻译接口url
class General_Option():
    option_dic={}
    def __init__(self):
        opr=redis.Redis(host='127.0.0.1',db=5)
        keys=opr.keys()
        self.option_dic={}
        for key in keys:
            value=opr.get(key)
            self.option_dic[key.decode('utf-8')]=value.decode('utf-8')
        #没域名的是翻译时调用，有域名是爬取时调用
        if 'domain' in self.option_dic.keys():
            self.domain = self.option_dic['domain']
        #下面是一些必选项，在如果在db4中有相应的键值对，初始化会直接读取
        #如果不存在的话会使用默认接口进行解析
        if "scrap_api" in self.option_dic.keys():
            self.scrap_api = self.option_dic['scrap_api']
        else:
            self.scrap_api="bing"
            opr.set("scrap_api","bing")
        if "translate_api" in self.option_dic.keys():
            self.translate_api = self.option_dic['translate_api']
        else:
            self.translate_api="baidu"
            opr.set("translate_api","baidu")
        if "label_api" in self.option_dic.keys():
            self.label_api=self.option_dic['label_api']
        else:
            self.label_api='baidu'
            opr.set('label_api',"baidu")
    # 返回的是一系列参数的字典，包括爬取的url，以及搜索元素的class名等
    def Get_scrap_dic(self):
        retdic = {}
        if self.scrap_api == 'bing':
            retdic['url'] = r'https://cn.bing.com/search?q=%2B' + self.domain + r'&ensearch=1'
            retdic['stop_element'] = 'b_footerItems_icp'  # 程序停止等待加载的元素类型
            retdic['scrap_element'] = 'b_caption'  # 程序爬取的元素类型

            return retdic

        if self.scrap_api == 'baidu':
            retdic['url']=r'https://www.baidu.com/s?&wd=inurl%3A'+self.domain
            retdic['stop_element']='pc'
            retdic['scrap_element']='c-abstract c-abstract-en'

            return retdic
        # 要添加API接口的话在这里加if-else语句即可，返回字典提供三个关键元素类型即可

        else:
            print('传入选项错误，请检查API选项调用设置')
            exit(1)



if __name__ == '__main__':
    print(Get_str_from_redis(key='https://www.csdn.net/', db=1))
