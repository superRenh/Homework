
# coding: utf-8

# In[522]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np
import argparse


# In[ ]:


def split_tool(url):
    base="https://movies.yahoo.com.tw/movieinfo_main.html/id="
    result = base+url.split('-')[-1]
    return(result)


# In[ ]:


def get_movieid(home_page):
    """
    
    https://movies.yahoo.com.tw/movie_intheaters.html
    
    """
    soup = BeautifulSoup(get_web_pages(home_page),'html.parser')
    a=map(split_tool,re.findall("href=\"(.*?)\">",str(soup.select('div[class="release_foto"]'))))
    urls = list(a)
    return urls


# In[ ]:


def surfing_all_page(base_url):
    """
    一頁10筆電影
    共"電影數/10" 頁
    """
    url_list =[]
    soup = BeautifulSoup(get_web_pages(base_url),'html.parser')
    num_movies = int(re.search("共(\d+)筆",soup.find('div','release_time _c').p.text).group(1))
    num_pages = np.ceil(num_movies/10).astype(int)
    each_page=base_url+'?page={}'
    for i in range(1,num_pages+1):
        url_list +=get_movieid(each_page.format(i))
    
    return url_list


# In[411]:


def get_web_pages(url):
    req = requests.get(url,cookies={'over18':'1'})
    if req.status_code!=200:
        print('Invalid web:',url)
        return None
    else:
        return req.text


# In[514]:


def get_movies(url):
    soup = BeautifulSoup(get_web_pages(url),'html.parser')
    dicts={}
    dicts['電影名稱(中)'] = soup.h1.text
    dicts['電影名稱(英)'] = soup.h3.text
    dicts['期待度'] = soup.find('div','circle_percent')['data-percent']+'%'
    dicts["滿意度"] = soup.find('div',"score_num count").text.strip()

    content = str(soup.find('div','movie_intro_info_r'))
    dicts["類型"] = '/'.join(re.findall("電影介紹_類型icon\\'\,\\'(.*?)\\'",content))




    for i in soup.find('div',"movie_intro_info_r").find_all('span'):
        try:
            title =i.text.strip().split("：")[0]
            title = re.sub("\u3000","",title)
            dicts[title]=i.text.strip().split("：")[1]
        except:
            pass

    dicts["演員"] = re.sub("\s+","",'/'.join(re.findall("電影介紹_演員資訊\\'\,\\'(.*?)\\'",content)))
    dicts["導演"] = re.sub("\s+","",soup.find('div',"movie_intro_list").text.strip())
    dicts["官方連結"] = '/'.join(re.findall("電影介紹_官網1\\'\,\\'(.*?)\\'",content))

    dicts["劇情介紹"] = soup.find('div','gray_infobox_inner').span.text.strip()
    
    return dicts


# In[519]:


def create_movie_df(base_url):
    urls = surfing_all_page(base_url)[:20]
    movies=[]
    for url in urls:
        movies.append(get_movies(url))
    result = pd.DataFrame(movies,columns=movies[0].keys())
    return result


# //*[@id="content_l"]/div[5]/div[2]/div[1]/div/span/text()[3]

# # dicts["劇情介紹"] = soup.find('div','gray_infobox_inner').span.text.strip()
# 

# In[ ]:


if __name__=='__main__':
    parse = argparse.ArgumentParser
    parse.add_argument("-u","--url",type=str,required=True,help='url for crawler')
    base_url=args.url
    create_movie_df(base_url)


# In[501]:


base_url="https://movies.yahoo.com.tw/movie_intheaters.html"


# In[520]:


create_movie_df(base_url)

