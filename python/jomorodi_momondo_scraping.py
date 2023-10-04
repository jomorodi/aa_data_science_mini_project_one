#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 23:10:56 2023

@author: jeffery
"""

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import itertools


class scraper ():

    def __init__(self):
        self.url = dict()
        self.driver = uc.Chrome()  # todo change to headless
        # uc.Chrome(headless=True,use_subprocess=False)
        self.actions = ActionChains(self.driver)
        self.momondo_data = {"departure_time": [], "arrival_time": [], "duration": [], "price": [
        ], "number_of_stops": [], "airline": [], "website": [], "extra_data": dict()}

        self.data = [self.momondo_data]
        self.size = 50  # size of the data to scrape
        self.counter = 0


    def _process_airline_name_from_image(self, locator):
         """
         imput is a web elemnt
         process the the airline name from the thier image alt adress

         """
         # pass in content_section_div
         image_tag_list = locator.find_elements(By.TAG_NAME, "img")
         result = []
         count = 1
         for img in image_tag_list:
             result.append(f'{count}. {img.get_attribute("alt")}')
             count += 1

         self.momondo_data["airline"].append(" ".join(result))

    def _process_the_top(self):
         """

         process the the the  first of the two important div that contains vital stat like best price , best duration
         cheapeast price , cheapeast duraion etc
         """
         top = self.driver.find_element(
             By.XPATH, "/html/body/div[2]/div[1]/div[5]/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[2]")
         div_list = top.find_elements(By.TAG_NAME, 'div')
         filter_div_list = [
             div for div in div_list if div.get_attribute('class') == "Hv20-value"]

         results = []
         for div in filter_div_list:
             span_list = div.find_elements(By.TAG_NAME, "span")
             for span in span_list:
                 results.append(span.text)
         self.momondo_data["extra_data"]["cheapest_price"] = results[0]
         self.momondo_data["extra_data"]["cheapest_duration"] = results[1]
         self.momondo_data["extra_data"]["best_price"] = results[2]
         self.momondo_data["extra_data"]["best_duration"] = results[3]
         self.momondo_data["extra_data"]["fastest_price"] = results[4]
         self.momondo_data["extra_data"]["fastest_duration"] = results[5]

    def _process_times(self, locator):
         """
         imput is a web elemnt
         process the depature time , arrival ,time and depature
         by finding the 3 time tag
         """
         # pass in content_section_div

         span_list = locator.find_elements(By.TAG_NAME, "span")
         span_list_filtered = [span for span in span_list if (
             span.get_attribute('class') == '' and span.get_attribute('style') == '')]
         div_list_with_duration = locator.find_elements(By.TAG_NAME, "div")
         duration_div = [div for div in div_list_with_duration if div.get_attribute(
             'class') == "vmXl vmXl-mod-variant-default"]
         self.momondo_data["departure_time"].append(span_list_filtered[0].text)
         self.momondo_data["duration"].append(duration_div[1].text)
         self.momondo_data["arrival_time"].append(
             span_list_filtered[1].text)  # second div as the duration 

    def _process_price(self, locator):
         """
         imput is a web elemnt
         process the the the price by finding the span that contains it

         """
         # pass in price_section_div
         div_list = locator.find_elements(By.TAG_NAME, "div")
         div_list_filtered = [div for div in div_list if div.get_attribute(
             'class') == 'f8F1-price-text']
         self.momondo_data["price"].append(div_list_filtered[0].text)

    def _process_stops(self, locator):
         """
         input is a web elemnt
         process the the the number of stops by findinf the div that contains it

         """
         # pass in content_section_div
         span_list = locator.find_elements(By.TAG_NAME, "span")
         span_list_filtered = [span for span in span_list if "JWEO-stops-text" in span.get_attribute(
             'class') ]
         self.momondo_data["number_of_stops"].append(span_list_filtered[0].text)

    def _process_the_rest(self):
         """
         input is a web elemnt
         process the  the other div
         self.counter ensures that 50 items are process
         count just loops through the divs
         """
         bottom = self.driver.find_element(
             By.XPATH, '/html/body/div[2]/div[1]/div[5]/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]/div[4]/div[2]/div[1]/div/div')
         div_list = bottom.find_elements(By.TAG_NAME, 'div')
         # filter_div_list = [div for div in div_list if div.get_attribute('class') != "G-5c" ] #remove advert
         filter_div_list = [div for div in div_list if div.get_attribute(
             'class') == "nrc6-inner"]  # remove advert

         # content_section_div = [div for div in filter_div_list if div.get_attribute(
         #     'class') == "nrc6-content-section"]
         # price_section_div = [div for div in filter_div_list if div.get_attribute(
         #     'class') == "nrc6-price-section"]
         # print("advert lenght == ", len(filter_div_list))

         for elem in filter_div_list:
             content_section_div_list = elem.find_elements(By.TAG_NAME, "div")
             content_section_div = [div for div in content_section_div_list if div.get_attribute(
                 'class') == "nrc6-content-section"]
             price_section_div_list = elem.find_elements(By.TAG_NAME, "div")
             price_section_div = [div for div in price_section_div_list if div.get_attribute(
                 'class') == "nrc6-price-section"]
             self._process_airline_name_from_image(content_section_div[0])
             self._process_times(content_section_div[0])
             self._process_price(price_section_div[0])
             self._process_stops(content_section_div[0])
             self.counter += 1
             print("count is now " , self.counter)
             if self.counter == self.size:
                 break

         print ("the size of all flifht tickect len (filter_div_list)" , len (filter_div_list))


    def momondo_scaper(self):
         self.url["momondo"] = "https://www.momondo.com"

         self.driver.get(
             "https://www.momondo.com/flight-search/HEL-FRA/2023-10-22?sort=bestflight_a")
         time.sleep(5)
         try:

             # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//html/body/div[2]/div[2]/section/div/div/div/section/div[2]/button[3]"))).click()
             WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                 (By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div[2]/div/div[1]/button'))).click()
             # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="uc-btn-accept-banner"]'))).click()
         except:
             print("Cookie popup not found")
         time.sleep(15)
         # load more contents
         show_more_button = self.driver.find_element(
             By.XPATH, '/html/body/div[2]/div[1]/div[5]/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div[1]/div/div/div')
         time.sleep(20)
         print("first click")
         # self.actions.move_to_element(show_more_button).click()
         # self.actions.perform()
         show_more_button.click()
         time.sleep(20)
         print("second click")
         show_more_button_2 = self.driver.find_element(
             By.XPATH, '/html/body/div[2]/div[1]/div[5]/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div[1]/div/div/div')
         show_more_button_2.click()
         # self.actions.move_to_element(show_more_button_2).click()
         # self.actions.perform()
         time.sleep(20)

         print("third click")

         show_more_button_3 = self.driver.find_element(
             By.XPATH, '/html/body/div[2]/div[1]/div[5]/div/div[2]/div[3]/div[1]/div[2]/div[1]/div[3]/div[1]/div/div/div')
         show_more_button_3.click()
         # self.actions.move_to_element(show_more_button_2).click()
         # self.actions.perform()
         time.sleep(20)
         # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
         #     (By.XPATH, '/html/body/div[2]/div[1]/main/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div/div/div'))).click()
         # time.sleep(15)
         # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
         #     (By.XPATH, '/html/body/div[2]/div[1]/main/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div/div/div'))).click()
         # time.sleep(15)
         self._process_the_top()
         self._process_the_rest()
         self.driver.close()

    def write_data(self):
         df = pd.DataFrame({"website": self.url["momondo"], "airline": self.momondo_data["airline"], "departure_time": self.momondo_data["departure_time"], "arrival_time": self.momondo_data["arrival_time"],
                           "duration": self.momondo_data["duration"], "price": self.momondo_data["price"], "number_of_stops": self.momondo_data["number_of_stops"]})
         #  website    airline    start_time    stop_time    duration    number_of_stops    price
         df2 = pd.DataFrame({"best_price": self.momondo_data["extra_data"]["best_price"], "best_duration": self.momondo_data["extra_data"]["best_duration"],
                             "cheapest_price": self.momondo_data["extra_data"]["cheapest_price"], "cheapest_duration": self.momondo_data["extra_data"]["cheapest_duration"],
                             "fastest_price": self.momondo_data["extra_data"]["fastest_price"], "fastest_duration": self.momondo_data["extra_data"]["fastest_duration"]}, index=[0])

         df.to_csv("momondo_data.csv")
         df2.to_csv("momondo_extra_data.csv")

         return df, df2

    def __del__(self):
         self.driver.quit()


test = scraper()

test.momondo_scaper()

result = test.write_data()
print (result[0].head())
print (result[1].head())