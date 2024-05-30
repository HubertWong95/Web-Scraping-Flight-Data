from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

import pandas as pd

import smtplib
from email.message import EmailMessage

import schedule

departure_flight_inputs = {'Departure': " ORD", "Arrival": " LAX", "Date":"Jun 20, 2021"}
return_flight_inputs = {'Departure': " LAX", "Arrival": " ORD", "Date":"Aug 28, 2021"}

def find_cheapest_flights(flight_info):
    PATH = r'/Users/hubert/My Programming Project/Web Scraping Flight Data/chromedriver'
    driver = webdriver.Chrome(executable_path=PATH)

    leaving_from = flight_info['Departure']
    going_to = flight_info['Arrival']
    trip_date = flight_info['Date']

    #Go to Expedia
    driver.get("https://www.expedia.ca/")

    #Click on Flights
    flight_xpath = '//*[@id="multi-product-search-form-1"]/div/div/div[1]/ul/li[2]/a'
    flight_element = WebDriverWait(driver,5).until(
        EC.presence_of_element_located((By.XPATH, flight_xpath))
    )
    flight_element.click()
    time.sleep(0.2)