from settings import c3_user
from selenium.webdriver.common.keys import Keys

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
        #self.find_customer()

    def find_customer(self):
        self.engine.find(xpath="//a[@href='https://www.qa.hotwireadmin.com/ccc/customerQuery']").click()
        cust_email = self.engine.find(id="emailAddress")
        cust_email.clear()
        cust_email.send_keys(self.params["email"])
        cust_email.send_keys(Keys.ENTER)




