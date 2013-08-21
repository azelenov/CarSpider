import random
from selenium.common.exceptions import NoSuchElementException
from settings import main_config
from selenium.webdriver.common.keys import Keys
from time import asctime
import search
import re
import time

'''Car results page classes'''
class Results(search.Search):
    def choose_car(self,results):
        sol = self.params['solution']
        if sol == 'first':
           _car = self.first_solution(results)
        elif sol == 'last':
           _car = self.last_solution(results)
        elif sol == 'random':
           _car = self.rand_solution(results)
        else:
           print "This solution is not availale yet"
        return _car

    def first_solution(self,results):
        self.log("First solution")
        return results[0]

    def last_solution(self,results):
        self.log("Last solution")
        return results[-1]

    def rand_solution(self,results):
        self.log("Random solution")
        return random.choice(results)

class ResultsIntl(search.SearchIntl):
      def __init__(self,params,engine,attemps):
          self.engine = engine
          self.params = params
          self.attemps = attemps

      def get_details(self):
         self.engine.wait_for(class_name="centerWrapper")
         results = self.get_results()
         if results:
             self.log("Found "+str(len(results))+" results")
             r=Results()
             car = r.choose_car(results)
             car.find(link_text='Continue').click()

      def get_results(self):
          print self.get_version_tests()
          self.log("Verifing results")
          try:
              _rs = self.engine.find(class_name='seleniumResultItem')
              return _rs
          except:
              self.log("No results")
              self.retry()

      def update(self):
          url = self.engine.current_url
          if "/results/" in url:
           self.fill(rs_flag=True)
          else:
           self.home_page()
           self.fill()

class ResultsDomestic(search.SearchDomestic):
      def __init__(self,params,engine,attemps):
          self.engine = engine
          self.params = params
          self.attemps = attemps
          self.res_type = params['solution']

      def update(self):
          url = self.engine.current_url
          if "results.jsp" in url:
           self.fill(rs_flag=True)
          else:
           self.home_page()
           self.fill()

      def get_details(self):
          #self.engine.wait_for(class_name="commonResultsPage")
          results = self.get_results()
          self.log("Found "+str(len(results))+" results/opaque results")
          if self.res_type == 'opaque':
             car = self.opaque_solution()
             car.click()
          elif self.res_type == 'retail':
             car = self.retail_solution()
             car.click()
          else:
             r=Results()
             car = r.choose_car(results)
             car.find(class_name='continueBtn').click()

      def get_results(self):
          print self.get_version_tests()
          self.log("Verifing results")
          try:
              _rs = self.engine.find(class_name='resultWrapper')
              return _rs
          except:
              self.log("No results")
              self.retry()

      def opaque_solution(self):
          self.log("Opaque solution")
          try:
             _rs = self.engine.find(
                    xpath="//input[@data-retail='false']/following::input[2]")
             _result = random.choice(_rs)
             return _result
          except:
              self.log("No opaque solutions")
              self.retry()

      def retail_solution(self):
          self.log("Retail solution")
          try:
              _rs = self.engine.find(
                    xpath="//input[@data-retail='true']/following::input[2]")
              _result = random.choice(_rs)
              return _result
          except:
              self.log("No retail solutions")
              self.retry()

class ResultsCCF(search.SearchCCF):
      def __init__(self,params,engine,attemps):
          self.engine = engine
          self.params = params
          self.attemps = attemps
          self.res_type = params['solution']

      def update(self):
          url = self.engine.current_url
          if re.search('/(results|details|billing)/',url):
           self.refill()
          else:
           self.home_page()
           self.fill()

      def get_details(self):
          self.engine.wait_for(class_name="content")
          results = self.get_results()
          self.log("Found "+str(len(results))+" results")
          if self.res_type == 'opaque':
             car = self.opaque_solution(results)
          elif self.res_type == 'retail':
             car = self.retail_solution(results)
          else:
             r=Results()
             car = r.choose_car(results)
          if car:
             car_type = car.find(class_name="carTypeName").text
             self.log("Car type: "+car_type)
             car_url = car.get_attribute('href')
             print car_url
             car.click()
             billing_url = car_url.replace('details','billing')
             print billing_url
             time.sleep(1)
             self.engine.find(xpath='//a[@href="'+billing_url+'"]').click()
##             self.engine.wait_for(xpath='"//div[@id="carDetails"]//h3[@class="carTypeName"][text()='+car_type+']"')
##             self.engine.find(link_text_contains='Continue').click()

      def get_results(self):
          print self.get_version_tests()
          self.log("Verifing results")
          try:
              self.engine.wait_for(".result")

          except:
              self.log("No results")
              self.retry()
          else:
              _rs = self.engine.find('a').filter(".result")
              return _rs


      def opaque_solution(self,results):
          self.log("Opaque solution")
          try:
              _rs = results.filter(".hotRate")
              _result = random.choice(_rs)
              return _result
          except:
              self.log("No opaque solutions")
              self.retry()

      def retail_solution(self,results):
          self.log("Retail solution")
          try:
            _op = results.filter(".hotRate")
            _rs = results - _op
            assert len(_rs) > 0
          except:
            _rs = results
          _result = random.choice(_rs)
          return _result
