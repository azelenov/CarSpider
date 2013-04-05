from Tkinter import *
import os
from settings import main_config
import settings
import sys
import json

class CarSpider:
    scenario = []
    EnvFrame = None
    def __init__(self):
        self.root = Tk()
        #os.chdir('hw')
        self.root.wm_title("HW CarSpider 2.0")
        self.root.wm_iconbitmap('static/spider.ico')
        #self.root.geometry("250x150+300+300")
        self.menu_bar()
        self.create_widgets()

    def menu_bar(self):
        menubar = Menu(self.root)
        menubar.add_command(label="File")
        menubar.add_command(label="Help")
        self.root.config(menu=menubar)

    def create_widgets(self):
        self.browsers_widget()
        self.domains_widget()
        self.scenario_widget()
        self.buttons_widget()
        self.options_widget()
        #self.buttons_widget(r=6)
        self.status_bar()

    def log(self,var):
        info = var.get()
        self.status.config(text=info)

    def destroy_buts(self,buts):
        for b in buts:
            b.destroy()

    def start(self):
        #print self.loop.get()
        if self.template.get():
           path = main_config["scenarios_dir"] + "/" + self.json.get()
           with open (path) as js:
                row = json.load(js)
                scenario = row['scenario']
           print scenario
        else:
            scenario = self.make_scenario()


    def make_scenario(self):
        browsers = []
        if self.firefox.get() == 1: browsers.append({"browser":"firefox"})
        if self.chrome.get() == 1: browsers.append({"browser":"chrome"})
        if self.ie.get() == 1: browsers.append({"browser":"ie"})
        if browsers:
           for browser in browsers:
               browser['domain'] = self.domain
               browser['enviroment'] = self.env.get()
               browser['account'] = self.account.get()
               browser['days_from_now'] = self.days_from_now.get()
               browser['trip_duration'] = self.duration.get()
               browser['driver_age'] = self.age.get()
               browser['currency'] = self.currency.get()
               if self.one_way.get():
                  pass
               else:
                  pass

               print browser

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
        self.chrome.set(1)
        self.ie = IntVar()
        browsers = {'Firefox':self.firefox,'Chrome':self.chrome,'IE':self.ie}
        BrowTypeFrame = LabelFrame(self.root,relief = RAISED,
        borderwidth=1,text = "Browsers:",padx=7,pady=7)
        BrowTypeFrame.grid(row = 0,column = 0,columnspan=2)
        self.br_buttons = self.create_checks(BrowTypeFrame,browsers)
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

    def buttons_widget(self,r=4):
        FuncFrame = Frame(self.root,relief = RAISED)
        FuncFrame.grid(row = r,column = 0,columnspan=2)
        Button(FuncFrame, text="start",command=self.start).pack(side = 'left')
        Button(FuncFrame, text="search").pack(side = 'left')
        Button(FuncFrame, text="details").pack(side = 'left')
        Button(FuncFrame, text="book").pack(side = 'left')
        Button(FuncFrame, text="full").pack(side = 'left')
        self.loop = BooleanVar()
        self.loop.set(False)
        self.loop_box = Checkbutton(FuncFrame, text="loop",
                   variable=self.loop)
        self.loop_box.pack(side = 'left')

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
        envs = sorted(self.urls.keys())
        self.env = StringVar()
        self.env.set('qa')
        EnvFrame = Frame(self.root)
        EnvFrame.grid(row = 2,column = 0,columnspan=2,padx=5,pady=5)
        Label(EnvFrame,text="Enviroment:").pack(side='left')
        om = apply(OptionMenu, (EnvFrame, self.env) + tuple(envs))
        om.pack(side='left')


    def scenario_widget(self):
        ScenarioFrame = Frame(self.root,relief = RIDGE,borderwidth=2)
        ScenarioFrame.grid(row = 3,column = 0,columnspan=2,padx = 40,pady = 5)
        self.template = BooleanVar()
        self.template.set(False)
        Checkbutton(ScenarioFrame,text = 'Scenario template',
        variable=self.template,command=self.hide_options).pack(side='left')
        self.json =  StringVar()
        temps = os.listdir(main_config['scenarios_dir'])
        self.json.set(temps[0])
        om = apply(OptionMenu, (ScenarioFrame, self.json) + tuple(temps))
        om.pack(side='left')

    def hide_options(self):
        if self.template.get():
           self.OptionsFrame.grid_forget()
        else:
             self.OptionsFrame.grid(row = 5,column = 0,columnspan=2,padx = 40)

    def status_bar(self):
        statusFrame = Frame(self.root,relief = GROOVE,borderwidth = 1)
        statusFrame.grid(row = 7,column = 0,columnspan=2,padx=5,pady=5)
        self.status = Label(statusFrame,text="Please choose options to start crawling",
                     bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(expand=1, fill=X)

    def options_widget(self):
        self.OptionsFrame = LabelFrame(self.root,
        text="Options",labelanchor='n',relief = RIDGE,borderwidth=4)
        self.OptionsFrame.grid(row = 5,column = 0,columnspan=2,padx = 40)
        self.account_widget()
        self.days_widget()
        self.age_widget()
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
        Label(DayFrame,text = "Start day(today+):").grid(row=0,column=0)
        self.days_from_now = Spinbox(DayFrame, from_=1, to=60,width=3)
        self.days_from_now.grid(row = 0,column=1)
        Label(DayFrame,text = "Duration:").grid(row=0,column=2)
        self.duration = Spinbox(DayFrame, from_=1, to=351,width=3)
        self.duration.grid(row = 0,column=3)

    def age_widget(self):
        AgeFrame = Frame(self.OptionsFrame)
        AgeFrame.pack(side = 'top',padx=5,pady=5)
        Label(AgeFrame,text = "Driver age:").grid(row=0,column=0)
        self.age = IntVar()
        self.age.set(25)
        Entry(AgeFrame, textvariable = self.age,width =3).grid(row=0,column=1)


    def currency_widget(self):
        CurFrame = LabelFrame(self.OptionsFrame,relief = RAISED,borderwidth=1,
        text = "Currency",labelanchor='n')
        CurFrame.pack(side = 'top',padx=5,pady=5)
        #Label(CurFrame,text = "Currency:").grid(row=0,column=0)
        money = main_config['currency']
        self.currency = StringVar()
        self.currency.set('GBP')
        Radiobutton(CurFrame,text='USD',variable = self.currency,value='USD').grid(row = 0,column = 0,sticky='W')
        Radiobutton(CurFrame,text='EUR',variable = self.currency,value='EUR').grid(row = 0,column = 1,sticky='W')
        Radiobutton(CurFrame,text='GBP',variable = self.currency,value='GBP').grid(row = 0,column = 2,sticky='W')
        Radiobutton(CurFrame,text='other',variable = self.currency,value='OTR').grid(row = 1,column = 0,sticky='W')
        Radiobutton(CurFrame,text='random',variable = self.currency,value='rand').grid(row = 1,column = 1,sticky='W')
        Radiobutton(CurFrame,text='code',variable = self.currency,value='code').grid(row = 1,column = 2,sticky='W')
        om = apply(OptionMenu, (CurFrame, self.currency) + tuple(money))
        om.grid(row = 1,column = 2)


    def search_widget(self):
        SearchFrame = LabelFrame(self.OptionsFrame,text = "Search",
                      labelanchor='n',relief = RAISED,borderwidth=1)
        SearchFrame.pack(side = 'top',padx=5,pady=5)
        #Label(SearchFrame,text = "Search:").grid(row=0,column=0)
        self.search = StringVar()
        self.air_code = StringVar()
        self.search.set('air')
        self.air_code.set('LHR')
        Radiobutton(SearchFrame,text='air',variable = self.search,value='air').grid(row = 0,column = 0,sticky='W')
        airCodeFrame = Frame(SearchFrame)
        airCodeFrame.grid(row = 0,column = 1,sticky='W')
        Radiobutton(airCodeFrame,text='air code:',variable = self.search,value='airCode').pack(side="left")
        Entry(airCodeFrame,width=4,textvariable = self.air_code).pack(side="left")
        Radiobutton(SearchFrame,text='city',variable = self.search,value='city').grid(row = 0,column = 2,sticky='W')
        Radiobutton(SearchFrame,text='zip',variable = self.search,value='zip').grid(row = 1,column = 0,sticky='W')
        Radiobutton(SearchFrame,text='random location',variable = self.search,value='random').grid(row = 1,column = 1,sticky='W')
        self.one_way = BooleanVar()
        self.one_way.set(False)
        ow = Checkbutton(SearchFrame,text = 'One way',variable=self.one_way)
        ow.grid(row = 1,column = 2,sticky='W')
        Label(SearchFrame,text="Locations list:").grid(row = 2,column = 1)
        locs = settings.locations.keys()
        self.locations = StringVar()
        self.locations.set(main_config["loc_list"])
        om = apply(OptionMenu, (SearchFrame, self.locations) + tuple(locs))
        om.grid(row = 2,column = 2)


    def results_widget(self):
        ResFrame = LabelFrame(self.OptionsFrame,relief = RAISED,
        borderwidth=1,text = "Solution",labelanchor='n')
        ResFrame.pack(side = 'top',expand=1,padx=10,pady=5)
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
        SippFrame = Frame(ResFrame)
        SippFrame.grid(row=3,column=1,sticky='W')
        Radiobutton(SippFrame,text='SIPP:',variable = self.r_var,value='sipp').pack(side='left')
        Entry(SippFrame,width=6,textvariable = self.sipp_var).pack(side='left')

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

    def account_widget(self):
        LoginFrame = Frame(self.OptionsFrame)
        LoginFrame.pack(side = 'top')
        Label(LoginFrame,text='Account:').grid(row = 0,column = 0)
        self.account = StringVar()
        self.account.set('no_account')
        logins = settings.accounts.keys()
        om = apply(OptionMenu, (LoginFrame, self.account) + tuple(logins))
        om.grid(row = 0,column = 1,padx=3,pady=3)




app = CarSpider()
app.root.mainloop()