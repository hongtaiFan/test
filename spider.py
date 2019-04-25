import re
import requests
from bs4 import BeautifulSoup

url1='http://today.hitwh.edu.cn/2019/0419/c1026a105442/page.htm'
url2="http://today.hitwh.edu.cn/2018/1119/c1026a100732/page.htm"
url3="http://today.hitwh.edu.cn/2019/0422/c1026a105616/page.htm"
wb_data=requests.get(url2)
wb_data.encoding = 'utf-8'
soup = BeautifulSoup(wb_data.text, 'html.parser')
a1=soup.select('a')
imgs=soup.select('img')
ps=soup.select('p')
news={}
images=[]

for i in imgs:
    if '.jpg' in str(i):
        a = re.search('src="', str(i)).end()
        b=re.search('" style', str(i)).start()
        c=re.search("title':'", str(i)).end()
        d = re.search("'}", str(i)).start()
        images.append(str(i)[c:d]+'：'+'http://today.hitwh.edu.cn'+str(i)[a:b])

for i in a1:
    if len(str(i.string))>4:
        a = str(i).index("=")
        b = str(i).index("m")
        news.update({i.string:'http://today.hitwh.edu.cn'+str(i)[a+2:b+1]})

content=''
for i in ps:
    s = re.sub('</?[^><]+>', '', str(i))
    content+=str(s)
for i in range(len(content)):
    if i%50==0 and i!=0:
        content=content[:i+1]+'\n'+content[i+1:]
        i+=2

a=re.search('录入时间',str(soup)).start()
b=re.search('日 ］',str(soup)).end()
time=str(soup)[a+4:b-1]

title=soup.select('title')[0].string
print(title)

innerTXT='标题：'+title+'\n时间：'+time+'\n内容：\n'+content+'\n图片：\n'
for i in images:
    innerTXT+=i+'\n'
innerTXT+='新闻：\n'
for i in news:
    innerTXT +=i+':'+news[i]+'\n'
print(innerTXT)

with open("news.txt","w",encoding='utf-8') as f:
    f.write(innerTXT)
    f.close
