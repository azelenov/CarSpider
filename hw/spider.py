from Tkinter import *
import os
from settings import main_config
import settings
import sys

class CarSpider:
    scenario = []
    EnvFrame = None
    def __init__(self):
        self.root = Tk()
        #os.chdir('hw')
        self.root.wm_title("HW CarSpider 2.0")
        self.root.wm_iconbitmap('static/spider.ico')
        self.create_widgets()

    def create_widgets(self):
        self.browsers_widget()
        self.domains_widget()
        self.buttons_widget()
        self.options_widget()
        self.buttons_widget(r=5)
        self.status_bar()


    def log(self,var):
        info = var.get()
        self.status.config(text=info)

    def make_radios(self,frame,args,var):
        buttons = []
        for d in args:
            r = Radiobutton(frame,text=d,variable = var,value=d)
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
        BrowTypeFrame = LabelFrame(self.root,relief = RAISED,
        borderwidth=1,text = "Browsers:",padx=5,pady=5)
        BrowTypeFrame.grid(row = 0,column = 0,columnspan=2)
        self.br_buttons = self.create_checks(BrowTypeFrame,browsers)
        print self.br_buttons
        all_br = Button(BrowTypeFrame,text='All',command=self.select_browsers)
        all_br.pack(side="left")
        none_br = Button(BrowTypeFrame,text='None',command=self.deselect_browsers)
        none_br.pack(side="left")

    def create_checks(self,frame,args):
        cbuts = []
        for t,v in args.items():
            cb = Checkbutton(frame,text=t,variable=v)
            cb.pack(side="left")
            cbuts.append(cb)
        return cbuts

    def buttons_widget(self,r=3):
        FuncFrame = Frame(self.root,relief = RAISED)
        FuncFrame.grid(row = r,column = 0,columnspan=2)
        Button(FuncFrame, text="start",command=self.start).pack(side = 'left')
        Button(FuncFrame, text="search").pack(side = 'left')
        Button(FuncFrame, text="details").pack(side = 'left')
        Button(FuncFrame, text="book").pack(side = 'left')
        Button(FuncFrame, text="full").pack(side = 'left')
        Button(FuncFrame, text="loop").pack(side = 'left')

    def domains_widget(self):
        self.d_var = StringVar()
        DomainFrame = Frame(self.root)
        DomainFrame.grid(row = 1,column = 0,columnspan=2,padx=5,pady=5)
        Label(DomainFrame,text="Domain:").pack(side='left')
        domains = main_config['domains']
        #print "Domain",main_config['domains']
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
           self.urls = settings.intl_urls
        elif self.domain == 'Domestic':
           self.urls = settings.dom_urls
        elif self.domain == 'CCF':
           self.urls = settings.ccf_urls
        envs = self.urls.keys()
        self.enviroment_widget()
        self.make_radios(self.EnvFrame,envs,self.e_var)


    def enviroment_widget(self):
        #env = StringVar()
        if self.EnvFrame: self.EnvFrame.destroy()
        self.EnvFrame = LabelFrame(self.root,relief=SUNKEN,borderwidth=1,
        text="Enviroment",labelanchor='n')
        self.EnvFrame.grid(row = 2,column = 0,columnspan=2,padx=5,pady=5)


    def status_bar(self):
        statusFrame = Frame(self.root,relief = GROOVE,borderwidth = 1)
        statusFrame.grid(row = 7,column = 0,columnspan=2,padx=5,pady=5)
        self.status = Label(statusFrame,text="Please choose options to start crawling",
                     bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(expand=1, fill=X)

    def options_widget(self):
        self.OptionsFrame = LabelFrame(self.root,
        text="Options",labelanchor='n',relief = RIDGE,borderwidth=4)
        self.OptionsFrame.grid(row = 4,column = 0,columnspan=2)
        self.days_widget()
        self.currency_widget()
        self.search_widget()
        self.results_widget()
        self.payment_widget()
        self.email_widget()
        self.insurance_widget()
        #self.check_domain()

    def days_widget(self):
        DayFrame = Frame(self.OptionsFrame)
        DayFrame.pack(side = 'top',padx=5,pady=5)
        Label(DayFrame,text = "Number of days:").grid(row=0,column=0)
        s = Spinbox(DayFrame, from_=3, to=350,width=3)
        s.grid(row = 0,column = 1)


    def currency_widget(self):
        CurFrame = Frame(self.OptionsFrame)
        CurFrame.pack(side = 'top',padx=5,pady=5)
        Label(CurFrame,text = "Currency:").grid(row=0,column=0)
        money = main_config['currency']
        self.currency = StringVar()
        self.currency.set('GBP')
        Radiobutton(CurFrame,text='USD',variable = self.currency,value='USD').grid(row = 0,column = 1)
        Radiobutton(CurFrame,text='EUR',variable = self.currency,value='EUR').grid(row = 0,column = 2)
        Radiobutton(CurFrame,text='GBP',variable = self.currency,value='GBP').grid(row = 0,column = 3)
        Radiobutton(CurFrame,text='other',variable = self.currency,value='OTR').grid(row = 1,column = 0)
        Radiobutton(CurFrame,text='random',variable = self.currency,value='rand').grid(row = 1,column = 1)
        Radiobutton(CurFrame,text='code',variable = self.currency,value='code').grid(row = 1,column = 2)
        om = apply(OptionMenu, (CurFrame, self.currency) + tuple(money))
        om.grid(row = 1,column = 2)


    def search_widget(self):
        SearchFrame = LabelFrame(self.OptionsFrame,text = "Search:",
                      labelanchor='n',relief = RAISED,borderwidth=1)
        SearchFrame.pack(side = 'top',padx=5,pady=5)
        #Label(SearchFrame,text = "Search:").grid(row=0,column=0)
        self.s_var = StringVar()
        self.a_var = StringVar()
        self.s_var.set('air')
        self.a_var.set('LHR')
        Radiobutton(SearchFrame,text='air',variable = self.s_var,value='air').grid(row = 0,column = 0,sticky='W')
        Radiobutton(SearchFrame,text='air code',variable = self.s_var,value='airCode').grid(row = 0,column = 1,sticky='W')
        Entry(SearchFrame,width=4,textvariable = self.a_var).grid(row = 0,column = 2,sticky='W')
        Radiobutton(SearchFrame,text='city',variable = self.s_var,value='city').grid(row = 1,column = 0,sticky='W')
        Radiobutton(SearchFrame,text='zip',variable = self.s_var,value='zip').grid(row = 1,column = 1,sticky='W')
        Radiobutton(SearchFrame,text='random',variable = self.s_var,value='random').grid(row = 1,column = 2,sticky='W')
        Label(SearchFrame,text="Locations list:").grid(row = 3,column = 1)
        locs = settings.locations.keys()
        self.locations = StringVar()
        self.locations.set(main_config["loc_list"])
        om = apply(OptionMenu, (SearchFrame, self.locations) + tuple(locs))
        om.grid(row = 3,column = 2,padx=3,pady=3)


    def results_widget(self):
        ResFrame = LabelFrame(self.OptionsFrame,relief = RAISED,
        borderwidth=1,text = "Solution",labelanchor='n')
        ResFrame.pack(side = 'top',expand=1,padx=5,pady=5)
        self.r_var = StringVar()
        self.sipp_var = StringVar()
        self.r_var.set('first')
        self.sipp_var.set('EBMN')
        Label(ResFrame,text = "Result:").grid(row=1,column=0)
        f = Radiobutton(ResFrame,text='first',variable = self.r_var,value='first')
        f.grid(row = 1,column = 1,sticky='W')
        l = Radiobutton(ResFrame,text='last',variable = self.r_var,value='last')
        l.grid(row = 1,column = 2,sticky='W')
        r = Radiobutton(ResFrame,text='random',variable = self.r_var,value='rand')
        r.grid(row = 1,column = 3,sticky='W')
        Label(ResFrame,text = "Type:").grid(row=2,column=0)
        self.o = Radiobutton(ResFrame,text='opaque',
        variable = self.r_var,value='opaque')
        self.o.grid(row = 2,column = 1,sticky='W')
        self.r = Radiobutton(ResFrame,text='retail',
        variable = self.r_var,value='retail')
        self.r.grid(row = 2,column = 2,sticky='W')
        sipp = Radiobutton(ResFrame,text='SIPP:',variable = self.r_var,value='sipp')
        sipp.grid(row=3,column=1,sticky='W')
        s_code = Entry(ResFrame,width=6,textvariable = self.sipp_var)
        s_code.grid(row = 3,column = 2,sticky='W',padx=3,pady=3)

    def payment_widget(self):
        PayFrame = Frame(self.OptionsFrame)
        PayFrame.pack(side = 'top')
        self.p_var = StringVar()
        self.p_var.set('visa')
        Label(PayFrame,text = "Pyment method:").grid(row=0,column=0)
        Radiobutton(PayFrame,text='Visa',variable = self.p_var,value='visa').grid(row = 0,column = 1,sticky='W')
        Radiobutton(PayFrame,text='MasterCard',variable = self.p_var,value='mc').grid(row = 0,column = 2,sticky='W')

    def email_widget(self):
        self.email = StringVar()
        self.email.set('gmail')
        EmailFrame = Frame(self.OptionsFrame)
        EmailFrame.pack(side = 'top')
        Label(EmailFrame,text = "Email type:").grid(row=0,column=0)
        Radiobutton(EmailFrame,text='Gmail',variable = self.email,value='gmail').grid(row = 0,column = 1,sticky='W')
        Radiobutton(EmailFrame,text='Yahoo',variable = self.email,value='yahoo').grid(row = 0,column = 2,sticky='W')

    def insurance_widget(self):
        InsurFrame = Frame(self.OptionsFrame)
        InsurFrame.pack(side = 'top')
        self.insurance = BooleanVar()
        self.insurance.set(False)
        cb = Checkbutton(InsurFrame,text="Insurance",variable=self.insurance)
        cb.pack(side='left')





app = CarSpider()
app.root.mainloop()