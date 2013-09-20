import random
from selenium.common.exceptions import NoSuchElementException
from settings import main_config
from selenium.webdriver.common.keys import Keys
from time import asctime
import search
import re
import time
import locators


class Results(search.Search):
    '''Car results page classes'''
    def choose_car(self, results):
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

    def first_solution(self, results):
        self.log("First solution")
        return results[0]

    def last_solution(self, results):
        self.log("Last solution")
        return results[-1]

    def rand_solution(self, results):
        self.log("Random solution")
        return random.choice(results)

    def get_results(self):
        self.log(self.get_version_tests())
        self.log("Verifing results")
        try:
            _rs = self.engine.find(**self.path['result'])
            return _rs
        except:
            self.log("No results")
            self.retry()

    def retry(self):
        if self.attemps > 0:
            self.attemps -= 1
            self.log("Retring search. Attemps left: " + str(self.attemps))
            self.re_fill()
            self.get_details()
        else:
            self.log("Can't find results. No attemps left")

    def update(self):
        url = self.engine.current_url
        if re.search(self.url_pattern, url):
            self.re_fill()
            return True
        else:
            return False

    def re_fill(self):
        self.set_locations()
        self.type_date()
        self.find()


class ResultsIntl(search.SearchIntl, Results):
    def __init__(self, params, engine, attemps):
        self.engine = engine
        self.params = params
        self.attemps = attemps
        self.url_pattern = "/results/"
        self.path = locators.search['International']
        self.path.update(locators.results['International'])

    def get_details(self):
        results = self.get_results()
        if results:
            self.log("Found " + str(len(results)) + " results")
            car = self.choose_car(results)
            car.find(**self.path['continue']).click()


class ResultsDomestic(search.SearchDomestic, Results):
    def __init__(self, params, engine, attemps):
        self.engine = engine
        self.params = params
        self.attemps = attemps
        self.url_pattern = "results.jsp"
        self.path = locators.search['Domestic']
        self.path.update(locators.results['Domestic'])
        self.res_type = params['solution']

    def get_details(self):
        #self.engine.wait_for(class_name="commonResultsPage")
        results = self.get_results()
        self.log("Found "+str(len(results))+" results/opaque results")
        car = self.choose_car(results)
        if car:
            car.find(**self.path['continue']).click()

    def opaque_solution(self, results):
        self.log("Opaque solution")
        try:
            _rs = results.find(*self.path['retail'])
            opaque = results - _rs.parent().parent()
            _result = random.choice(opaque)
            return _result
        except:
            self.log("No opaque solutions")
            self.retry()

    def retail_solution(self, results):
        self.log("Retail solution")
        try:
            _rs = results.find(**self.path['retail'])
            _result = random.choice(_rs)
            return _result
        except:
            self.log("No retail solutions")
            self.retry()

    def find(self):
        self.engine.find(**self.path['search']).click()


class ResultsCCF(search.SearchCCF, Results):
    def __init__(self, params, engine, attemps):
        self.engine = engine
        self.params = params
        self.attemps = attemps
        self.url_pattern = '/(results|details|billing)/'
        self.res_type = params['solution']
        self.path = locators.search['CCF']
        self.path.update(locators.results['CCF'])

    def get_details(self):
        #self.engine.wait_for(class_name="content")
        results = self.get_results()
        self.log("Found "+str(len(results))+" results")
        car = self.choose_car(results)
        if car:
            car.click()
            time.sleep(1)
            self.engine.find(**self.path['continue']).click()

    def opaque_solution(self, results):
        self.log("Opaque solution")
        try:
            _rs = results.find(**self.path['opaque'])
            _result = random.choice(_rs)
            return _result
        except:
            self.log("No opaque solutions")
            self.retry()

    def retail_solution(self, results):
        self.log("Retail solution")
        try:
            _op = results.filter(**self.path['opaque'])
            _rs = results - _op
            assert len(_rs) > 0
        except:
            _rs = results
            _result = random.choice(_rs)
        return _result

    def set_locations(self):
        self.locator = self.engine.find(**self.path['pickup_loc'])
        if self.params['drop_location']:
            self.type_location(self.params['pick_location'])
            self.locator = self.engine.find(**self.path['dropoff_loc'])
            self.type_location(self.params['drop_location'])
        else:
            pick_loc = self.type_location(self.params['pick_location'])
            self.locator = self.engine.find(**self.path['dropoff_loc'])
            self.type_location(pick_loc)
