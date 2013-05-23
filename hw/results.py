import random
from selenium.common.exceptions import NoSuchElementException
from settings import main_config
from selenium.webdriver.common.keys import Keys
from time import asctime


class Results():
    def load_test(self):
        print "load_test"
##      mask = self.cfind("mask")
##      timer = 1
##      self.log("Waiting ...")
##      time.sleep(timer)
##      flag = mask.is_displayed()
##      while  flag:
##        mask = self.cfind("mask")
##        flag = mask.is_displayed()
##        time.sleep(1)
##        timer += 1
##      self.log("Page loaded. Load time: "+str(timer)+" seconds")


##        time.sleep(2)
##        try:
##            self.cfind("seleniumResultItem")
##
##        except NoSuchElementException:
##            self.log("No results found!")
##            self.log("Search attempts left:"+str(self.attempts))
##
##            self.refill()
##            if self.attempts > 0:
##               self.attempts -= 1
##               self.verify_results()
##            else:
##               self.log("No attemps left...Sorry")
##               sys.exit()
##        else:
##             self.log(self.cfind("searchResultsHeader").text)

    def choose_car(self,results):
        sol = self.params['solution']
        if sol == 'first':
           _car = self.first_solution(results)
        elif sol == 'last':
           _car = self.last_solution(results)
        elif sol == 'random':
           _car = self.rand_solution(results)
        elif sol == 'opaque':
           _car = self.opaque_solution(results)
        elif sol == 'retail':
           _car = self.retail_solution(results)
        else:
           print "This solution is not availale yet"
        return _car

    def first_solution(self,results):
        print "first solution"
        return results[0]

    def last_solution(self,results):
        print "last solution"
        return results[-1]

    def rand_solution(self,results):
        print "random solution"
        return random.choice(results)

##          solutions = self.engine.find_elements_by_class_name("seleniumResultItem")
##          rand_sol = random.choice(solutions)
##          car_name = self.cfind("seleniumModelName",rand_sol).text
##          self.log(car_name+" SIPP: "+rand_sol.get_attribute("data-sipp-code"))
##          Btn = self.cfind("btn",rand_sol)
##          link= Btn.get_attribute("href")
##          Btn.click()
##          self.log("Details page: "+link)

class ResultsIntl(Results):
      def __init__(self,params,engine):
          Results.engine = engine
          Results.params = params
          self.load_test()
          results = self.verify_results()
          car = self.choose_car(results)
          car.find(link_text='Continue').click()

##          self.details(car)
      def verify_results(self):
          print "verify results"
          _rs = self.engine.find(class_name='seleniumResultItem')
          return _rs
          #print results

class ResultsDomestic(Results):
      def __init__(self,params,engine):
          Results.engine = engine
          Results.params = params
          self.load_test()
          results = self.verify_results()
          car = self.choose_car(results)
          #car.find(tag_name='form').submit()

##          self.details(car)
      def verify_results(self):
          print "verify results"
          _rs = self.engine.find(class_name='resultWrapper')
          return _rs

      def opaque_solution(self,results):
          try:
              _rs = self.engine.find(xpath="//input[@data-retail='true']")
          except:
              print "not found"
          else:
               print "found"
               print _rs.text
          return _rs

      def retail_solution(self,results):
          print "retail solution unavalable"

class ResultsCCF(Results):
      def __init__(self,params,engine):
          Results.engine = engine
          Results.params = params
          self.load_test()
          results = self.verify_results()
          car = self.choose_car(results)
          car.click()

##          self.details(car)
      def verify_results(self):
          print "verify results"
          _rs = self.engine.find(class_name='result')
          return _rs

      def retail_solution(self,results):
          print "retail solution unavalable"

##class IntlResults(search.IntlSearch):
##    def __init__(self,browsers,params):
##        self.locations = main_config['loc_list']
##        self.wait = main_config['wait']
##        self.attempts = main_config['attempts']
##        #self.url = domain
##        self.drivers = browsers
##        self.config = params
##        wait_me = main_config['wait_element']
##        for driver in self.drivers:
##          #assert "Search results" in driver.page_source
##          self.params = params[self.drivers.index(driver)]
##          self.engine = driver
##          self.load_test()
##          self.verify_results()
##          self.rand_solution()
##
##

##
##    def refill (self):
##        self.autocomplete = False
##        self.set_locations()
##        self.type_date(True)
##        self.submit()
##        self.load_test()
##

