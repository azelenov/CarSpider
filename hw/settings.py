import lists

#MAIN script configuration
main_config = {
"wait":1, #time in seconds for watching on ui elements
"wait_element":5,
"wait_on_page":1,
"loc_list":lists.uk_list,
"default_loc":"LHR",
"domains":["International","Domestic"],
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

#Specify browser positions according to your screen resolution
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

#Specify testing eviroments urls
intl_urls = {
'qa':'http://www.qa.hotwire.com/uk/car',
'qaci':'http://www.qaci.hotwire.com/intl/car',
'sfo':'http://sfo-5ozelenov-v:7001/intl/car',
'local':'http://localhost:7001/intl/car',
'dev':'http://dev05.dev.hotwire.com:7001/intl/uk/car',
'preprod':'http://www.preprod.hotwire.com/uk/car',
'prod':'http://www.hotwire.com/uk/car',
}
dom_urls = {
'qa':'http://www.qa.hotwire.com/car',
'qaci':'http://www.qaci.hotwire.com/car'
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
intl_card ={
    'visa':{
    'name':['VISA','VISA DEBIT','VISA ELECTRON'],
    'number':'4263971921001307'
    },
    'mc':{
    'name':['MASTER CARD'],
    'number':'5425232820001308'
    }
}


