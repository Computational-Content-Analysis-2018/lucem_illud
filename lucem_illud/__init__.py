from .data_dirs  import *
from .downloaders import *
from .loaders import *


import requests
import re
import pkg_resources

_setupURL = 'https://raw.githubusercontent.com/Computational-Content-Analysis-2018/lucem_illud/master/setup.py'

def _checkCurrentVersion():
    r = requests.get(_setupURL, timeout=0.5)
    serverVersion = re.search(r'versionString = \'(.+)\'', r.text).group(1)
    localVersion = pkg_resources.get_distribution('lucem_illud').version
    if serverVersion != serverVersion:
        print('lucem_illud is out of date, please update')
        print('pip install -U git+git://github.com/Computational-Content-Analysis-2018/lucem_illud.git')

try:
    checkCurrentVersion()
except:
    pass
