#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      v-ozelenov
#
# Created:     30/01/2013
# Copyright:   (c) v-ozelenov 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import json

def main():
    with open ("search.json") as File:
         row = json.load(File)

         print row['search']['rates'][0]['id']

if __name__ == '__main__':
    main()
