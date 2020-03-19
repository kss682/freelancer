import sys
import time
import urllib2
from selenium import webdriver
from collections import defaultdict
import pickle
reload(sys)
sys.setdefaultencoding('utf8')

PATH = "/home/srinidhi/chromedriver"

City_Links = defaultdict(list)

def read_from_pickle():
    try:
        dbfile = open('city_links','rb')
        while 1:
            try:
                City_Links = pickle.load(dbfile)
            except EOFError:
                break
            return City_Links
    except:
        City_Links = defaultdict(list)
        return City_Links

City_Links = read_from_pickle()
print(City_Links)
browser = webdriver.Chrome(executable_path = PATH)
url = "https://www.stanzaliving.com/residences/"
city_name = sys.argv[1]
url = url + city_name
print(url)
browser.get(url)
browser.execute_script("window.scrollTo(0,  document.body.scrollHeight);")
time.sleep(10)
tags = browser.find_elements_by_xpath("//div[contains(@class,'resdenceListingSection__LandscapeMainContainer')]//a")
for tag in tags:
    link = tag.get_attribute('href')
    if link not in City_Links[city_name]:
        City_Links[city_name].append(link)
print(City_Links[city_name])
print("Number of links crawled :" + str(len(City_Links[city_name])))
browser.close()
dbfile = open('city_links','wb')
pickle.dump(City_Links,dbfile)
dbfile.close()
