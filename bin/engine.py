from webdriverplus import WebDriver

from time import asctime
from settings import browser_positions, main_config
import os
from webdriverplus import WebDriver
import tkMessageBox
import psutil
import threading

class Engine(threading.Thread):
    def __init__(self,br,arrange,timeout):
        threading.Thread.__init__(self)
        self.br_name = br['browser']
        self.timeout = timeout
        if not self.timeout: self.timeout = main_config["wait_element"]
        self.move_flag = arrange

    def run(self,num):
        try:
            engine = WebDriver(self.br_name ,
            reuse_browser=True,
            wait=self.timeout,
            quit_on_exit=True)
            if self.move_flag: self.move(engine,num)
            print
        except Exception  as e:
            print "ERROR:"+str(e)
            #print self.br_name+" was closed. Reopening..."
            print "You should relaunch app for reusing browser"
            answer = tkMessageBox.askokcancel("Browser Closed!",
            "Browser window closed manually.\
            \nWebdriver connection refused...\
            \nRelaunch the app for using "+self.br_name+" browser?")
            self.kill_drivers()
            if answer:
                print os.listdir(os.curdir)
                os.execl('..\App\python.exe','python','spider.py')

##            engine = WebDriver(self.br_name,
##            reuse_browser=False,
##            wait=main_config["wait_element"],
##            quit_on_exit=True)
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


    def kill_drivers(self):
        print "kill browsers driver"
        for proc in psutil.process_iter():
           if proc.name in ['chromedriver.exe','IEDriverServer.exe']:
              proc.kill()

##e1 = Engine({'browser':'firefox'},1,10)
##e2 = Engine({'browser':'chrome'},1,10)
##e1.run(0)
##e2.run(1)
