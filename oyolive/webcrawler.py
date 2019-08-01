# -*- coding: utf-8 -*-
import sys
import urllib2
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import csv
import pandas as pd
from collections import defaultdict

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--start-maximized')
#options.add_argument('--disable-features=NetworkService')
PATH = "C:\chromedriver" 
Details = defaultdict(list)

class TextScrapper:
    def __init__(self,url):
        self.browser1 = webdriver.Chrome(executable_path = PATH)#,chrome_options=options)
        self.browser1.get(url)

    def details(self):
        Name = self.browser1.find_element_by_id("property-name").text
        Address = self.browser1.find_element_by_id("property-address").text
        Overview = self.browser1.find_element_by_xpath("//div[@class='property-desc-inner-container']").text
        typ = self.browser1.find_element_by_xpath("//img[@class = 'property-details-gender-tag']").get_attribute('src')
        typ = typ.split('/')[-1].strip('.svg')
        if typ == 'woman':
            Gender = 'Women'
        elif typ == 'unisex':
            Gender = "Unisex"
        else:
            Gender = "Man"
        Rent = self.browser1.find_element_by_xpath("//div[@class = 'occupancy-prices-container']").text
        Rent = Rent.encode('utf-8').replace('₹','Rs. ')
        amenities = self.browser1.find_elements_by_xpath("//div[@id = 'amenities-container']//h5")
        Amenities = " "
        for i in amenities:
            Amenities = Amenities + " %s"%i.get_attribute('innerHTML')
        #for i in range(5):
        #   span_element = self.browser1.find_element_by_xpath("//div[@class = 'slick-arrow slick-house-parts-images-item-next']")
        #    hover = ActionChains(self.browser1).double_click(span_element)
        #    hover.perform()
        #   time.sleep(5)
        print(Amenities)
        #print("The details :\n" + "Name: " + Name +'\nAddress: '+ Address
        #       + "\nGender: " + Gender + '\nOverview: ' + Overview
        #       + '\nRent: ' + Rent + "\n Amenities: " + Amenities)
        Details['Name'].append(Name)
        Details["Address"].append(Address)
        Details["Gender"].append(Gender)
        Details["Overview"].append(Overview)
        Details["Rent"].append(Rent)
        Details["Amenities"].append(Amenities)
       
    def get_images(self):
        div = self.browser1.find_element_by_xpath('//*[@id="div-property-details"]/div[1]/div[1]/div[1]/div[2]')
        mouse_click_1 = ActionChains(self.browser1).double_click(div)
        mouse_click_1.perform()
        time.sleep(5)
        imgs = []
        img_parts_tab = self.browser1.find_elements_by_xpath("//*[@class = 'living-images-parts-tabs']//ul//li//a")
        for list_values in img_parts_tab:
            #img_parts_tab = self.browser1.find_elements_by_xpath("//*[@class = 'living-images-parts-tabs']//ul//li//a")
            #print(img_parts_tab[i])
            mouse_click_2 = ActionChains(self.browser1).double_click(list_values)
            mouse_click_2.perform()
            time.sleep(10)
            for i in range(5):
                try:
                    nxt = self.browser1.find_element_by_xpath("//div[@class = 'slick-slider house-parts-images-slider-container slick-initialized']//div[@class = 'slick-arrow slick-house-parts-images-item-next']")
                    mouse_click_3 = ActionChains(self.browser1).double_click(nxt)
                    mouse_click_3.perform()
                except:
                    break
            IMGS = self.browser1.find_elements_by_xpath("//div[@class = 'slick-slider house-parts-images-slider-container slick-initialized']//div[@class = 'slick-track']//img")
            print(len(IMGS))
            for i in IMGS:
                i = i.get_attribute('src')
                if 'uploads' in i:
                    imgs.append(i)
                    print(i)
        Details["Desktop_Img"].append(imgs)
        print(len(Details["Desktop_Img"]))

    def close(self):
        self.browser1.close()

browser = webdriver.Chrome(executable_path = PATH,chrome_options=options)
url = "https://www.oyolife.in/pg-in-"
city_name = sys.argv[1]
url = url+city_name
print(url)
browser.get(url)
for i in range(4):
    browser.execute_script("""
                        var element = document.querySelector('.prop-listing-main-div');
                        element.scrollTop = 999999999;
                        """)
    time.sleep(10)
tags = browser.find_elements_by_xpath('//div[@class = "property-wrapper"]/a')
link = [tag.get_attribute('href') for tag in tags]
print("Number of links avaiable " + str(len(link)))
Low_site = int(input("Enter the lower link id"))
High_site = int(input("Enter the higher link id"))
print(Low_site)
print(High_site)
if Low_site > 0 and High_site <= len(link):
    for lk in range(Low_site-1,High_site):
        Details["Id"].append(lk+1)
        Details["Link"].append(link[lk])
        time.sleep(5)
        obj = TextScrapper(link[lk])
        obj.details()
        obj.get_images()
        obj.close()
    columns = ['Id','Name','Address','Gender','Overview','Rent','Amenities','Desktop_Img','Link']
    df = pd.DataFrame(Details,columns = columns)
    filename = "%s.csv"%city_name
    df.to_csv(filename,mode = 'a',header = False,columns = columns)
else:
    print("Wrong Range")
browser.close()
