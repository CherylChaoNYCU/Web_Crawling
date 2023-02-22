import requests
from bs4 import BeautifulSoup
import json
'''
if you are banned by the website:"
use sleep() or random sleep to pretend you are not using for loop
'''

article_list = []
#article = {}



def get_resp():
    cookies = {
    'over18': '1'
    }
    resp = requests.get(url, cookies=cookies)
    if resp.status_code!=200:
        return 'error'
    else:
        return resp
#one page article
def get_articles(resp,pg):

    soup = BeautifulSoup(resp.text, 'html5lib')
    arts = soup.find_all('div', class_='r-ent')
    for art in arts:
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
            elif(pg == 2): #last page
                 if(not date=='0101'):
                    article = {
                        'date: ': date,
                        'title: ': title,
                        'url: ': link
                    }
                    article_list.append(article)
            else:
                 article = {
                    'date: ': date,
                    'title: ': title,
                    'url: ': link
                 }
                 article_list.append(article)
    
    #repetitively crawl the next pages
    next_url = 'https://www.ptt.cc' + \
        soup.select_one(
            '#action-bar-container > div > div.btn-group.btn-group-paging > a:nth-child(3)')['href']
    return next_url

if __name__ == '__main__':
    #first page url
    url = 'https://www.ptt.cc/bbs/Beauty/index3647.html' #the page of 2022 1/1
    #crawl til the final page
    #first page: no 12/31, last page: no 01/01
    for now_pg in range(309):
        print(f'crawing {url}')
        resp = get_resp()
        if resp != 'error':
            if(now_pg == 0):
                url = get_articles(resp,1)
            elif(now_pg == 308):
                url = get_articles(resp,2)
            else:
                url = get_articles(resp,0)

        print('===current page: {} / 308 ==='.format(now_pg))
    
    with open('all_article.jsonl','w',encoding='utf-8') as f:
        json.dump(article_list,f,indent=2,sort_keys=True,ensure_ascii=False)