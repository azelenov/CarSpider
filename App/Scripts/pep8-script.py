#!h:\CarSpider\dev\App\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pep8==1.4.6','console_scripts','pep8'
__requires__ = 'pep8==1.4.6'
import sys
from pkg_resources import load_entry_point

sys.exit(
   load_entry_point('pep8==1.4.6', 'console_scripts', 'pep8')()
)
