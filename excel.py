import requests
from bs4 import BeautifulSoup
import xlwings as xw

url="https://wiki.hitwh.net.cn/uploads/2019spring-course.html"
wb_data=requests.get(url)
soup = BeautifulSoup(wb_data.text, 'html.parser')
ths=soup.select('th')
trs=soup.select('tr')

thData=[]
for th in ths:
    if th.string not in['详细信息','课容量','选课限制说明','考试类型']:
        thData.append(th.string)
print(thData,'\n\n')

tdData=[]
i=1
for tr in trs:
    if i>1:
        trsoup = BeautifulSoup(tr.text, 'html.parser')
        tdintrData = str(trsoup).split('\n')
        tdintrData.remove('')
        del tdintrData[1]
        tdintrData.pop()
        tdintrData.pop()
        tdintrData.pop()
        if tdintrData[6]!='':
            tdData.append(tdintrData)
    i+=1
for j in tdData:
    print(j)

app=xw.App(visible=True,add_book=False)
wb=app.books.add()
b=65
for a in thData:
    wb.sheets['sheet1'].range(chr(b)+str(1)).value=a
    b+=1
c=2
#1668条数据
for j in tdData:
    b = 65
    for k in j:
        wb.sheets['sheet1'].range(chr(b) + str(c)).value = k
        b+=1
    c+=1

wb.save(r'CourseInformation.xlsx')
wb.close()
app.quit()




