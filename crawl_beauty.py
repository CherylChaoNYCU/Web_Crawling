from urllib import request
import requests
from bs4 import BeautifulSoup
import os
#ref: https://ithelp.ithome.com.tw/articles/10290234?sc=rss.iron
url = "https://www.ptt.cc/bbs/Beauty/M.1662872395.A.BCC.html"

#response = requests.get(url,headers={"cookie":"over18 = 1","user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"}) #set over18 to 1 so the cookie won't impede your way
response = requests.get(url, cookies={"over18":"1"})
html = BeautifulSoup(response.text,"html.parser")
#print(html)

#making the folders to store all images we crawled 
dn = "ptt/" + url.split("/")[-1]  # 資料夾檔名
if not os.path.exists(dn):  
    os.makedirs(dn)


#all allowed image format

allow = ['jpg','jpeg','png','gif']
links = html.find_all('a')

for l in links:
    href = l['href']
    #fetch the data type(jpg...)
    sub = href.split('.')[-1]

    if sub.lower() in allow:
        print('download:',href)
        response = requests.get(href,stream=True) #非純文字檔而是圖檔，要讓stream + True
        fp = dn+'/'+href.split('/')[-1]

        f = open(fp,'wb') #open the folder
        f.write(response.raw.read()) #write the image into the folder

        f.close()
        

    
