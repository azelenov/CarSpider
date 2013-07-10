from settings import conf_email
import book
from selenium.webdriver.common.keys import Keys
from engine import Engine
import tkMessageBox

class Email():
    def __init__(self,params,engine):
        self.engine = engine
        if params["browser"] == 'firefox':
            self.engine.find('body').send_keys(Keys.CONTROL +"t")
        self.email = params['email']
        if self.email == 'gmail':
            self.login_gmail()
        elif self.email == 'yahoo':
            self.login_yahoo()
        elif self.email == 'guest':
            self.login_guest()
        else:
            tkMessageBox.showwarning("Error","There is NO handler for this email type")

    def login_gmail(self):
        self.engine.get("http://gmail.com")
        email = self.engine.find(id="Email")
        email.clear()
        email.send_keys(conf_email['gmail']['user'])
        password = self.engine.find(id="Passwd")
        password.clear()
        password.send_keys(conf_email['gmail']['pass'])
        self.engine.find(id='signIn').click()

    def login_yahoo(self):
        self.engine.get("http://mail.yahoo.com")
        email = self.engine.find(id="username")
        email.clear()
        email.send_keys(conf_email['yahoo']['user'])
        password = self.engine.find(id="passwd")
        password.clear()
        password.send_keys(conf_email['yahoo']['pass'])
        password.send_keys(Keys.ENTER)

    def login_guest(self):
        self.engine.get("https://www.guerrillamail.com/")
