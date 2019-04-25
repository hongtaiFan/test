import requests
from bs4 import BeautifulSoup
import json

url="https://wiki.hitwh.net.cn/uploads/2019spring-course.html"
wb_data=requests.get(url)
soup = BeautifulSoup(wb_data.text, 'html.parser')
trs=soup.select('tr')

primaryData=[]
for tr in trs:
    trsoup = BeautifulSoup(tr.text, 'html.parser')
    tdintrData = str(trsoup).split('\n')
    msg = [tdintrData[8],tdintrData[10],tdintrData[11]]
    if msg[0] != ''and msg[0][0]!='研' and tdintrData[9] == '星期1' and msg[1] != '第大节' and msg[2] != '':
        primaryData.append(msg)

# 21周上
# 1-8周上
# 1-9,16周上
# 1-3,6-8周上
# 1-3,7-10,13-15周上


finalData=[]
for j in primaryData:
    string=j[2]
    msg=[j[0][0:2],j[0][2]+'层',j[0][0]+j[0][2:5],j[1][1]]
    n=m=0
    for i in string:
        if i=='-':
            n+=1
        if i==',':
            m+=1

    h = string.index("周")
    if n==0:
        if int(string[0:h]) == 8:
            finalData.append(msg)
    elif n == 1:
        t1 = string.index("-")
        a = int(string[0:t1])
        if m == 0:
            b = int(string[t1 + 1:h])
            if a <= 8 and b >= 8:
                finalData.append(msg)
        else:
            t2 = string.index(",")
            b = int(string[t1 + 1:t2])
            c = int(string[t2 + 1:h])
            if (a <= 8 and b >= 8) or c == 8:
                finalData.append(msg)
    elif n==2:
        t1 = string.index("-")
        t2 = string.index(",")
        a = int(string[0:t1])
        b = int(string[t1 + 1:t2])
        s = string[t2 + 1:h]
        t3 = s.index("-")
        c = int(s[0:t3])
        d = int(s[t3 + 1:])
        if (a <= 8 and b >= 8) or (c <= 8 and d >= 8):
            finalData.append(msg)
    else:
        t1 = string.index("-")
        t2 = string.index(",")
        a = int(string[0:t1])
        b = int(string[t1 + 1:t2])
        s1 = string[t2 + 1:h]
        t3 = s1.index("-")
        t4 = s1.index(",")
        c = int(s1[0:t3])
        d = int(s1[t3 + 1:t4])
        s2 = s1[t4 + 1:h]
        t5 = s2.index("-")
        e = int(s2[0:t5])
        f = int(s2[t5 + 1:])
        if (a <= 8 and b >= 8) or (c <= 8 and d >= 8) or (e <= 8 and f >= 8):
            finalData.append(msg)

n=0
primaryJsonData=[]
for i in finalData:
    data=[i[0],i[1],i[2],[True,True,True,True,True,True]]
    a=0
    for j in primaryJsonData:
        if j==data:
            a=1
    if a==0:
        primaryJsonData.append(data)

for i in finalData:
    for j in primaryJsonData:
        if i[0]==j[0] and i[1]==j[1] and i[2]==j[2]:
            j[3][int(i[3])-1]=False

midle1JsonData=[]
for i in range(len(primaryJsonData)):
    msg=[primaryJsonData[i][0],primaryJsonData[i][1],{primaryJsonData[i][2]:str(primaryJsonData[i][3])}]
    for j in range(i+1,len(primaryJsonData)):
        if primaryJsonData[i][0]==primaryJsonData[j][0] and primaryJsonData[i][1]==primaryJsonData[j][1]:
            msg[2].update({primaryJsonData[j][2]:str(primaryJsonData[j][3])})
    a=0
    for w in midle1JsonData:
        if primaryJsonData[i][0]==w[0] and primaryJsonData[i][1]==w[1]:
            a=1
    if a==0:
        midle1JsonData.append(msg)

midle2JsonData=[]
for i in range(len(midle1JsonData)):
    msg=[midle1JsonData[i][0],{midle1JsonData[i][1]:midle1JsonData[i][2]}]
    for j in range(i+1,len(midle1JsonData)):
        if midle1JsonData[i][0]==midle1JsonData[j][0]:
            msg[1].update({midle1JsonData[j][1]:midle1JsonData[j][2]})
        a=0
        for w in midle2JsonData:
            if midle1JsonData[i][0]==w[0]:
                a=1
        if a==0:
            midle2JsonData.append(msg)

finalJsonData={}
for i in midle2JsonData:
    finalJsonData.update({i[0]:i[1]})
finalJsonData.update({"day":1})
finalJsonData.update({"week":8})
json = json.dumps(finalJsonData, ensure_ascii=False, sort_keys=True, indent=4, separators=(',',':'))
print(json)

f=open('json.txt','w')
f.write(json)
f.close
