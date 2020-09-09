from general import makestr,General_Option

#输入['www.baidu.com','www.google.com']的列表
#返回的是{'www.baidu.com':'百度是一家科技公司'}这种字典
def get_domain_description(domainlist,global_option):
    import time
    import redis
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By


    en_des_dic={}
    options = Options()
    options.binary_location = "D:\我的资料库\Documents\Downloads\Chrome 懒人版 v4.1.4\chrome.exe"
    #options.add_argument('headless')  # 设置option,不显示浏览器
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    browser = webdriver.Chrome(chrome_options=options, desired_capabilities=capa)
    wait = WebDriverWait(browser, 30)

    for domain in domainlist:
        global_option.option_dic['domain']=domain
        global_option.domain=domain
        #根据general_option对象,返回一些关键参数
        scrap_dic=global_option.Get_scrap_dic()
        #url = r'https://cn.bing.com/search?q=%2B' + domain + r'&ensearch=1'
        url=scrap_dic['url']

        # 新开一个窗口，通过执行js来新开一个窗口
        js = 'window.open("%s");' % (url)
        browser.execute_script(js)
        windows_handles = browser.window_handles
        browser.switch_to.window(windows_handles[1])
        #转到新的窗口进行操作
        try:
            #wait.until(EC.presence_of_element_located((By.CLASS_NAME, "b_footerItems_icp")))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, scrap_dic['stop_element'])))
            time.sleep(0.25)
        except:
            pass
        #elements_list = browser.find_elements_by_class_name("b_caption")
        elements_list = browser.find_elements_by_css_selector("[class='%s']"%(scrap_dic["scrap_element"]))
        text_list = []
        if elements_list == []:
            text_list.append('NoResult')
        else:
            elements_list = elements_list[0:2]
            for element in elements_list:
                text_list.append(element.text.replace('\n', ':'))
            browser.close()
            browser.switch_to.window(windows_handles[0])
            list_text=makestr(text_list)
            des_r=redis.Redis(host='127.0.0.1',db=1)#英文描述存到数据库1中去
            des_r.set(domain,list_text)
            en_des_dic[domain]=list_text
            print("英文描述："+list_text)
    browser.quit()
    #返回的是{'www.baidu.com':'百度是一家科技公司'}这种
    return en_des_dic





if __name__=='__main__':
    ret=get_domain_description(['www.yale.edu'])
    pass