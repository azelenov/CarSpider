from settings import c3_user
from selenium.webdriver.common.keys import Keys
from settings import conf_email

class C3():
    def __init__(self,params,engine):
        self.engine = engine
        self.params = params
        user = self.engine.find(id="username")
        user.clear()
        user.send_keys(c3_user["user"])
        password = self.engine.find(id="password")
        password.clear()
        password.send_keys(c3_user["password"])
        self.engine.find(name='Submit').click()
        self.find_customer()

    def find_customer(self):
        self.engine.switch_to_frame("c3Frame")
        self.engine.find(link_text="Search for a Hotwire customer").click()
        email = conf_email[self.params["email"]]['user']
        cust_email = self.engine.find(id="emailAddress")
        cust_email.clear()
        cust_email.send_keys(email)
        cust_email.send_keys(Keys.ENTER)




