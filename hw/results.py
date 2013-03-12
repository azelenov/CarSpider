import random
from selenium.common.exceptions import NoSuchElementException
import sys
import search

import locators
from settings import main_config
import datetime
import time


class IntlResults(search.IntlSearch):
    def __init__(self,browsers,params):
        self.locations = main_config['loc_list']
        self.wait = main_config['wait']
        self.attempts = main_config['attempts']
        #self.url = domain
        self.drivers = browsers
        self.config = params
        wait_me = main_config['wait_element']
        for driver in self.drivers:
          #assert "Search results" in driver.page_source
          self.params = params[self.drivers.index(driver)]
          self.engine = driver
          self.load_test()
          self.verify_results()
          self.rand_solution()


    def verify_results(self):
        time.sleep(2)
        try:
            self.cfind("seleniumResultItem")

        except NoSuchElementException:
            self.log("No results found!")
            self.log("Search attempts left:"+str(self.attempts))

            self.refill()
            if self.attempts > 0:
               self.attempts -= 1
               self.verify_results()
            else:
               self.log("No attemps left...Sorry")
               sys.exit()
        else:
             self.log(self.cfind("searchResultsHeader").text)

    def refill (self):
        self.autocomplete = False
        self.set_locations()
        self.type_date(True)
        self.submit()
        self.load_test()

    def rand_solution(self):
        solutions = self.engine.find_elements_by_class_name("seleniumResultItem")
        rand_sol = random.choice(solutions)
        car_name = self.cfind("seleniumModelName",rand_sol).text
        self.log(car_name+" SIPP: "+rand_sol.get_attribute("data-sipp-code"))
        Btn = self.cfind("btn",rand_sol)
        link= Btn.get_attribute("href")
        Btn.click()
        self.log("Details page: "+link)





