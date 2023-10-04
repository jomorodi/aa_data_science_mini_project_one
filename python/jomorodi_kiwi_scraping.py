#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 05:57:05 2023

@author: jeffery
"""

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd


class scraper ():

    def __init__(self):
        self.url = dict()
        self.driver = uc.Chrome()  # todo change to headless
        # uc.Chrome(headless=True,use_subprocess=False)
        self.kiwi_data = {"departure_time": [], "arrival_time": [], "duration": [], "price": [
        ], "number_of_stops": [], "airline": [], "website": [], "extra_data": dict()}

        self.data = [self.kiwi_data]
        self.size = 50  # size of the data to scrape
        self.counter = 0

    def _process_airline_name_from_image(self, locator):
        """
        imput is a web elemnt 
        process the the airline name from the thier image alt adress

        """
        image_tag_list = locator.find_elements(By.TAG_NAME, "img")
        result = []
        count = 1
        for img in image_tag_list:
            result.append(f'{count}. {img.get_attribute("alt")}')
            count += 1

        self.kiwi_data["airline"].append(" ".join(result))

    def _process_times(self, locator):
        """
        imput is a web elemnt 
        process the depature time , arrival ,time and depature
        by finding the 3 time tag
        """
        time_list = locator.find_elements(By.TAG_NAME, "time")
        self.kiwi_data["departure_time"].append(time_list[0].text)
        self.kiwi_data["duration"].append(time_list[1].text)
        self.kiwi_data["arrival_time"].append(time_list[2].text)

    def _process_price(self, locator):
        """
        imput is a web elemnt 
        process the the the price by finding the span that contains it

        """
        span_list = locator.find_elements(By.TAG_NAME, "span")
        for elem in span_list:
            if elem.get_attribute("class").startswith(" length") :
                self.kiwi_data["price"].append(elem.text)

    def _process_stops(self, locator):
        """
        input is a web elemnt 
        process the the the number of stops by findinf the div that contains it

        """
        div_list = locator.find_elements(By.TAG_NAME, "div")
        for elem in div_list:
            if elem.get_attribute("class") == "BadgePrimitive__StyledBadgeContent-sc-1aa3b9c-2 jVwdZH" and ( "stop" in elem.text or "Direct" in elem.text):
                self.kiwi_data["number_of_stops"].append(elem.text)

    def _process_the_top(self):
        """
        input is a web elemnt 
        process the the the  first of the two important div that contains vital stat like best price , best duration
        cheapeast price , cheapeast duraion etc
        """
        top = self.driver.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/div[4]/div/div/div/div/div/div[2]/div/div/div[1]')
        self.kiwi_data["extra_data"]["best_price"] = top.find_element(
            By.XPATH, '//*[@id="react-view"]/div[2]/div[4]/div/div/div/div/div/div[2]/div/div/div[1]/div[2]/div/button[1]/div/span').text
        self.kiwi_data["extra_data"]["best_duration"] = top.find_element(
            By.XPATH, '//*[@id="react-view"]/div[2]/div[4]/div/div/div/div/div/div[2]/div/div/div[1]/div[2]/div/button[1]/div/time').text
        self.kiwi_data["extra_data"]["cheapest_price"] = top.find_element(
            By.XPATH, '//*[@id="react-view"]/div[2]/div[4]/div/div/div/div/div/div[2]/div/div/div[1]/div[2]/div/button[2]/div[2]/span').text
        self.kiwi_data["extra_data"]["cheapest_duration"] = top.find_element(
            By.XPATH, '//*[@id="react-view"]/div[2]/div[4]/div/div/div/div/div/div[2]/div/div/div[1]/div[2]/div/button[2]/div[2]/time').text
        self.kiwi_data["extra_data"]["fastest_price"] = top.find_element(
            By.XPATH, '//*[@id="react-view"]/div[2]/div[4]/div/div/div/div/div/div[2]/div/div/div[1]/div[2]/div/button[3]/div[2]/span').text
        self.kiwi_data["extra_data"]["fastest_duration"] = top.find_element(
            By.XPATH, '//*[@id="react-view"]/div[2]/div[4]/div/div/div/div/div/div[2]/div/div/div[1]/div[2]/div/button[3]/div[2]/time').text

    def _process_the_rest(self):
        """
        input is a web elemnt 
        process the  the other div 
        self.counter ensures that 50 items are process
        count just loops through the divs
        """
        bottom = self.driver.find_element(
            By.XPATH, '/html/body/div[2]/div[2]/div[4]/div/div/div/div/div/div[2]/div/div/div[2]')
        count = 1
        while True:
            if self.counter == self.size:
                break
            div = bottom.find_element(
                By.XPATH, f'/html/body/div[2]/div[2]/div[4]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[{ count }]')
            # avoid div with advert
            if div.get_attribute('class').lower() != "mb-md":
                count += 1
                continue
            self._process_airline_name_from_image(div)
            self._process_times(div)
            self._process_price(div)
            self._process_stops(div)
            count += 1
            self.counter += 1

    def kiwi_scaper(self):
        self.url["kiwi"] = "https://www.kiwi.com/en/"

        self.driver.get(
            "https://www.kiwi.com/en/search/results/helsinki-helsinki-finland/frankfurt-frankfurt-germany/2023-10-22/no-return")
        time.sleep(5)
        try:

            # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//html/body/div[2]/div[2]/section/div/div/div/section/div[2]/button[3]"))).click()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="cookies_accept"]'))).click()
            # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="uc-btn-accept-banner"]'))).click()
        except:
            print("Cookie popup not found")
        time.sleep(15)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable( (By.XPATH, '/html/body/div[2]/div[2]/div[4]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/button'))).click()
        time.sleep(15)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable( (By.XPATH, '/html/body/div[2]/div[2]/div[4]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/button'))).click()
        time.sleep(15)
        self._process_the_top()
        self._process_the_rest()
        self.driver.close()

    def write_data(self):
        df = pd.DataFrame({"website": self.url["kiwi"], "airline": self.kiwi_data["airline"], "departure_time": self.kiwi_data["departure_time"], "arrival_time":self.kiwi_data["arrival_time"] ,
                          "duration": self.kiwi_data["duration"], "price": self.kiwi_data["price"], "number_of_stops": self.kiwi_data["number_of_stops"]})
        #  website	airline	start_time	stop_time	duration	number_of_stops	price
        df2 = pd.DataFrame({"best_price": self.kiwi_data["extra_data"]["best_price"], "best_duration": self.kiwi_data["extra_data"]["best_duration"],
                            "cheapest_price": self.kiwi_data["extra_data"]["cheapest_price"], "cheapest_duration": self.kiwi_data["extra_data"]["cheapest_duration"],
                            "fastest_price": self.kiwi_data["extra_data"]["fastest_price"], "fastest_duration": self.kiwi_data["extra_data"]["fastest_duration"]} ,index=[0] )

        df.to_csv("kiwi_data.csv")
        df2.to_csv("kiwi_extra_data.csv")
        
        return df, df2

    def __del__(self):
        self.driver.quit()


test = scraper()

test.kiwi_scaper()

result = test.write_data()
print (result[0].head())
print (result[1].head())
