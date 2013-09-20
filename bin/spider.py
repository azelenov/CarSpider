#! ../App/python.exe

from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
from settings import main_config
from selenium.webdriver.common.keys import Keys
from my_account import MyAccount
from engine import Engine
from email import Email
from c3 import C3
import settings
import search
import results
import book
import json
import random
import re


class CarSpider:
    '''Portable selenium script for semi-automation'''
    version = "2.35"

    def __init__(self):
        '''GUI app initialization'''
        self.root = Tk()
        self.list = StringVar()
        self.payment = StringVar()
        #print os.listdir(os.curdir)
        #os.chdir('bin')
        self.root.wm_title("HW CarSpider "+self.version)
        self.root.wm_iconbitmap('static/spider.ico')
        self.root.geometry("+200+200")
        #self.root.geometry("250x150+300+300")
        self.create_widgets()
        self.menu_bar()

    def menu_bar(self):
        '''Configure and show bar on the top'''
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu = Menu(menubar, tearoff=0)
        #filemenu.add_command(label="Open")
        filemenu.add_command(label="Save scenario..",
                             command=self.save_scenario)
        filemenu.add_separator()
        #filemenu.add_command(label="Exit")
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Manual",
                             command=lambda: self.open_service("help"))
        helpmenu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)
        #self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.set_hot_keys()

    def set_hot_keys(self):
        '''Configuring app hot keys using settings'''
        keys = settings.hot_keys
        self.root.bind_all(keys["home_page"], lambda e: self.start())
        self.root.bind_all(keys["search"], lambda e: self.search())
        self.root.bind_all(keys["show_details"], lambda e: self.show_details())
        self.root.bind_all(keys["update_results"],
                           lambda e: self.udate_results())
        self.root.bind_all(keys["fill_details"], lambda e: self.fill())
        self.root.bind_all(keys["book"], lambda e: self.book())
        self.root.bind_all(keys["my_account"], lambda e: self.my_account())
        self.root.bind_all(keys["email"], lambda e: self.open_service("email"))
        self.root.bind_all(keys["c3"], lambda e: self.open_service("c3"))
        self.root.bind_all(keys["refresh_utils"],
                           lambda e: self.open_service("refresh_utils"))
        self.root.bind_all(keys["clear_cookies"],
                           lambda e: self.clear_cookies())

    def about(self):
        about_msg = "CarSpider "+self.version \
                    + "\nAuthor: Alexandr Zelenov\nSupport:\
                         v-ozelenov@hotwire.com"
        tkMessageBox.showinfo("About", about_msg)

    def save_scenario(self):
        '''Saving browser paramets to json file'''
        scenario = str(json.dumps(self.make_scenario(), sort_keys=True,
                       indent=4, separators=(',', ': '))
                       )
        fileName = tkFileDialog.asksaveasfilename(parent=self.root,
                                                  filetypes=
                                                  [('JSON format', '*.json')],
                                                  title=
                                                  "Save the scenario as...",
                                                  initialdir="scenarios/",
                                                  defaultextension='.json')
        with open(fileName, 'w') as f:
            f.write(scenario)

    def create_widgets(self):
        '''Show all the options widgets on main frame'''
        self.browsers_widget()
        self.browser_features()
        self.domains_widget()
        self.enviroment_widget()
        self.scenario_widget()
        self.buttons_widget()
        self.options_widget()
        self.status_bar()

    def log(self, var):
        '''Logging to status bar'''
        info = var
        self.status.config(text=info)

    def warning(self, title, msg):
        '''Showing warning message'''
        tkMessageBox.showwarning(title, msg)

    def destroy_buts(self, buts):
        for b in buts:
            b.destroy()

    def run(self, params):
        '''Initialize the browser instance'''
        arrange = self.arrange.get()
        timeout = int(self.timeout_field.get())
        e = Engine(params, arrange, timeout)
        e = e.run(self.scenario['browsers'].index(params))
        return e

    def make_url(self, item):
        self.urls = settings.urls[item['domain']]
        vt = settings.version_tests[item['domain']]
        base_url = self.urls[item['enviroment']]
        if vt:
            url = base_url + "?vt." + vt[0]
            if vt:
                url = url + "&vt." + "&vt.".join(vt[1:])
        else:
            url = base_url
        return url

    def home_page(self, eng, item):
        '''Going to specified enviroment/domain home page'''
        url = self.make_url(item)
        eng.get(url)
        self.log("Home Page loaded")

    def start(self):
        self.clear_cookies()

    def search(self):
        '''Creating scenario and run search for all selected browsers'''
        self.scenario = self.make_scenario()
        repeat = int(self.scenario["repeat"])
        for item in self.scenario["browsers"]:
            engine = self.run(item)
            if item['domain'] == 'International':
                s = search.SearchIntl(item, engine)
            elif item['domain'] == 'Domestic':
                s = search.SearchDomestic(item, engine)
            elif item['domain'] == 'CCF':
                s = search.SearchCCF(item, engine)
            self.log("Search request sent")

    def udate_results(self):
        '''refresihng results from results page Fare Finder'''
        self.scenario = self.make_scenario()
        attemps = int(self.scenario["retry"])
        for item in self.scenario["browsers"]:
            engine = self.run(item)
            if item['domain'] == 'International':
                r = results.ResultsIntl(item, engine, attemps)
            elif item['domain'] == 'Domestic':
                r = results.ResultsDomestic(item, engine, attemps)
            elif item['domain'] == 'CCF':
                r = results.ResultsCCF(item, engine, attemps)
            if not r.update():
                self.search()
            self.log("Results updated")

    def fill(self, confirm=False):
        '''Filling the billing page without clicking on confirm button'''
        self.scenario = self.make_scenario()
        for item in self.scenario["browsers"]:
            engine = self.run(item)
            if item['domain'] == 'International':
                b = book.BookIntl(item, engine)
            elif item['domain'] == 'Domestic':
                b = book.BookDomestic(item, engine)
            elif item['domain'] == 'CCF':
                b = book.BookCCF(item, engine)
            self.log("The billing form is filled")
            if confirm:
                b.submit()

    def book(self):
        '''Full booking action. Use for booking all soecified parameters'''
        self.log("Booking...")
        self.scenario = self.make_scenario()
        repeat = int(self.scenario["repeat"])
        attemps = int(self.scenario["retry"])
        for i in range(repeat + 1):
            print "Run #:", i
            prod_flag = False
            for item in self.scenario["browsers"]:
                if item['enviroment'] == 'prod':
                    self.warning("Production booking",
                                 "LIVE booking must be performed"
                                 + " ONLY manually!")
                    prod_flag = True
            if not prod_flag:
                self.search()
                self.log("Search request was sent")
                self.details()
                self.log("Car details opened")
                self.fill(True)
                self.log("Car booked")
                #self.clear_cookies()

    def details(self):
        '''Go to details/billing page of specified solution
         without filling the form'''
        attemps = int(self.scenario["retry"])
        for item in self.scenario["browsers"]:
            engine = self.run(item)
            if item['domain'] == 'International':
                r = results.ResultsIntl(item, engine, attemps)
            elif item['domain'] == 'Domestic':
                r = results.ResultsDomestic(item, engine, attemps)
            elif item['domain'] == 'CCF':
                r = results.ResultsCCF(item, engine, attemps)
            r.get_details()
        self.log("Car details opened")

    def show_details(self):
        self.scenario = self.make_scenario()
        repeat = int(self.scenario["repeat"])
        attemps = int(self.scenario["retry"])
        for i in range(repeat+1):
            print "Run #:", i
            self.search()
            self.details()
            #self.clear_cookies()

    def my_account(self):
        '''Go to hotwire my account of specified user'''
        self.clear_cookies()
        for item in self.scenario["browsers"]:
            m = MyAccount(item, self.engine)
            m.go_to_account()
        self.log("My account opening.")

    def open_service(self, service):
        '''Open hotwire internal applications such as c3
         and external services such as email'''
        self.scenario = self.make_scenario()
        item = self.scenario["browsers"][0]
        item["browser"] = "firefox"
        engine = self.run(item)
        url = self.make_url(item)
        if service == 'refresh_utils':
            ru_url = self.extract_domain(url)+'/test/refreshUtil.jsp'
            print ru_url
            engine.get(ru_url)
            self.log("Refresh Utils loaded")
        elif service == 'c3':
            c3_url = self.extract_domain(url)+'/ccc/login.jsp'
            engine.get(c3_url)
            c = C3(item, engine)
            self.log("C3 loaded")
        elif service == 'email':
            e = Email(item, engine)
            self.log("Email inbox loaded")
        elif service == 'help':
            help_url = settings.help_urls['manual']
            engine.get(help_url)

    def extract_domain(self, url):
        '''Extracting domain from enviroment home page'''
        parts = url.split('/')
        return "http://" + parts[2]

    def update_scenario(self, scenario):
        '''Update json scenario according to
        current Domain and Enviroment options'''
        for browser in scenario['browsers']:
            num = scenario['browsers'].index(browser)
            if not self.domain_ovewrite.get():
                scenario['browsers'][num]['domain'] = self.domain.get()
            if not self.env_ovewrite.get():
                scenario['browsers'][num]['enviroment'] = self.env.get()
        return scenario

    def make_scenario(self):
        if self.template.get():
            '''Reading scenario from json file from scenarious folder'''
            path = main_config["scenarios_dir"] + "/" + self.json.get()
            with open(path) as js:
                scenario = json.load(js)
                scenario = self.update_scenario(scenario)
            return scenario
        else:
            '''Creating scenario from GUI application'''
            scenario = {}
            scenario["repeat"] = self.repeat.get()
            scenario["retry"] = self.retry.get()
            browsers = []
            if self.firefox.get() == 1:
                browsers.append({"browser": "firefox"})
            if self.chrome.get() == 1:
                browsers.append({"browser": "chrome"})
            if self.ie.get() == 1:
                browsers.append({"browser": "ie"})
            if self.phantomjs.get() == 1:
                browsers.append({"browser": "phantomjs"})
            if browsers:
                for browser in browsers:
                    browser['domain'] = self.domain.get()
                    browser['enviroment'] = self.env.get()
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
                        browser['solution'] = self.solution.get()
                    if self.rand_payment.get():
                        browser['payment'] = 'random'
                    else:
                        browser['payment'] = self.payment.get()
                    if browser['payment'] in ['HotDollars', 'SavedCard',
                                              'SavedBML']:
                        self.logged.set(True)
                    browser['insurance'] = self.insurance.get()
                    if self.rand_email.get():
                        browser['email'] = random.choice(self.emails)
                    else:
                        browser['email'] = self.email.get()
                    browser['logged'] = self.logged.get()
                scenario['browsers'] = browsers
                return scenario
            else:
                self.warning("No browsers",
                             "No browser selected!\nPlease select a browser.")

    def select_browsers(self):
        '''Selecting all browsers'''
        for a in self.br_buttons:
            a.select()

    def deselect_browsers(self):
        '''Unchecking all browser in browsers frame'''
        for a in self.br_buttons:
            a.deselect()

    def browsers_widget(self):
        '''Configuring and showing browsers frame'''
        self.firefox = IntVar()
        self.chrome = IntVar()
        self.ie = IntVar()
        self.phantomjs = IntVar()
        br = main_config['default_browser']
        if br == 'chrome':
            self.chrome.set(1)
        elif br == 'firefox':
            self.firefox.set(1)
        elif br == 'ie':
            self.ie.set(1)
        elif br == 'phantomjs':
            self.phantomjs.set(1)
        browsers = {'Firefox': self.firefox, 'Chrome': self.chrome,
                    'IE': self.ie}
        self.BrowsersFrame = LabelFrame(self.root,
                                        relief=RAISED,
                                        borderwidth=1,
                                        text="Browsers",
                                        padx=7,
                                        pady=7)
        self.BrowsersFrame.grid(row=0, column=0, columnspan=2)
        self.br_buttons = self.create_checks(self.BrowsersFrame, browsers)
        all_br = Button(self.BrowsersFrame, text='All',
                        command=self.select_browsers)
        all_br.pack(side="left")
        none_br = Button(self.BrowsersFrame, text='None',
                         command=self.deselect_browsers)
        none_br.pack(side="left")

    def browser_features(self):
        '''Additional features on browsers frame'''
        self.arrange = BooleanVar()
        self.arrange.set(True)
        BrowFeaturesFrame = Frame(self.root, relief=GROOVE,
                                  borderwidth=1, padx=2, pady=2)
        BrowFeaturesFrame.grid(row=1, column=0, columnspan=2)
        MoveCheck = Checkbutton(BrowFeaturesFrame, text='Arrange',
                                variable=self.arrange)
        MoveCheck.pack(side="left")
        del_cookies = Button(BrowFeaturesFrame,
                             text='Clear Cookies',
                             command=self.clear_cookies)
        del_cookies.pack(side="left")

    def clear_cookies(self):
        '''Delete all cookies in all selected browsers'''
        self.scenario = self.make_scenario()
        for item in self.scenario["browsers"]:
            self.engine = self.run(item)
            self.engine.delete_all_cookies()
            self.home_page(self.engine, item)
        self.log("Cookies deleted")

    def create_checks(self, frame, args):
        cbuts = []
        for t, v in args.items():
            cb = Checkbutton(frame, text=t, variable=v)
            cb.pack(side="left")
            cbuts.append(cb)
        return cbuts

    def buttons_widget(self, frame='root'):
        '''Configuring main functional buttons'''
        if frame == 'root':
            FuncFrame = Frame(self.root, relief=RAISED)
            FuncFrame.grid(row=5, column=0, columnspan=2, padx=3, pady=3)
        elif frame == 'options':
            FuncFrame = Frame(self.OptionsFrame, relief=RAISED)
            FuncFrame.pack(side='top', pady=5, padx=5)
        Button(FuncFrame, text="Home", command=self.start).pack(side='left')
        Button(FuncFrame, text="Search", command=self.search).pack(side='left')
        Button(FuncFrame, text="Retry",
               command=self.udate_results).pack(side='left')
        Button(FuncFrame, text="Details",
               command=self.show_details).pack(side='left')
        Button(FuncFrame, text="Fill", command=self.fill).pack(side='left')
        Button(FuncFrame, text="Book", command=self.book).pack(side='left')
        Button(FuncFrame, text="Account",
               command=self.my_account).pack(side='left')
        Button(FuncFrame, text="Email",
               command=lambda: self.open_service("email")).pack(side='left')
        Button(FuncFrame, text="Utils",
               command=
               lambda: self.open_service("refresh_utils")).pack(side='left')
        Button(FuncFrame, text="C3",
               command=lambda: self.open_service("c3")).pack(side='left')
##        Button(FuncFrame, text="Test",
##               command=
##               lambda: self.make_url({'enviroment': 'qa','domain':'CCF'})
##               ).pack(side='left')

    def domains_widget(self):
        '''Configuring domain frame'''
        self.domain = StringVar()
        DomainFrame = Frame(self.root)
        DomainFrame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        Label(DomainFrame, text="Domain").pack(side='left')
        domains = main_config['domains']
        self.domain.set(main_config['default_domain'])
        self.urls = settings.urls[self.domain.get()]
        self.list.set(settings.default_lists[self.domain.get()])
        self.show_domains(DomainFrame, domains, self.domain)

    def show_domains(self, frame, args, var):
        '''Creating domains buttons'''
        for d in args:
            r = Radiobutton(frame, text=d, variable=var,
                            value=d, indicatoron=0,
                            command=self.change_domain).pack(side='left')

    def change_domain(self):
        '''Action on changing domain.'''
        try:
            self.engine.delete_all_cookies()
        except:
            self.log("New session")
        self.list.set(settings.default_lists[self.domain.get()])
        results = settings.solutions[self.domain.get()]['result']

        OptionMenu(self.ListFrame, self.list, *self.lists,
                   command=self.change_list).grid(row=2, column=1, sticky='W')
        om = OptionMenu(self.ListFrame, self.pickup, *self.get_lists())
        om.grid(row=2, column=2, sticky='W')
        self.payment.set('Visa')
        self.money = settings.payment_methods[self.domain.get()].keys()
        om = apply(OptionMenu, (self.PayFrame, self.payment)
                   + tuple(self.money))
        om.grid(row=0, column=1, sticky='W')
        results = settings.solutions[self.domain.get()]['result']
        self.res_menu.forget()
        self.solution.set("first")
        self.res_menu = OptionMenu(self.r_frame, self.solution, *results)
        self.res_menu.pack(side='left')
        self.start()

    def update_options(self, menu, List):
        menu.option_clear()
        for item in List:
            menu.option_add(List.index(item), item)
        menu.update()

    def enviroment_widget(self):
        envs = sorted(self.urls.keys())
        self.env = StringVar()
        self.env.set('qa')
        self.EnvFrame = Frame(self.root)
        self.EnvFrame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        Label(self.EnvFrame, text="Enviroment").pack(side='left')
        self.env_menu = OptionMenu(self.EnvFrame, self.env, *envs)
        self.env_menu.pack(side='left')
        Label(self.EnvFrame, text="Timeout").pack(side='left')
        self.timeout_field = Spinbox(self.EnvFrame, from_=10, to=60, width=3)
        self.timeout_field.pack(side='left')
        Label(self.EnvFrame, text="seconds").pack(side='left')
##        Checkbutton(self.EnvFrame,text = 'Check all servers in tabs',
##        variable=self.all_env,state=DISABLED).pack(side='left')

    def scenario_widget(self):
        '''Read json scenarious if activated'''
        self.ScenarioFrame = Frame(self.root, relief=RIDGE, borderwidth=2)
        self.ScenarioFrame.grid(row=4, column=0, columnspan=2, padx=40, pady=5)
        self.template = BooleanVar()
        self.template.set(False)
        Checkbutton(self.ScenarioFrame, text='Scenario template',
                    variable=self.template,
                    command=self.hide_options).grid(row=0, column=0)
        self.refresh_scenarious()

    def refresh_scenarious(self):
        self.json = StringVar()
        temps = os.listdir(main_config['scenarios_dir'])
        self.json.set(temps[0])
        self.scenarious_om = apply(OptionMenu, (self.ScenarioFrame, self.json)
                                   + tuple(temps))
        self.scenarious_om.grid(row=0, column=1)

    def hide_options(self):
        '''Hide scenario options if scenario template mode is activated'''
        if self.template.get():
            self.OptionsFrame.grid_forget()
            self.BrowsersFrame.grid_forget()
            '''Refresh scenarious button'''
            self.refresh_scenario_btn = Button(self.ScenarioFrame,
                                               text='Refresh',
                                               command=self.refresh_scenarious)
            self.refresh_scenario_btn.grid(row=1, column=0)
            self.refresh_scenarious()
            self.domain_ovewrite = BooleanVar()
            self.env_ovewrite = BooleanVar()
            self.domain_ovewrite.set(False)
            self.env_ovewrite.set(False)
            self.domain_ow_cb = Checkbutton(self.ScenarioFrame,
                                            text='Domain overwrite',
                                            variable=self.domain_ovewrite)
            self.domain_ow_cb.grid(row=1, column=1, sticky='W')
            self.env_ow_cb = Checkbutton(self.ScenarioFrame,
                                         text='Enviroment overwrite',
                                         variable=self.env_ovewrite)
            self.env_ow_cb.grid(row=2, column=1, sticky='W')
        else:
            self.refresh_scenario_btn.grid_forget()
            self.domain_ow_cb.grid_forget()
            self.env_ow_cb.grid_forget()
            self.scenarious_om.grid_forget()
            self.browsers_widget()
            self.options_widget()

    def options_widget(self):
        self.OptionsFrame = LabelFrame(self.root,
                                       text="Options",
                                       labelanchor='n',
                                       relief=RIDGE,
                                       borderwidth=4)
        self.OptionsFrame.grid(row=6, column=0, columnspan=2, padx=40)
        self.days_widget()
        self.age_widget()
        self.currency_widget()
        self.search_widget()
        self.payment_widget()
        self.email_widget()
        self.buttons_widget("options")

    def days_widget(self):
        DayFrame = Frame(self.OptionsFrame, relief=RAISED, borderwidth=1)
        DayFrame.pack(side='top', padx=3, pady=3)
        Label(DayFrame, text="Days left").grid(row=0, column=0)
        self.days_left = Spinbox(DayFrame, from_=1, to=60, width=3)
        self.days_left.grid(row=0, column=1)
        Label(DayFrame, text="Trip duration").grid(row=0, column=2)
        self.trip_duration = Spinbox(DayFrame, from_=1, to=351, width=3)
        self.trip_duration.grid(row=0, column=3)
        self.rand_dates = BooleanVar()
        self.rand_dates.set(True)
        Checkbutton(DayFrame, text='Random dates',
                    variable=self.rand_dates).grid(row=0, column=4, sticky='W')

    def age_widget(self):
        AgeFrame = Frame(self.OptionsFrame, relief=RAISED, borderwidth=1)
        AgeFrame.pack(side='top', padx=3, pady=3)
        Label(AgeFrame, text="Driver age").grid(row=0, column=0)
        self.age = IntVar()
        self.age.set(25)
        Entry(AgeFrame, textvariable=self.age, width=3).grid(row=0, column=1)
        self.rand_age = BooleanVar()
        self.rand_age.set(True)
        Checkbutton(AgeFrame, text='Random age',
                    variable=self.rand_age).grid(row=0, column=2, sticky='W')

    def currency_widget(self):
        CurFrame = LabelFrame(self.OptionsFrame, relief=RAISED,
                              borderwidth=1, text="Currency", labelanchor='n')
        CurFrame.pack(side='top', padx=1, pady=1)
        #Label(CurFrame,text = "Currency:").grid(row=0,column=0)
        money = main_config['currency']
        self.currency = StringVar()
        self.currency.set(main_config['default_currency'])
        Radiobutton(CurFrame, text='USD',
                    variable=self.currency,
                    value='USD').grid(row=0, column=0, sticky='W')
        Radiobutton(CurFrame, text='EUR',
                    variable=self.currency,
                    value='EUR').grid(row=0, column=1, sticky='W')
        Radiobutton(CurFrame, text='GBP',
                    variable=self.currency,
                    value='GBP').grid(row=0, column=2, sticky='W')
        Radiobutton(CurFrame, text='random',
                    variable=self.currency,
                    value='random').grid(row=0, column=3, sticky='W')
        om = apply(OptionMenu, (CurFrame, self.currency) + tuple(money))
        om.grid(row=0, column=5)

    def search_widget(self):
        self.SearchFrame = LabelFrame(self.OptionsFrame,
                                      text="Search",
                                      labelanchor='n',
                                      relief=RAISED,
                                      borderwidth=1)
        self.SearchFrame.pack(side='top', padx=1, pady=1)
        self.air_code = BooleanVar()
        self.air_field = StringVar()
        self.air_field.set('LHR')
        self.pickup = StringVar()
        ChoiceFrame = Frame(self.SearchFrame)
        ChoiceFrame.grid(row=0)
        '''Search by pickup airport code'''
        airCodeFrame = LabelFrame(ChoiceFrame, text='Air Code')
        airCodeFrame.grid(row=0, column=0, sticky='W', padx=2, pady=2)
        Checkbutton(airCodeFrame, variable=self.air_code,
                    command=self.hide_location_lists).pack(side="left")
        Entry(airCodeFrame, width=4,
              textvariable=self.air_field).pack(side="left", padx=2)
        self.search_results_frame()

    def search_results_frame(self):
        '''Search results option frame'''
        ResFrame = LabelFrame(self.SearchFrame, relief=RAISED,
                              borderwidth=1,
                              text="Solution",
                              labelanchor='n')
        ResFrame.grid(row=0, column=1, padx=2, pady=2)
        self.solution = StringVar()
        self.solution.set('first')
        self.r_frame = LabelFrame(ResFrame, text="Result")
        self.r_frame.grid(row=0, column=0, padx=1, pady=1)
        retry_frame = LabelFrame(ResFrame, text="Retry")
        retry_frame.grid(row=0, column=2, padx=1, pady=1)
        repeat_frame = LabelFrame(ResFrame, text="Repeat")
        repeat_frame.grid(row=0, column=3, padx=1, pady=1)
        results = settings.solutions[self.domain.get()]['result']
        self.res_menu = OptionMenu(self.r_frame, self.solution, *results)
        self.res_menu.pack(side='left')
        #checks = settings.solutions[self.domain.get()]['check']
        #self.check = StringVar()
        #OptionMenu(c_frame, self.check,*checks).pack(side='left')
        attempts = StringVar()
        attempts.set(settings.main_config['retry'])
        self.retry = Spinbox(retry_frame, from_=0,
                             to=10, width=3, textvariable=attempts)
        self.retry.pack(side='left')
        self.repeat = Spinbox(repeat_frame, from_=0, to=100, width=3)
        self.repeat.pack(side='left')
        self.location_lists_widget()

    def location_lists_widget(self):
        '''Search using location lists'''
        self.ListFrame = LabelFrame(self.SearchFrame, text='Lists')
        self.ListFrame.grid(row=1, columnspan=2, padx=1, pady=1, sticky='W')
        self.one_way = BooleanVar()
        self.one_way.set(False)
        Checkbutton(self.ListFrame, text='One way',
                    variable=self.one_way,
                    command=self.show_dropoff
                    ).grid(row=1, column=0, sticky='W')
        Label(self.ListFrame, text='Location list').grid(row=1,
                                                         column=1,
                                                         sticky='W'
                                                         )
        Label(self.ListFrame, text='Search type').grid(row=1,
                                                       column=2,
                                                       sticky='W')
        Label(self.ListFrame, text='Pickup location').grid(row=2,
                                                           column=0,
                                                           sticky='W')
        self.pickup.set('random')
        self.lists = os.listdir(main_config['lists_dir'])
        OptionMenu(self.ListFrame, self.list, *self.lists,
                   command=self.change_list).grid(row=2,
                                                  column=1,
                                                  sticky='W')
        OptionMenu(self.ListFrame, self.pickup,
                   *self.get_lists()).grid(row=2, column=2, sticky='W')
        self.dropoff = StringVar()
        self.dropoff.set('')
##        self.all_lists = BooleanVar()
##        self.all_lists.set(False)
##        Checkbutton(self.ListFrame, text='All lists',
##                    variable=self.all_lists, state=DISABLED
##                    ).grid(row=4, column=1, sticky='W')
##        self.whole_list = BooleanVar()
##        self.whole_list.set(False)
##        Checkbutton(self.ListFrame, text='Whole list',
##                    variable=self.whole_list, state=DISABLED
##                    ).grid(row=4, column=2, sticky='W')

    def hide_location_lists(self):
        '''Hide location lists if air code search is activated'''
        if self.air_code.get():
            self.one_way.set(False)
            self.ListFrame.grid_forget()
        else:
            self.location_lists_widget()

    def change_list(self, event):
        OptionMenu(self.ListFrame, self.pickup,
                   *self.get_lists()).grid(row=2, column=2, sticky='W')
        if self.one_way.get():
            self.dropFile = OptionMenu(self.ListFrame,
                                       self.dropoff, *self.get_lists())
            self.dropFile.grid(row=3, column=2, sticky='W')

    def get_lists(self):
        #self.list.set(settings.default_lists[self.domain.get()])
        _files = os.listdir(main_config['lists_dir']+"/"+self.list.get())
        _files = [f.replace('.txt', '') for f in _files]
        _files.append('random')
        return _files

    def show_dropoff(self):
        if self.one_way.get():
            self.dropLabel = Label(self.ListFrame, text='Dropoff location')
            self.dropLabel.grid(row=3, column=0, sticky='W')
            self.dropoff.set('random')
            self.dropFile = OptionMenu(self.ListFrame,
                                       self.dropoff,
                                       *self.get_lists())
            self.dropFile.grid(row=3, column=2, sticky='W')
        else:
            self.dropLabel.grid_forget()
            self.dropFile.grid_forget()

    def results_widget(self):
        ResFrame = LabelFrame(self.OptionsFrame,
                              relief=RAISED,
                              borderwidth=1,
                              text="Solution",
                              labelanchor='n')
        ResFrame.pack(side='top', expand=1, padx=3, pady=3)
        self.solution = StringVar()
        self.sipp = StringVar()
        self.solution.set('first')
        self.sipp.set('EBMN')
        r_frame = LabelFrame(ResFrame, text="Result")
        r_frame.grid(row=0, column=0)
        c_frame = LabelFrame(ResFrame, text="Check")
        c_frame.grid(row=0, column=1)
        results = settings.solutions[self.domain.get()]['result']
        self.res_menu = OptionMenu(r_frame, self.solution, *results)
        self.res_menu.pack(side='left')
        checks = settings.solutions[self.domain.get()]['check']
        self.check = StringVar()
        OptionMenu(c_frame, self.check, *checks).pack(side='left')

        self.sipp = BooleanVar()
        self.sipp_field = StringVar()
        #SippFrame = LabelFrame(ResFrame,text='SIPP:')
        #SippFrame.grid(row=0,column=3,sticky='W')
        #Checkbutton(SippFrame,variable=self.sipp,
        #state=DISABLED).pack(side="left")
        #Entry(SippFrame,width=4,
        #textvariable = self.sipp_field).pack(side="left",padx=2)

    def payment_widget(self):
        self.PayFrame = Frame(self.OptionsFrame, relief=RAISED, borderwidth=1)
        self.PayFrame.pack(side='top', pady=5)
        self.money = settings.payment_methods[self.domain.get()].keys()
        self.payment.set('Visa')
        Label(self.PayFrame, text="Payment method").grid(row=0,
                                                         column=0,
                                                         sticky='W')
        om = apply(OptionMenu, (self.PayFrame, self.payment)
                   + tuple(self.money))
        om.grid(row=0, column=1, sticky='W')
        self.rand_payment = BooleanVar()
        self.rand_payment.set(False)
        Checkbutton(self.PayFrame, text="Random",
                    variable=self.rand_payment
                    ).grid(row=0, column=2, sticky='W')
        self.insurance = BooleanVar()
        self.insurance.set(False)
        Checkbutton(self.PayFrame, text="Insurance",
                    variable=self.insurance).grid(row=1, column=1, sticky='W')
##        self.all_cards = BooleanVar()
##        self.all_cards.set(False)
##        Checkbutton(self.PayFrame, text='Book with all',
##                    variable=self.all_cards,
##                    state=DISABLED
##                    ).grid(row=1, column=2, sticky='W')

    def email_widget(self):
        self.email = StringVar()
        self.email.set('gmail')
        EmailFrame = Frame(self.OptionsFrame, relief=RAISED, borderwidth=1)
        EmailFrame.pack(side='top')
        self.email = StringVar()
        self.emails = sorted(settings.conf_email.keys())
        self.email.set('gmail')
        Label(EmailFrame, text="Email type").grid(row=0, column=0)
        om = apply(OptionMenu, (EmailFrame, self.email) + tuple(self.emails))
        om.grid(row=0, column=1, sticky='W')
        self.rand_email = BooleanVar()
        self.rand_email.set(False)
        self.logged = BooleanVar()
        self.logged.set(False)
        Checkbutton(EmailFrame, text="Random",
                    variable=self.rand_email).grid(row=1, column=0, sticky='W')
        Checkbutton(EmailFrame, text="Logged",
                    variable=self.logged).grid(row=1, column=1, sticky='W')

    def status_bar(self):
        statusFrame = Frame(self.root, relief=GROOVE, borderwidth=1)
        statusFrame.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
        self.status = Label(statusFrame,
                            text="Please choose options to start crawling",
                            bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(expand=1, fill=X)

app = CarSpider()
app.root.mainloop()
