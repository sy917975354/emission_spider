import os
import pandas as pd
import execjs
import requests
import re
from tqdm import tqdm

os.chdir(r"D:\Python\Data_analysis\爬虫\生活垃圾发电厂焚烧数据爬虫")


def getParams():
    dic = {}
    with open(r'jsCode.js', encoding='UTF-8', mode='r') as f:
        JsData = f.read()
    ctx = execjs.compile(JsData) #执行js文件
    dic['tc'] = ctx.eval('a')
    ctmy = ctx.eval('ctmy')
    dic['ts'] = execjs.eval('(new Date).valueOf()')
    dic["sgn"] = ctx.call('pscc',ctmy+str(dic['ts'])+str(dic['tc']))
    return dic
def setParams():
    dic = getParams()
    dic['pscode'] = '187BB3F9C98925BFF1CAC32EC6D2CD5C'
    dic['outputcode'] = ''
    dic['day'] = ""
    dic['SystemType'] = 'C16A882D480E678F' #可能跟系统的版本或者浏览器版本有关。不随企业变化
    return dic


header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://ljgk.envsc.cn/monitordata.html',
        'Host': 'ljgk.envsc.cn',
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive'
}
def DataParse(txt):
    pat = re.compile('"ps_code":"(.*?)",')
    ps_code = pat.findall(response.text)
    pat = re.compile('"mp_code":"(.*?)",')
    mp_code = pat.findall(response.text)
    df_copy = pd.DataFrame({'ps_code':ps_code,"mp_code":mp_code})
    return df_copy
if __name__ == '__main__':
    url = 'https://ljgk.envsc.cn/OutInterface/GetBurnList.ashx'
    df = pd.read_csv('ps_code.csv')
    # df = df.loc[0:3,:]
    list = df['pscode'].to_list()
    df_all = pd.DataFrame()
    try:
        for i in tqdm(range(len(list))):
            li = list[i]
            params = setParams()
            params['pscode'] = li
            response = requests.get(url, headers=header, params=params)
            df_all = df_all.append(DataParse(response.text), ignore_index=True)
        df_all.to_csv('example.csv')
    except :
        df_all.to_csv('example.csv')
        print('爬取过程中因出现不明错误断开，当前进度已经保存，请查看')
