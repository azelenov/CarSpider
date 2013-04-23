from settings import main_config
from datetime import date,timedelta
import time
import random
from selenium.webdriver.common.keys import Keys
from time import asctime
import os
import threading


class Search(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue


    def log(self,message):
        t = asctime()
        name = self.engine.name
        print "[{}]<{}> {}".format(t,name,message)

    def get_currency(self,cur):
        currencies = main_config['currency']
        if cur:
            if cur == 'random': cur = random.choice(currencies)
            elif cur == 'other':
                  currencies.remove('USD')
                  currencies.remove('GBP')
                  currencies.remove('EUR')
                  cur = random.choice(currencies)
            cur = cur.upper()
            if cur in currencies:
                return cur
                self.log("Currency: "+cur)
            else:
                 print "Currency "+cur+" not available!"
        else:
             print "Default currency"

    def get_dates(self):
        start = self.params['days_left']
        long = self.params['trip_duration']
        while True:
              self.log("Randomizing dates")
              if start == 'random':
                 s = random.randint(1,330)
              else:
                 s = int(start)
              if long == 'random':
                 l = random.randint(1,60)
              else:
                 l = int(long)
              d = s + l
              if d < 330: break
        pick = date.today() + timedelta(days=s)
        drop = date.today() + timedelta(days=d)
        return self.date_format(pick),self.date_format(drop)

    def date_format(self,D):
        year,mon,day = D.timetuple()[:3]
        sdate = "/".join([str(mon),str(day),str(year)[2:]])
        return sdate

    def type_date(self):
         pick_day,drop_day = self.get_dates()
         p_date = self.engine.find(name='startDate')
         p_date.clear()
         p_date.send_keys(pick_day)
         p_date.send_keys(Keys.TAB)
         d_date = self.engine.find(name='endDate')
         d_date.clear()
         d_date.send_keys(drop_day)
         d_date.send_keys(Keys.TAB)

    def type_location(self,search_type):
        if search_type == 'random':
           _files = os.listdir(main_config['lists_dir']
             +"/"+self.params['location_list'])
           _files = [f.replace('.txt','') for f in _files]
           search_type = random.choice(_files)
        if search_type == 'air':
           self.type_air()
        elif search_type == 'city':
           self.type_city()
        elif search_type == 'zip':
           self.type_zip()
        else:
           self.locator.clear().send_keys(search_type)

    def random_location (self,list_name):
        path = main_config['lists_dir']+"/"+list_name
        with open(path) as l:
             vars = l.readlines()
             random.shuffle(vars)
             loc = vars[0].strip()
        return loc

    def type_air(self):
        _list = self.params['location_list']+'/'+'air.txt'
        loc = self.random_location(_list)
        print loc
        self.locator.clear().send_keys(loc)
        #self.log("Airport: "+loc)
        #if self.autocomplete:
           #self.xtype(elem_name,loc)
           #time.sleep(self.wait/4)
           #a = self.cfind('airplane')
           #a.click()
        #else:
           #self.xtype(elem_name,loc)

    def type_zip(self):
        _list = self.params['location_list']+'/'+'zip.txt'
        loc = self.random_location(_list)
        print loc
        self.locator.clear().send_keys(loc)

    def type_city(self):
        _list = self.params['location_list']+'/'+'city.txt'
        loc = self.random_location(_list)
        self.log("City: "+loc)
        self.locator.clear().send_keys(loc)

##        city,country = loc.split(', ')
##        self.locator.clear().send_keys(city)
##        time.sleep(main_config['ui_wait'])
##        self.locator.send_keys(', '+country)
##        time.sleep(main_config['ui_wait'])


class SearchIntl(Search):
      def __init__(self,params,engine):
          print "International search"
          Search.engine = engine
          Search.params = params
          assert "Car Hire" in self.engine.title
          self.fill()

      def fill (self):
          self.set_currency()
          self.set_locations()
          self.type_date()
          self.type_age()
          self.find()

      def set_currency(self):
          self.log('Setting currency')
          cur = self.get_currency(self.params['currency'])
          self.engine.find(id='currencyCode-button').click()
          self.engine.find(class_name=cur).click()

      def set_locations(self):
          Search.locator = self.engine.find(class_name='seleniumPickupLocation')
          if self.params['drop_location']:
             self.oneway()
             self.type_location(self.params['pick_location'])
             Search.locator = self.engine.find(class_name='seleniumDropoffLocation')
             self.type_location(self.params['drop_location'])
          else:
             self.type_location(self.params['pick_location'])

      def oneway(self):
           self.log("Switch to one way trip")
           self.engine.find(class_name='seleniumCarOneWay').click()

      def date_format(self,D):
           year,mon,day = D.timetuple()[:3]
           sdate = "/".join([str(day),str(mon),str(year)[2:]])
           return sdate

      def type_age(self):
           if self.params['driver_age'] == 'random':
              age = str(random.randint(25,75))
           else:
              age = self.params['driver_age']
           self.engine.find(name='driverAge').clear().send_keys(age)

      def find(self):
           self.log("Searching...")
           self.engine.find(class_name='seleniumContinueButton').click()

class SearchDomestic(Search):
      def __init__(self,params,engine):
          print "Domestic search"
          Search.engine = engine
          Search.params = params
          assert "Cheap" in self.engine.title
          self.fill()

      def fill (self):
          self.set_currency()
          cur = self.get_currency(self.params['currency'])
          self.set_locations()
          self.type_date()
          self.find()

      def set_currency(self):
          cur = self.get_currency(self.params['currency'])
          form = self.engine.find(name='selectCurrencyForm')
          form.click()
          self.engine.find(value=cur).click()
          form.submit()
          #time.sleep(1)

      def set_locations(self):
          Search.locator = self.engine.find(name='startLocation')
          print Search.locator.is_displayed
          if self.params['drop_location']:
             self.oneway()
             self.type_location(self.params['pick_location'])
             Search.locator = self.engine.find(name='endLocation')
             self.type_location(self.params['drop_location'])
          else:
             self.type_location(self.params['pick_location'])

      def oneway(self):
           self.log("Switch to one way trip")
           self.engine.find(id='carOneWay').click()

      def find(self):
          try:
              self.engine.find(name='selectedPartners').uncheck()
          except:
              self.log("no partners on page")
          finally:
              self.engine.find(type='submit').click()

class SearchCCF(SearchDomestic):
      def __init__(self,params,engine):
          print "CCF search"
          Search.engine = engine
          Search.params = params
          assert "Cheap" in self.engine.title
          self.fill()


##class SearchIntl():
##    autocomplete = main_config['autocomplete']
##    locations = main_config['loc_list']
##    wait = main_config['wait']
##    attempts = main_config['attempts']
##    wait_me = main_config['wait_element']
##
##    def __init__(self,domain,browsers,params):
##
##        self.url = domain
##        #autocomplete is only available in one browser testing
##        if len(browsers) > 1: self.autocomplete = False
##        print "Checking autocomplete:",self.autocomplete
##        self.drivers = browsers
##        self.config = params
##        for b in browsers:
##            b.implicitly_wait(self.wait_me)
##            #b.delete_all_cookies()
##            b.get(self.url)
##
##
##    def xfind(self,loc_name,element = None):
##        if element:
##           res = element.find_element_by_xpath(locators.intl[loc_name])
##        else:
##           res = self.engine.find_element_by_xpath(locators.intl[loc_name])
##        return res
##
##    def xclick(self,loc_name,element = None):
##        self.xfind(loc_name,element).click()
##
##    def xtype(self,elem_name,text,enter = False):
##        #print elem_name
##        loc = self.xfind(elem_name)
##        #print loc
##        loc.clear()
##        loc.send_keys(text)
##        if enter: loc.send_keys(Keys.ENTER)
##
##    def submit(self):
##         self.xfind('submit').click()
##
##    def cfind(self,class_name,element = None):
##        if element:
##           res = element.find_element_by_class_name(class_name)
##        else:
##             res = self.engine.find_element_by_class_name(class_name)
##        return res
##
##    def click_text(self,link_text):
##        t = self.engine.find_element_by_link_text(link_text)
##        time.sleep(self.wait/2)
##        t.click()
##
##    def load_test(self):
##        mask = self.cfind("mask")
##        timer = 1
##        self.log("Waiting ...")
##        time.sleep(timer)
##        flag = mask.is_displayed()
##        while  flag:
##            mask = self.cfind("mask")
##            flag = mask.is_displayed()
##            time.sleep(1)
##            timer += 1
##        self.log("Page loaded. Load time: "+str(timer)+" seconds")
##
##    def log(self,message):
##        t = asctime()
##        name = self.engine.name
##        print "[{}]<{}> {}".format(t,name,message)
##
##    def fill (self,age = None,cur = None):
##        for driver in self.drivers:
##            assert "Car Hire" in driver.title
##            print driver.name
##            self.params = self.config[self.drivers.index(driver)]
##            self.engine = driver
##            print self.params
##            self.set_currency()
##            self.set_locations()
##
##            self.type_date()
##            #self.type_date("dropoff_date",nextdate)
##            if age: self.type_age()
##            self.go()
##
##

##
##    def set_locations(self):
##        params = self.params
##        if params.has_key("dropoff_loc") and params["dropoff_loc"]:
##           self.oneway()
##           self.type_location("pickup_loc")
##           self.type_location("dropoff_loc")
##        else:
##           self.type_location("pickup_loc")
##
##    def oneway(self):
##        self.log("Switch to one way trip")
##        self.xfind('oneway').click()
##        time.sleep(self.wait)
##
##    def type_location(self,field):
##        mode = self.params[field]
##        if mode == 'air':
##           self.type_air(field)
##        elif mode == 'city':
##           self.type_city(field)
##        elif mode == 'zip':
##           self.type_zip(field)
##        else:
##           self.xtype(field,mode)
##
##    def type_air(self,elem_name):
##        loc = self.random_location(self.locations['air'])
##        self.log("Airport: "+loc)
##        if self.autocomplete:
##           self.xtype(elem_name,loc)
##           time.sleep(self.wait/4)
##           a = self.cfind('airplane')
##           a.click()
##        else:
##           self.xtype(elem_name,loc)
##
##
##    def type_zip(self,elem_name):
##        loc = self.random_location(self.locations['zip'])
##        self.log("Zipcode: "+loc)
##        self.xtype(elem_name,loc)
##        time.sleep(self.wait)
##
##    def type_city(self,elem_name):
##        loc = self.random_location(self.locations['city'])
##        self.log("City: "+loc)
##        city,country = loc.split(', ')
##        self.xtype(elem_name,city)
##        time.sleep(self.wait)
##        self.xfind(elem_name).send_keys(', '+country)
##        time.sleep(self.wait)
##
##    def type_cities(self,elem_name):
##        locs = self.all_locations(self.locations['city'])
##        for loc in locs:
##            print "City:", loc
##            city,country = loc.split(', ')
##            self.xtype(elem_name,city)
##            time.sleep(self.wait*2)
##            self.xfind(elem_name).send_keys(', '+country)
##            time.sleep(self.wait*5)
##
##    def type_date(self,enter = False):
##        tomorrow = date.today() + timedelta(days=1)
##        nextday = date.today() + timedelta(days=4)
##        if self.autocomplete:
##           cal = self.xfind("pickup_date")
##           cal.click()
##           self.click_text(str(tomorrow.day))
##        else:
##           self.xtype("pickup_date",self.date_format(tomorrow),enter)
##           self.xtype("dropoff_date",self.date_format(nextday),enter)
##
##
##    def date_format(self,D):
##        year,mon,day = D.timetuple()[:3]
##        sdate = "/".join([str(day),str(mon),str(year)])
##        return sdate
##
##
##    def type_age(self,age=None):
##        if not age:
##           dr_age = str(random.randint(25,50))
##        else:
##             dr_age = age
##        if self.autocomplete:
##           self.log("Driver age: "+dr_age)
##           self.xtype('age',dr_age,False)
##        else:
##           self.xtype('age',dr_age,True)
##
##    def go(self):
##        if self.autocomplete:
##           self.submit()
##        time.sleep(1)
##
##    def verify(self):
##        try:
##            assert "Error" not in self.engine.page_source
##        except AssertionError:
##            if self.attempts > 0:
##               self.attempts -= 1
##               self.log("Error on page")
##               self.log("Search attempts left:"+self.attempts)
##               self.fill()
##            else:
##               self.log("No attemps left...Sorry")
##               sys.exit()
##
##    def random_location (self,list_name):
##        path = main_config['lists_dir']+"/"+list_name
##        with open(path) as l:
##             vars = l.readlines()
##             random.shuffle(vars)
##             loc = vars[0].strip()
##        return loc
##
##    def all_locations (self,list_name):
##        path = main_config['lists_dir']+"/"+list_name
##        with open(path) as l:
##             vars = l.readlines()
##        return vars
##
##def find(url,drivers,scenario, fill = True):
##    if main_config["domain"] == 'uk':
##       s = IntlSearch(url,drivers,scenario)
##    if fill:
##       s.fill(age=True,cur=True)
