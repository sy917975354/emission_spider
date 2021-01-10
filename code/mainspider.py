import execjs
import os
import requests
import re
import pandas as pd
from tqdm import tqdm
os.chdir(r"D:\Python\Data_analysis\爬虫\生活垃圾发电厂焚烧数据爬虫")

def resetParams(dic):

    with open(r'jsCode.js', encoding='UTF-8', mode='r') as f:
        JsData = f.read()
    ctx = execjs.compile(JsData) #执行js文件
    dic['tc'] = ctx.eval('a')
    ctmy = ctx.eval('ctmy')
    dic['ts'] = execjs.eval('(new Date).valueOf()')
    dic["sgn"] = ctx.call('pscc',ctmy+str(dic['ts'])+str(dic['tc']))
    return dic

def setParams(pscode,outputcode):
    dic={}
    dic['tc'] = '62201040'
    dic['ts'] = '1610197807403'
    dic['sgn'] = 'c250eb3bc6b8fadbf01d4cae101045b118190c24'
    dic['pscode'] = pscode #每一个企业对应一个值
    dic['outputcode'] = outputcode #每一个焚烧炉对应一个值
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
    pat = re.compile('"monitor_time":"(.*?)"')
    monitor_time = pat.findall(txt)
    pat = re.compile('"pollutant_name":"(.*?)"')
    pollutant_name = pat.findall(txt)
    pat = re.compile('"day":"(.*?)"')
    day = pat.findall(txt)
    pat = re.compile('"strength":(.*?),')
    strength = pat.findall(txt)
    pat = re.compile('"standard_value":"(.*?)",')
    standard_value = pat.findall(txt)
    pat = re.compile('"ps_code":"(.*?)",')
    pscode = pat.findall(txt)
    pat = re.compile('"mp_code":"(.*?)",')
    mpcode = pat.findall(txt)
    df_copy = pd.DataFrame({"监测时间":monitor_time,"监测因子":pollutant_name,'监测日期':day,'折算浓度':strength,
                       '标准浓度':standard_value,'pscode':pscode,'mpcode':mpcode})
    return df_copy

if __name__ == '__main__':
    timerange = pd.date_range('2020-01-01', '2021-12-31').to_pydatetime()
    df = pd.read_csv('mp_code.csv')
    df = df.iloc[:,1:]
    for i in tqdm(range(len(df))):
        pscode = df.iloc[i,0]
        outputcode = df.iloc[i,1]
        df_all = pd.DataFrame()
        params = setParams(pscode, outputcode)
        try:
            for date in timerange:
                day = date.strftime('%Y%m%d')
                params['day'] = day
                url = 'https://ljgk.envsc.cn/OutInterface/GetMonitorDataList.ashx'
                response = requests.get(url,headers=header,params=params)
                df_all = df_all.append(DataParse(response.text),ignore_index=True)
            df_all.to_csv("result/"+pscode+'_'+outputcode+'.csv')
        except :
            print('当爬取pscode:%s,\nmpcode:%s时出现了错误。\n跳过并更新参数' %(pscode,outputcode))
            params = resetParams(params)
            pass



