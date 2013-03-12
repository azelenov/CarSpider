#-------------------------------------------------------------------------------
# Name:        carspy
# Purpose:     help with manual testing
#
# Author:      v-ozelenov
#
# Created:     23/01/2013
# Copyright:   (c) v-ozelenov 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import argparse
from selenium import webdriver as wb
from search import find
from results import IntlResults
from book import IntlBook
import sys
import json
import random
import os
from settings import browser_positions,intl_urls, main_config



def show (params,num):
    if params['browser'] == 'firefox':
       fp = wb.FirefoxProfile()
       exts = main_config.get("firefox_extentions")
       if exts:
          for e in exts:
              fp.add_extension(extension=e)
              parts = e.replace(".xpi","").split("-")
              name = "extensions."+parts[0]+".currentVersion"
              ver = parts[1]
              print "Extention:",name,ver
              fp.set_preference(name, ver) #Avoid startup screen
       dr = wb.Firefox(firefox_profile=fp)
       print "Firefox started"
    elif params['browser'] == 'ie':
       dr = wb.Ie()
       print "Internet explorer started"
    elif params['browser'] == 'chrome':
       dr = wb.Chrome()
       print "Chrome started"
    move(dr,num)
    return dr


def move(browser,place):
    if place == 0:
       pos = browser_positions[0]
    elif place == 1:
       pos = browser_positions[1]
    elif place == 2:
       pos = browser_positions[2]
    browser.set_window_size(pos["xsize"],pos["ysize"])
    browser.set_window_position(pos["xpos"],pos["ypos"])


def main():

    parser=argparse.ArgumentParser()


    parser.add_argument('mode',help='choose operation type start,search or book',
                      choices=['start','st', 'search','se',
                       'book','bo','details','de'])
    parser.add_argument('domain',help='chose domain')
    parser.add_argument('-f','--firefox',help='firefox webbrowser',action='store_true')
    parser.add_argument('-c','--chrome',help='chrome webbrowser',action='store_true')
    parser.add_argument('-i','--ie',help='Internet Explorer webbrowser',action='store_true')
    parser.add_argument('-a','--air',help='Airport search',action='store',default = main_config["default_loc"], nargs = '?')
    parser.add_argument('-l','--city',help='Local town/city search',action='store_true')
    parser.add_argument('-z','--zip',help='Local zip search',action='store_true')
    parser.add_argument('-r','--rand',help='Random local/air search',action='store_true')
    parser.add_argument('-o','--oway',help='One-way search',action='store_true')
    parser.add_argument('-e','--exchange',help='Specify currency(exchange) \
    in format e.g. usd, eur. Special formats rnd = random currenct,\
     otr - any currency except of usd, gbp,eur')
    parser.add_argument('-v','--visa',help='Visa card booking',action='store_true')
    parser.add_argument('-m','--mc',help='Mastercard/maestro booking',action='store_true')
    parser.add_argument('-g','--gmail',help='Gmail confirmation email',action='store_true')
    parser.add_argument('-y','--yahoo',help='Yahoo confirmation email',action='store_true')
    parser.add_argument('-j','--json',help='JSON file with parameters')
    #parser.add_argument('--emul',help='Switch rest simulator',choices = ['on','off'])



    args=parser.parse_args()

    urls = intl_urls
    if args.domain not in intl_urls:
       sys.exit("Domain "+args.domain+" in settings!")
    else:
       url = intl_urls[args.domain]

    drivers=[]

    #os.chdir('../hw')
    if args.json:
       path = main_config["scenarios_dir"] + "/" + args.json + ".json"
       with open (path) as js:
         row = json.load(js)
       scenario = row['scenario']
    else:
         scenario = []
         if args.firefox: scenario.append({"browser":"firefox"})
         if args.chrome: scenario.append({"browser":"chrome"})
         if args.ie: scenario.append({"browser":"ie"})
         if not args.firefox and not args.chrome and not args.ie:
            scenario.append({"browser":main_config["default_browser"]})
         for br in scenario:
            #print args.air
            if args.city:
                br["pickup_loc"] = "city"
            elif args.zip:
                br["pickup_loc"] = "zip"
            elif args.rand:
                br["pickup_loc"] = random.choice(["zip","city","air"])
            elif args.air == None:
                br["pickup_loc"] = "air"
            elif args.air != None:
                br["pickup_loc"] = args.air.upper()


            if args.oway:
                if args.city:
                   br["dropoff_loc"] = "city"
                elif args.zip:
                     br["dropoff_loc"] = "zip"
                elif args.rand:
                     br["dropoff_loc"] = random.choice(["zip","city","air"])
                elif args.air == None:
                     br["dropoff_loc"] = "air"
                elif args.air != None:
                     br["dropoff_loc"] = args.air.upper()


            if args.exchange:
               br["currency"] = args.exchange

            if args.gmail: br["email_type"] = "gmail"
            if args.yahoo: br["email_type"] = "yahoo"
            if args.visa: br["card_vendor"] = "visa"
            if args.mc: br["card_vendor"] = "mc"

            if not args.gmail and not args.yahoo:
               br["email_type"] = main_config["default_email"]
            if not args.visa and not args.mc:
               br["card_vendor"] = main_config["default_card"]

    print scenario
    #sys.exit()

    i = 0
    for entity in scenario:
       if args.mode == 'book' and (not entity.has_key("email_type")  or
       not entity.has_key("card_vendor") ):
           sys.exit("Please specify email type and card vendor for booking!")
       driver = show(entity,i)
       i +=1
       drivers.append(driver)

    if args.mode == 'start' or args.mode == 'st':
       find(url,drivers,scenario, False)
    elif args.mode == 'search' or args.mode == 'se':
       find(url,drivers,scenario, True)
       results = IntlResults(drivers,scenario)
    elif args.mode == 'details' or args.mode == 'de':
       find(url,drivers,scenario, True)
       results = IntlResults(drivers,scenario)
       results.rand_solution()
       book = IntlBook(drivers,scenario)
       book.fill()
    elif args.mode == 'book' or args.mode == 'bo':
       find(url,drivers,scenario, True)
       results = IntlResults(drivers,scenario)
       book = IntlBook(drivers,scenario)
       book.fill(True)


if __name__ == '__main__':
    main()