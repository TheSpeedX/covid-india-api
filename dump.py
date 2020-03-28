from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get("https://www.covid19india.org/")
time.sleep(2)
html = driver.page_source
driver.quit()
f=open('map.dump','w')
f.write(html)
f.close()