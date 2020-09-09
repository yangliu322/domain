import redis

#输入英文，输出中文的API
from translate_API import baidu_get_translate,tencent_get_translate,get_domain_chdescription
from scrap_API import get_domain_description
from label_API import chdes_to_label
from general import General_Option
#对于拿下来的域名进行处理
def domain_dealing(domainlist):
    global_option=General_Option()

    #首先是爬取域名相关信息(英文)，domain_des_dic={'www.baidu.com':'this is a company'}
    domain_des_dic=get_domain_description(domainlist,global_option)

    #然后调用API进行翻译保存,domain_chdes_dic={'www.baidu.com':'这是一家公司'}
    #domain_chdes_dic=baidu_dic_ch(domain_des_dic)
    #有百度的也有腾讯的翻译接口
    domain_chdes_dic = get_domain_chdescription(domain_des_dic,global_option)

    #然后根据域名的相关信息打标签,暂时没留接口了
    chdes_to_label(domain_chdes_dic,global_option)

    print('完成标签任务，标记标签的域名有'+str(domainlist))


#主函数，不断访问redis数据，一旦发现有域名数据，就提取出来进行处理
def Run(ip):
    r = redis.Redis(host=ip, port=6379, decode_responses=True)
    #r.set(name='csdn', value='www.csdn.net')
    while (True):
        if len(r.keys()) != 0:
            l = r.keys()
            domainlist=[]
            for key in l:
                domain=r.get(key)
                domainlist.append(domain)
                # domain_dealing(domain)
                print(domain)
                r.delete(key)
            domain_dealing(domainlist)


if __name__ =='__main__':
    ip='127.0.0.1'
    #scrap_api暂时只有必应，translate_api有tencent，baidu
    #要添加scrap_api的话去general.py中加
    #要添加translate_api的话去translate_API.py中加
    #option = {'scrap_api': 'bing', 'translate_api': 'tencent'}
    Run(ip)
