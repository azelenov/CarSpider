from settings import conf_email
from time import asctime

class MyAccount():
    def __init__(self,params,engine):
        self.engine = engine
        domain = params['domain']
        self.email = conf_email[params["email"]]['user']
        if domain == "International":
            self.domain = MyAccountIntl(params,engine)
        else:
            self.domain = MyAccountDomestic(params,engine)

    def log(self,message):
        t = asctime()
        name = self.engine.name
        print "[{}]<{}> {}".format(t,name,message)

    def go_to_account(self):
        self.log("Go to My Account")
        if not self.is_logged():
            self.sign_in()
        else:
            self.engine.find(link_text="My Account").click()

    def sign_in(self):
        self.log("Signing in")
        self.engine.find(link_text="My Account").click()
        form = self.domain.get_login_form()
        email = self.domain.get_email_field(form)
        email.clear()
        email.send_keys(self.email)
        passwd = self.domain.get_passwd_field(form)
        passwd.clear()
        passwd.send_keys("password")
        form.submit()

    def is_logged(self):
        header = self.domain.get_header()
        if "Sign in" in header:
            self.log("User is NOT logged")
            return False
        elif "Sign out" in header:
            self.log("User is logged")
            return True

class MyAccountIntl(MyAccount):
    def __init__(self,params,engine):
        self.engine = engine
        domain = params['domain']
        self.email = conf_email[params["email"]]['user']

    def get_login_form(self):
        return self.engine.find(class_name="signInModule").find("form")

    def get_email_field(self,login_form):
        return login_form.find(id="email")

    def get_passwd_field(self,login_form):
        return login_form.find(id="password")

    def get_header(self):
        return self.engine.find(class_name = "account").text

class MyAccountDomestic(MyAccount):
    def __init__(self,params,engine):
        self.engine = engine
        domain = params['domain']
        self.email = conf_email[params["email"]]['user']

    def get_login_form(self):
        return self.engine.find(name="myLoginForm")

    def get_email_field(self,login_form):
        return login_form.find(name="_NAE_emailLogin")

    def get_passwd_field(self,login_form):
        return login_form.find(name="_NAE_passwordLogin")

    def get_header(self):
        return self.engine.find(id = "globalAccountStatusMessaging").text




