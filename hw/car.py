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
from engine import Engine
import search


def main():

    parser=argparse.ArgumentParser()


    parser.add_argument('mode',help='choose operation type start,search or book',
                      choices=['start','st', 'search','se',
                       'book','bo','details','de'])
    parser.add_argument('env',help='Chose enviroment, E.g. qa, preprod,prod')
    parser.add_argument('-d','--domain',help='Work with other domain. E.g. US domestic',action='store', nargs = '?',choices = ['uk','us'])

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



    drivers=[]

    os.chdir('../hw')
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
            if args.domain:
               br["domain"] = 'us'
            if args.env:
               br["env"] = args.env
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
       driver = Engine(entity,i)
       i +=1
       drivers.append(driver)

    if args.mode == 'start' or args.mode == 'st':
       pass
    elif args.mode == 'search' or args.mode == 'se':
         for driver in drivers:
           d = driver.domain
           p = driver.params
           e = driver.engine
           print d,p,e
           sys.exit()
           if driver.domain == 'intl':
              s = search.IntlSearch(p,e)
           elif driver.domain == 'domestic':
              pass
              #s = search.IntlSearch(p,e)

    elif args.mode == 'details' or args.mode == 'de':
       pass
    elif args.mode == 'book' or args.mode == 'bo':
       pass


if __name__ == '__main__':
    main()