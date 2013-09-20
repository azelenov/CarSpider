from settings import main_config, urls, version_tests
from my_account import MyAccount
import locators

from datetime import date, timedelta
import time
import random
from selenium.webdriver.common.keys import Keys
from time import asctime
import os
import sys


class Search():
    def make_url(self, item):
        self.urls = urls[item['domain']]
        vt = version_tests[item['domain']]
        base_url = self.urls[item['enviroment']]
        if vt:
            url = base_url + "?vt." + vt[0]
            if vt:
                url = url + "&vt." + "&vt.".join(vt[1:])
        else:
            url = base_url
        return url

    def log(self, message):
        t = asctime()
        name = self.engine.name
        print "[{}]<{}> {}".format(t, name, message)

    def get_version_tests(self, evar='eVar1'):
        version_tests = "Version tests on page:" + \
            str(self.engine.execute_script("return AnalyticsSupport.\
                                           getAnalyticsContextVariable('" +
                                           evar + "');"))
        return version_tests

    def get_currency(self, cur):
        currencies = main_config['currency']
        if cur:
            if cur == 'random':
                cur = random.choice(currencies)
            cur = cur.upper()
            if cur in currencies:
                return cur
                self.log("Currency: " + cur)
            else:
                self.log("Currency " + cur + " not available!")
        else:
            self.log("Default currency")

    def get_dates(self):
        if self.params["payment"] in ["PayPal", "BillMeLater", "SavedBML"]:
            self.params['solution'] = 'opaque'
            self.params['insurance'] = False
            self.log("Switching to opaque solution for PayPal,"
                     + "BML")
        start = self.params['days_left']
        long = self.params['trip_duration']
        while True:
            if start == 'random':
                if self.params['solution'] == 'opaque':
                    s = random.randint(1, 14)
                else:
                    s = random.randint(1, 330)
            else:
                s = int(start)
            if long == 'random':
                if self.params['solution'] == 'opaque':
                    l = random.randint(1, 10)
                else:
                    l = random.randint(1, 60)
            else:
                l = int(long)
            d = s + l
            if d < 330:
                break
        pick = date.today() + timedelta(days=s)
        drop = date.today() + timedelta(days=d)
        return self.date_format(pick), self.date_format(drop)

    def date_format(self, D):
        year, mon, day = D.timetuple()[:3]
        sdate = "/".join([str(mon), str(day), str(year)[2:]])
        return sdate

    def type_date(self):
        pick_day, drop_day = self.get_dates()
        p_date = self.engine.find(name='startDate')
        p_date.clear()
        self.log("Start date: " + pick_day)
        p_date.send_keys(pick_day)
        p_date.send_keys(Keys.TAB)
        d_date = self.engine.find(name='endDate')
        self.log("Start date: " + drop_day)
        d_date.clear()
        d_date.send_keys(drop_day)
        d_date.send_keys(Keys.TAB)

    def type_location(self, search_type):
        if search_type == 'random':
            search_type = self.rand_type()
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
                            + "/" + self.params['location_list'])
        _files = [f.replace('.txt', '') for f in _files]
        _search_type = random.choice(_files)
        return _search_type

    def random_location(self, list_name):
        path = main_config['lists_dir'] + "/"+list_name
        with open(path) as l:
            vars = l.readlines()
            random.shuffle(vars)
            loc = vars[0].strip()
        return loc

    def type_air(self):
        _list = self.params['location_list'] + '/' + 'air.txt'
        loc = self.random_location(_list)
        self.log("Airport: " + loc)
        self.locator.clear()
        self.locator.send_keys(loc)
        return loc

    def type_zip(self):
        _list = self.params['location_list'] + '/' + 'zip.txt'
        loc = self.random_location(_list)
        self.log("Zip code: "+loc)
        self.locator.clear().send_keys(loc)
        return loc

    def type_city(self):
        _list = self.params['location_list'] + '/' + 'city.txt'
        loc = self.random_location(_list)
        self.log("City: " + loc)
        self.locator.clear().send_keys(loc)
        return loc

    def oneway(self):
        self.log("Switch to one way trip")
        self.engine.find(**self.path['oneway']).click()

    def round_trip(self):
        self.log("Switch to roundtrip")
        self.engine.find(**self.path['roundtrip']).click()

    def set_locations(self):
        self.locator = self.engine.find(**self.path['pickup_loc'])
        if self.params['drop_location']:
            self.oneway()
            self.type_location(self.params['pick_location'])
            self.locator = self.engine.find(**self.path['dropoff_loc'])
            self.type_location(self.params['drop_location'])
        else:
            self.round_trip()
            self.type_location(self.params['pick_location'])

    def sign_in(self):
        m = MyAccount(self.params, self.engine)
        if not m.is_logged():
            m.sign_in()
            self.home_page()

    def sign_out(self):
        m = MyAccount(self.params, self.engine)
        if m.is_logged():
            self.engine.delete_all_cookies()

    def fill(self):
        self.set_currency()
        self.set_locations()
        self.type_date()
        self.find()


class SearchIntl(Search):
    def __init__(self, params, engine):
        Search.engine = engine
        Search.params = params
        self.path = locators.search['International']
        self.log("International search")
        self.home_page()
        if params['logged']:
            self.sign_in()
        else:
            self.sign_out()
            self.fill()

    def home_page(self):
        home = self.make_url({'domain': "International",
                             'enviroment': self.params['enviroment']})
        self.engine.get(home)
        self.log(self.get_version_tests())
        self.log("Geting home page")
        try:
            assert "Car Hire" in self.engine.title
        except AssertionError:
            self.log("Site is down or timeout error")

    def fill(self):
        self.set_currency()
        self.set_locations()
        self.type_date()
        self.type_age()
        self.find()

    def set_currency(self):
        self.log('Setting currency')
        cur = self.get_currency(self.params['currency'])
        self.log('Currency: '+cur)
        self.engine.find(**self.path['currency']).click()
        self.engine.find(class_name=cur).click()

    def date_format(self, D):
        year, mon, day = D.timetuple()[:3]
        sdate = "/".join([str(day), str(mon), str(year)[2:]])
        return sdate

    def type_age(self):
        if self.params['driver_age'] == 'random':
            age = str(random.randint(25, 75))
        else:
            age = self.params['driver_age']
        self.log("Driver age: " + str(age))
        self.engine.find(**self.path['age']).clear().send_keys(age)

    def find(self):
        time.sleep(0.5)
        self.engine.find(**self.path['search']).click()
        self.log("Searching...")


class SearchDomestic(Search):
    def __init__(self, params, engine):
        Search.engine = engine
        Search.params = params
        self.path = locators.search['Domestic']
        self.log("Domestic search")
        self.home_page()
        if params['logged']:
            self.sign_in()
        else:
            self.sign_out()
        self.fill()

    def home_page(self):
        #if not 'index.jsp' in self.engine.current_url:
        home = self.make_url({'domain': "Domestic",
                              'enviroment': self.params['enviroment']})
        self.engine.get(home)
        self.log(self.get_version_tests())
        self.log("Geting home page")
        try:
            assert "Cheap" in self.engine.title
        except AssertionError:
            self.log("Site is down or timeout error")

    def set_currency(self):
        self.log('Setting currency')
        cur = self.get_currency(self.params['currency'])
        self.log('Currency: ' + cur)
        cur_loc = {}
        for k, v in self.path['currency'].items():
            cur_loc[k] = v % cur
        self.engine.find(**cur_loc).click()
        time.sleep(0.5)

    def find(self):
        if "Compare with " in self.engine.page_source:
                self.engine.find(**self.path['partners']).uncheck()
                time.sleep(0.5)
        self.engine.find(**self.path['search']).click()


class SearchCCF(SearchDomestic):
    def __init__(self, params, engine):
        Search.engine = engine
        Search.params = params
        #Locators the same as on Domestic
        self.path = locators.search['Domestic']
        self.log("CCF search")
        self.home_page()
        if params['logged']:
            self.sign_in()
        else:
            self.sign_out()
        self.fill()

    def home_page(self):
        home = self.make_url({'domain': "CCF",
                              'enviroment': self.params['enviroment']})
        self.engine.get(home)
        self.log(self.get_version_tests())
        self.log("Geting home page")
        try:
            assert "Cheap" in self.engine.title
        except AssertionError:
            self.log("Site is down or timeout error")
