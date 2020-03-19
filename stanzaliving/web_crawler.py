# -*- coding: utf-8 -*-
from selenium import webdriver
from collections import defaultdict
import pandas as pd
import csv
import sys
import pickle

Details = defaultdict(list)

PATH = "/home/srinidhi/chromedriver"

Details = defaultdict(list)

class TextScrapper:
    def __init__(self,url):
        self.browser1 = webdriver.Chrome(executable_path = PATH)
        self.browser1.get(url)

    def details(self):
        name = self.browser1.find_element_by_xpath('//*[@class="residenceDetailMainSection__ResidenceTitle-zp1koj-1 pSmdV"]').text
        des = self.browser1.find_element_by_xpath('//*[@class="aboutResidenceDetail__AboutDetail-sc-1xseatz-1 eNRyMY"]').text
        loc = des.split(",")[0]
        action = self.browser1.find_elements_by_xpath('//*[@class="residenceIncludeSection__TabContainer-sc-1gv6zsp-2 heDQoy"]/div')
        roomfeaturelist = defaultdict(list)
        for z in action:
        #Click on Room amenities like Room features .....
            st = z.click()
            z = z.text
            roomfeature = self.browser1.find_elements_by_xpath('//*[@class="residenceIncludeSection__GridTitle-sc-1gv6zsp-6 kRSgJn"]')
            for y in roomfeature:
            #Room amenities dictionary
                roomfeaturelist[z].append(y.text)
        gender = self.browser1.find_element_by_xpath("//p[contains(@class,'residenceDetailMainSection__ResidenceAdd-zp1koj-2')]").text
        gender = gender.split("|")
        location = loc + "," + gender[0]
        roomtype = self.browser1.find_elements_by_xpath('//*[@class="residenceDetailOccupancy__OccTitle-vtazqv-8 cFNLZE"]')
        roomprice = self.browser1.find_elements_by_xpath('//*[@class="residenceDetailOccupancy__OccPrice-vtazqv-9 halzNF"]')
        length1 = len(roomtype)
        x = 0
        y = 0
        roomdetailslist = []
        while x < length1:
            con1 = roomtype[x].text
            con2 = roomprice[y].text
            con3 = roomprice[y+1].text
            con2 = con2.encode('utf-8').replace("₹","Rs.")
            con = con1 + " " + str(con2) + con3
            roomdetailslist.append(con)
            y = y + 2
            x = x + 1
        image = self.browser1.find_elements_by_xpath('//li[@class="residenceDetailMainSection__CarousalImgLI-zp1koj-8 eUkiOg"]/img')
        imglist = []
        for y in image:
            images = y.get_attribute('src')
            #image link list
            imglist.append(images)
            #print (imglist)
    #Write on CSV file
        Details['Name'].append(name)
        Details['Gender'].append(gender[1])
        Details['Address'].append(location)
        Details['RoomType_Rent'].append(roomdetailslist)
        Details['Overview'].append(des)
        Details['Amenities'].append(roomfeaturelist)
        Details['Images'].append(imglist)
        print(name,gender[1],location,des,roomfeaturelist,roomdetailslist,imglist)

    def close(self):
        self.browser1.close()

dbfile = open('city_links','rb')
while 1:
    try:
        City_Links = pickle.load(dbfile)
    except EOFError:
        break
dbfile.close()
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
        columns = ['Id','Name','Address','Gender','RoomType_Rent','Overview','Amenities','Images']
        df = pd.DataFrame(Details,columns = columns)
        filename = "%s.csv"%city_name
        df.to_csv(filename,mode = 'a',header = False,columns = columns,encoding = 'utf-8')
    else:
            print("Wrong Range")
else:
    print("{}'s links is not crawled please collect the links".format(city_name))
