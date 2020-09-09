# coding=utf-8
import http.client
import hashlib
from urllib import parse
import random
from general import General_Option


def dic_ch(domain_des_dic,api_selected):
    import redis
    chdes_r = redis.Redis(host='127.0.0.1', db=2)

    domain_ch_des_dic = {}
    for domain in domain_des_dic.keys():
        if api_selected=='baidu':
            ch_des = baidu_get_translate(domain_des_dic[domain])
        if api_selected=='tencent':
            ch_des=tencent_get_translate(domain_des_dic[domain])
        #添加翻译api在这加就行，提供一个输入英文输出中文的接口函数，加在后面就行，
        #如： ch_des=tencent_get_translate(domain_des_dic[domain])
        domain_ch_des_dic[domain] = ch_des
        chdes_r.set(domain, ch_des)
        print(domain + '翻译结果： ' + ch_des)
    return domain_ch_des_dic


# 百度翻译API，传入外文字符，返回中文翻译结果
def baidu_get_translate(enstr):
    appid = '20200730000529687'
    secretKey = 'pzC0c6FMk0wdsBD7uVKN'
    # appid = '20200731000530224'
    # secretKey = '6oCtSo2Ho1gXTx5pafwE'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = enstr
    fromLang = 'auto'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode(encoding='utf-8'))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    # file = open('translate_result.txt', 'w')
    try:
        chstr = ''
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        restr = response.read().decode('utf-8')
        restr = eval(restr)
        for line in restr['trans_result']:
            # file.write(line['dst'] + '\n')
            chstr += line['dst']

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
        return chstr

# 腾讯翻译API，输入英文字符，返回中文
def tencent_get_translate(enstr):
    from tencentcloud.common import credential
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.tmt.v20180321 import tmt_client, models

    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey
        cred = credential.Credential("AKIDVpthFYiS3Pdbqx8RpztUs53kCOhnrFZd", "NWQBp9CqDLFxOYXExqlY5PUNCn4C7iyc")
        # 实例化要请求产品(以cvm为例)的client对象
        client = tmt_client.TmtClient(cred, "ap-guangzhou")
        # 实例化一个请求对象
        req = models.TextTranslateRequest()
        req.SourceText = enstr
        req.Source = "auto"
        req.Target = "zh"
        req.ProjectId = 0

        # 通过client对象调用想要访问的接口，需要传入请求对象
        resp = client.TextTranslate(req)
        # 输出json格式的字符串回包
        return resp.TargetText

    except TencentCloudSDKException as err:
        print(err)


def get_domain_chdescription(domain_des_dic, global_option):
        return dic_ch(domain_des_dic,global_option.translate_api)


if __name__ == "__main__":
    a = input("翻译文本")
    print(baidu_get_translate(a))
