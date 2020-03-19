# -*- coding: utf-8 -*-
import sys
import time
import urllib2
from selenium import webdriver
import csv
import pandas as pd
from collections import defaultdict
import pickle

Details = defaultdict(list)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
PATH = "/home/srinidhi/chromedriver"


class TextScrapper:
    def __init__(self,url):
        self.browser1 = webdriver.Chrome(executable_path = PATH,chrome_options = options)
        self.browser1.get(url)

    def details(self):
        Name = self.browser1.find_element_by_xpath("//h1[@class = 'title']").text
        print(Name)
        Address = self.browser1.find_element_by_xpath("//div[@class = 'nearby']//p").text
        print(Address)
        Gender = self.browser1.find_element_by_xpath("//h5[@class = 'description']").text
        print(Gender)
        Offers = self.browser1.find_element_by_xpath("//div[@class = 'propertyCoupon']").text
        print(Offers)
        Overview = self.browser1.find_element_by_xpath("//div[@class = 'aboutCard']").text
        print(Overview)
    #    amenities = self.browser1.find_elements_by_xpath("//div[@class = 'amenities itemSlide']//p[@class = 'amenities-title']")
    #    Amenities = [amnt.get_attribute('innerHTML') for amnt in amenities]
    #    print(Amenities)
        roomtype = self.browser1.find_elements_by_xpath('//*[@id="room"]/div/div[2]//div[@class= "roomContainer"]')
    #    Amenities = []
        Rent = []
        for rt in roomtype:
            type = rt.text
            #self.browser1.execute_script("arguments[0].click();",rt)
            Rent.append(type)
        Amenities = self.browser1.find_element_by_xpath("//p[@class = 'amenities-title']").text
    #    Info = self.browser1.find_element_by_xpath("//div[@class =  'informationContainer']").text
    #    print(Info)
        IMGS = self.browser1.find_elements_by_xpath("//img[@class = 'img-fluid']")
        imgs = []
        for img in IMGS:
            image = img.get_attribute('src')
            if 'uploads' in image:
                imgs.append(image)
        print(imgs)
        Details["Name"].append(Name)
        Details["Address"].append(Address)
        Details["Gender"].append(Gender)
        Details["Offers"].append(Offers)
        Details["Rent"].append(Rent)
    #    Details["Info"].append(Info)
        Details["Overview"].append(Overview)
        Details["Amenities"].append(Amenities)
        Details["Images"].append(imgs)

    def close(self):
        self.browser1.close()

dbfile = open('city_links','rb')
while 1:
    try:
        City_Links = pickle.load(dbfile)
    except EOFError:
        break
dbfile.close()
#print(City_Links)
city_name = sys.argv[1]
if city_name in City_Links.keys():
    print("Number of available links for {} is ".format(city_name) + str(len(City_Links[city_name])))
    links = City_Links[city_name]
    Low_site = int(input("Enter the lower link id"))
    High_site = int(input("Enter the higher link id"))
    print(Low_site)
    print(High_site)
    if Low_site > 0 and High_site <= len(links):
        for lk in range(Low_site-1,High_site):
            Details["Id"].append(lk+1)
            obj = TextScrapper(links[lk])
            obj.details()
            obj.close()

        columns = ['Id','Name','Address','Gender','Offers','Rent','Overview','Amenities','Images']
        df = pd.DataFrame(Details,columns = columns)
        filename = "%s.csv"%city_name
        df.to_csv(filename,mode = 'a',header = False,columns = columns,encoding = 'utf-8')
    else:
        print("Wrong Range")
else:
    print("{}'s links is not crawled please collect the links".format(city_name))
