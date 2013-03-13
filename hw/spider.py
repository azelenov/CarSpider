from Tkinter import *
import os
from settings import main_config

def show_choice(var):
    info = var.get()
    #print info
    status.config(text=info)

def log(t):
    status.config(text=t)

def make_radios(frame,args,var):
    for d in args:
        r = Radiobutton(frame,text=d,indicatoron = 0,variable = var,
        value=d,
        command=(lambda: show_choice(var))).pack(side='left')

def start():
    scenario = []
    if firefox.get() == 1:
         scenario.append({"browser":"firefox"})
    elif chrome.get() == 1:
         scenario.append({"browser":"chrome"})
    elif ie.get() == 1:
         scenario.append({"browser":"ie"})
    print scenario

scenario = []
root = Tk()
os.chdir('hw')
root.wm_title("HW CarSpider 2.0")
root.wm_iconbitmap('static/spider.ico')

menu = Menu(root)

#Browser Frame
firefox = IntVar()
chrome = IntVar()
ie = IntVar()
AllBr = IntVar()
NoBr = IntVar()
BrowTypeFrame = LabelFrame(root,relief = RAISED,borderwidth=1,text = "Browsers:",padx=5,pady=5)
BrowTypeFrame.grid(row = 0,column = 0,columnspan=2)

Checkbutton(BrowTypeFrame,text='All',variable=AllBr).grid(row = 0,column = 0)
Checkbutton(BrowTypeFrame,text='Firefox',variable=firefox).grid(row = 0,column = 1)
Checkbutton(BrowTypeFrame,text='Chrome',variable=chrome).grid(row = 0,column = 2)
Checkbutton(BrowTypeFrame,text='IE',variable=ie).grid(row = 0,column = 3)
Checkbutton(BrowTypeFrame,text='None',variable=NoBr).grid(row = 0,column = 4)


domain = StringVar()
DomainFrame = Frame(root)
DomainFrame.grid(row = 1,column = 0,columnspan=2,padx=5,pady=5)
Label(DomainFrame,text="Domain:").pack(side='left')
domains = main_config['domains']
domain.set(main_config['default_domain'])
make_radios(DomainFrame,domains,domain)

env = StringVar()
print domain.get()
EnvFrame =LabelFrame(root,relief=SUNKEN,borderwidth=1,text="Enviroment",labelanchor='n')
EnvFrame.grid(row = 2,column = 0,columnspan=2,padx=5,pady=5)
#Label(EnvFrame,text="Enviroment:").pack(side = 'top')
Radiobutton(EnvFrame,text='Local').pack(side = 'left')
Radiobutton(EnvFrame,text='Dev').pack(side = 'left')
Radiobutton(EnvFrame,text='QACI').pack(side = 'left')
Radiobutton(EnvFrame,text='QA').pack(side = 'left')
Radiobutton(EnvFrame,text='PREPROD').pack(side = 'left')
Radiobutton(EnvFrame,text='PROD').pack(side = 'left')

FuncFrame = Frame(root,relief = RAISED)
FuncFrame.grid(row = 3,column = 0,columnspan=2)
Button(FuncFrame, text="start",command=start).pack(side = 'left')
Button(FuncFrame, text="search").pack(side = 'left')
Button(FuncFrame, text="details").pack(side = 'left')
Button(FuncFrame, text="book").pack(side = 'left')

OptionsFrame = LabelFrame(root,relief = RAISED,borderwidth =2,text="Options",labelanchor='n')
OptionsFrame.grid(row = 4,column = 0,columnspan=2)

#BrowserFrame = Frame(OptionsFrame,relief = GROOVE,borderwidth =1)
#BrowserFrame.grid(row = 0,column = 0)
#Radiobutton(BrowserFrame,text='By browser').pack()

AllFrame = Frame(OptionsFrame,relief = GROOVE,borderwidth = 1)
AllFrame.grid(row = 0,column = 0)
#Radiobutton(AllFrame,text='All browsers').pack()


#search frame
SearchFrame = Frame(AllFrame)
SearchFrame.pack(side = 'top')
Label(SearchFrame,text = "Search").grid(row=0,column=0)
Radiobutton(SearchFrame,text='air').grid(row = 0,column = 1)
Entry(SearchFrame,width=3).grid(row = 0,column = 2)
Radiobutton(SearchFrame,text='city').grid(row = 0,column = 3)
Radiobutton(SearchFrame,text='zip').grid(row = 0,column = 4)
Radiobutton(SearchFrame,text='random').grid(row = 0,column = 5)

#Solution frame
SolFrame = LabelFrame(AllFrame,relief = RAISED,borderwidth=1,text = "Solution",labelanchor='n')
SolFrame.pack(side = 'top',expand=1)
#Label(SolFrame,text = "Solution").grid(row=0,column=1)
Label(SolFrame,text = "Result:").grid(row=1,column=0)
Radiobutton(SolFrame,text='first').grid(row = 1,column = 1,sticky='W')
Radiobutton(SolFrame,text='last').grid(row = 1,column = 2,sticky='W')
Label(SolFrame,text = "Type:").grid(row=2,column=0)
Radiobutton(SolFrame,text='opaque').grid(row = 2,column = 1,sticky='W')
Radiobutton(SolFrame,text='retail').grid(row = 2,column = 2,sticky='W')
Label(SolFrame,text = "SIPP:").grid(row=3,column=0)
Entry(SolFrame,width=4).grid(row = 3,column = 1,padx=5,pady=5,sticky='W')

#Payment method
PayFrame = Frame(AllFrame)
PayFrame.pack(side = 'top')
Label(PayFrame,text = "Pyment method:").grid(row=0,column=0)
Radiobutton(PayFrame,text='VISA').grid(row = 0,column = 1,sticky='W')
Radiobutton(PayFrame,text='MasterCard').grid(row = 0,column = 2,sticky='W')

#Email type
EmailFrame = Frame(AllFrame)
EmailFrame.pack(side = 'top')
Label(EmailFrame,text = "Email type:").grid(row=0,column=0)
Radiobutton(EmailFrame,text='Gmail').grid(row = 0,column = 1,sticky='W')
Radiobutton(EmailFrame,text='Yahoo').grid(row = 0,column = 2,sticky='W')

FuncFrame = Frame(root,relief = RAISED)
FuncFrame.grid(row = 5,column = 0,columnspan=2)
Button(FuncFrame, text="start").pack(side = 'left')
Button(FuncFrame, text="search").pack(side = 'left')
Button(FuncFrame, text="details").pack(side = 'left')
Button(FuncFrame, text="book").pack(side = 'left')

statusFrame = Frame(root,relief = GROOVE,borderwidth = 1)
statusFrame.grid(row = 6,column = 0,columnspan=2,padx=5,pady=5)
status = Label(statusFrame,text="Please choose options to start crawling",
             bd=1, relief=SUNKEN, anchor=W)
status.pack(expand=1, fill=X)

root.mainloop()
