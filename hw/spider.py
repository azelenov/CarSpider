from Tkinter import *
import os
from settings import main_config,intl_urls,dom_urls

class GUI:
    scenario = []
    EnvFrame = None
    def __init__(self):
        self.root = Tk()
        os.chdir('hw')
        self.root.wm_title("HW CarSpider 2.0")
        self.root.wm_iconbitmap('static/spider.ico')
        self.create_widgets()

    def create_widgets(self):
        self.browsers_widget()
        self.domains_widget()
        self.buttons_widget()
        #self.options_widget()
        self.status_bar()


    def log(self,var):
        info = var.get()
        self.status.config(text=info)


    def make_radios(self,frame,args,var):
        buttons = []
        for d in args:
            r = Radiobutton(frame,text=d,variable = var,
            value=d,
            command=(lambda: self.log(var)))
            buttons.append(r)
            r.pack(side='left')
        return buttons

    def destroy_buts(self,buts):
        for b in buts:
            b.destroy()

    def start(self):
        scenario = []
        if self.firefox.get() == 1: scenario.append({"browser":"firefox"})
        if self.chrome.get() == 1: scenario.append({"browser":"chrome"})
        if self.ie.get() == 1: scenario.append({"browser":"ie"})
        if scenario:
           print scenario
        else:
           print "No browser selected"

    def select_browsers(self):
        for a in self.br_buttons:
            a.select()

    def deselect_browsers(self):
        for a in self.br_buttons:
            a.deselect()

    #Browser Frame
    def browsers_widget(self):
        self.firefox = IntVar()
        self.chrome = IntVar()
        self.ie = IntVar()
        browsers = {'Firefox':self.firefox,'Chrome':self.chrome,'IE':self.ie}
        BrowTypeFrame = LabelFrame(self.root,relief = RAISED,borderwidth=1,text = "Browsers:",padx=5,pady=5)
        BrowTypeFrame.grid(row = 0,column = 0,columnspan=2)
        self.br_buttons = self.create_checks(BrowTypeFrame,browsers)
        print self.br_buttons
        Button(BrowTypeFrame,text='All',command=self.select_browsers).pack(side="left")
        Button(BrowTypeFrame,text='None',command=self.deselect_browsers).pack(side="left")

    def create_checks(self,frame,args):
        cbuts = []
        for t,v in args.items():
            cb = Checkbutton(frame,text=t,variable=v)
            cb.pack(side="left")
            cbuts.append(cb)
        return cbuts

    def buttons_widget(self):
        FuncFrame = Frame(self.root,relief = RAISED)
        FuncFrame.grid(row = 3,column = 0,columnspan=2)
        Button(FuncFrame, text="start",command=self.start).pack(side = 'left')
        Button(FuncFrame, text="search").pack(side = 'left')
        Button(FuncFrame, text="details").pack(side = 'left')
        Button(FuncFrame, text="book").pack(side = 'left')

    def domains_widget(self):
        self.d_var = StringVar()
        DomainFrame = Frame(self.root)
        DomainFrame.grid(row = 1,column = 0,columnspan=2,padx=5,pady=5)
        Label(DomainFrame,text="Domain:").pack(side='left')
        domains = main_config['domains']
        self.d_var.set(main_config['default_domain'])
        self.show_domains(DomainFrame,domains,self.d_var)
        self.change_domain()


    def show_domains(self,frame,args,var):
        for d in args:
            r = Radiobutton(frame,text=d,variable = var,
            value=d,indicatoron = 0,
            command=self.change_domain).pack(side='left')

    def change_domain(self):
        envs = []
        self.e_var = StringVar()
        self.e_var.set('qa')
        self.domain = self.d_var.get()
        if self.domain == 'International':
           envs = intl_urls.keys()
        elif self.domain == 'Domestic':
           envs = dom_urls.keys()
        self.enviroment_widget()
        #print "Env",envs
        #print "Rads",env_rads
        env_rads = self.make_radios(self.EnvFrame,envs,self.e_var)

        #destroy_buts(env_rads)

    def enviroment_widget(self):
        #env = StringVar()
        if self.EnvFrame: self.EnvFrame.destroy()
        self.EnvFrame =LabelFrame(self.root,relief=SUNKEN,borderwidth=1,text="Enviroment",labelanchor='n')
        self.EnvFrame.grid(row = 2,column = 0,columnspan=2,padx=5,pady=5)


    def status_bar(self):
        statusFrame = Frame(self.root,relief = GROOVE,borderwidth = 1)
        statusFrame.grid(row = 6,column = 0,columnspan=2,padx=5,pady=5)
        self.status = Label(statusFrame,text="Please choose options to start crawling",
                     bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(expand=1, fill=X)

    def options_widget(self):
        self.OptionsFrame = LabelFrame(self.root,relief = RAISED,borderwidth =2,text="Options",labelanchor='n')
        self.OptionsFrame.grid(row = 4,column = 0,columnspan=2)
        self.search_widget()

    def search_widget(self):
        SearchFrame = Frame(self.OptionsFrame)
        SearchFrame.pack(side = 'top')
        Label(SearchFrame,text = "Search").grid(row=0,column=0)
        self.s_var = StringVar()
        self.a_var = StringVar()
        self.s_var.set('air')
        Radiobutton(SearchFrame,text='air',variable = self.s_var,value='air').grid(row = 0,column = 1)
        Entry(SearchFrame,width=3,textvariable = self.a_var).grid(row = 0,column = 2)
        Radiobutton(SearchFrame,text='city',variable = self.s_var,value='city').grid(row = 0,column = 3)
        Radiobutton(SearchFrame,text='zip',variable = self.s_var,value='zip').grid(row = 0,column = 4)
        Radiobutton(SearchFrame,text='random',variable = self.s_var,value='random').grid(row = 0,column = 5)





app = GUI()
app.root.mainloop()



###search frame
##SearchFrame = Frame(AllFrame)
##SearchFrame.pack(side = 'top')
##Label(SearchFrame,text = "Search").grid(row=0,column=0)
##Radiobutton(SearchFrame,text='air').grid(row = 0,column = 1)
##Entry(SearchFrame,width=3).grid(row = 0,column = 2)
##Radiobutton(SearchFrame,text='city').grid(row = 0,column = 3)
##Radiobutton(SearchFrame,text='zip').grid(row = 0,column = 4)
##Radiobutton(SearchFrame,text='random').grid(row = 0,column = 5)
##
###Results frame
##SolFrame = LabelFrame(AllFrame,relief = RAISED,borderwidth=1,text = "Solution",labelanchor='n')
##SolFrame.pack(side = 'top',expand=1)
###Label(SolFrame,text = "Solution").grid(row=0,column=1)
##Label(SolFrame,text = "Result:").grid(row=1,column=0)
##Radiobutton(SolFrame,text='first').grid(row = 1,column = 1,sticky='W')
##Radiobutton(SolFrame,text='last').grid(row = 1,column = 2,sticky='W')
##Label(SolFrame,text = "Type:").grid(row=2,column=0)
##Radiobutton(SolFrame,text='opaque').grid(row = 2,column = 1,sticky='W')
##Radiobutton(SolFrame,text='retail').grid(row = 2,column = 2,sticky='W')
##Label(SolFrame,text = "SIPP:").grid(row=3,column=0)
##Entry(SolFrame,width=4).grid(row = 3,column = 1,padx=5,pady=5,sticky='W')
##
###Payment method
##PayFrame = Frame(AllFrame)
##PayFrame.pack(side = 'top')
##Label(PayFrame,text = "Pyment method:").grid(row=0,column=0)
##Radiobutton(PayFrame,text='VISA').grid(row = 0,column = 1,sticky='W')
##Radiobutton(PayFrame,text='MasterCard').grid(row = 0,column = 2,sticky='W')
##
###Email type
##EmailFrame = Frame(AllFrame)
##EmailFrame.pack(side = 'top')
##Label(EmailFrame,text = "Email type:").grid(row=0,column=0)
##Radiobutton(EmailFrame,text='Gmail').grid(row = 0,column = 1,sticky='W')
##Radiobutton(EmailFrame,text='Yahoo').grid(row = 0,column = 2,sticky='W')
