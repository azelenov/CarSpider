import locators
from settings import main_config
from datetime import date,timedelta
import time
import sys
import random
from selenium.webdriver.common.keys import Keys
from time import asctime



class IntlSearch:
    autocomplete = main_config['autocomplete']
    locations = main_config['loc_list']
    wait = main_config['wait']
    attempts = main_config['attempts']
    wait_me = main_config['wait_element']

    def __init__(self,domain,browsers,params):

        self.url = domain
        #autocomplete is only available in one browser testing
        if len(browsers) > 1: self.autocomplete = False
        print "Checking autocomplete:",self.autocomplete
        self.drivers = browsers
        self.config = params
        for b in browsers:
            b.implicitly_wait(self.wait_me)
            #b.delete_all_cookies()
            b.get(self.url)


    def xfind(self,loc_name,element = None):
        if element:
           try:
               res = element.find_element_by_xpath(locators.intl[loc_name])
               return res
           except:
               self.log(loc_name + " not found")
        else:
           try:
               res = self.engine.find_element_by_xpath(locators.intl[loc_name])
               return res
           except:
               self.log(loc_name + " not found")


    def xclick(self,loc_name,element = None):
        self.xfind(loc_name,element).click()

    def xtype(self,elem_name,text,enter = False):
        #print elem_name
        loc = self.xfind(elem_name)
        #print loc
        loc.clear()
        loc.send_keys(text)
        if enter: loc.send_keys(Keys.ENTER)

    def submit(self):
         self.xfind('submit').click()

    def cfind(self,class_name,element = None):
        if element:
           res = element.find_element_by_class_name(class_name)
        else:
             res = self.engine.find_element_by_class_name(class_name)
        return res

    def click_text(self,link_text):
        t = self.engine.find_element_by_link_text(link_text)
        time.sleep(self.wait/2)
        t.click()

    def load_test(self):
        mask = self.cfind("mask")
        timer = 0
        self.log("Waiting ...")
        #time.sleep(timer)
        flag = mask.is_displayed()
        while  flag:
            mask = self.cfind("mask")
            flag = mask.is_displayed()
            time.sleep(1)
            timer += 1
        self.log("Page loaded. Load time: "+str(timer)+" seconds")

    def log(self,message):
        t = asctime()
        name = self.engine.name
        print "[{}]<{}> {}".format(t,name,message)

    def fill (self,age = None,cur = None):
        for driver in self.drivers:
            assert "Car Hire" in driver.title
            print driver.name
            self.params = self.config[self.drivers.index(driver)]
            self.engine = driver
            print self.params
            self.set_currency()
            self.set_locations()

            self.type_date()
            #self.type_date("dropoff_date",nextdate)
            if age: self.type_age()
            self.go()


    def set_currency(self):
        cur = self.params.get('currency')
        currencies = main_config['currency']

        if cur:
            cur = cur.upper()

            if cur == 'RND': cur = random.choice(currencies)
            elif cur == 'OTR':
                  currencies.remove('USD')
                  currencies.remove('GBP')
                  currencies.remove('EUR')
                  cur = random.choice(currencies)
            if cur in currencies:
                self.xfind('currency').click()
                self.cfind(cur).click()
                self.log("Currency: "+cur)
                time.sleep(self.wait)
            else:
                 sys.exit("Currency "+cur+" not available!")
        else:
             self.log("Default currency")

    def set_locations(self):
        params = self.params
        if params.has_key("dropoff_loc") and params["dropoff_loc"]:
           self.oneway()
           self.type_location("pickup_loc")
           self.type_location("dropoff_loc")
        else:
           self.type_location("pickup_loc")

    def oneway(self):
        self.log("Switch to one way trip")
        self.xfind('oneway').click()
        time.sleep(self.wait)

    def type_location(self,field):
        mode = self.params[field]
        if mode == 'air':
           self.type_air(field)
        elif mode == 'city':
           self.type_city(field)
        elif mode == 'zip':
           self.type_zip(field)
        else:
           self.xtype(field,mode)

    def type_air(self,elem_name):
        loc = self.random_location(self.locations['air'])
        self.log("Airport: "+loc)
        if self.autocomplete:
           self.xtype(elem_name,loc)
           time.sleep(self.wait/4)
           a = self.cfind('airplane')
           a.click()
        else:
           self.xtype(elem_name,loc)

    def type_zip(self,elem_name):
        loc = self.random_location(self.locations['zip'])
        self.log("Zipcode: "+loc)
        self.xtype(elem_name,loc)
        time.sleep(self.wait)

    def type_city(self,elem_name):
        loc = self.random_location(self.locations['city'])
        self.log("City: "+loc)
        city,country = loc.split(', ')
        self.xtype(elem_name,city)
        time.sleep(self.wait)
        self.xfind(elem_name).send_keys(', '+country)
        time.sleep(self.wait)

    def type_cities(self,elem_name):
        locs = self.all_locations(self.locations['city'])
        for loc in locs:
            print "City:", loc
            city,country = loc.split(', ')
            self.xtype(elem_name,city)
            time.sleep(self.wait*2)
            self.xfind(elem_name).send_keys(', '+country)
            time.sleep(self.wait*5)

    def type_date(self,enter = False):
        tomorrow = date.today() + timedelta(days=1)
        nextday = date.today() + timedelta(days=4)
        if self.autocomplete:
           cal = self.xfind("pickup_date")
           cal.click()
           self.click_text(str(tomorrow.day))
        else:
           self.xtype("pickup_date",self.date_format(tomorrow),enter)
           self.xtype("dropoff_date",self.date_format(nextday),enter)

    def date_format(self,D):
        year,mon,day = D.timetuple()[:3]
        sdate = "/".join([str(day),str(mon),str(year)])
        return sdate

    def type_age(self,age=None):
        if not age:
           dr_age = str(random.randint(25,50))
        else:
             dr_age = age
        if self.autocomplete:
           self.log("Driver age: "+dr_age)
           self.xtype('age',dr_age,False)
        else:
           self.xtype('age',dr_age,True)

    def go(self):
        if self.autocomplete:
           self.submit()
        time.sleep(1)

    def verify(self):
        try:
            assert "Error" not in self.engine.page_source
        except AssertionError:
            if self.attempts > 0:
               self.attempts -= 1
               self.log("Error on page")
               self.log("Search attempts left:"+self.attempts)
               self.fill()
            else:
               self.log("No attemps left...Sorry")
               sys.exit()

    def random_location (self,list_name):
        path = main_config['lists_dir']+"/"+list_name
        with open(path) as l:
             vars = l.readlines()
             random.shuffle(vars)
             loc = vars[0].strip()
        return loc

    def all_locations (self,list_name):
        path = main_config['lists_dir']+"/"+list_name
        with open(path) as l:
             vars = l.readlines()
        return vars

def find(url,drivers,scenario, fill = True):
    if main_config["domain"] == 'uk':
       s = IntlSearch(url,drivers,scenario)
    if fill:
       s.fill(age=True,cur=True)