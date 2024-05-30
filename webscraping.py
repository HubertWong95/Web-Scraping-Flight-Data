from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

def kayakScrape(origin, destination, startdate, enddate):

    url = f"https://www.ca.kayak.com/flights/{origin}-{destination}/{startdate}/{enddate}/2adults/children-11?sort=bestflight_a&fs=stops=0"

    PATH = r'/Users/hubert/My Programming Project/Web Scraping Flight Data/chromedriver'
    service = Service(executable_path=PATH)
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'vmXl.vmXl-mod-variant-large')))

    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Get departure time
    deptimes = []

    for deptime in soup.select('.vmXl.vmXl-mod-variant-large'):
        deptimes.append(deptime.select('span')[0].getText())

    deptimes = np.asarray(deptimes)
    deptimes = deptimes.reshape(int(len(deptimes)/2),2)

    # Get arrival time
    arrtimes = []
    for arrtime in soup.select('.vmXl.vmXl-mod-variant-large'):
        arrtimes.append(arrtime.select('span')[2].getText())

    arrtimes = np.asarray(arrtimes)
    arrtimes = arrtimes.reshape(int(len(arrtimes)/2),2)

    # Get price
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
                    "currency": "CAD"})
    
    df.to_excel("flight_data.xlsx", index=False)



def skyscannerScrape(origin, destination, startdate, enddate):

    url = f"https://www.skyscanner.ca/transport/flights/{origin}/{destination}/{startdate}/{enddate}/?adults=2&adultsv2=2&cabinclass=economy&children=1&childrenv2=4&inboundaltsenabled=false&infants=0&outboundaltsenabled=false&preferdirects=true&ref=home&rtn=1"

    driver = webdriver.Chrome()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    # ******
    # Get departure time
    # ******
    deptimes = []

    for deptime in soup.select('.BpkText_bpk-text__ODgwN.BpkText_bpk-text--heading-5__MjJhN'):
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
                    "currency": "CAD"})
    
    df.to_excel("flight_data.xlsx", index=False)