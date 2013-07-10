from webdriverplus import WebDriver

from time import asctime
from settings import browser_positions, main_config
import os
from webdriverplus import WebDriver


class Engine:
    def __init__(self,br):
        self.br_name = br['browser']
        self.move_flag = br['arrange']

    def run(self,num):
        try:
            engine = WebDriver(self.br_name ,
            reuse_browser=True,
            wait=main_config["wait_element"],
            quit_on_exit=True)
            if self.move_flag: self.move(engine,num)
            print
        except Exception  as e:
            print "ERROR:"+str(e)
            print self.br_name+" was closed. Reopening..."
            print "You should relaunch app for reusing browser"
            #self.kill_driver()
##            engine = WebDriver(self.br_name,
##            reuse_browser=False,
##            wait=main_config["wait_element"],
##            quit_on_exit=True)
            if self.move_flag: self.move(engine,num)
        return engine

    def move(self,engine,position):
        if position == 0:
           pos = browser_positions[0]
        elif position == 1:
           pos = browser_positions[1]
        elif position == 2:
           pos = browser_positions[2]
        engine.set_window_size(pos["xsize"],pos["ysize"])
        engine.set_window_position(pos["xpos"],pos["ypos"])


##    def kill_driver(self):
##        print "kill the browser driver"
##        if self.br_name == 'chrome':
##           process = 'chromedriver.exe'
##        elif self.br_name == 'ie':
##           process = 'IEDriverServer.exe'
##        elif self.br_name == 'firefox':
##           process = 'none'
##        for proc in psutil.process_iter():
##           if proc.name == process:
##              proc.kill()

