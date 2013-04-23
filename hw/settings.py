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
"default_browser":"firefox",
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
    #'sfo':'http://sfo-5ozelenov-v:7001/intl/car',
    #'local':'http://localhost:7001/intl/car',
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
    'qaci':'http://www.qaci.hotwire.com/car/index.jsp?vt.CCF13=0',
    'preprod':'http://www.preprod.hotwire.com/car/index.jsp?vt.CCF13=0',
    'prod':'http://www.hotwire.com/car/index.jsp?vt.CCF13=0'
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
driver_info = {
'first_name':'Tester',
'last_name':'Selenium',
'phone':'44-20-8203-6420',
'address':'44a Albert Rd',
'city':'London'
}

#emails types
conf_email = {
    'gmail':'alex.hotwire@gmail.com',
    'yahoo':'alex.hotwire@yahoo.com',
    'outlook':'v-ozelenov@hotwire.com'
}

#credit card types
cards = {
    'International':{
    'Visa':{
    'name':['VISA','VISA DEBIT','VISA ELECTRON'],
    'number':'4263971921001307'
    },
    'MC':{
    'name':['MASTER CARD'],
    'number':'5425232820001308'
         }
     },
     'Domestic':{
     'Visa':{
     'name':['VISA'],
     'number':''
     }},
     'CCF':{
     'Visa':{
     'name':['VISA'],
     'number':''
            }}
     }



