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
response__likelist = []
response__boolist = []
push_boo_rank = []
img_urls = []
all_img = []

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
        self.like = 0
        self.boo = 0

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
    
    def pushes(self,art_url):
        
        res  = self.session.get(art_url, verify=False)
        soup = BeautifulSoup(res.text, 'html5lib')




        for r in soup.select(".push"):
            if "warning-box" not in r['class']: #avoid 'large file error'
                
                if(r.select(".push-tag")[0].contents[0][0] == '推'):
                    self.like+=1
                    user = r.select(".push-userid")[0].contents[0]                  
                    r_dict_like = {
                            'user_id':user,
                        }
                    response__likelist.append(r_dict_like)
                
                elif(r.select(".push-tag")[0].contents[0][0] == '噓'):
                    self.boo+=1
                    user = r.select(".push-userid")[0].contents[0]                  
                    r_dict_boo = {
                            'user_id':user,
                        }
                    response__boolist.append(r_dict_boo)

        #print(response__likelist)
        #print(response__boolist)
    
    
    def count_push_boo(self):
        
        likes = len(response__likelist)
        boos = len(response__boolist)
        count_like = {}
        count_boo = {}

        for i in range(likes):
            user = response__likelist[i]['user_id']
            if(user in count_like.keys()):
                count_like[user] += 1
            else:
                count_like[user] = 1
        #sort the dict by counts
        count_like = {k: v for k, v in sorted(count_like.items(), key=lambda item: item[1],reverse=True)}
        #print(count_like)
        #print('\n\n')

        for i in range(boos):
            user = response__boolist[i]['user_id']
            if(user in count_boo.keys()):
                count_boo[user] += 1
            else:
                count_boo[user] = 1
        count_boo = {k: v for k, v in sorted(count_boo.items(), key=lambda item: item[1],reverse=True)}
        #print(count_boo)

        print('total like and boo: {} , {}'.format(self.like,self.boo))
        
        first10_like = {k: count_like[k] for k in list(count_like)[:10]}
        first10_boo = {k: count_boo[k] for k in list(count_boo)[:10]}
        keysl = []
        valuesl = []
        keysb = []
        valuesb = []
        
        items = first10_like.items()
        for item in items:
            keysl.append(item[0]), valuesl.append(item[1])
        
        items = first10_boo.items()
        for item in items:
            keysb.append(item[0]), valuesb.append(item[1])
        
        
        #compose final boo,push
        final = {
            "all-like":self.like,
            "all-boo":self.boo,
            "like 1":{"user_id":keysl[0],"count":valuesl[0]},
            "like 2":{"user_id":keysl[1],"count":valuesl[1]},
            "like 3":{"user_id":keysl[2],"count":valuesl[2]},
            "like 4":{"user_id":keysl[3],"count":valuesl[3]},
            "like 5":{"user_id":keysl[4],"count":valuesl[4]},
            "like 6":{"user_id":keysl[5],"count":valuesl[5]},
            "like 7":{"user_id":keysl[6],"count":valuesl[6]},
            "like 8":{"user_id":keysl[7],"count":valuesl[7]},
            "like 9":{"user_id":keysl[8],"count":valuesl[8]},
            "like 10":{"user_id":keysl[9],"count":valuesl[9]},
            "boo 1":{"user_id":keysb[0],"count":valuesb[0]},
            "boo 2":{"user_id":keysb[1],"count":valuesb[0]},
            "boo 3":{"user_id":keysb[2],"count":valuesb[2]},
            "boo 4":{"user_id":keysb[3],"count":valuesb[3]},
            "boo 5":{"user_id":keysb[4],"count":valuesb[4]},
            "boo 6":{"user_id":keysb[5],"count":valuesb[5]},
            "boo 7":{"user_id":keysb[6],"count":valuesb[6]},
            "boo 8":{"user_id":keysb[7],"count":valuesb[7]},
            "boo 9":{"user_id":keysb[8],"count":valuesb[8]},
            "boo 10":{"user_id":keysb[9],"count":valuesb[9]},
        }

        push_boo_rank.append(final)
    
    def popular(self,art_url,num):
        
        
        res  = self.session.get(art_url, verify=False)
        soup = BeautifulSoup(res.text, 'html5lib')
        
        allow = ['jpg','jpeg','png','gif']
        links = soup.find_all('a')

        for l in links:
            href = l['href']
            #fetch the data type(jpg...)
            sub = href.split('.')[-1]

            if sub.lower() in allow:
                 print('download:',href)
            
                 img_urls.append(href)
        
        comments = soup.find_all("div", class_="push")
        
        # for c in comments:
        #     push_tag = c.find(
        #         "span", class_="push-tag").string  
        #     print(f'cur push tag:{push_tag}')
        #     if(push_tag == '推' or push_tag == '噓'):
        #         img = c.find("span", class_="push-content").a['href'].strip
        #         img_urls.append(img)
    
    
    def popular_json(self):

        print(img_urls)
        article = {
            "number_of_popular_articles": num,
             "image_urls": img_urls
        }
        
        all_img.append(article)



        



        
        




                    

                    






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
    
    elif len(argv) == 4: #for push srt, end
        #load the json file we just crawled
        print(argv[1])
        if(argv[1] == 'push'):
            with open('all_article.jsonl','r') as f:
                data = json.load(f)

            srt_d = int(argv[2])
            end_d = int(argv[3])
            srtidx = endidx = 0
            i = 0
             
           
            while(i <  len(data)):
                cur_date = int(data[i]['date: '])
                if((cur_date == srt_d) and srtidx == 0):
                    srtidx = i
                elif(cur_date > end_d): #no end date found
                    endidx = i
                    break
                i+=1

            for idx in range(srtidx,endidx):

                    url = data[idx]['url: ']
                    print('===searching...===')
                    print('===current url:{}==='.format(url))
                    print('===current date:{}==='.format(data[idx]['date: ']))
                    print('\n')
                    crawler.pushes(url) #crawl all like and boos


            crawler.count_push_boo() #count the first 10 and output it

            with open('push_{}_{}.json'.format(srt_d,end_d),'w',encoding='utf-8') as f:
                json.dump(push_boo_rank,f,indent=1,ensure_ascii=False)
        
        elif(argv[1] == 'popular'):

            
            with open('all_popular.jsonl','r') as f:
                data = json.load(f)
            
            srt_d = int(argv[2])
            end_d = int(argv[3])
            srtidx = endidx = 0
            i = 0
           
            
           
            while(i <  len(data)):
                cur_date = int(data[i]['date: '])
                if((cur_date == srt_d) and srtidx == 0):
                    srtidx = i
                # elif(cur_date == end_d):
                #     while(int(data[i]['date: ']) == end_d):
                #         i+=1
                #     endidx = i
                #     break
                elif(cur_date > end_d): #no end date found
                    endidx = i
                    break
                i+=1

           
  

            #number of popular articles:
            num = (endidx - srtidx)

            
            for idx in range(srtidx,endidx):

                    url = data[idx]['url: ']
                    print('===searching...===')
                    print('===current url:{}==='.format(url))
                    print('===current date:{}==='.format(data[idx]['date: ']))
                    print('\n')
                    crawler.popular(url,num) 
            crawler.popular_json()
            
            with open('popular_{}_{}.json'.format(srt_d,end_d),'w',encoding='utf-8') as f:
                json.dump(all_img,f,indent=1,ensure_ascii=False)
            






