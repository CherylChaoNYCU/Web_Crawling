import requests
from bs4 import BeautifulSoup
import json
from sys import argv
import time

'''
if you are banned by the website:"
use sleep() or random sleep to pretend you are not using for loop
'''

article_list = []
popular_article_list = []
#article = {}


class Ptt_Crawler:
    
    root = "https://www.ptt.cc/bbs/"
    main = "https://www.ptt.cc"
    beauty_data = {
            "from":"/bbs/Beauty/index3650.html",
            "yes": "yes"
        }

    def __init__(self):
        self.session = requests.session()
        requests.packages.urllib3.disable_warnings()
        self.session.post("https://www.ptt.cc/ask/over18",
                           verify=False,
                           data=self.beauty_data)

    #for crawling
    def get_articles(self,resp,pg):
        
        res  = self.session.get(resp, verify=False)
        soup = BeautifulSoup(res.text, 'html5lib')
        arts = soup.find_all('div', class_='r-ent')

        for art in arts:
            pop = art.find('div',class_='nrec').getText().strip()


            title = art.find('div', class_='title').getText().strip()
            if not title.startswith('('): #reminders: some articles might be deleted! usually start with '('
                        link = 'https://www.ptt.cc' + \
                                art.find('div', class_='title').a['href'].strip()
            
            date = art.find('div', class_='date').getText().strip()
            #converting m/d to 0m0d
            date = date.split('/')
            for i in range(2):
                if(len(date[i]) == 1):
                    tmp = ''.join('0'+date[i])
                    date[i] = tmp
            date = ''.join(date)

            if(title[1]!='公' and title[0]!='F'):
                if(pg == 1): #first page
                    if(not date=='1231'):
                        #print('first pg cur date: ',date)
                        article = {
                            'date: ': date,
                            'title: ': title,
                            'url: ': link
                        }
                        article_list.append(article)
                    if(pop == '爆'):
                        popular_article_list.append(article)

                elif(pg == 2): #last page
                    if(not date=='0101'):
                        article = {
                            'date: ': date,
                            'title: ': title,
                            'url: ': link
                        }
                        article_list.append(article)
                    if(pop == '爆'):
                        popular_article_list.append(article)
                else:
                    article = {
                        'date: ': date,
                        'title: ': title,
                        'url: ': link
                    }
                    article_list.append(article)
                    if(pop == '爆'):
                        popular_article_list.append(article)
        
        #repetitively crawl the next pages
        next_url = 'https://www.ptt.cc' + \
            soup.select_one(
                '#action-bar-container > div > div.btn-group.btn-group-paging > a:nth-child(3)')['href']
        return next_url

if __name__ == '__main__':
    
    
    #crawl til the final page
    #first page: no 12/31, last page: no 01/01
    crawler = Ptt_Crawler()

    if len(argv) == 2: #for crawl
        url = 'https://www.ptt.cc/bbs/Beauty/index3647.html'
        for now_pg in range(309): #should be 309 for homework
            #first page 20221/1 url
            print(f'crawing {url}')
            
            if(now_pg == 0):
                    url = crawler.get_articles(url,1)
            elif(now_pg == 308):
                    url = crawler.get_articles(url,2)
            else:
                    url = crawler.get_articles(url,0)

            print('===current page: {} / 308 ==='.format(now_pg))
            time.sleep(0.5)
    
            with open('all_article.jsonl','w',encoding='utf-8') as f:
                json.dump(article_list,f,indent=2,sort_keys=True,ensure_ascii=False)
            
            with open('all_popular.jsonl','w',encoding='utf-8') as f:
                json.dump(popular_article_list,f,indent=2,sort_keys=True,ensure_ascii=False)