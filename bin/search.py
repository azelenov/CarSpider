from settings import main_config,urls
from my_account import MyAccount

from datetime import date,timedelta
import time
import random
from selenium.webdriver.common.keys import Keys
from time import asctime
import os
import sys

class Search():
    def log(self,message):
        t = asctime()
        name = self.engine.name
        print "[{}]<{}> {}".format(t,name,message)

    def get_version_tests(self,evar='eVar1'):
        version_tests = self.engine.execute_script(
            "return AnalyticsSupport.getAnalyticsContextVariable('"+evar+"');")
        return version_tests

    def retry(self):
        if self.attemps >0:
             self.attemps -= 1
             self.log("Retring search. Attemps left: "+str(self.attemps))
             self.update()
             self.get_details()
        else:
             self.log("Can't find results. No attemps left")

    def get_currency(self,cur):
        currencies = main_config['currency']
        if cur:
            if cur == 'random':
               cur = random.choice(currencies)
            cur = cur.upper()
            if cur in currencies:
                return cur
                self.log("Currency: "+cur)
            else:
                self.log("Currency "+cur+" not available!")
        else:
             self.log("Default currency")

    def get_dates(self):
        if self.params["payment"] in ["PayPal","BillMeLater","HotDollars"] :
           self.params['solution'] = 'opaque'
           self.params['insurance'] = False
           self.log("Switching to opaque solution for PayPal, BML or HotDollars")
        start = self.params['days_left']
        long = self.params['trip_duration']
        while True:
              if start == 'random':
                 if self.params['solution'] == 'opaque':
                    s = random.randint(1,14)
                 else:
                    s = random.randint(1,330)
              else:
                 s = int(start)
              if long == 'random':
                 if self.params['solution'] == 'opaque':
                    l = random.randint(1,10)
                 else:
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
         self.log("Start date: "+pick_day)
         p_date.send_keys(pick_day)
         p_date.send_keys(Keys.TAB)
         d_date = self.engine.find(name='endDate')
         self.log("Start date: "+drop_day)
         d_date.clear()
         d_date.send_keys(drop_day)
         d_date.send_keys(Keys.TAB)

    def type_location(self,search_type):
        if search_type == 'random': search_type = self.rand_type()
        if search_type == 'air':
           place = self.type_air()
        elif search_type == 'city':
           place = self.type_city()
        elif search_type == 'zip':
           place = self.type_zip()
        else:
           place = search_type
           self.locator.clear().send_keys(place)
        return place

    def rand_type(self):
       _files = os.listdir(main_config['lists_dir']
         +"/"+self.params['location_list'])
       _files = [f.replace('.txt','') for f in _files]
       _search_type = random.choice(_files)
       return _search_type

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
        self.log("Airport: "+loc)
        self.locator.clear()
        self.locator.send_keys(loc)
        #self.engine.wait_for(class_name="airplane")
        #self.locator.send_keys(Keys.TAB)
        return loc

    def type_zip(self):
        _list = self.params['location_list']+'/'+'zip.txt'
        loc = self.random_location(_list)
        self.log("Zip code: "+loc)
        self.locator.clear().send_keys(loc)
        return loc

    def type_city(self):
        _list = self.params['location_list']+'/'+'city.txt'
        loc = self.random_location(_list)
        self.log("City: "+loc)
        self.locator.clear().send_keys(loc)
        return loc

    def sign_in(self):
        m = MyAccount(self.params,self.engine)
        if not m.is_logged():
            m.sign_in()
            self.home_page()

    def sign_out(self):
        m = MyAccount(self.params,self.engine)
        if m.is_logged():
            self.engine.delete_all_cookies()

class SearchIntl(Search):
      def __init__(self,params,engine):
          Search.engine = engine
          Search.params = params
          self.log("International search")
          self.home_page()
          if params['logged']:
            self.sign_in()
          else:
            self.sign_out()
          self.fill()

      def home_page(self):
          #if not self.engine.current_url.endswith("/car"):
          home = urls["International"][self.params['enviroment']]
          self.engine.get(home)
          print self.get_version_tests()
          self.log("Geting home page")
          try:
              assert "Car Hire" in self.engine.title
          except AssertionError:
              self.log("Site is down or timeout error")

      def fill (self,rs_flag = False):
          if not rs_flag: self.set_currency()
          self.set_locations()
          self.type_date()
          if not rs_flag:
             self.type_age()
          else:
             time.sleep(0.5)
          self.find()

      def set_currency(self):
          self.log('Setting currency')
          cur = self.get_currency(self.params['currency'])
          self.log('Currency: '+cur)
          self.engine.find(id='currencyCode-button').click()
          self.engine.find(class_name=cur).click()

      def set_locations(self):
          Search.locator = self.engine.find(class_name='seleniumPickupLocation')
          if self.params['drop_location']:
             self.oneway()
             self.type_location(self.params['pick_location'])
             Search.locator = self.engine.find(
                                class_name='seleniumDropoffLocation')
             self.type_location(self.params['drop_location'])
          else:
             self.round_trip()
             self.type_location(self.params['pick_location'])

      def oneway(self):
           self.log("Switch to one way trip")
           self.engine.find(class_name='seleniumCarOneWay').click()

      def round_trip(self):
           self.log("Switch to roundtrip")
           self.engine.find(class_name='seleniumCarRoundTrip').click()

      def date_format(self,D):
           year,mon,day = D.timetuple()[:3]
           sdate = "/".join([str(day),str(mon),str(year)[2:]])
           return sdate

      def type_age(self):
           if self.params['driver_age'] == 'random':
              age = str(random.randint(25,75))
           else:
              age = self.params['driver_age']
           self.log("Driver age: "+str(age))
           self.engine.find(name='driverAge').clear().send_keys(age)

      def find(self):
           find_btn = self.engine.find(xpath='//div[@class="searchBtn"]/button')
           find_btn.click()
           self.log("Searching...")

class SearchDomestic(Search):
      def __init__(self,params,engine):
          Search.engine = engine
          Search.params = params
          self.log("Domestic search")
          self.home_page()
          if params['logged']:
            self.sign_in()
          else:
            self.sign_out()
          self.home_page()
          self.fill()

      def home_page(self):
          #if not 'index.jsp' in self.engine.current_url:
          home = urls["Domestic"][self.params['enviroment']]
          self.engine.get(home)
          print self.get_version_tests()
          self.log("Geting home page")
          try:
              assert "Cheap" in self.engine.title
          except AssertionError:
              self.log("Site is down or timeout error")

      def fill (self,rs_flag=False):
          self.set_currency()
          self.set_locations()
          self.type_date()
          self.find(rs_flag)

      def set_currency(self):
          self.log('Setting currency')
          cur = self.get_currency(self.params['currency'])
          self.log('Currency: '+cur)
          x = "//select[@name='selectedCurrencyCode']/option[text()='" \
                +cur+"']"
          self.engine.find(xpath = x).click()
          time.sleep(0.5)

      def set_locations(self):
          Search.locator = self.engine.find(name='startLocation')
          if self.params['drop_location']:
             self.oneway()
             self.type_location(self.params['pick_location'])
             Search.locator = self.engine.find(name='endLocation')
             self.type_location(self.params['drop_location'])
          else:
             self.round_trip()
             self.type_location(self.params['pick_location'])

      def oneway(self):
           self.log("Switch to one way trip")
           self.engine.find(id='carOneWay').click()

      def round_trip(self):
           self.log("Switch to roundtrip")
           self.engine.find(id='carRoundTrip').click()

      def find(self,rs_flag=False):
          if "Compare with " in self.engine.page_source \
          and not rs_flag:
             self.engine.find(name='selectedPartners').uncheck()
          self.engine.find(
                    xpath='//form[@name="carIndexForm"]//button[@type="submit"]'
                     ).click()

class SearchCCF(SearchDomestic):
      def __init__(self,params,engine):
        Search.engine = engine
        Search.params = params
        self.log("CCF search")
        self.home_page()
        if params['logged']:
            self.sign_in()
        else:
            self.sign_out()
        self.home_page()
        self.fill()

      def home_page(self):
          home = urls["CCF"][self.params['enviroment']]
          self.engine.get(home)
          print self.get_version_tests()
          self.log("Geting home page")
          try:
              assert "Cheap" in self.engine.title
          except AssertionError:
              self.log("Site is down or timeout error")

      def refill(self):
        #self.rs_currency()
        self.rs_locations()
        self.type_date()
        self.update_results()

      def rs_currency(self):
        self.log('Setting currency')
        cur = self.get_currency(self.params['currency'])
        self.engine.find(name='selectCurrencyForm').click()
        self.engine.find(link_text=cur).click()

      def rs_locations(self):
          Search.locator = self.engine.find(name='pickupLocation')
          loc = self.type_location(self.params['pick_location'])
          Search.locator = self.engine.find(name='dropOffLocation')
          if self.params['drop_location']:
             self.type_location(self.params['drop_location'])
          else:
             self.type_location(loc)

      def update_results(self):
          if "Compare with " in self.engine.page_source \
          and "/results" not in self.engine.current_url:
             self.engine.find(name='selectedPartners').uncheck()
          self.engine.find(
                    xpath='//div[@class="searchBtn"]//button[@type="submit"]'
                    ).click()
