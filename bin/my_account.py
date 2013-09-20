from settings import conf_email
from time import asctime
import locators


class MyAccount:
    def __init__(self, params, engine):
        self.engine = engine
        self.email = conf_email[params["email"]]['user']
        self.password = conf_email[params["email"]]['pass']
        if params['domain'] == "International":
            self.path = locators.my_account['International']
        else:
            self.path = locators.my_account['Domestic']

    def log(self, message):
        t = asctime()
        name = self.engine.name
        print "[{}]<{}> {}".format(t, name, message)

    def go_to_account(self):
        self.log("Go to My Account")
        if not self.is_logged():
            self.sign_in()
        else:
            self.engine.find(link_text="My Account").click()

    def sign_in(self):
        self.log("Signing in")
        self.engine.find(link_text="My Account").click()
        form = self.engine.find(**self.path['form'])
        email = form.find(**self.path['email'])
        email.clear()
        email.send_keys(self.email)
        passwd = form.find(**self.path['password'])
        passwd.clear()
        passwd.send_keys(self.password)
        form.submit()

    def is_logged(self):
        header = self.engine.find(**self.path['header'])
        if "Sign in" in header:
            self.log("User is NOT logged")
            return False
        elif "Sign out" in header:
            self.log("User is logged")
            return True
