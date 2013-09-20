#This file is collection of all Car Locators
#In code named as 'self.path' collection
#Locators using in search

search = {
    'International': {
        'currency': {'id': 'currencyCode-button'},
        'pickup_loc': {'class_name': 'seleniumPickupLocation'},
        'dropoff_loc': {'class_name': 'seleniumDropoffLocation'},
        'oneway': {'class_name': 'seleniumCarOneWay'},
        'roundtrip': {'class_name': 'seleniumCarRoundTrip'},
        'age': {'name': 'driverAge'},
        'search': {'class_name': 'seleniumContinueButton'}
    },
    'Domestic': {
        #symbols %s means that this is place for chosen currency
        'currency': {'xpath': "//select[@name='selectedCurrencyCode']/option[text()='%s']"},
        'pickup_loc': {'name': 'startLocation'},
        'dropoff_loc': {'name': 'endLocation'},
        'oneway': {'id': 'carOneWay'},
        'roundtrip': {'id': 'carRoundTrip'},
        'search': {'css': 'form.carFields button'},
        'partners': {'name': 'selectedPartners'}
    },
    #CCF FareFinder the same as Domestic but different  on results
    'CCF': {
        'pickup_loc': {'name': 'pickupLocation'},
        'dropoff_loc': {'name': 'dropOffLocation'},
        'search': {'xpath': '//div[@class="searchBtn"]//button[@type="submit"]'}
    }
}

results = {
    'International': {
        'continue': {'link_text': 'Continue'},
        'result': {'class_name': 'seleniumResultItem'}
    },
    'Domestic': {
        'continue': {'class_name': 'continueBtn'},
        'result': {'class_name': 'resultWrapper'},
        'retail': {'css': ".gray"}
        #opaque calculates as not retail
    },
    'CCF': {
        'continue': {'css': '.continueBtn a'},
        'result': {'css': 'a.result'},
        'opaque': {'css': ".hotRate"},
        #retail calculates as not opaque
    }
}

book = {
    'International': {
        #driver details
        'first_name': {'class_name': 'seleniumFirstName'},
        'last_name': {'class_name': 'seleniumLastName'},
        'email': {'class_name': 'seleniumEmailAddress'},
        'conf_email': {'class_name': 'seleniumConfirmEmailAddress'},
        'phone': {'class_name': 'seleniumPhoneNumber'},
        'address': {'class_name': 'seleniumStreetAddress'},
        'city': {'class_name': 'seleniumCityAddress'},

        #payment section
        'payment_form': {'class_name': "payment"},
        'card_type': {'id': "ccType-button"},
        'card_num': {'class_name': 'seleniumCreditCardNumber'},
        'card_month': {'id': "cardExpiryMonth-button"},
        'card_year': {'id': "cardExpiryYear-button"},
        'card_code': {'id': 'creditCard.securityCode'},
        'confirm_terms': {'class_name': 'seleniumDepositTypeTermsAccepted'},
        'card_submit': {'xpath': "//button[@type='submit']"}
    },

    'Domestic': {
        #driver details
        'first_name': {'id': 'billingForm.travelerForm.driverFirstName'},
        'last_name': {'id': 'billingForm.travelerForm.driverLastName'},
        'email': {'id': "billingForm.travelerForm._NAE_email"},
        'conf_email': {'id': 'billingForm.travelerForm._NAE_confirmEmail'},
        'phone': {'id': 'billingForm.travelerForm.phoneNo'},
        'age_and_deposit': {'id': 'ageAndDepositTerms'},

        #insurance section
        #ins means insurance
        'ins_header': {'class_name': 'protectionWrapper'},
        #dy_ins means dynamic insurance
        'dy_ins_yes': {'id': 'insurancePurchaseCheckTrue'},
        'dy_ins_no': {'id': 'insurancePurchaseCheckFalse'},
        #st_ins means static insurance
        'st_ins_yes': {'id': "yesBtn"},
        'st_ins_no': {'id': "noBtn"},

        #payment section
        'payment_section': {'id': "paymentSection"},
        'card_btn': {'id': "defaultPmIdNewCC"},
        #symbols %s means that this is place for chosen card type
        'card_type': {'xpath': '//select[@id="cardTypeSelector"]/option[text()="%s"]'},
        'card_num': {'id': 'billingForm.paymentForm._NAE_acctNumber'},
        'card_month': {'xpath': "//select[@name='billingForm.paymentForm.cardMonth']/option[text()='%s']"},
        'card_year': {'xpath': "//select[@name='billingForm.paymentForm.cardYear']/option[text()='%s']"},
        'card_code': {'id': "billingForm.paymentForm._NAE_cpvNumber"},
        #card fn - first name, ln - last name
        'card_fn': {'id': "billingForm.paymentForm.billingFirstName"},
        'card_ln': {'id': 'billingForm.paymentForm.billingLastName'},
        'card_address': {'id': 'billingForm.paymentForm._NAE_stAddress1'},
        'card_city': {'id': 'billingForm.paymentForm.city'},
        'card_state': {'xpath': "//select[@name='billingForm.paymentForm.state']/option[text()='CA']"},
        'card_zip': {'id': 'billingForm.paymentForm._NAE_zip'},
        'confirm_terms': {'name': 'billingForm.agreement'},
        'card_submit': {'class_name': "btnC"}
    },
    'CCF': {
        #optional signIn (op_sign)
        'op_sign_link': {'xpath': "//div[@id='optionalSignInLink']//a"},
        'op_sign_form': {'id': "optionalSignInFormFields"},
        'op_sign_email': {'id': 'email'},
        'op_sign_passwd': {'id': 'optionalSignIn-password'},
        'op_sign_submit': {'xpath': "//div[@id='optionalSignIn-bd']//button"},


        #driver details
        'first_name': {'class_name': 'seleniumFirstName'},
        'last_name': {'class_name': 'seleniumLastName'},
        'email': {'class_name': 'seleniumEmailAddress'},
        'conf_email': {'class_name': 'seleniumConfirmEmailAddress'},
        'phone': {'class_name': 'seleniumPhoneNumber'},
        'age_and_deposit': {'class_name': 'ageAndDepositTerms'},

        #insurance section
        #ins means insurance
        'ins_header': {'class_name': 'carSinglePageInsurance'},
        #Locators for both static and dynamic insurance
        'ins_yes': {'xpath': "//input[@id='insurancePurchaseCheckTrue'] | //input[@value='staticInsuranceYes']"},
        'ins_no': {'xpath': "//input[@id='insurancePurchaseCheckFalse'] | //input[@value='staticInsuranceNo']"},

        'confirm_terms': {'class_name': 'seleniumDepositTypeTermsAccepted'},

        #payment section
        'payment_section': {'class_name': "paymentMethod"},

        #credit card
        'card_btn': {'id': "creditCard"},
        'card_num': {'class_name': 'seleniumCreditCardNumber'},
        'card_month': {'id': "cardExpiryMonth-button"},
        'card_year': {'id': "cardExpiryDate-button"},
        'card_code': {'class_name': 'seleniumSecurityCode'},
        #card fn - first name, ln - last name
        'card_fn': {'id': 'creditCard.billingFirstName'},
        'card_ln': {'id': 'creditCard.billingLastName'},
        'card_address': {'id': 'creditCard.address'},
        'card_city': {'id': 'creditCard.city'},
        'card_state': {'class_name': "cardState"},
        'card_zip': {'name': 'creditCard.postalCode'},
        'card_submit': {'id': "billingConfirm"},

        #saved payment methods, bml means BillMeLater
        'saved_card_btn': {'id': "CREDIT_CARD_0"},
        'saved_card_code': {'id': 'SAVED_CREDIT_CARD_0_CVV'},
        'saved_bml_btn': {'id': "BILL_ME_LATER_2"},

        #BillMeLater locators
        'bml_btn': {'xpath': "//input[@id='billMeLater']"},
        #BillMeLater fn - first name, ln - last name
        'bml_fn': {'name': "billMeLater.holder.firstName"},
        'bml_ln': {'name': "billMeLater.holder.lastName"},
        'bml_address': {'id': "billMeLater.billingAddress.address"},
        'bml_city': {'id': "billMeLater.billingAddress.city"},
        'bml_state': {'name': "billMeLater.billingAddress.state"},
        'bml_zip': {'name': "billMeLater.billingAddress.postalCode"},
        'bml_phone_region': {'id': "billMeLater.billingPhoneRegion"},
        'bml_phone_num': {'id': "billMeLater.billingPhoneNumber"},
        'bml_proceed': {'id': "goToBillMeLater"},
        #On BML website
        'bml_month': {'id': 'date_of_birth_month'},
        'bml_date': {'id': 'date_of_birth_day'},
        'bml_year': {'id': 'date_of_birth_year'},
        'bml_code': {'name': 'ssn'},
        'bml_terms': {'id': "esign_consent"},
        'bml_submit': {'id': "submit_button"},

        #HotDollars (hd)
        'hd_btn': {'id': "hotDollarsChecked"},

        #PayPal (pp)
        'pp_btn': {'xpath': "//input[@id='payPal']"},
        #PayPal fn - first name, ln - last name
        'pp_fn': {'id': "payPal.holder.firstName"},
        'pp_ln': {'id': "payPal.holder.lastName"},
        'pp_address': {'id': "payPal.billingAddress.address"},
        'pp_city': {'id': "payPal.billingAddress.city"},
        'pp_state': {'name': "payPal.billingAddress.state"},
        'pp_zip': {'name': "payPal.billingAddress.postalCode"},
        'pp_proceed': {'id': "goToPayPal"},
        #On PayPal website
        'pp_load': {'id': "loadLogin"},
        'pp_email': {'id': 'login_email'},
        'pp_passwd': {'id': 'login_password'},
        'pp_submit': {'id': "submitLogin"},
        'pp_continue': {'id': "continue"},
    }
}

my_account = {
    'International': {
        'header': {'class_name': "account"},
        'form': {'css': 'div.logInModule form'},
        'email': {'id': "email"},
        'password': {'id': "password"},
        'submit': {'css': "div.signInModule button"},
    },
    'Domestic': {
        'header': {'id': "globalAccountStatusMessaging"},
        'form': {'css': 'div#signInBox form'},
        'email': {'name': "_NAE_emailLogin"},
        'password': {'name': "_NAE_passwordLogin"},
        'submit': {'css': "div.signInBox button"},
    }
}

email = {
    'gmail': {
        'email': {'id': "Email"},
        'password': {'id': "Passwd"}
    },
    'yahoo': {
        'email': {'id': "username"},
        'password': {'id': "passwd"},
    }
}

c3 = {
    'user': {'id': "username"},
    'password': {'id': "password"},
    'email': {'id': "emailAddress"}
}
