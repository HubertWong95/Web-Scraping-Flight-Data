import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

origin = "HKG"
destination = "YVR"
startdate = "2024-08-18"
enddate = "2024-09-01"

url = f"https://www.ca.kayak.com/flights/{origin}-{destination}/{startdate}/{enddate}/2adults?fs=fdDir=true;stops=~0&sort=bestflight_a"

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')

# ******
# Get departure time
# ******
deptimes = []

for deptime in soup.select('.vmXl.vmXl-mod-variant-large'):
    deptimes.append(deptime.select('span')[0].getText())

deptimes = np.asarray(deptimes)
deptimes = deptimes.reshape(int(len(deptimes)/2),2)

# ******
# Get arrival time
# ******
arrtimes = []
for arrtime in soup.select('.vmXl.vmXl-mod-variant-large'):
    arrtimes.append(arrtime.select('span')[2].getText())

arrtimes = np.asarray(arrtimes)
arrtimes = arrtimes.reshape(int(len(arrtimes)/2),2)

# ******
# Get price
# ******
prices = []

for price in soup.select('.f8F1-price-text'):
    prices.append(price.getText()[3:])

df = pd.DataFrame({"origin": origin,
                   "destination": destination,
                   "startdate": startdate,
                   "enddate": enddate,
                   "deptime_sd": deptimes[:,0],
                   "arrtime_sd": arrtimes[:,0],
                   "deptime_ed": deptimes[:,1],
                   "arrtime_ed": arrtimes[:,1],
                   "price": prices,
                   "currency": "USD"})

print(deptimes)
print(len(deptimes))
print('\n')
print(arrtimes)
print(len(arrtimes))
print('\n')
print(prices)
print(len(prices))
print('\n')
print(df)