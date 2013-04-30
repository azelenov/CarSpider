#! ../App/python.exe

from Tkinter import *
import tkFileDialog
import os
from settings import main_config
from engine import Engine
import settings
import search
import json
import random

class CarSpider:
    def __init__(self):
        self.root = Tk()
        self.list = StringVar()
        #print os.listdir(os.curdir)
        os.chdir('hw')
        self.root.wm_title("HW CarSpider 2.0")
        self.root.wm_iconbitmap('static/spider.ico')
        self.root.geometry("+200+200")
        #self.root.geometry("250x150+300+300")
        self.menu_bar()
        self.create_widgets()

    def menu_bar(self):
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu = Menu(menubar, tearoff=0)
        #filemenu.add_command(label="Open")
        filemenu.add_command(label="Save scenario...",command=self.save_scenario)
        filemenu.add_separator()
        #filemenu.add_command(label="Exit")
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)
        #self.root.protocol("WM_DELETE_WINDOW", self.quit)

    def save_scenario(self):
        scenario = '['
        #scenario_order = ['browser','domain','enviroment','account',
                         # 'days_left','trip_duration','driver_age',
                          #'currency','pick_location','drop_location',
                         # 'solution','payment','email','insurance']
        scenario = self.make_scenario()
        scenario = str(self.make_scenario()).replace(',',',\n').replace('},','},\n').replace("'",'"')
        fileName = tkFileDialog.asksaveasfilename(parent=self.root,
                   filetypes=[('JSON format','*.json')] ,
                   title="Save the scenario as...",
                   initialdir="scenarios/",
                   defaultextension = '.json')
        with open(fileName,'w') as f:
             f.write(scenario)

    def create_widgets(self):
        self.browsers_widget()
        self.domains_widget()
        self.enviroment_widget()
        self.scenario_widget()
        self.buttons_widget()
        self.options_widget()
        self.status_bar()

    def log(self,var):
        info = var.get()
        self.status.config(text=info)

    def destroy_buts(self,buts):
        for b in buts:
            b.destroy()

    def home_page(self,params):
        e = Engine(params)
        e = e.run(self.scenario.index(params))
        url = self.urls[params['enviroment']]
        e.get(url)
        return e

    def start(self):
       self.scenario = self.make_scenario()
       for item in self.scenario:
           self.urls = settings.urls[item['domain']]
           self.engine = self.home_page(item)

    def search(self):
        self.scenario = self.make_scenario()
        for item in self.scenario:
            print item
            self.urls = settings.urls[item['domain']]
            #self.engine = self.home_page(item)
            if item['domain'] == 'International':
               self.engine = self.home_page(item)
               s = search.SearchIntl(item,self.engine)
            elif item['domain'] == 'Domestic':
               self.engine = self.home_page(item)
               s = search.SearchDomestic(item,self.engine)
            elif item['domain'] == 'CCF':
               self.engine = self.home_page(item)
               s = search.SearchCCF(item,self.engine)

    def make_scenario(self):
       if self.template.get():
           path = main_config["scenarios_dir"] + "/" + self.json.get()
           with open (path) as js:
                scenario = json.load(js)
                #scenario = row['scenario']
                return scenario
       else:
            browsers = []
            if self.firefox.get() == 1: browsers.append({"browser":"firefox"})
            if self.chrome.get() == 1: browsers.append({"browser":"chrome"})
            if self.ie.get() == 1: browsers.append({"browser":"ie"})
            if browsers:
               for browser in browsers:
                   browser['domain'] = self.domain.get()
                   browser['enviroment'] = self.env.get()
                   browser['account'] = self.account.get()
                   if self.rand_dates.get():
                      browser['days_left'] = 'random'
                      browser['trip_duration'] = 'random'
                   else:
                      browser['days_left'] = self.days_left.get()
                      browser['trip_duration'] = self.trip_duration.get()
                   if self.rand_age.get():
                      browser['driver_age'] = 'random'
                   else:
                      browser['driver_age'] = self.age.get()
                   browser['currency'] = self.currency.get()
                   if self.air_code.get():
                      browser['pick_location'] = self.air_field.get()
                   else:
                      browser['pick_location'] = self.pickup.get()
                   if self.one_way.get():
                      browser['drop_location'] = self.dropoff.get()
                   else:
                      browser['drop_location'] = ''
                   browser['location_list'] = self.list.get()
                   if self.solution.get() == 'sipp':
                      browser['solution'] = self.sipp.get()
                   else:
                      browser['solution'] =  self.solution.get()
                   if self.rand_payment.get():
                      browser['payment'] = random.choice(self.money)
                   else:
                      browser['payment'] = self.payment.get()
                   browser['insurance'] = self.insurance.get()
                   if self.rand_email.get():
                      browser['email'] = random.choice(self.emails)
                   else:
                      browser['email'] = self.email.get()
                   print browser
               return browsers
            else:
               print "No browser selected"

    def select_browsers(self):
        for a in self.br_buttons:
            a.select()

    def deselect_browsers(self):
        for a in self.br_buttons:
            a.deselect()

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

    def buttons_widget(self,frame = 'root'):
        if frame == 'root':
           FuncFrame = Frame(self.root,relief = RAISED)
           FuncFrame.grid(row = 4,column = 0,columnspan=2)
        elif frame == 'options':
           FuncFrame = Frame(self.OptionsFrame,relief = RAISED)
           FuncFrame.pack(side = 'top',pady=5)
        Button(FuncFrame, text="start",command=self.start).pack(side = 'left')
        Button(FuncFrame, text="search",command=self.search).pack(side = 'left')
        Button(FuncFrame, text="details",state=DISABLED).pack(side = 'left')
        Button(FuncFrame, text="book",state=DISABLED).pack(side = 'left')
        Button(FuncFrame, text="full",state=DISABLED).pack(side = 'left')

    def domains_widget(self):
        self.domain = StringVar()
        DomainFrame = Frame(self.root)
        DomainFrame.grid(row = 1,column = 0,columnspan=2,padx=5,pady=5)
        Label(DomainFrame,text="Domain:").pack(side='left')
        domains = main_config['domains']
        self.domain.set(main_config['default_domain'])
        self.urls = settings.urls[self.domain.get()]
        self.list.set(settings.default_lists[self.domain.get()])
        self.show_domains(DomainFrame,domains,self.domain)
        #self.change_domain()

    def show_domains(self,frame,args,var):
        for d in args:
            r = Radiobutton(frame,text=d,variable = var,
            value=d,indicatoron = 0,
            command=self.change_domain).pack(side='left')

    def change_domain(self):
        if self.domain.get() == 'CCF':
           try:
               self.engine.delete_all_cookies()
           except:
               print "new session"
        self.list.set(settings.default_lists[self.domain.get()])
        OptionMenu(self.ListFrame,self.list,*self.lists,
                  command=self.change_list).grid(row = 2,column = 1,sticky='W')
        OptionMenu(self.ListFrame, self.pickup,*self.get_lists()).grid(row = 2,column = 2,sticky='W')
        #self.change_list(None)
        self.enviroment_widget()

    def enviroment_widget(self):
        envs = sorted(self.urls.keys())
        self.env = StringVar()
        self.env.set('qa')
        self.EnvFrame = Frame(self.root)
        self.EnvFrame.grid(row = 2,column = 0,columnspan=2,padx=5,pady=5)
        Label(self.EnvFrame,text="Enviroment:").pack(side='left')
        self.env_menu = apply(OptionMenu, (self.EnvFrame, self.env) + tuple(envs))
        self.env_menu.pack(side='left')
        self.all_env = BooleanVar()
        self.all_env.set(False)
        Checkbutton(self.EnvFrame,text = 'Check all servers in tabs',
        variable=self.all_env,state=DISABLED).pack(side='left')

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
        self.all_scenario = BooleanVar()
        self.all_scenario.set(False)
        Checkbutton(ScenarioFrame,text = 'All',
        variable=self.all_scenario).pack(side='left')

    def hide_options(self):
        if self.template.get():
           self.OptionsFrame.grid_forget()
        else:
             self.OptionsFrame.grid(row = 5,column = 0,columnspan=2,padx = 40)

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
        self.buttons_widget("options")

    def disable_widget(self,widget):
        try:
            widget.config(state='DISABLED')
        except TclError:
            for child in widget:
                self.disable_widget(child)


    def account_widget(self):
        LoginFrame = Frame(self.OptionsFrame)
        LoginFrame.pack(side = 'top')
        Label(LoginFrame,text='Account:',state=DISABLED).grid(row = 0,column = 0)
        self.account = StringVar()
        self.account.set('no_account')
        logins = settings.accounts.keys()
        om = apply(OptionMenu, (LoginFrame, self.account) + tuple(logins))
        om.grid(row = 0,column = 1,padx=3,pady=3)

        #self.disable_widget(LoginFrame)

    def days_widget(self):
        DayFrame = Frame(self.OptionsFrame,relief = RAISED,borderwidth=1)
        DayFrame.pack(side = 'top',padx=5,pady=5)
        Label(DayFrame,text = "Days left:").grid(row=0,column=0)
        self.days_left = Spinbox(DayFrame, from_=1, to=60,width=3)
        self.days_left.grid(row = 0,column=1)
        Label(DayFrame,text = "Trip duration:").grid(row=0,column=2)
        self.trip_duration = Spinbox(DayFrame, from_=1, to=351,width=3)
        self.trip_duration.grid(row = 0,column=3)
        self.rand_dates = BooleanVar()
        self.rand_dates.set(True)
        Checkbutton(DayFrame,text = 'Random dates',
        variable=self.rand_dates).grid(row = 0,column = 4,sticky='W')





    def age_widget(self):
        AgeFrame = Frame(self.OptionsFrame,relief = RAISED,borderwidth=1)
        AgeFrame.pack(side = 'top',padx=5,pady=5)
        Label(AgeFrame,text = "Driver age:").grid(row=0,column=0)
        self.age = IntVar()
        self.age.set(25)
        Entry(AgeFrame, textvariable = self.age,width =3).grid(row=0,column=1)
        self.rand_age = BooleanVar()
        self.rand_age.set(True)
        Checkbutton(AgeFrame,text = 'Random age',
        variable=self.rand_age).grid(row = 0,column = 2,sticky='W')

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
        Radiobutton(CurFrame,text='other',variable = self.currency,value='other').grid(row = 1,column = 0,sticky='W')
        Radiobutton(CurFrame,text='random',variable = self.currency,value='random').grid(row = 1,column = 1,sticky='W')
        Radiobutton(CurFrame,text='code',variable = self.currency,value='code').grid(row = 1,column = 2,sticky='W')
        om = apply(OptionMenu, (CurFrame, self.currency) + tuple(money))
        om.grid(row = 1,column = 2)

    def search_widget(self):
        SearchFrame = LabelFrame(self.OptionsFrame,text = "Search",
                      labelanchor='n',relief = RAISED,borderwidth=1)
        SearchFrame.pack(side = 'top',padx=5,pady=5)
        self.air_code = BooleanVar()
        self.air_field = StringVar()
        self.air_field.set('LHR')
        self.pickup = StringVar()
        ChoiceFrame = Frame(SearchFrame)
        ChoiceFrame.grid(row=0)
        airCodeFrame = LabelFrame(ChoiceFrame,text='air code:')
        airCodeFrame.grid(row=0,column=0,sticky='W',padx=10,pady=5)
        Checkbutton(airCodeFrame,variable=self.air_code).pack(side="left")
        Entry(airCodeFrame,width=4,textvariable = self.air_field).pack(side="left",padx=2)
        CityFrame = LabelFrame(ChoiceFrame,text='City:')
        CityFrame.grid(row=0,column=1,padx=10,pady=5,sticky='W')
        with open('lists/United kingdom/city.txt') as c:
             lines = c.readlines()
             cities = [line.strip() for line in lines]
        om = apply(OptionMenu, (CityFrame, self.pickup) + tuple(cities))
        om.pack(side="left",padx=1)
        self.ListFrame = LabelFrame(SearchFrame,text='Lists:')
        self.ListFrame.grid(row=1,padx=1,pady=1,sticky='W')
        self.one_way = BooleanVar()
        self.one_way.set(False)
        Checkbutton(self.ListFrame,text = 'One way',variable=self.one_way,
                    command=self.show_dropoff).grid(row = 1,column = 0,sticky='W')
        Label(self.ListFrame,text='Location list').grid(row = 1,column = 1,sticky='W')
        Label(self.ListFrame,text='Location/Search type').grid(row = 1,column = 2,sticky='W')
        Label(self.ListFrame,text='Pickup location:').grid(row = 2,column = 0,sticky='W')
        self.pickup.set('random')
        self.lists = os.listdir(main_config['lists_dir'])
        OptionMenu(self.ListFrame,self.list,*self.lists,
                  command=self.change_list).grid(row = 2,column = 1,sticky='W')
        OptionMenu(self.ListFrame, self.pickup,*self.get_lists()).grid(row = 2,column = 2,sticky='W')
        self.dropoff = StringVar()
        self.dropoff.set('')
        self.all_lists = BooleanVar()
        self.all_lists.set(False)
        Checkbutton(self.ListFrame,text = 'All lists',
                   variable=self.all_lists).grid(row = 4,column = 1,sticky='W')
        self.whole_list = BooleanVar()
        self.whole_list.set(False)
        Checkbutton(self.ListFrame,text = 'Whole list',
                   variable=self.whole_list).grid(row = 4,column = 2,sticky='W')

    def change_list(self,event):
        OptionMenu(self.ListFrame, self.pickup,*self.get_lists()).grid(row = 2,column = 2,sticky='W')
        print self.one_way.get()
        if self.one_way.get():
           self.dropFile = OptionMenu(self.ListFrame, self.dropoff,*self.get_lists())
           self.dropFile.grid(row = 3,column = 2,sticky='W')

    def get_lists(self):
        #self.list.set(settings.default_lists[self.domain.get()])
        _files = os.listdir(main_config['lists_dir']+"/"+self.list.get())
        _files = [f.replace('.txt','') for f in _files]
        _files.append('random')
        return _files

    def show_dropoff(self):
        if self.one_way.get():
            self.dropLabel = Label(self.ListFrame,text='Dropoff location:')
            self.dropLabel.grid(row = 3,column = 0,sticky='W')
            self.dropoff.set('random')
            self.dropFile = OptionMenu(self.ListFrame, self.dropoff,*self.get_lists())
            self.dropFile.grid(row = 3,column = 2,sticky='W')
        else:
            self.dropLabel.grid_forget()
            self.dropFile.grid_forget()

    def results_widget(self):
        ResFrame = LabelFrame(self.OptionsFrame,relief = RAISED,
        borderwidth=1,text = "Solution",labelanchor='n')
        ResFrame.pack(side = 'top',expand=1,padx=10,pady=5)
        self.solution = StringVar()
        self.sipp = StringVar()
        self.solution.set('first')
        self.sipp.set('EBMN')
        Label(ResFrame,text = "Result:").grid(row=1,column=0)
        Radiobutton(ResFrame,text='first',variable = self.solution,
                        value='first').grid(row = 1,column = 1,sticky='W')
        Radiobutton(ResFrame,text='last',variable = self.solution,
                        value='last').grid(row = 1,column = 2,sticky='W')
        Radiobutton(ResFrame,text='all',variable = self.solution,
                        value='all').grid(row = 1,column = 3,sticky='W')
        Label(ResFrame,text = "Type:").grid(row=2,column=0)
        Radiobutton(ResFrame,text='opaque',variable = self.solution,
                    value='opaque').grid(row = 2,column = 1,sticky='W')
        Radiobutton(ResFrame,text='retail',variable = self.solution,
                    value='retail').grid(row = 2,column = 2,sticky='W')
        Radiobutton(ResFrame,text='random',variable = self.solution,
                    value='random').grid(row = 2,column = 3,sticky='W')
        Label(ResFrame,text = "SIPP:").grid(row = 3,column = 0,sticky='W')
        SippFrame = Frame(ResFrame)
        SippFrame.grid(row=3,column=1,sticky='W')
        Radiobutton(SippFrame,variable = self.solution,value='sipp').pack(side='left')
        Entry(SippFrame,width=6,textvariable = self.sipp).pack(side='left')
        self.policy = BooleanVar()
        self.policy.set(False)
        Checkbutton(ResFrame,text = 'policy',
        variable=self.policy).grid(row=4,column=1,sticky='W')
        self.amenities = BooleanVar()
        self.amenities.set(False)
        Checkbutton(ResFrame,text = 'amenities',
        variable=self.amenities).grid(row=4,column=2,sticky='W')

    def payment_widget(self):
        PayFrame = Frame(self.OptionsFrame,relief = RAISED,borderwidth=1)
        PayFrame.pack(side = 'top',pady=5)
        self.payment = StringVar()
        self.money = settings.cards[self.domain.get()].keys()
        self.payment.set(self.money[0])
        Label(PayFrame,text = "Pyment method:").grid(row=0,column=0,sticky='W')
        om = apply(OptionMenu, (PayFrame, self.payment) + tuple(self.money))
        om.grid(row=0,column=1,sticky='W')
        self.rand_payment = BooleanVar()
        self.rand_payment.set(True)
        Checkbutton(PayFrame,text="Random",
                    variable=self.rand_payment).grid(row=0,column=2,sticky='W')
        self.insurance = BooleanVar()
        self.insurance.set(False)
        Checkbutton(PayFrame,text="Insurance",
                    variable=self.insurance).grid(row=1,column=1,sticky='W')
        self.all_cards = BooleanVar()
        self.all_cards.set(False)
        Checkbutton(PayFrame,text = 'Book with all',
                    variable=self.all_cards).grid(row=1,column=2,sticky='W')

    def email_widget(self):
        self.email = StringVar()
        self.email.set('gmail')
        EmailFrame = Frame(self.OptionsFrame,relief = RAISED,borderwidth=1)
        EmailFrame.pack(side = 'top')
        self.email = StringVar()
        self.emails = sorted(settings.conf_email.keys())
        self.email.set('gmail')
        Label(EmailFrame,text = "Email type:").grid(row=0,column=0,sticky='W')
        om = apply(OptionMenu, (EmailFrame, self.email) + tuple(self.emails))
        om.grid(row=0,column=1,sticky='W')
        self.rand_email = BooleanVar()
        self.rand_email.set(True)
        Checkbutton(EmailFrame,text="Random",
                    variable=self.rand_email).grid(row=0,column=2,sticky='W')

    def status_bar(self):
        statusFrame = Frame(self.root,relief = GROOVE,borderwidth = 1)
        statusFrame.grid(row = 7,column = 0,columnspan=2,padx=5,pady=5)
        self.status = Label(statusFrame,text="Please choose options to start crawling",
                     bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(expand=1, fill=X)



app = CarSpider()
app.root.mainloop()