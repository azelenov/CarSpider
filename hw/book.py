from selenium.common.exceptions import NoSuchElementException

import random
import time
import tkMessageBox

import settings
import search

class Book(search.Search):
    def type_name(self,fn_class='seleniumFirstName',ln_class='seleniumLastName'):
        self.log("Typing driver name")
        first_name = self.engine.find(class_name = fn_class)
        first_name.clear()
        fn = self.customer['first_name']
        first_name.send_keys(self.customer['first_name'])
        last_name = self.engine.find(class_name = ln_class)
        last_name.clear()
        last_name.send_keys(self.customer['last_name'])

    def type_email(self,email_class='seleniumEmailAddress',conf_em_class='seleniumConfirmEmailAddress'):
        self.log("Email: "+self.params["email"])
        email = settings.conf_email[self.params["email"]]['user']
        email_field = self.engine.find(class_name = email_class)
        email_field.clear()
        email_field.send_keys(email)
        conf_email_field = self.engine.find(class_name = conf_em_class)
        conf_email_field.clear()
        conf_email_field.send_keys(email)

    def confirm_terms(self):
        self.engine.find(class_name='seleniumDepositTypeTermsAccepted').check()

class BookIntl(Book):
    def __init__(self,params,engine):
        self.customer = settings.driver_info['International']
        try:
            assert "details?solutionId" in engine.current_url
        except AssertionError:
            tkMessageBox.showwarning("Error","You must be on Details page for filling")
        else:
            Book.engine = engine
            Book.params = params
            self.fill()

    def fill(self):
        self.log("Fill INTL")
        self.type_name()
        self.type_email()
        self.type_contacts()
        self.set_card()
        self.confirm_terms()

    def type_contacts(self):
        self.log("Typing driver contacts info")
        phone = self.engine.find(class_name = 'seleniumPhoneNumber')
        phone.clear()
        phone.send_keys(self.customer['phone'])
        street = self.engine.find(class_name = 'seleniumStreetAddress')
        street.clear()
        street.send_keys(self.customer['address'])
        city = self.engine.find(class_name = 'seleniumCityAddress')
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
           payment = self.engine.find(class_name="payment")
           if pay_type == 'random':
              pay_type = random.choice(settings.payment_methods['International'].keys())
           card = settings.payment_methods['International'][pay_type]
           self.set_card_vendor(card["name"])
           card_num_field = payment.find(class_name='seleniumCreditCardNumber')
           card_num_field.clear()
           card_num_field.send_keys(card['number'])
           payment.find(id="cardExpiryMonth-button").click()
           payment.find(link_text='01').click()
           payment.find(id="cardExpiryYear-button").click()
           payment.find(link_text='2017').click()
           code_field = payment.find(id='creditCard.securityCode')
           code_field.clear()
           if card.get('code'):
              code_field.send_keys(card['code'])
           else:
              code_field.send_keys('111')
        else:
           self.log("No billing section. Postpaid. Skip")

    def set_card_vendor(self,card_names):
        random.shuffle(card_names)
        card_name = card_names[0]
        self.log("Select payment method: "+card_name)
        card_menu = self.engine.find(id="ccType-button").click()
        try:
            self.engine.find(link_text=card_name).click()
        except:
            tkMessageBox.showwarning("Error",card_name + "Not AVAILABLE")

    def submit(self):
        self.engine.find(xpath="//button[@type='submit']").click()

class BookDomestic(Book):
    def __init__(self,params,engine):
        self.customer = settings.driver_info['Domestic']
        try:
            assert "details-billing.jsp" in engine.current_url
        except AssertionError:
            tkMessageBox.showwarning("Error","You must be on Details page for filling")
        else:
            Book.engine = engine
            Book.params = params
            self.fill()

    def fill(self):
        self.log("Fill Domestic")
        self.type_name()
        self.type_email()
        self.type_phone()
        self.confirm_age_deposit()
        self.set_insurance()
        self.set_card()
        self.confirm_terms()

    def type_name(self):
        self.log("Typing driver name")
        first_name = self.engine.find(id='billingForm.travelerForm.driverFirstName')
        first_name.clear()
        fn = self.customer['first_name']
        first_name.send_keys(self.customer['first_name'])
        last_name = self.engine.find(id='billingForm.travelerForm.driverLastName')
        last_name.clear()
        last_name.send_keys(self.customer['last_name'])

    def type_email(self):
        self.log("Email: "+self.params["email"])
        email = settings.conf_email[self.params["email"]]['user']
        email_field = self.engine.find(id="billingForm.travelerForm._NAE_email")
        email_field.clear()
        email_field.send_keys(email)
        conf_email_field = self.engine.find(id='billingForm.travelerForm._NAE_confirmEmail')
        conf_email_field.clear()
        conf_email_field.send_keys(email)

    def type_phone(self):
        phone = self.engine.find(id='billingForm.travelerForm.phoneNo')
        phone.clear()
        phone.send_keys(self.customer['phone'])

    def confirm_age_deposit(self):
        self.engine.find(id='isSubscribed').uncheck()
        block = self.engine.find(id='ageAndDepositTerms')
        checks = block.find('input')
        for box in checks:
            if box.is_displayed():
               box.check()

    def set_insurance(self,timer=0):
        insurance_header =  self.engine.find(class_name='protectionWrapper').text
        if 'unavailable' in insurance_header:
           self.log('Insurance unavailable. Skip setting insurance')
        elif 'recommended' in insurance_header.lower():
           self.log("Insurance available")
           if self.params['insurance']:
              self.log("Book with insurance")
              self.engine.find(id='insurancePurchaseCheckTrue').click()
              time.sleep(0.5)
           else:
              self.log("Book withOUT insurance")
              self.engine.find(id='insurancePurchaseCheckFalse').click()
        elif 'optional' in insurance_header.lower():
             self.log("Static insurance")
             if self.params['insurance']:
                self.engine.find(id="yesBtn").click()
             else:
                self.engine.find(id="noBtn").click()
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
                  self.engine.find(class_name='paymentMethodWrapper')
                  self.set_payment_info()
              except NoSuchElementException:
                  self.log("No billing section. Retail without insurance. Skip")

    def set_payment_info(self):
        self.log("Filling payment fields")
        if self.pay_type == 'random':
          self.pay_type = random.choice(settings.payment_methods['Domestic'].keys())
        card = settings.payment_methods['Domestic'][self.pay_type]
        self.log("Credit card: "+self.pay_type)
        if self.params['currency'] != 'USD':
          self.engine.find(xpath='//select[@id="cardTypeSelector"]/option[text()="'+self.pay_type+'"]').click()
        card_num_field = self.engine.find(id='billingForm.paymentForm._NAE_acctNumber')
        card_num_field.clear()
        card_num_field.send_keys(card['number'])
        self.engine.find(xpath="//select[@name='billingForm.paymentForm.cardMonth']/option[text()='05']").click()
        self.engine.find(xpath="//select[@name='billingForm.paymentForm.cardYear']/option[text()='2017']").click()
        code_field = self.engine.find(id="billingForm.paymentForm._NAE_cpvNumber")
        code_field.clear()
        if card.get('code'):
          code_field.send_keys(card['code'])
        else:
          code_field.send_keys('111')
        fn = self.engine.find(id="billingForm.paymentForm.billingFirstName").exclude('[disabled]')
        fn.clear()
        fn.send_keys(self.customer['first_name'])
        ln = self.engine.find(id='billingForm.paymentForm.billingLastName').exclude('[disabled]')
        ln.clear()
        ln.send_keys(self.customer['last_name'])
        address = self.engine.find(id='billingForm.paymentForm._NAE_stAddress1').exclude('[disabled]')
        address.clear()
        address.send_keys(self.customer['address'])
        city = self.engine.find(id='billingForm.paymentForm.city').exclude('[disabled]')
        city.clear()
        city.send_keys(self.customer['city'])
        self.engine.find(xpath="//select[@name='billingForm.paymentForm.state']/option[text()='CA']").click()
        zip = self.engine.find(id='billingForm.paymentForm._NAE_zip').exclude('[disabled]')
        zip.clear()
        zip.send_keys(self.customer['zip'])

    def confirm_terms(self):
        self.engine.find(name='billingForm.agreement').check()

    def submit(self):
        self.log('Submit billing form')
        self.engine.find(class_name="btnC").click()

class BookCCF(Book):
    def __init__(self,params,engine):
        self.customer = settings.driver_info['CCF']
        try:
            assert "billing" in engine.current_url
        except AssertionError:
            tkMessageBox.showwarning("Error","You must be on Details page for filling")
        else:
            Book.engine = engine
            Book.params = params
            self.fill()

    def fill(self):
        self.log("Fill CCF")
        self.type_name()
        self.type_email()
        self.type_phone()
        self.confirm_age_deposit()
        self.set_insurance()
        self.set_card()
        self.confirm_terms()

    def type_phone(self):
        phone = self.engine.find(class_name = 'seleniumPhoneNumber')
        phone.clear()
        phone.send_keys(self.customer['phone'])

    def confirm_age_deposit(self):
        self.engine.find(name='carDriver.wantsHwNewsLetters').uncheck()
        block = self.engine.find(class_name='ageAndDepositTerms')
        checks = block.find('input')
        for box in checks:
            if box.is_displayed():
               box.check()

    def set_insurance(self,timer=0):
        insurance_header =  self.engine.find(class_name='carSinglePageInsurance').text
        if 'unavailable' in insurance_header:
           self.log('Insurance unavailable. Skip setting insurance')
        elif 'recommended' in insurance_header.lower() or 'optional' in insurance_header.lower():
           self.log("Insurance available")

           if self.params['insurance']:
              self.log("Book with insurance")
              self.engine.find(xpath="//input[@id='insurancePurchaseCheckTrue'] | //input[@value='staticInsuranceYes']").click()
           else:
              self.log("Book withOUT insurance")
              self.engine.find(xpath="//input[@id='insurancePurchaseCheckFalse'] | //input[@value='staticInsuranceNo']").click()
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
        else:
           self.pay_by_card()

    def pay_by_card(self):
        self.log("Filling payment fields")
        payment = self.engine.find(id="paymentWrapper")
        if self.pay_type == 'random':
          self.pay_type = random.choice(settings.payment_methods['Domestic'].keys())
        card = settings.payment_methods['Domestic'][self.pay_type]
        self.log("Credit card: "+self.pay_type)
        card_num_field = payment.find(class_name='seleniumCreditCardNumber')
        card_num_field.clear()
        card_num_field.send_keys(card['number'])
        payment.find(id="cardExpiryMonth-button").click()
        payment.find(xpath='//li/a[text()="01"]').click()
        payment.find(id="cardExpiryDate-button").click()
        payment.find(xpath='//li/a[text()="2017"]').click()
        code_field = payment.find(class_name='seleniumSecurityCode')
        code_field.clear()
        if card.get('code'):
          code_field.send_keys(card['code'])
        else:
          code_field.send_keys('111')
        fn = self.engine.find(id='creditCard.billingFirstName')
        fn.clear()
        fn.send_keys(self.customer['first_name'])
        ln = self.engine.find(id='creditCard.billingLastName')
        ln.clear()
        ln.send_keys(self.customer['last_name'])
        address = self.engine.find(id='creditCard.address')
        address.clear()
        address.send_keys(self.customer['address'])
        city = self.engine.find(id='creditCard.city')
        city.clear()
        city.send_keys(self.customer['city'])
        self.set_state()
        zip = self.engine.find(name='creditCard.postalCode')
        zip.clear()
        zip.send_keys(self.customer['zip'])

    def pay_by_bml(self):
        self.log("Filling Bill Me Later form")
        bml = settings.BillMeLater
        self.engine.find(xpath="//input[@id='billMeLater']").click()
        fn = self.engine.find(id="billMeLater.holder.firstName")
        fn.clear()
        fn.send_keys(bml["first_name"])
        ln = self.engine.find(id="billMeLater.holder.lastName")
        ln.clear()
        ln.send_keys(bml["last_name"])
        address = self.engine.find(id="billMeLater.billingAddress.address")
        address.clear()
        address.send_keys(bml["address"])
        city = self.engine.find(id="billMeLater.billingAddress.city")
        city.clear()
        city.send_keys(bml["city"])
        self.engine.find(name="billMeLater.billingAddress.state").next().find('a').click()
        self.engine.find(xpath='//li/a[text()="'+bml["state"]+'"]').click()
        #self.set_state(bml["state"]);
        zip = self.engine.find(name="billMeLater.billingAddress.postalCode")
        zip.clear()
        zip.send_keys(bml["zip"])
        phone_reg = self.engine.find(id="billMeLater.billingPhoneRegion")
        phone_reg.clear()
        phone_reg.send_keys(bml["phone_region"])
        phone_num = self.engine.find(id="billMeLater.billingPhoneNumber")
        phone_num.clear()
        phone_num.send_keys(bml["phone_number"])

    def pay_by_paypal(self):
        paypal = settings.PayPal
        self.log("Filling Bill Me Later form")
        self.engine.find(xpath="//input[@id='payPal']").click()
        fn = self.engine.find(id="payPal.holder.firstName")
        fn.clear()
        fn.send_keys(paypal["first_name"])
        ln = self.engine.find(id="payPal.holder.lastName")
        ln.clear()
        ln.send_keys(paypal["last_name"])
        address = self.engine.find(id="payPal.billingAddress.address")
        address.clear()
        address.send_keys(paypal["address"])
        city = self.engine.find(id="payPal.billingAddress.city")
        city.clear()
        city.send_keys(paypal["city"])
        self.engine.find(name="payPal.billingAddress.state").next().find('a').click()
        self.engine.find(xpath='//li/a[text()="'+paypal["state"]+'"]').click()
        #self.set_state(bml["state"]);
        zip = self.engine.find(name="payPal.billingAddress.postalCode")
        zip.clear()
        zip.send_keys(paypal["zip"])

    def set_state(self,state="CA"):
        self.log("Set state: CA")
        hidden_select = self.engine.find(class_name="cardState")
        hidden_select.next().find('a').click()
        self.engine.find(xpath='//li/a[text()="'+state+'"]').click()

    def submit(self):
        self.log('Submit billing form')
        if self.pay_type == "BillMeLater":
           self.confirm_bml()
        elif self.pay_type == "PayPal":
           self.confirm_paypal()
        else:
           self.engine.find(id="billingConfirm").click()

    def confirm_paypal(self):
        paypal = settings.PayPal
        self.engine.find(id="goToPayPal").click()
        try:
            self.engine.find(id="loadLogin").click()
        except:
            self.log("Already logged in")
        login = self.engine.find(id='login_email')
        login.clear()
        login.send_keys(paypal["user"])
        passd = self.engine.find(id='login_password')
        passd.clear()
        passd.send_keys(paypal["password"])
        self.engine.find(id="submitLogin").click()
        self.engine.find(id="continue").click()

    def confirm_bml(self):
        bml = settings.BillMeLater
        self.engine.find(id="goToBillMeLater").click()
        self.engine.find(id='date_of_birth_month').send_keys(bml["birth_mon"])
        self.engine.find(id='date_of_birth_day').send_keys(bml["birth_date"])
        self.engine.find(id='date_of_birth_year').send_keys(bml["birth_year"])
        ssn = self.engine.find(name='ssn')
        ssn.clear()
        ssn.send_keys(bml["ssn"])
        self.engine.find(id="esign_consent").click()
        self.engine.execute_javascript("document.getElementById('terms').contentWindow.scrollTo(0,50000);");
        self.engine.find(id="submit_button").click()

