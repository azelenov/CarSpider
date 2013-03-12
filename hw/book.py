from selenium.common.exceptions import NoSuchElementException

import sys
import random
from settings import driver_info,conf_email, intl_card
import search
import locators
import time


class IntlBook(search.IntlSearch):
    def __init__(self,browsers,config):
        self.drivers = browsers
        self.config = config


    def fill(self,confirm=False):
        for driver in self.drivers:
            self.params = self.config[self.drivers.index(driver)]
            self.engine = driver
            self.test_head()
            #self.load_test()
            #self.engine.switch_to_active_element()
            self.type_name(driver)
            self.type_email(driver)
            self.type_contacts(driver)
            self.set_card(driver)
            if confirm: self.agree_and_go(driver)

    def test_head(self):
        try:
            assert "Car hire details" in self.engine.page_source
            self.log("Loaded")
        except AssertionError:
            time.sleep(1)
            self.log("Not loaded")
            self.test_head()


    def type_name(self,eng):
        self.log("Typing driver name")
        self.xtype('first_name',driver_info['first_name'])
        self.xtype('last_name',driver_info['last_name'])

    def type_email(self,eng):
        self.log("Typing email: "+self.params["email_type"])
        email = conf_email[self.params["email_type"]]
        self.xtype('email',email)
        self.xtype('conf_email',email)

    def type_contacts(self,eng):
        self.log("Typing driver contacts info")
        self.xtype('phone',driver_info['phone'])
        self.xtype('address',driver_info['address'])
        self.xtype('city',driver_info['city'])

    def set_card(self,eng):
        try:
            eng.find_element_by_class_name("payment")
        except NoSuchElementException:
               print "POSTPAID"
        else:
            card = intl_card[self.params["card_vendor"]]

            self.set_card_vendor(eng,card["name"])

            self.xtype("card_num",card['number'])
            self.xclick("card_mon")
            self.click_text('01')
            self.xclick("card_year")
            self.click_text('2016')
            self.xtype("card_code","111")


    def set_card_vendor(self,dr,cn):
        random.shuffle(cn)
        card_name = cn[0]
        self.log("Typing payment method: "+card_name)
        card_menu = dr.find_element_by_id("ccType-button").click()
        try:
            dr.find_element_by_link_text(card_name).click()
        except:
            print card_name + "Not AVAILABLE"
            sys.exit()

    def agree_and_go(self,eng):
        self.log("Accept terms")
        self.xclick("accept")
        self.submit()