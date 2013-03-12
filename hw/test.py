from selenium import webdriver as wb

from locators import intl_loc

f = wb.Firefox()
#e = wb.Ie()
#c = wb.Chrome()

url = 'http://www.hotwire.com/'
print url
f.set_window_size(960,1080)
f.set_window_position(0,0)
#c.set_window_size(960,1080)
#c.set_window_position(960,0)
#e.set_window_size(960,1080)
#e.set_window_position(1920,0)

#e.get(url)
f.get(url)
#c.get(url)
print "I'm in"