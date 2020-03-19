import sys
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from collections import defaultdict

options = webdriver.ChromeOptions()
options.add_argument("--headless")

City_Links = defaultdict(list)
PATH = "/home/srinidhi/chromedriver"

def write_into_picke(City_Links):
    dbfile = open('city_links','wb')
    pickle.dump(City_Links,dbfile)
    dbfile.close()

def read_from_pickle():
    try:
        dbfile = open('city_links','rb')
        while 1:
            try:
                City_Links = pickle.load(dbfile)
                return City_Links
            except EOFError:
                break
    except:
        City_Links = defaultdict(list)
        return City_Links

city_name = sys.argv[1]
url = "https://www.coho.in/flats-in-{}".format(city_name)
print(url)
City_Links = read_from_pickle()
browser = webdriver.Chrome(executable_path = PATH,chrome_options = options)
browser.get(url)
print(City_Links)
area = browser.find_elements_by_xpath("//div[@class = 'slick-track']//li[@role = 'option']//a//span")
print(len(area))
for ar in area:
    if "Others" not in ar.get_attribute('innerHTML'):
        print(ar.get_attribute('innerHTML'))
        browser.execute_script("arguments[0].click()",ar)
        time.sleep(5)
links = browser.find_elements_by_xpath("//div[@role = 'tabpanel']//ul[@class = 'list_card clearfix']//li//a")
for ln in links:
    href = ln.get_attribute('href')
    if "flats-in-{}".format(city_name) in href:
        print(href)
        City_Links[city_name].append(href)
City_Links[city_name] = list(set(City_Links[city_name]))
print(City_Links)
write_into_picke(City_Links)
browser.close()
browser.quit()
