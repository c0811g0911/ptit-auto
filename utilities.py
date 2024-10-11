import json
import time
from types import SimpleNamespace

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller




def load_driver():        
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--domain')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')    
    options.add_argument('--incognito')
    options.add_argument('--disable-gpu')    
    options.add_argument("--start-maximized")
    options.add_argument("--window-position=1367,0")
    options.add_argument('--disable-extensions')
    
    chromedriver_autoinstaller.install()    
    driver = webdriver.Chrome(options=options)
    return driver

