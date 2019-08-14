# -*- coding: utf-8 -*-
import sys
import time
import urllib3
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import csv
import pandas as pd
from collections import defaultdict
import pickle

options = webdriver.ChromeOptions()
prefs={"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
options.add_experimental_option('prefs',prefs)
options.add_argument("--headless")
options.add_argument("--start-maximized")
room_type = {
    'S' : "Shared Room",
    'P' : "Private Room",
    'E' : "Entire House",
}
PATH = "C:\chromedriver"
Details = defaultdict(list)

class TextScrapper:
    def __init__(self,url):
        self.browser1 = webdriver.Chrome(executable_path = PATH,chrome_options = options)
        self.browser1.get(url)

    def details(self):
        Name = self.browser1.find_element_by_xpath("//div[@class = 'apartmaneName ellipsis']").text
        Address = self.browser1.find_element_by_xpath("//div[@class = 'tittleSection']//h1//span").text
        amenities = self.browser1.find_elements_by_xpath("//div[@class = 'houseAmenities']//li[@class = 'active']//span[@class = 'text']")
        Amenities = [i.get_attribute('innerHTML') for i in amenities ]
        features = self.browser1.find_elements_by_xpath("//div[@class = 'overviewDetails']//li[@class = 'halfScreen']//span[@class = 'text']")
        Features = [i.text for i in features]
        Rent = " "

        rent_tab = self.browser1.find_elements_by_xpath('//*[@id="hdp"]/div[2]/div[1]/div[4]/div/div[2]/div/div[1]/div')
        print(rent_tab)
        for rt in rent_tab:
            type = rt.text
            self.browser1.execute_script("arguments[0].click();",rt)
            #hover = ActionChains(self.browser1).double_click(rt)
            #hover.perform()
            time.sleep(3)
            rent = self.browser1.find_element_by_xpath('//*[@id="hdp"]/div[2]/div[1]/div[4]/div/div[2]/div/div[2]/div[1]/div/div[2]').text
            print(rent)
            onetimefee = self.browser1.find_element_by_xpath('//*[@id="hdp"]/div[2]/div[1]/div[4]/div/div[2]/div/div[2]/div[3]/div/div[2]').text
            # onetimefee
            Rent = Rent + ' ' +  rent + '/' + type.split(' ')[1] + " One Time Nestaway Fee :" + onetimefee.encode("utf-8") + "|| "

            #except Exception as e:
            #    continue
        #//*[@id="hdp"]/div[2]/div[1]/div[4]/div/div[2]/div/div[1]/div[1]
        Security = self.browser1.find_element_by_xpath("//div[@class = 'securityDepositeWidget']").text
        #rent_security = self.browser1.find_elements_by_xpath("//div[@class = 'rentSecurity']")
        Rent_Security  = Rent + ' ' +  Security
        #for rs in rent_security:
        #    Rent_Security = Rent_Security + rs.text
        Rent_Security = Rent_Security.encode("utf-8").replace('₹',"Rs.")
        Gender = self.browser1.find_element_by_xpath('//div[@class = "lastSection"]').text
        
        Details["Name"].append(Name)
        Details["Address"].append(Address)
        Details["Gender"].append(Gender)
        Details['Rent_Security'].append(Rent_Security)
        Details["Features"].append(Features)
        Details["Amenities"].append(Amenities)
        
        #print(Details)

    def get_images(self):
        time.sleep(2)
        IMG = []
        new_len = len(IMG)
        old_len = -1
        while True:
            imgs = self.browser1.find_elements_by_xpath("//div[@class = 'Image']")
            for i in imgs:
                url = i.get_attribute('style')
                url = url[23:len(url)-3]
                if url not in IMG:
                    IMG.append(url)
            new_len = len(IMG)
            if old_len == new_len:
                break
            else:
                old_len = new_len
            for i in range(3):
                next_btn = self.browser1.find_element_by_xpath('//div[@class = "HouseGallery"]//div[@style = "position: absolute; top: 50%; transform: translateY(-50%); right: 0px; padding: 20px; touch-action: none; cursor: pointer;"]')
                mouse_click = ActionChains(self.browser1).double_click(next_btn)
                mouse_click.perform()
                time.sleep(2)
        print(new_len)
        Details["Images"].append(IMG)
        print(Details["Images"])

    def close(self):
        self.browser1.close()

start = time.time()
dbfile = open('city_links','rb')
while 1:
    try:
        City_Links = pickle.load(dbfile)
    except EOFError:
        break
dbfile.close()
city_name = sys.argv[1]
type = room_type[sys.argv[2]]
if city_name in City_Links.keys():
    if type in City_Links[city_name].keys():
        print("Number of available links for {} {}is ".format(city_name,type) + str(len(City_Links[city_name][type])))
        links = City_Links[city_name][type]
        Low_site = int(input("Enter the lower link id"))
        High_site = int(input("Enter the higher link id"))
        print(Low_site)
        print(High_site)
        if Low_site > 0 and High_site <= len(links):
            for lk in range(Low_site-1,High_site):
                #if 'houses' in links[lk]:
                while True:
                    try:
                        obj = TextScrapper(links[lk])
                       # obj.details()
                        obj.get_images()
                        Details["Id"].append(lk+1)
                        Details["Link"].append(links[lk])
                        obj.close()
                        break
                    except Exception as x:
                        print(x)
                        print("Waiting")
                        time.sleep(20)
            columns = ['Id','Link','Name','Address','Gender','Rent_Security','Features','Amenities','Images']
            df = pd.DataFrame(Details,columns = columns)
            filename = "{}_{}.csv".format(city_name,type)
            df.to_csv(filename,mode = 'a',header = False,columns = columns,encoding = 'utf-8')
        else:
            print("Wrong Range")
    else:
        print("The particular room type is not there")
else:
    print("The particular city is not there")
end = time.time()
print(end-start)