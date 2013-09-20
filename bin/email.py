from settings import conf_email
from selenium.webdriver.common.keys import Keys
import tkMessageBox
import locators


class Email():
    def __init__(self, params, engine):
        self.engine = engine
        self.email = params['email']
        if self.email == 'gmail':
            self.url = "http://gmail.com"
            self.conf_email = conf_email['gmail']
            self.path = locators.email['gmail']
            self.login()
        elif self.email == 'yahoo':
            self.url = "http://mail.yahoo.com"
            self.conf_email = conf_email['yahoo']
            self.path = locators.email['yahoo']
            self.login()
        else:
            tkMessageBox.showwarning("Error",
                                     "There is NO handler for this email type")

    def login(self):
        self.engine.get(self.url)
        email = self.engine.find(**self.path['email'])
        email.clear()
        email.send_keys(self.conf_email['user'])
        password = self.engine.find(**self.path['password'])
        password.clear()
        password.send_keys(self.conf_email['pass'])
        password.send_keys(Keys.ENTER)
