from selenium.common.exceptions import NoSuchElementException

import random
import time
import tkMessageBox
from selenium.webdriver.common.keys import Keys

import settings
import search
from my_account import MyAccount
import locators


class Book(search.Search):

    def type_name(self):
        self.log("Typing driver name")
        first_name = self.engine.find(**self.path['first_name'])
        first_name.clear()
        fn = self.customer['first_name']
        first_name.send_keys(self.customer['first_name'])
        last_name = self.engine.find(**self.path['last_name'])
        last_name.clear()
        last_name.send_keys(self.customer['last_name'])

    def type_email(self):
        self.log("Email: "+self.params["email"])
        email = settings.conf_email[self.params["email"]]['user']
        email_field = self.engine.find(**self.path['email'])
        email_field.clear()
        email_field.send_keys(email)
        conf_email_field = self.engine.find(**self.path['conf_email'])
        conf_email_field.clear()
        conf_email_field.send_keys(email)

    def type_phone(self):
        phone = self.engine.find(**self.path['phone'])
        phone.clear()
        phone.send_keys(self.customer['phone'])

    def is_logged(self):
        m = MyAccount(self.params, self.engine)
        return m.is_logged()

    def confirm_age_deposit(self):
        #self.engine.find(id='isSubscribed').uncheck()
        block = self.engine.find(**self.path['age_and_deposit'])
        checks = block.find('input')
        for box in checks:
            if box.is_displayed():
                box.check()

    def check_avilable_payments(self):
        labels = self.engine.find(**self.path['payment_section']).find('label')
        return [l.text for l in labels]

    def confirm_terms(self):
        self.engine.find(**self.path['confirm_terms']).check()

    def submit(self):
        self.log('Submit billing form')
        self.engine.find(**self.path['card_submit']).click()


class BookIntl(Book):
    def __init__(self, params, engine):
        self.customer = settings.driver_info['International']
        try:
            assert "details?solutionId" in engine.current_url
        except AssertionError:
            tkMessageBox.showwarning("Error",
                                     "You must be on Details page for filling")
        else:
            self.path = locators.book['International']
            Book.engine = engine
            Book.params = params
            self.fill()

    def fill(self):
        self.log(self.get_version_tests())
        self.log("Fill INTL")
        self.type_name()
        self.type_email()
        self.type_contacts()
        self.set_card()
        self.confirm_terms()

    def type_contacts(self):
        self.log("Typing driver contacts info")
        self.type_phone()
        street = self.engine.find(**self.path['address'])
        street.clear()
        street.send_keys(self.customer['address'])
        city = self.engine.find(**self.path['city'])
        city.clear()
        city.send_keys(self.customer['city'])

    def set_card(self):
        pay_type = self.params["payment"]
        headers = self.engine.find('h2')
        pay_flag = False
        for header in headers:
            if header.text == 'Payment and billing':
                pay_flag = True
        if pay_flag:
            self.log("Filling payment fields")
            payment = self.engine.find(**self.path['payment_form'])
            if pay_type == 'random':
                pay_type = random.choice(settings.
                                         payment_methods['International'].
                                         keys())
            card = settings.payment_methods['International'][pay_type]
            card_defaults = settings.card_defaults
            self.set_card_vendor(card["name"])
            card_num_field = payment.find(**self.path['card_num'])
            card_num_field.clear()
            card_num_field.send_keys(card['number'])
            payment.find(**self.path['card_month']).click()
            payment.find(link_text=card_defaults['month']).click()
            year = payment.find(**self.path['card_year'])
            year.click()
            year.send_keys(Keys.PAGE_DOWN)
            self.engine.find(link_text=card_defaults['year']).click()
            code_field = payment.find(**self.path['card_code'])
            code_field.clear()
            if card.get('code'):
                code_field.send_keys(card['code'])
            else:
                code_field.send_keys(card_defaults['code'])
        else:
            self.log("No billing section. Postpaid. Skip")

    def set_card_vendor(self, card_names):
        random.shuffle(card_names)
        card_name = card_names[0]
        self.log("Select payment method: "+card_name)
        card_menu = self.engine.find(**self.path['card_type']).click()
        try:
            self.engine.find(link_text=card_name).click()
        except:
            tkMessageBox.showwarning("Error", card_name + "Not AVAILABLE")


class BookDomestic(Book):
    def __init__(self, params, engine):
        self.customer = settings.driver_info['Domestic']
        try:
            assert "details-billing.jsp" in engine.current_url
        except AssertionError:
            tkMessageBox.showwarning("Error",
                                     "You must be on Details page for filling")
        else:
            self.path = locators.book['Domestic']
            Book.engine = engine
            Book.params = params
            self.fill()

    def fill(self):
        self.log(self.get_version_tests())
        self.log("Fill Domestic")
        if not self.is_logged():
            self.type_name()
            self.type_email()
            self.type_phone()
        self.confirm_age_deposit()
        self.set_insurance()
        self.set_card()
        self.confirm_terms()

    def set_insurance(self, timer=0):
        insurance_header = self.engine.find(**self.path['ins_header']
                                            ).text
        if 'unavailable' in insurance_header:
            self.log('Insurance unavailable. Skip setting insurance')
        elif 'recommended' in insurance_header.lower():
            self.log("Insurance available")
            if self.params['insurance']:
                self.log("Book with insurance")
                self.engine.find(**self.path['dy_ins_yes']).click()
                time.sleep(0.5)
            else:
                self.log("Book withOUT insurance")
                self.engine.find(**self.path['dy_ins_no']).click()
        elif 'optional' in insurance_header.lower():
            self.log("Static insurance")
            if self.params['insurance']:
                self.engine.find(**self.path['st_ins_yes']).click()
            else:
                self.engine.find(**self.path['st_ins_no']).click()
        else:
            if timer == 0:
                self.log('Waiting for insurance...')
            time.sleep(1)
            timer += 1
            self.set_insurance(timer=timer)

    def set_card(self):
        self.log("Setting a payment method")
        self.pay_type = self.params["payment"]
        headers = self.engine.find('h1')
        pay_flag = False
        for header in headers:
            if 'Payment and Billing' in header.text:
                pay_flag = True
        if pay_flag:
            self.set_payment_info()
        else:
            if self.params['insurance']:
                try:
                    self.set_payment_info()
                except NoSuchElementException or ElementNotVisibleException:
                    self.log("No billing section. \
                             Retail without insurance. Skip")

    def set_payment_info(self):
        self.log("Filling payment fields")
        if self.pay_type == 'random':
            self.pay_type = random.choice(settings.
                                          payment_methods['Domestic'].keys())
        card = settings.payment_methods['Domestic'][self.pay_type]
        self.log("Credit card: "+self.pay_type)
        payments = self.check_avilable_payments()
        if 'Credit card' in payments or "Credit/Debit card" in payments:
            self.engine.find(**self.path['card_btn']).click()
        if self.params['currency'] != 'USD':
            card_loc = {}
            for k, v in self.path['card_type'].items():
                card_loc[k] = v % pay_type
            self.engine.find(card_loc).click()
        card_num_field = self.engine.find(**self.path['card_num'])
        card_num_field.clear()
        card_num_field.send_keys(card['number'])
        card_defaults = settings.card_defaults
        card_mon_loc = {}
        for k, v in self.path['card_month'].items():
            card_mon_loc[k] = v % card_defaults['month']
        self.engine.find(**card_mon_loc).click()
        card_year_loc = {}
        for k, v in self.path['card_year'].items():
            card_year_loc[k] = v % card_defaults['year']
        self.engine.find(**card_year_loc).click()
        code_field = self.engine.find(**self.path['card_code']
                                      ).exclude('[disabled]')
        code_field.clear()
        if card.get('code'):
            code_field.send_keys(card['code'])
        else:
            code_field.send_keys(card_defaults['code'])
        fn = self.engine.find(**self.path['card_fn']).exclude('[disabled]')
        fn.clear()
        fn.send_keys(self.customer['first_name'])
        ln = self.engine.find(**self.path['card_ln']).exclude('[disabled]')
        ln.clear()
        ln.send_keys(self.customer['last_name'])
        address = self.engine.find(**self.path['card_address']
                                   ).exclude('[disabled]')
        address.clear()
        address.send_keys(self.customer['address'])
        city = self.engine.find(**self.path['card_city']).exclude('[disabled]')
        city.clear()
        city.send_keys(self.customer['city'])
        self.engine.find(**self.path['card_state']).click()
        zip = self.engine.find(**self.path['card_zip']).exclude('[disabled]')
        zip.clear()
        zip.send_keys(self.customer['zip'])


class BookCCF(Book):
    def __init__(self, params, engine):
        self.customer = settings.driver_info['CCF']
        try:
            assert "billing" in engine.current_url
        except AssertionError:
            tkMessageBox.showwarning("Error",
                                     "You must be on Details page for filling")
        else:
            self.path = locators.book['CCF']
            Book.engine = engine
            Book.params = params
            self.fill()

    def fill(self):
        self.log(self.get_version_tests())
        self.log("Fill CCF")
        if not self.is_logged():
            optional_signed = self.optional_sign_in()
            if not optional_signed:
                self.type_name()
                self.type_email()
                self.type_phone()
        self.confirm_age_deposit()
        self.set_insurance()
        self.set_card()
        self.confirm_terms()

    def optional_sign_in(self):
        if self.params['logged']:
            self.log("LogIn through OptionalSignIn")
            link = self.engine.find(**self.path['op_sign_link'])
            link.click()
            form = self.engine.find(**self.path['op_sign_form'])
            email = form.find(**self.path['op_sign_email'])
            passwd = form.find(**self.path['op_sign_passwd'])
            email.clear
            email.send_keys(settings.conf_email[self.params["email"]]['user'])
            passwd.clear()
            passwd.send_keys(settings.conf_email[self.params["email"]]['pass'])
            submit = self.engine.find(**self.path['op_sign_submit'])
            submit.click()
            time.sleep(0.5)
            return True
        else:
            return False

    def set_insurance(self, timer=0):
        insurance_header = self.engine.find(**self.path['ins_header']).text
        if 'unavailable' in insurance_header:
            self.log('Insurance unavailable. Skip setting insurance')
        elif 'recommended' in insurance_header.lower() \
             or 'optional' in insurance_header.lower():
            self.log("Insurance available")

            if self.params['insurance']:
                self.log("Book with insurance")
                self.engine.find(**self.path['ins_yes']).click()
                return True
            else:
                self.log("Book withOUT insurance")
                self.engine.find(**self.path['ins_no']).click()
                return False
        else:
            if timer == 0:
                self.log('Waiting for insurance...')
            time.sleep(1)
            timer += 1
            self.set_insurance(timer=timer)

    def set_card(self):
        self.pay_type = self.params["payment"]
        headers = self.engine.find('h2')
        pay_flag = False
        for header in headers:
            if 'Payment and billing' in header.text:
                pay_flag = True
        if pay_flag:
            self.set_payment_info()
        else:
            self.log("No billing section. Retail without insurance. Skip")

    def set_payment_info(self):
        if self.pay_type == "BillMeLater":
            self.pay_by_bml()
        elif self.pay_type == "PayPal":
            self.pay_by_paypal()
        elif self.pay_type == "HotDollars":
            self.pay_by_hotdollars()
        elif self.pay_type == "SavedCard":
            self.pay_by_saved_card()
        elif self.pay_type == "SavedBML":
            self.pay_by_saved_bml()
        else:
            self.pay_by_card()

    def pay_by_card(self):
        self.log("Filling payment fields")
        payments = self.check_avilable_payments()
        if 'Credit card' in payments or "Credit/Debit card" in payments:
            self.engine.find(**self.path['card_btn']).click()
        if self.pay_type == 'random':
            self.pay_type = random.choice(settings.payment_methods['CCF']
                                          .keys())
        card = settings.payment_methods['CCF'][self.pay_type]
        self.log("Credit card: " + self.pay_type)
        card_defaults = settings.card_defaults
        card_num_field = self.engine.find(**self.path['card_num'])
        card_num_field.clear()
        card_num_field.send_keys(card['number'])
        self.engine.find(**self.path['card_month']).click()
        self.engine.find(link_text=card_defaults['month']).click()
        year = self.engine.find(**self.path['card_year'])
        year.click()
        year.send_keys(Keys.PAGE_DOWN)
        self.engine.find(link_text=card_defaults['year']).click()
        code_field = self.engine.find(**self.path['card_code'])
        if len(code_field) > 1:
            code_field.exclude('[disabled]')
        code_field.clear()
        if card.get('code'):
            code_field.send_keys(card['code'])
        else:
            code_field.send_keys(card_defaults['code'])
        fn = self.engine.find(**self.path['card_fn'])
        fn.clear()
        fn.send_keys(self.customer['first_name'])
        ln = self.engine.find(**self.path['card_ln'])
        ln.clear()
        ln.send_keys(self.customer['last_name'])
        address = self.engine.find(**self.path['card_address'])
        address.clear()
        address.send_keys(self.customer['address'])
        city = self.engine.find(**self.path['card_city'])
        city.clear()
        city.send_keys(self.customer['city'])
        self.set_state()
        zip = self.engine.find(**self.path['card_zip'])
        zip.clear()
        zip.send_keys(self.customer['zip'])

    def set_state(self, state="CA"):
        self.log("Set state: CA")
        hidden_select = self.engine.find(**self.path['card_state'])
        hidden_select.next().find('a').click()
        self.engine.find(xpath='//li/a[text()="'+state+'"]').click()

    def pay_by_saved_card(self):
        payments = self.check_avilable_payments()
        available_flag = [p for p in payments
                          if 'savedVisa' in p or 'savedMasterCard' in payments]
        if available_flag:
            self.engine.find(**self.path['saved_card_btn']).click()
            code = self.engine.find(**self.path['saved_card_code'])
            code.clear()
            code.send_keys(setting.card_defaults['code'])
        else:
            tkMessageBox.showwarning("Error", "Saved CreditCard not avilable")

    def pay_by_saved_bml(self):
        payments = self.check_avilable_payments()
        if "BARBARA's Bill Me Later" in payments:
            self.engine.find(**self.path['saved_bml_btn']).click()
        else:
            tkMessageBox.showwarning("Error", "Saved BML is not avilable")

    def pay_by_bml(self):
        self.log("Filling Bill Me Later form")
        bml = settings.BillMeLater
        self.engine.find(**self.path['bml_btn']).click()
        fn = self.engine.find(**self.path['bml_fn'])
        fn.clear()
        fn.send_keys(bml["first_name"])
        ln = self.engine.find(**self.path['bml_ln'])
        ln.clear()
        ln.send_keys(bml["last_name"])
        address = self.engine.find(**self.path['bml_address'])
        address.clear()
        address.send_keys(bml["address"])
        city = self.engine.find(**self.path['bml_city'])
        city.clear()
        city.send_keys(bml["city"])
        state_loc = self.engine.find(**self.path['bml_state'])
        state_loc.next().find('a').click()
        self.engine.find(xpath='//li/a[text()="' + bml["state"] + '"]').click()
        #self.set_state(bml["state"]);
        zip = self.engine.find(**self.path['bml_zip'])
        zip.clear()
        zip.send_keys(bml["zip"])
        phone_reg = self.engine.find(**self.path['bml_phone_region'])
        phone_reg.clear()
        phone_reg.send_keys(bml["phone_region"])
        phone_num = self.engine.find(**self.path["bml_phone_num"])
        phone_num.clear()
        phone_num.send_keys(bml["phone_number"])

    def pay_by_paypal(self):
        paypal = settings.PayPal
        self.log("Filling Bill Me Later form")
        self.engine.find(**self.path["pp_btn"]).click()
        fn = self.engine.find(**self.path["pp_fn"])
        fn.clear()
        fn.send_keys(paypal["first_name"])
        ln = self.engine.find(**self.path["pp_ln"])
        ln.clear()
        ln.send_keys(paypal["last_name"])
        address = self.engine.find(**self.path["pp_address"])
        address.clear()
        address.send_keys(paypal["address"])
        city = self.engine.find(**self.path["pp_city"])
        city.clear()
        city.send_keys(paypal["city"])
        pp_state_loc = self.engine.find(**self.path["pp_state"])
        pp_state_loc.next().find('a').click()
        self.engine.find(xpath='//li/a[text()="'+paypal["state"]+'"]').click()
        #self.set_state(bml["state"]);
        zip = self.engine.find(**self.path["pp_zip"])
        zip.clear()
        zip.send_keys(paypal["zip"])

    def pay_by_hotdollars(self):
        self.log("Pay by HotDollars")
        self.engine.find(**self.path['hd_btn']).click()
        if self.set_insurance():
            self.pay_type == 'random'
            self.pay_by_card()

    def submit(self):
        self.log('Submit billing form')
        if self.pay_type in ["BillMeLater", "SavedBML"]:
            self.confirm_bml()
        elif self.pay_type == "PayPal":
            self.confirm_paypal()
        else:
            self.engine.find(**self.path['card_submit']).click()
            self.log(self.engine.current_url)

    def confirm_paypal(self):
        paypal = settings.PayPal
        self.engine.find(**self.path['pp_proceed']).click()
        try:
            self.engine.find(**self.path['pp_load']).click()
        except:
            self.log("Already logged in")
        login = self.engine.find(**self.path['pp_email'])
        login.clear()
        login.send_keys(paypal["user"])
        passd = self.engine.find(**self.path['pp_passwd'])
        passd.clear()
        passd.send_keys(paypal["password"])
        self.engine.find(**self.path['pp_submit']).click()
        self.engine.find(**self.path['pp_continue']).click()

    def confirm_bml(self):
        bml = settings.BillMeLater
        self.engine.find(**self.path['bml_proceed']).click()
        self.engine.find(**self.path['bml_month']).send_keys(bml["birth_mon"])
        self.engine.find(**self.path['bml_date']).send_keys(bml["birth_date"])
        self.engine.find(**self.path['bml_year']).send_keys(bml["birth_year"])
        ssn = self.engine.find(**self.path['bml_code'])
        ssn.clear()
        ssn.send_keys(bml["ssn"])
        self.engine.execute_script("document.getElementById('terms')\
                                   .contentWindow.scrollTo(0,50000);")
        self.engine.find(**self.path['bml_terms']).click()
        self.engine.find(**self.path['bml_submit']).click()
