#!C:\development\script\gui\CarSpider\App\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'rsa==3.1.1','console_scripts','pyrsa-verify'
__requires__ = 'rsa==3.1.1'
import sys
from pkg_resources import load_entry_point

sys.exit(
   load_entry_point('rsa==3.1.1', 'console_scripts', 'pyrsa-verify')()
)
