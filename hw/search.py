from settings import main_config
from datetime import date,timedelta
import time
import random
from selenium.webdriver.common.keys import Keys
from time import asctime
import os

class Search():
    def log(self,message):
        t = asctime()
        name = self.engine.name
        print "[{}]<{}> {}".format(t,name,message)

    def get_currency(self,cur):
        print main_config['currency']
        currencies = main_config['currency']
        if cur:
            if cur == 'random':
               cur = random.choice(currencies)
            elif cur == 'other':
                  #print currencies
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
          x = "//select[@name='selectedCurrencyCode']/option[text()='"+cur+"']"
          self.engine.find(xpath = x).click()
          time.sleep(0.5)

      def set_locations(self):
          Search.locator = self.engine.find(name='startLocation')
          print Search.locator.is_displayed
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
