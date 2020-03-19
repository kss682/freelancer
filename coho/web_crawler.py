import time
import sys
import pickle
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

Details = defaultdict(list)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
PATH = "/home/srinidhi/chromedriver"

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

class TextScrapper:
    def __init__(self,url):
        self.browser = webdriver.Chrome(executable_path = PATH,chrome_options = options)
        self.browser.get(url)

    def details(self):
        Name = self.browser.find_element_by_xpath("//div[@class = 'detail_near']//h1").text
        amenities = self.browser.find_elements_by_xpath("//div[@class = 'detail_ami']//div[@class = 'ami_box amclass']//li")
        Amenities = []
        for amn in amenities:
            Amenities.append(amn.text)
        overview = self.browser.find_elements_by_xpath("//div[@class = 'detail_loung_area']//div[@class = 'lounge_text']")
        Overview = " "
        for ov in overview:
            Overview = Overview + ' , ' + ov.text
        images = self.browser.find_elements_by_xpath("//div[@class = 'detail_loung_area']//div[@class = 'lounge_image']//a")
        imgs = []
        for i in images:
            href = i.get_attribute('href')
            if 'assets' in href:
                imgs.append(href)

    def close(self):
        self.browser.close()
            
City_Links = read_from_pickle()
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

        columns = ['Id','Name','Address','Gender','Rent','Overview','Amenities','Images']
        df = pd.DataFrame(Details,columns = columns)
        filename = "%s.csv"%city_name
        df.to_csv(filename,mode = 'a',header = False,columns = columns,encoding = 'utf-8')
    else:
        print("Wrong range of link id")
else:
    print("{} links not in city links".format(city_name))
