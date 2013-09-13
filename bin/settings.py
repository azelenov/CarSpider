#MAIN script configuration
main_config = {
"loc_list":"United Kingdom",
"default_loc":"LHR",
"domains":["International","Domestic","CCF"],
"default_domain":"CCF",
"attempts":2,
"currency":["AUD","NZD","GBP","NOK","CHF","DKK","SEK","EUR","USD"],
"default_currency":"USD",
"default_browser":"firefox",
"default_email":"gmail",
"default_card":"visa",
"autocomplete":True,
#"firefox_extentions":["firebug-1.11.1-fx.xpi"],
"scenarios_dir":"scenarios",
"lists_dir":"lists"
}

hot_keys = {
    'home_page':'<Control-h>',
    'search':'<Control-s>',
    'show_details':'<Control-d>',
    'update_results':'<Control-r>',
    'fill_details':'<Control-f>',
    'book':'<Control-b>',
    'my_account':'<Control-a>',
    'email':'<Control-e>',
    'c3':'<Control-c>',
    'refresh_utils':'<Control-u>',
    'clear_cookies':'<Control-x>'
}

#Browser positions according to screen resolution,
#common multimonitor configuration, left monitor is a main
browser_positions = [
    {
    "id":0,
    "xsize":1000,
    "ysize":1050,
    "xpos":920,
    "ypos":0
    },
    {
    "id":1,
    "xsize":960,
    "ysize":1050,
    "xpos":1920,
    "ypos":0
    },
    {
    "id":2,
    "xsize":960,
    "ysize":1050,
    "xpos":2880,
    "ypos":0
    },
    {
    "id":3,
    "xsize":960,
    "ysize":1050,
    "xpos":0,
    "ypos":0
    },

]
#Default list for each Domain
default_lists = {
'International':'United Kingdom',
'Domestic':'Domestic Popular',
'CCF':'CCF'
}


#Specify testing eviroments urls
urls = {
    'International':
    {
    'qa':'http://www.qa.hotwire.com/uk/car?useCluster=1',
    'qaci':'http://www.qaci.hotwire.com/intl/uk/car',
    'myVM':'http://sje-ozelenov-v:7001/intl/uk/car',
    'local':'http://localhost:7001/intl/uk/car',
    'dev01':'http://dev01.dev.hotwire.com:7001/intl/uk/car',
    'dev05':'http://dev05.dev.hotwire.com:7001/intl/uk/car',
    'preprod':'http://www.preprod.hotwire.com/uk/car',
    'prod':'http://www.hotwire.com/uk/car',
    },

    'Domestic':{
    'qa':'http://www.qa.hotwire.com/car/index.jsp?useCluster=1&vt.CCF13=0&vt.NSI13=1',
    'qaci':'http://www.qaci.hotwire.com/car/index.jsp?vt.CCF13=0&vt.NSI13=1',
    'myVM':'http://sje-ozelenov-v:7001/car/index.jsp?vt.CCF13=0&vt.NSI13=1',
    'local':'http://localhost:7001/car/index.jsp?vt.CCF13=0&vt.NSI13=1',
    'dev01':'http://dev01.dev.hotwire.com:7001/car/index.jsp?vt.CCF13=0&vt.NSI13=1',
    'dev05':'http://dev05.dev.hotwire.com:7001/car/index.jsp?vt.CCF13=0&vt.NSI13=1',
    'preprod':'http://www.preprod.hotwire.com/car/index.jsp?vt.CCF13=0&vt.NSI13=1',
    'prod':'http://www.hotwire.com/car/index.jsp?vt.CCF13=0&vt.NSI13=1',
    },

    'CCF': {
    'qa':'http://www.qa.hotwire.com/car/index.jsp?useCluster=1&vt.CCF13=4&vt.NSI13=1&vt.CLS13=2',
    'dev01':'http://dev01.dev.hotwire.com:7001/car/index.jsp?vt.CCF13=4&vt.NSI13=1&vt.CLS13=2',
    'dev05':'http://dev05.dev.hotwire.com:7001/car/index.jsp?vt.CCF13=4&vt.NSI13=1&vt.CLS13=2',
    'qaci':'http://www.qaci.hotwire.com/car/index.jsp?vt.CCF13=4&vt.NSI13=1&vt.CLS13=2',
    'myVM':'http://sje-ozelenov-v:7001/car/index.jsp?vt.CCF13=4&vt.NSI13=1&vt.CLS13=2',
    'local':'http://localhost:7001/car/index.jsp?vt.CCF13=4&vt.NSI13=1&vt.CLS13=2',
    'preprod':'http://www.preprod.hotwire.com/car/index.jsp?vt.CCF13=4&vt.NSI13=1',
    'prod':'http://www.hotwire.com/car/index.jsp?vt.CCF13=4&vt.NSI13=1&vt.CLS13=2'
    }
}
#Read only documents
help_urls = {
'manual':'https://docs.google.com/document/d/1_AjKDU7TztVdt5XDNDQkOzuwfUgbpOaudYg5rz9i7rE/edit?usp=sharing',
'backlog':'https://docs.google.com/spreadsheet/ccc?key=0AmxBNf0BrexydC11djJYNm92eEprdGRSX0RCVnA3bXc&usp=sharing'
}

#which result is available in Results widget
solutions = {
        'International':{
        'result':['first','last','random']
        },
        'Domestic':{
        'result':['first','last','random','opaque','retail']
        },
        'CCF':{
        'result':['first','last','random','opaque','retail']
        }
}

#emails types (use the same password for my account and email
conf_email = {
    'gmail':{'user':'carspider1@gmail.com','pass':'car@spider'},
    'yahoo':{'user':'carspider1@yahoo.com','pass':'car@spider'},
    'outlook':{'user':'v-ozelenov@hotwire.com','pass':None},
    'payableUser':{'user':'payableUser3@hotwire.com','pass':'testing'},
    'qa_regression':{'user':'qa_regression@hotwire.com','pass':'hotwire333'}
}

#Driver info fields
driver_info =  {
    'International':{
    'first_name':'CarSpider',
    'last_name':'TestBooking',
    'phone':'44-20-8203-6420',
    'address':'44a Albert Rd',
    'city':'London'
    },
    'Domestic':{
    'first_name':'CarSpider',
    'last_name':'TestBooking',
    'phone':'2525252500',
    'address':'655 Montgomery Street Suite 600',
    'city':'San Francisco',
    'state':'CA',
    'zip':'94111'
    },
    'CCF':{
    'first_name':'CarSpider',
    'last_name':'TestBooking',
    'phone':'2525252500',
    'address':'655 Montgomery Street Suite 600',
    'city':'San Francisco',
    'state':'CA',
    'zip':'94111'
    }
}

#payment types (security code if not specified 111
payment_methods = {
    'International':{
    'Visa':{
    'name':['VISA','VISA DEBIT','VISA ELECTRON'],
    'number':'4263971921001307'},
    'Mastercard':{
    'name':['MASTER CARD'],
    'number':'5425232820001308'}
     },
     'Domestic':{
     'Visa':{'number':'4111111111111111'},
     'Mastercard':{'number':'5555555555554444'},
     'American Express':{
     'number':'373235387881007',
     'code':'1111'},
     'Discover':{'number':'6011000990139424'},
     'JCB Card':{'number':'3566111111111113'}
     },
     'CCF':{
     'Visa':{'number':'4111111111111111'},
     'Mastercard':{'number':'5555555555554444'},
     'American Express':{
     'number':'373235387881007',
     'code':'1111'},
     'Discover':{'number':'6011000990139424'},
     'JCB Card':{'number':'3566111111111113'},
     'BillMeLater':None,
     'PayPal':None,
     'HotDollars':{'number':'4111111111111111'},
     'SavedCard':None,
     'SavedBML':None
     }
}

BillMeLater = {
    'first_name':'BARBARA',
    'last_name':'MERCHANTC',
    'address':'2306 YORK ROAD',
    'city':'TIMONIUM',
    'state':'MD',
    'zip':'21093',
    'phone_region':'443',
    'phone_number':'9211900',
    'birth_date':'02',
    'birth_mon':'Aug',
    'birth_year':'1971',
    'ssn':'4002'
     }

PayPal = {
    'first_name':'PayPal',
    'last_name':'TestBooking',
    'address':'2306 YORK ROAD',
    'city':'TIMONIUM',
    'state':'MD',
    'zip':'21093',
    'user':'hotwire@paypal.com',
    'password':'expedia1'
       }

c3_user = {
    'user':'csrcroz1',
    'password':'Admin1234!'
}