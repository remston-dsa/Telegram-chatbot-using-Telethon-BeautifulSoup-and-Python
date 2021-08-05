#import all the modules
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re

#set the driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# search function
def search(keyword):
    url=f'https://tdirectory.me/search/{keyword}'
    driver.get(url)

    channels=[]
    groups=[] 
    bots=[]
    join_channels=[]
    join_groups=[]
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    all_links=set()
    for link in soup.findAll('a'):
        if '#' not in link.get('href'):
            all_links.add('https://tdirectory.me/'+link.get('href'))
        
    for link in all_links:
        if re.search("https://tdirectory.me//channel/", link):
            channels.append(link)
        elif re.search("https://tdirectory.me//group/", link):
            groups.append(link)
        elif re.search("https://tdirectory.me//bot/", link):
            bots.append(link)

    for channel in channels:
        channel=re.sub(r'https://tdirectory.me//channel/', 'https://t.me/', channel)
        channel=re.sub(r'.dhtml', '', channel)
        join_channels.append(channel)
    
    for group in channels:
        group=re.sub(r'https://tdirectory.me//channel/', 'https://t.me/', group)
        group=re.sub(r'.dhtml', '', group)
        join_groups.append(group)

    return channels, groups, bots, join_channels, join_groups
    
    

