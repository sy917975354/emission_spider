import os
import re
import pandas as pd
os.chdir(r"D:\Python\Data_analysis\爬虫\生活垃圾发电厂焚烧数据爬虫")
with open('pscode.txt','r',encoding='UTF-8') as f:
    content = f.read()

pat = re.compile('"ps_code":"(.*?)",')
ps_code = pat.findall(content)
pat = re.compile('"ps_name":"(.*?)",')
ps_name = pat.findall(content)
pat = re.compile('"region_name":"(.*?)",')
region_name = pat.findall(content)
pat = re.compile('"address":"(.*?)",')
address = pat.findall(content)
pat = re.compile('"longitude":(.*?),')
longitude = pat.findall(content)
pat = re.compile('"latitude":(.*?),')
latitude = pat.findall(content)

df = pd.DataFrame({'pscode':ps_code,'企业名称':ps_name,'所在区域':region_name,'详细地址':address,'经度':longitude,
                   '纬度':latitude})
df.to_csv('ps_code.csv')