import requests
from bs4 import BeautifulSoup
import time
import json
import random

r = requests.get('https://www.allbud.com/marijuana-strains/search?results=4005')
soup = BeautifulSoup(r.text, 'lxml')

l = soup.find('div', attrs= {'id':'search-results'}).find_all('div', attrs={'class':'col-sm-6 col-md-4 col-lg-3'})

base_url = 'https://www.allbud.com'
links = []
for i in l:
    url_ = i.find('a')['href']
    url = base_url + url_
    links.append(url)


for link in links:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'lxml')
    time.sleep(random.randint(1,3))
    detail = soup.find('div', attrs={'id':'strain_detail_accordion'})
    data = {}
    data['strain_link'] = link
    data['strain_name'] = detail.find('h1').text.strip()
    info = detail.find_all('div', attrs={'class':'row'})[1].find('div', attrs={'id':'strain-info'})
    st = info.find('h4', attrs={'class':'variety'}).text.strip().split('\n')[0]
    try:
        si = info.find('h4', attrs={'class':'variety'}).text.strip().split('\n')[2].strip().split('/')
        data['strain_type'] = st
        if 'Hybrid' in st:
            if st == 'Hybrid':
                data['%indica'] = 50
                data['%sativa'] = 50
            else:
                if 'Indica' in si[0]:
                    data['%indica'] = si[0]
                    data['%sativa'] = si[1]
                elif 'Sativa' in si[0]:
                    data['%indica'] = si[1]
                    data['%sativa'] = si[0]
                else:
                    data['%indica'] = ''
                    data['%sativa'] = ''
    except IndexError:
        if 'Indica' in info.find('h4', attrs={'class':'variety'}).text.strip().split('\n')[0]:
            data['%indica'] = 100
            data['%sativa'] = 0
        elif 'Sativa' in info.find('h4', attrs={'class':'variety'}).text.strip().split('\n')[0]:
            data['%sativa'] = 100
            data['%indica'] = 0
            
            
    if info.find('h4', attrs={'class':'percentage'}).text:
        all_per = info.find('h4', attrs={'class':'percentage'}).text.replace(' ','').replace('\n','').split(':')
        if not 'CBD' in info.find('h4', attrs={'class':'percentage'}).text:
            data['%CBD'] = ''
        if not 'CBN' in info.find('h4', attrs={'class':'percentage'}).text:
            data['%CBN'] = ''
                
        for i in range(len(all_per)):
            if 'THC' in all_per[i]:
                if 'C' in all_per[i+1]:
                    data['%THC'] = all_per[i+1].split(',')[0]
                else:
                    data['%THC'] = all_per[i+1]
            elif 'CBD' in all_per[i]:
                if 'C' in all_per[i+1]:
                    data['%CBD'] = all_per[i+1].split(',')[0]
                else:
                    data['%CBD'] = all_per[i+1]
            elif 'CBN' in all_per[i]:
                if 'C' in all_per[i+1]:
                    data['%CBN'] = all_per[i+1].split(',')[0]
                else:
                    data['%CBN'] = all_per[i+1]
    else:
        data['%THC'] = ''
        data['%CBD'] = ''
        data['%CBN'] = ''
        
    effects_div = detail.find_all('div', attrs={'class':'row'})[1].find_all('div', attrs={'class':'row small-gutter'})

    data['moods'] = effects_div[0].find('div',attrs={'class':'panel-body well tags-list'}).text.replace(' ','').replace('\n','')    
    data['flavors'] = effects_div[1].find('div',attrs={'class':'panel-body well tags-list'}).text.replace(' ','').replace('\n','')  
    
    with open('data.txt', 'a') as outfile:
        json.dump(data, outfile)
        outfile.write('\n')
