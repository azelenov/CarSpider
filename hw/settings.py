#MAIN script configuration
main_config = {
"ui_wait":1, #time in seconds for watching on ui elements
"wait_element":5,
"wait_on_page":1,
"loc_list":"United Kingdom",
"default_loc":"LHR",
"domains":["International","Domestic","CCF"],
"default_domain":"International",
"attempts":2,
"currency":["AUD","NZD","GBP","NOK","CHF","DKK","SEK","EUR","USD"],
"default_browser":"chrome",
"default_email":"gmail",
"default_card":"visa",
"autocomplete":True,
#"firefox_extentions":["firebug-1.11.1-fx.xpi"],
"scenarios_dir":"scenarios",
"lists_dir":"lists"


}

#Browser positions according to screen resolution
browser_positions = [
    {
    "id":0,
    "xsize":960,
    "ysize":1050,
    "xpos":960,
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

default_lists = {
'International':'United Kingdom',
'Domestic':'Domestic Popular',
'CCF':'CCF'
}


#Specify testing eviroments urls

urls = {
     'International':
    {
    'qa':'http://www.qa.hotwire.com/uk/car',
    'qaci':'http://www.qaci.hotwire.com/intl/car',
    'sfo':'http://sfo-5ozelenov-v:7001/intl/car',
    'local':'http://localhost:7001/intl/car',
    'dev':'http://dev05.dev.hotwire.com:7001/intl/uk/car',
    'preprod':'http://www.preprod.hotwire.com/uk/car',
    'prod':'http://www.hotwire.com/uk/car',
    },

    'Domestic':{
    'qa':'http://www.qa.hotwire.com/car/index.jsp?vt.CCF13=0',
    'qaci':'http://www.qaci.hotwire.com/car/index.jsp?vt.CCF13=0',
    #'sfo':'http://sfo-5ozelenov-v:7001/car/index.jsp?vt.CCF13=0',
    #'local':'http://localhost:7001/car/index.jsp?vt.CCF13=0',
    'dev':'http://dev05.dev.hotwire.com:7001/car/index.jsp?vt.CCF13=0',
    'preprod':'http://www.preprod.hotwire.com/car/index.jsp?vt.CCF13=0',
    'prod':'http://www.hotwire.com/car/index.jsp?vt.CCF13=0',
    },

    'CCF': {
    'qa':'http://www.qa.hotwire.com/car/index.jsp?vt.CCF13=2',
    'dev':'http://dev05.dev.hotwire.com:7001/car/index.jsp?vt.CCF13=2',
    'qaci':'http://www.qaci.hotwire.com/car/index.jsp?vt.CCF13=2',
    'preprod':'http://www.preprod.hotwire.com/car/index.jsp?vt.CCF13=2',
    'prod':'http://www.hotwire.com/car/index.jsp?vt.CCF13=2'
    }
}

#refreshUtil urls
ref_urls =  {
'qa':'http://www.qa.hotwire.com/test/refreshUtil.jsp',
'qaci':'http://www.qaci.hotwire.com/test/refreshUtil.jsp',
'sfo':'http://sfo-5ozelenov-v:7001/test/refreshUtil.jspr',
'local':'http://localhost:7001/test/refreshUtil.jsp',
'dev':'http://dev05.dev.hotwire.com:7001/test/refreshUtil.jsp',
'preprod':'http://www.preprod.hotwire.com/test/refreshUtil.jsp'
}


solutions = {
        'International':{
        'result':['first'],
        #'check':['none','policy','amenities','all_policy','all_amenities']
        'check':['none']
        },
        'Domestic':{
        'result':['first'],
        #'result':['first','last','random','opaque','retail'],

        'check':['none']},
        'CCF':{
        'result':['first'],
        #'result':['first','last','random','opaque','retail'],
        'check':['none']
        }
}

#Login options
accounts = {
       'no_account':{
                     'login':None
                     },
       'gmail': {
                'type':'regular',
                'login':'alex.hotwire@gmail.com',
                'pass':'password'
       },
       'yahoo':{
                'type':'regular',
                'login':'alex.hotwire@yahoo.com',
                'pass':'password'
       },
       'forC3':{
                'type':'regular',
                'login':'ozelenov@luxoft.com',
                'pass':'password'
       },
       'guest_visa':{
                'type':'guest',
                'login':'alex.hotwire@gmail.com',
                'pass':'01307'
       }
}


#Driver info fields
driver_info =  {
    'International':{
    'first_name':'Selenium',
    'last_name':'Hotwire',
    'phone':'44-20-8203-6420',
    'address':'44a Albert Rd',
    'city':'London'
    },
    'Domestic':{
    'first_name':'Selenium',
    'last_name':'Hotwire',
    'phone':'2525252500',
    'address':'655 Montgomery Street Suite 600',
    'city':'San Francisco',
    'state':'CA',
    'zip':'94111'
    },
    'CCF':{
    'first_name':'Selenium',
    'last_name':'Hotwire',
    'phone':'2525252500',
    'address':'655 Montgomery Street Suite 600',
    'city':'San Francisco',
    'state':'CA',
    'zip':'94111'
    }
}

#emails types
conf_email = {
    'gmail':'carspider1@gmail.com',
    'yahoo':'carspider1@yahoo.com',
    'outlook':'v-ozelenov@hotwire.com'
}

#credit card types
cards = {
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
     'JCB Card':{'number':'3566111111111113'}
     }
}



