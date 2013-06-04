#! ../App/python.exe

from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
from settings import main_config
from engine import Engine
import settings
import search
import results
import book
import json
import random

class CarSpider:
    def __init__(self):
        self.root = Tk()
        self.list = StringVar()
        self.payment = StringVar()
        #print os.listdir(os.curdir)
        os.chdir('hw')
        self.root.wm_title("HW CarSpider 2.0 Beta")
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
        helpmenu.add_command(label="About",command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)
        #self.root.protocol("WM_DELETE_WINDOW", self.quit)

    def about(self):
        about_msg = "CarSpider 2.0\nAuthor:Alexandr Zelenov\nSupport:v-ozelenov@hotwire.com"
        tkMessageBox.showinfo("About",about_msg)

    def save_scenario(self):
        scenario = '['
        #scenario_order = ['browser','domain','enviroment','account',
                         # 'days_left','trip_duration','driver_age',
                          #'currency','pick_location','drop_location',
                         # 'solution','payment','email','insurance']
        #scenario = self.make_scenario()



        scenario = str(self.make_scenario()).replace(',',',\n').replace('},','},\n').replace("'",'"').replace("[{","\n[{\n").replace("}],","\n}],\n")

        fileName = tkFileDialog.asksaveasfilename(parent=self.root,
                   filetypes=[('JSON format','*.json')] ,
                   title="Save the scenario as...",
                   initialdir="scenarios/",
                   defaultextension = '.json')
        with open(fileName,'w') as f:
             f.write(scenario)

    def create_widgets(self):
        self.browsers_widget()
        self.browser_features()
        self.domains_widget()
        self.enviroment_widget()
        self.scenario_widget()
        self.buttons_widget()
        self.options_widget()
        self.status_bar()

    def log(self,var):
        info = var
        self.status.config(text=info)

    def warning(self,title,msg):
        tkMessageBox.showwarning(title,msg)

    def destroy_buts(self,buts):
        for b in buts:
            b.destroy()

    def run(self,params):
        e = Engine(params)
        e = e.run(self.scenario['browsers'].index(params))
        return e

    def home_page(self,eng,item):
        self.urls = settings.urls[item['domain']]
        url = self.urls[item['enviroment']]
        eng.get(url)
        print "Geting home page"

    def start(self):
       self.log("Starting browsers...")
       self.scenario = self.make_scenario()
       print self.scenario
       for item in self.scenario['browsers']:
           print item
           self.urls = settings.urls[item['domain']]
           engine = self.run(item)
           self.home_page(engine,item)

    def search(self):
        self.scenario = self.make_scenario()
        repeat = int(self.scenario["repeat"])
        for item in self.scenario["browsers"]:
            engine = self.run(item)
            if item['domain'] == 'International':
               s = search.SearchIntl(item,engine)
            elif item['domain'] == 'Domestic':
               s = search.SearchDomestic(item,engine)
            elif item['domain'] == 'CCF':
               s = search.SearchCCF(item,engine)

    def udate_results(self):
        self.log("Updating results")
        self.scenario = self.make_scenario()
        attemps = int(self.scenario["retry"])
        for item in self.scenario["browsers"]:
            engine = self.run(item)
            if item['domain'] == 'International':
               r = results.ResultsIntl(item,engine,attemps)
            elif item['domain'] == 'Domestic':
               r = results.ResultsDomestic(item,engine,attemps)
            elif item['domain'] == 'CCF':
               r = results.ResultsCCF(item,engine,attemps)
            r.update()

    def fill(self,confirm=False):
        self.log("Filling booking info...")
        self.scenario = self.make_scenario()
        for item in self.scenario["browsers"]:
            engine = self.run(item)
            if item['domain'] == 'International':
               b = book.BookIntl(item,engine)
            elif item['domain'] == 'Domestic':
               b = book.BookDomestic(item,engine)
            elif item['domain'] == 'CCF':
               b = book.BookCCF(item,engine)
            if confirm: b.submit()

    def book(self):
        self.scenario = self.make_scenario()
        repeat = int(self.scenario["repeat"])
        attemps = int(self.scenario["retry"])
        for i in range(repeat+1):
            print "Run #:",i
            prod_flag = False
            for item in self.scenario["browsers"]:
                if item['enviroment'] == 'prod':
                   self.warning("Production booking","LIVE booking must be performed ONLY manually!")
                   prod_flag =  True
            if not prod_flag:
               self.search()
               self.details()
               self.fill(True)

    def details(self):
        attemps = int(self.scenario["retry"])
        for item in self.scenario["browsers"]:
            engine = self.run(item)
            if item['domain'] == 'International':
               r = results.ResultsIntl(item,engine,attemps)
            elif item['domain'] == 'Domestic':
               r = results.ResultsDomestic(item,engine,attemps)
            elif item['domain'] == 'CCF':
               r = results.ResultsCCF(item,engine,attemps)
            r.get_details()

    def make_scenario(self):
       if self.template.get():
           path = main_config["scenarios_dir"] + "/" + self.json.get()
           with open (path) as js:
                scenario = json.load(js)
                return scenario
       else:
            scenario = {}
            scenario["repeat"] = self.repeat.get()
            scenario["retry"] = self.retry.get()
            browsers = []
            if self.firefox.get() == 1: browsers.append({"browser":"firefox"})
            if self.chrome.get() == 1: browsers.append({"browser":"chrome"})
            if self.ie.get() == 1: browsers.append({"browser":"ie"})
            if browsers:
               for browser in browsers:
                   browser['domain'] = self.domain.get()
                   browser['enviroment'] = self.env.get()
                   #browser['account'] = self.account.get()
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
                      browser['payment'] = 'random'
                   else:
                      browser['payment'] = self.payment.get()
                   browser['insurance'] = self.insurance.get()
                   if self.rand_email.get():
                      browser['email'] = random.choice(self.emails)
                   else:
                      browser['email'] = self.email.get()
                   browser['arrange'] = self.arrange.get()
               scenario['browsers'] = browsers
               return scenario
            else:
               self.warning("No browsers","No browser selected!\nPlease select a browser!")

    def select_browsers(self):
        for a in self.br_buttons:
            a.select()

    def deselect_browsers(self):
        for a in self.br_buttons:
            a.deselect()

    def browsers_widget(self):
        self.firefox = IntVar()
        self.chrome = IntVar()
        self.ie = IntVar()
        br = main_config['default_browser']
        if br == 'chrome':
           self.chrome.set(1)
        elif br == 'firefox':
           self.firefox.set(1)
        elif br == 'ie':
           self.ie.set(1)
        browsers = {'Firefox':self.firefox,'Chrome':self.chrome,'IE':self.ie}
        BrowTypeFrame = LabelFrame(self.root,relief = RAISED,
        borderwidth=1,text = "Browsers:",padx=7,pady=7)
        BrowTypeFrame.grid(row = 0,column = 0,columnspan=2)
        self.br_buttons = self.create_checks(BrowTypeFrame,browsers)
        all_br = Button(BrowTypeFrame,text='All',command=self.select_browsers)
        all_br.pack(side="left")
        none_br = Button(BrowTypeFrame,text='None',command=self.deselect_browsers)
        none_br.pack(side="left")

    def browser_features(self):
        self.arrange = BooleanVar()
        self.arrange.set(True)
        BrowFeaturesFrame = Frame(self.root,relief = GROOVE,
        borderwidth=1,padx=2,pady=2)
        BrowFeaturesFrame.grid(row = 1,column = 0,columnspan=2)
        MoveCheck = Checkbutton(BrowFeaturesFrame,text='Arrange',variable=self.arrange)
        MoveCheck.pack(side="left")
        del_cookies = Button(BrowFeaturesFrame,text='Clear Cookies',command=self.clear_cookies)
        del_cookies.pack(side="left")

    def clear_cookies(self):
        self.scenario = self.make_scenario()
        for item in self.scenario["browsers"]:
            engine = self.run(item)
            engine.delete_all_cookies()
            self.home_page(engine,item)
        self.log("Cookies deleted")

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
           FuncFrame.grid(row = 5,column = 0,columnspan=2)
        elif frame == 'options':
           FuncFrame = Frame(self.OptionsFrame,relief = RAISED)
           FuncFrame.pack(side = 'top',pady=5)
        Button(FuncFrame, text="Home",command=self.start).pack(side = 'left')
        Button(FuncFrame, text="Search",command=self.search).pack(side = 'left')
        Button(FuncFrame, text="Update",command=self.udate_results).pack(side = 'left')
        Button(FuncFrame, text="Fill",command=self.fill).pack(side = 'left')
        Button(FuncFrame, text="Book",command=self.book).pack(side = 'left')
        Button(FuncFrame, text="Full",state=DISABLED).pack(side = 'left')

    def domains_widget(self):
        self.domain = StringVar()
        DomainFrame = Frame(self.root)
        DomainFrame.grid(row = 2,column = 0,columnspan=2,padx=5,pady=5)
        Label(DomainFrame,text="Domain:").pack(side='left')
        domains = main_config['domains']
        self.domain.set(main_config['default_domain'])
        self.urls = settings.urls[self.domain.get()]
        self.list.set(settings.default_lists[self.domain.get()])
        self.show_domains(DomainFrame,domains,self.domain)

    def show_domains(self,frame,args,var):
        for d in args:
            r = Radiobutton(frame,text=d,variable = var,
            value=d,indicatoron = 0,
            command=self.change_domain).pack(side='left')

    def change_domain(self):
        try:
            self.engine.delete_all_cookies()
        except:
            self.log("New session")
        self.list.set(settings.default_lists[self.domain.get()])
        results = settings.solutions[self.domain.get()]['result']

        OptionMenu(self.ListFrame,self.list,*self.lists,
                  command=self.change_list).grid(row = 2,column = 1,sticky='W')
        OptionMenu(self.ListFrame, self.pickup,*self.get_lists()).grid(row = 2,column = 2,sticky='W')
        self.money = settings.cards[self.domain.get()].keys()
        om = apply(OptionMenu, (self.PayFrame, self.payment) + tuple(self.money))
        om.grid(row=0,column=1,sticky='W')
        results = settings.solutions[self.domain.get()]['result']
        self.res_menu.forget()
        self.res_menu = OptionMenu(self.r_frame, self.solution,*results)
        self.res_menu.pack(side='left')
        self.start()

    def update_options(self,menu,List):
        menu.option_clear()
        for  item in List:
             menu.option_add(List.index(item),item)
        menu.update()

    def enviroment_widget(self):
        envs = sorted(self.urls.keys())
        self.env = StringVar()
        self.env.set('qa')
        self.EnvFrame = Frame(self.root)
        self.EnvFrame.grid(row = 3,column = 0,columnspan=2,padx=5,pady=5)
        Label(self.EnvFrame,text="Enviroment:").pack(side='left')
        self.env_menu = OptionMenu(self.EnvFrame, self.env, *envs)
        self.env_menu.pack(side='left')
        self.all_env = BooleanVar()
        self.all_env.set(False)
        Checkbutton(self.EnvFrame,text = 'Check all servers in tabs',
        variable=self.all_env,state=DISABLED).pack(side='left')

    def scenario_widget(self):
        ScenarioFrame = Frame(self.root,relief = RIDGE,borderwidth=2)
        ScenarioFrame.grid(row = 4,column = 0,columnspan=2,padx = 40,pady = 5)
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
        variable=self.all_scenario,state=DISABLED).pack(side='left')

    def hide_options(self):
        if self.template.get():
           self.OptionsFrame.grid_forget()
        else:
             self.OptionsFrame.grid(row = 5,column = 0,columnspan=2,padx = 40)

    def options_widget(self):
        self.OptionsFrame = LabelFrame(self.root,
        text="Options",labelanchor='n',relief = RIDGE,borderwidth=4)
        self.OptionsFrame.grid(row = 6,column = 0,columnspan=2,padx = 40)
        #self.account_widget()
        self.days_widget()
        self.age_widget()
        self.currency_widget()
        self.search_widget()
        #self.results_widget()
        self.payment_widget()
        self.email_widget()
        self.buttons_widget("options")

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
        DayFrame.pack(side = 'top',padx=3,pady=3)
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
        AgeFrame.pack(side = 'top',padx=3,pady=3)
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
        CurFrame.pack(side = 'top',padx=1,pady=1)
        #Label(CurFrame,text = "Currency:").grid(row=0,column=0)
        money = main_config['currency']
        self.currency = StringVar()
        self.currency.set('GBP')
        Radiobutton(CurFrame,text='USD',variable = self.currency,value='USD').grid(row = 0,column = 0,sticky='W')
        Radiobutton(CurFrame,text='EUR',variable = self.currency,value='EUR').grid(row = 0,column = 1,sticky='W')
        Radiobutton(CurFrame,text='GBP',variable = self.currency,value='GBP').grid(row = 0,column = 2,sticky='W')
        Radiobutton(CurFrame,text='random',variable = self.currency,value='random').grid(row = 0,column = 3,sticky='W')
        #Radiobutton(CurFrame,text='code',variable = self.currency,value='code').grid(row = 1,column = 2,sticky='W')
        om = apply(OptionMenu, (CurFrame, self.currency) + tuple(money))
        om.grid(row = 0,column = 5)

    def search_widget(self):
        self.SearchFrame = LabelFrame(self.OptionsFrame,text = "Search",
                      labelanchor='n',relief = RAISED,borderwidth=1)
        self.SearchFrame.pack(side = 'top',padx=1,pady=1)
        self.air_code = BooleanVar()
        self.air_field = StringVar()
        self.air_field.set('LHR')
        self.pickup = StringVar()
        ChoiceFrame = Frame(self.SearchFrame)
        ChoiceFrame.grid(row=0)
        airCodeFrame = LabelFrame(ChoiceFrame,text='air code:')
        airCodeFrame.grid(row=0,column=0,sticky='W',padx=1,pady=1)
        Checkbutton(airCodeFrame,variable=self.air_code).pack(side="left")
        Entry(airCodeFrame,width=4,textvariable = self.air_field).pack(side="left",padx=2)

        ResFrame = LabelFrame(self.SearchFrame,relief = RAISED,
        borderwidth=1,text = "Solution",labelanchor='n')
        ResFrame.grid(row=0,column=1,padx=1,pady=1)
        self.solution = StringVar()
        self.solution.set('first')
        self.r_frame = LabelFrame(ResFrame,text = "Result:")
        self.r_frame.grid(row=0,column=0)
        c_frame = LabelFrame(ResFrame,text = "Check:")
        c_frame.grid(row=0,column=1)
        retry_frame = LabelFrame(ResFrame,text = "Retry:")
        retry_frame.grid(row=0,column=2)
        repeat_frame = LabelFrame(ResFrame,text = "Repeat:")
        repeat_frame.grid(row=0,column=3)

        results = settings.solutions[self.domain.get()]['result']
        self.res_menu = OptionMenu(self.r_frame, self.solution,*results)
        self.res_menu.pack(side='left')
        checks = settings.solutions[self.domain.get()]['check']
        self.check = StringVar()
        OptionMenu(c_frame, self.check,*checks).pack(side='left')
        attempts= StringVar()
        attempts.set("3")
        self.retry = Spinbox(retry_frame, from_=0, to=10,width=3,textvariable=attempts)
        self.retry.pack(side='left')
        self.repeat = Spinbox(repeat_frame, from_=0, to=100,width=3)
        self.repeat.pack(side='left')

        self.ListFrame = LabelFrame(self.SearchFrame,text='Lists:')
        self.ListFrame.grid(row=1,columnspan=2,padx=1,pady=1,sticky='W')
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
                   variable=self.all_lists,state=DISABLED).grid(row = 4,column = 1,sticky='W')
        self.whole_list = BooleanVar()
        self.whole_list.set(False)
        Checkbutton(self.ListFrame,text = 'Whole list',
                   variable=self.whole_list,state=DISABLED).grid(row = 4,column = 2,sticky='W')

    def change_list(self,event):
        OptionMenu(self.ListFrame, self.pickup,*self.get_lists()).grid(row = 2,column = 2,sticky='W')
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
        ResFrame.pack(side = 'top',expand=1,padx=3,pady=3)
        self.solution = StringVar()
        self.sipp = StringVar()
        self.solution.set('first')
        self.sipp.set('EBMN')
        r_frame = LabelFrame(ResFrame,text = "Result:")
        r_frame.grid(row=0,column=0)
        c_frame = LabelFrame(ResFrame,text = "Check:")
        c_frame.grid(row=0,column=1)
        results = settings.solutions[self.domain.get()]['result']
        self.res_menu = OptionMenu(r_frame, self.solution,*results)
        self.res_menu.pack(side='left')
        checks = settings.solutions[self.domain.get()]['check']
        self.check = StringVar()
        OptionMenu(c_frame, self.check,*checks).pack(side='left')

        self.sipp = BooleanVar()
        self.sipp_field = StringVar()
        #SippFrame = LabelFrame(ResFrame,text='SIPP:')
        #SippFrame.grid(row=0,column=3,sticky='W')
        #Checkbutton(SippFrame,variable=self.sipp,state=DISABLED).pack(side="left")
        #Entry(SippFrame,width=4,textvariable = self.sipp_field).pack(side="left",padx=2)

    def payment_widget(self):
        self.PayFrame = Frame(self.OptionsFrame,relief = RAISED,borderwidth=1)
        self.PayFrame.pack(side = 'top',pady=5)
        self.money = settings.cards[self.domain.get()].keys()
        self.payment.set('Visa')
        Label(self.PayFrame,text = "Pyment method:").grid(row=0,column=0,sticky='W')
        om = apply(OptionMenu, (self.PayFrame, self.payment) + tuple(self.money))
        om.grid(row=0,column=1,sticky='W')
        self.rand_payment = BooleanVar()
        self.rand_payment.set(False)
        Checkbutton(self.PayFrame,text="Random",
                    variable=self.rand_payment).grid(row=0,column=2,sticky='W')
        self.insurance = BooleanVar()
        self.insurance.set(False)
        Checkbutton(self.PayFrame,text="Insurance",
                    variable=self.insurance).grid(row=1,column=1,sticky='W')
        self.all_cards = BooleanVar()
        self.all_cards.set(False)
        Checkbutton(self.PayFrame,text = 'Book with all',
                    variable=self.all_cards,state=DISABLED).grid(row=1,column=2,sticky='W')

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
        self.rand_email.set(False)
        Checkbutton(EmailFrame,text="Random",
                    variable=self.rand_email).grid(row=0,column=2,sticky='W')

    def status_bar(self):
        statusFrame = Frame(self.root,relief = GROOVE,borderwidth = 1)
        statusFrame.grid(row = 8,column = 0,columnspan=2,padx=5,pady=5)
        self.status = Label(statusFrame,text="Please choose options to start crawling",
                     bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(expand=1, fill=X)

app = CarSpider()
app.root.mainloop()