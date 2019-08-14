import sys
import time
import urllib3
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from collections import defaultdict
import pickle
import random as rd

options = webdriver.ChromeOptions()
options.add_argument("--headless")

room_type = {
    'S' : "Shared Room",
    'P' : "Private Room",
    'E' : "Entire House",
}
PATH = "C:\chromedriver"
City_Links = {}

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
        City_Links = {}
        return City_Links

def crawl_links(url,browser):
    print(url)
    browser.execute_script("window.scrollTo(0,  document.body.scrollHeight);")
    browser.get(url)
    browser.implicitly_wait(rd.randint(1,6))
    span_element = browser.find_element_by_xpath('//*[@id="header"]/div/div[2]/div/div[1]/div[1]/div/ul/li[contains(text(),"{}")]'.format(type))
    print(type)
    hover = ActionChains(browser).double_click(span_element)
    hover.perform()
    browser.implicitly_wait(rd.randint(3,11))
    pagination = browser.find_elements_by_xpath('//*[@id="result_area"]/div[2]/div[3]/ul/li')
    len_pg = len(pagination)
    total_pages = pagination[len_pg - 2].text
    print("Total pages : %s"%total_pages)
    low_page = int(input("Enter lower page number"))
    high_page = int(input("Enter high page number"))
    i = 1
    while i <= high_page:
        print(i)
        if i >= low_page and i <= high_page:
            browser.implicitly_wait(rd.randint(6,12))
            tags = browser.find_elements_by_xpath('//*[@id="house_cards"]//a')
            for tag in tags:
                tg = tag.get_attribute('href')
                if 'houses' in tg:#or 'search_new' in tg:
                    City_Links[city_name][type].append(tg)
                if 'search_new' in tg:
                    while True:
                        #Try crawling multiple house links
                        browser2 = webdriver.Chrome(executable_path = PATH,chrome_options = options)
                        try:
                            crawl_links(tg,browser2)
                            break
                        except Exception as x:
                            print(x)
                            browser2.implicitly_wait(rd.randint(60,100))
                            continue
        browser.execute_script("window.scrollTo(0,  document.body.scrollHeight);")
        pg = browser.find_elements_by_xpath('//*[@id="result_area"]/div[2]/div[3]/ul/li')
        print(len(pg))
        #pagination
        try:
            browser.implicitly_wait(rd.randint(10,20))
            next = pg[len(pg)-1]
            next_page = ActionChains(browser).double_click(next)
            next_page.perform()
        except Exception as x:
            print(x)
            break
        i = i + 1
    print("Total links crawled %s"%str(len(City_Links[city_name][type])))
    browser.close()
    browser.quit()


while True:
    browser1 = webdriver.Chrome(executable_path = PATH,chrome_options = options)
    try:
        start = time.time()
        #browser1 = webdriver.Chrome(executable_path = PATH)
        City_Links = read_from_pickle()
        print(City_Links)
        city_name = sys.argv[1]
        type = room_type[sys.argv[2]]
        if city_name not in City_Links.keys():
            City_Links[city_name] = defaultdict(list)
        url = """https://www.nestaway.com/properties-in-{}""".format(city_name)

        crawl_links(url,browser1)
        write_into_picke(City_Links)
        end = time.time()
        print(end-start)
        break
    except Exception as x:
        print("Waiting")
        print(x)
        browser1.implicitly_wait(rd.randint(30,60))
        continue
