import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import json
from sys import argv
import time
import os


class Ptt_Crawler:
    
    root = "https://www.ptt.cc/bbs/"
    main = "https://www.ptt.cc"
    beauty_data = {
            "from":"/bbs/Beauty/index3650.html",
            "yes": "yes"
        }
    dn = 'popular_img'  # for popular img, label = 1
    if not os.path.exists(dn):  
                os.makedirs(dn)
    dn2 = 'normal_img'  # label = 0
    if not os.path.exists(dn2):  
                os.makedirs(dn2)
    
    

    


    def __init__(self):
        self.session = requests.session()
        requests.packages.urllib3.disable_warnings()
        self.session.post("https://www.ptt.cc/ask/over18",
                           verify=False,
                           data=self.beauty_data)
        
        

    def crawl_image(self,url):
        res  = self.session.get(url, verify=False)
        soup = BeautifulSoup(res.text, 'html5lib')
        
        like = 0
        allow = ['jpg','jpeg','png','gif']
        links = soup.find_all('a')


        for r in soup.select(".push"):
            if "warning-box" not in r['class']: #avoid 'large file error'
                
                if(r.select(".push-tag")[0].contents[0][0] == '推'):
                    like+=1
        for l in links:
            href = l['href']
            #fetch the data type(jpg...)
            sub = href.split('.')[-1]

            if sub.lower() in allow:
                print('download:',href)

                try:
                    response = requests.get(href,stream=True) #stream + True for image downloading
                    if(like >= 35): #for popular image, label = 1
                        print(f'the popular articel: {url}')
                        fp = self.dn+'/'+href.split('/')[-1]

                        
                    else: #for normal image, label = 0
                        fp = self.dn2+'/'+href.split('/')[-1]
                    
                    f = open(fp,'wb') #open the folder
                    f.write(response.raw.read()) #write the image into the folder

                    f.close()
                except TimeoutError:
                    print('timeout error, skip and move on')
                    continue

        
            

            

if __name__ == '__main__':
    
    
    
    #crawl popular, normal image for training
    crawler = Ptt_Crawler()
    with open('all_article.jsonl','r') as f:
                data = json.load(f)
    i = 0
    while(i < len(data)): 
        
        url = data[i]['url: ']
        print('===searching...===')
        print('===current url:{}==='.format(url))
        print(f'===current idx:{i} ===')
        print('===current date:{}==='.format(data[i]['date: ']))
        print('\n')

        crawler.crawl_image(url)
        i+=1
        time.sleep(0.5)

