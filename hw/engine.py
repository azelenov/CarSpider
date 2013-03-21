from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys

from time import asctime

from settings import browser_positions,intl_urls, main_config
import sys
from webdriverplus import WebDriver


class Engine():
    def __init__(self,params,num):
      self.pos = num
      self.params = params
      domain = params.get('domain')
      if not domain: domain = main_config['domain']
      if domain in ['uk']:
         urls = intl_urls
         self.domain = 'intl'
      elif domain in ['us']:
         urls = intl_urls
         self.domain = 'domestic'
      env = params['env']
      if env not in urls:
         sys.exit("Enviroment "+env+" not in settings for"+self.domain)
      self.url = urls[env]
      self.engine = self.show()
      self.move()
      self.log("Browser started with new session")
      self.log(self.params)
      self.engine.implicitly_wait(main_config["wait_element"])
      self.go()

    def go(self):
        self.engine.get(self.url)
        assert "Car Hire" in self.engine.title
        self.log("Homepage loaded")

    def show (self):
        if self.params['browser'] == 'firefox':
           fp = wb.FirefoxProfile()
           exts = main_config.get("firefox_extentions")
           if exts:
              for e in exts:
                  fp.add_extension(extension=e)
                  parts = e.replace(".xpi","").split("-")
                  name = "extensions."+parts[0]+".currentVersion"
                  ver = parts[1]
                  print "Firefox extention:",name,ver
                  fp.set_preference(name, ver) #Avoid startup screen
           dr = wb.Firefox(firefox_profile=fp)
        elif self.params['browser'] == 'ie':
           dr = wb.Ie()
        elif self.params['browser'] == 'chrome':
           browser = WebDriver('firefox', reuse_browser=True,quit_on_exit=False)
           browser.get('http://www.google.com')
           browser.quit()
           #sys.exit(browser.session_id)
        return dr


    def move(self):
        if self.pos == 0:
           pos = browser_positions[0]
        elif self.pos == 1:
           pos = browser_positions[1]
        elif self.pos == 2:
           pos = browser_positions[2]
        self.engine.set_window_size(pos["xsize"],pos["ysize"])
        self.engine.set_window_position(pos["xpos"],pos["ypos"])

    def log(self,message):
        t = asctime()
        name = self.engine.name
        print "[{}]<{}>(pos:{}) {}".format(t,name,self.pos,message)

    def xfind(self,loc_name,element = None):
        if element:
           res = element.find_element_by_xpath(intl_clp[loc_name])
        else:
           res = self.engine.find_element_by_xpath(intl_clp[loc_name])
        return res

    def xtype(self,elem_name,text,enter = False):
        loc = self.xfind(elem_name)
        loc.clear()
        loc.send_keys(text)
        if enter: loc.send_keys(Keys.ENTER)

    def cfind(self,class_name,element = None):
        if element:
           res = element.find_element_by_class_name(class_name)
        else:
             res = self.engine.find_element_by_class_name(class_name)
        return res

    def click_text(self,link_text):
        t = self.engine.find_element_by_link_text(link_text)
        time.sleep(self.wait/2)
        t.click()

    def verify(self):
        try:
            assert "Error" not in self.engine.page_source
        except AssertionError:
            if self.attempts > 0:
               self.attempts -= 1
               print "Error on page"
               print "Search attempts left:",self.attempts
               self.fill()
            else:
               print "No attemps left...Sorry"
               sys.exit()

    def random_location (self,list_name):
        with open(list_name) as l:
             vars = l.readlines()
             random.shuffle(vars)
             loc = vars[0].strip()
        return loc

