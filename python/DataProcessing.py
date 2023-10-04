#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 13:13:20 2023

@author: jeffery
"""

import pandas as pd
import datetime
import seaborn as sns
from matplotlib import pyplot as plt



# assume date is an array dd mm yyyy
# csv files keys kiwi momondo kayak

csv_dict = {'kiwi': 'kiwi_data.csv',
    'momondo': 'momondo_data.csv', 'kayak': 'kayak_data.csv'}

# year month date array
departure_date = None
arrival_date = None


class Data_processing:
    
    def __init__ (self, csv_file_dict):
        self.csv_files = csv_file_dict
        self.data = {}
        self.data_processed = {}
        self.departure_date = [2023 , 10 , 22]

    def read_csv(self):

        for key in self.csv_files.keys():
            self.data[key] = pd.read_csv(self.csv_files[key])

        pass

    def kiwi_clean(self):

        def clean_departure_time(m_before: str) -> datetime.datetime:
            """
            find m in am or pm and chops it off

            """
           
            before = m_before.strip()
            time_array = []
            time_array.extend([int(x) for x in before.split(':')])
                       # create date time object
            before = datetime.datetime(*self.departure_date, *time_array)
            return before

        def clean_arrival_time(m_before: str) -> datetime.datetime:
            before = m_before.strip()
            time_array = []
            time_array.extend([int(x) for x in before.split(':')])
                       # create date time object
            before = datetime.datetime(*self.departure_date, *time_array)
            return before

        def clean_duration(m_before: str) -> datetime.timedelta:
            before = m_before.split()
            result = []
            for x in before:
                
                result.append(int(x[: -1].strip()))  # remove h and m
            if len(result)== 1:
                return datetime.timedelta(hours=result[0])

            return datetime.timedelta(hours=result[0], minutes=result[1])

        def clean_price(m_before: str) -> float:
            m_before = m_before.strip()
            before = m_before[:-1]
            before = float(before)
            return before

        def clean_number_of_stops(m_before: str) -> int:
            if "direct" in m_before.lower():
                return 0
            else:
                s_index = m_before.find('s')
                before = m_before[: s_index].strip()
                return int(before)

# airline    departure_time    arrival_time    duration    price    number_of_stops
        self.data_processed['kiwi'] = pd.DataFrame()
        self.data_processed['kiwi']["departure_time"] = self.data['kiwi']["departure_time"].apply(
            clean_departure_time)
        self.data_processed['kiwi']["arrival_time"] = self.data['kiwi']["arrival_time"].apply(
            clean_arrival_time)
        self.data_processed['kiwi']["duration"] = self.data['kiwi']["duration"].apply(
            clean_duration)
        self.data_processed['kiwi']["price"] = self.data['kiwi']["price"].apply(
            clean_price)
        self.data_processed['kiwi']["number_of_stops"] = self.data['kiwi']["number_of_stops"].apply(
            clean_number_of_stops)
        self.data_processed['kiwi']["airline"] = self.data['kiwi']["airline"]



    def write_kiwi_processed(self):
       
       self.data_processed['kiwi'].to_csv("kiwi_data_cleaned.csv")
       
    
         
      
    
    def exploratory_data_analysis_kiwi (self):
        self.data_processed['kiwi'].describe ().to_csv("kiwi_summary_statistic")
        print (self.data_processed['kiwi'].describe ())
        plt.figure(figsize=(12, 6))
        
        sns.countplot(x = self.data_processed['kiwi']["number_of_stops"])  
        sns.countplot(x = self.data_processed['kiwi']["price"])
        sns.countplot(x = self.data_processed['kiwi']["duration"])
        sns.countplot(x = self.data_processed['kiwi']["departure_time"])
        sns.countplot(x = self.data_processed['kiwi']["arrival_time"])
        
        
        
        plt.xticks(rotation=90)
        plt.show()
        
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=self.data_processed['kiwi'], y='price', hue='number_of_stops')
        plt.show()
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=self.data_processed['kiwi'], x='departure_time', y='price')
        plt.show()
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=self.data_processed['kiwi'], x="arrival_time", y='price')
        plt.show()
        
        self.data_processed['kiwi'].hist (bins=20, figsize=(12, 6))
        plt.show()  
        
        
        plt.figure(figsize=(12, 6))
        self.data_processed['kiwi'].boxplot()
        plt.show()
        
        plt.figure(figsize=(12, 6))
        sns.pairplot(self.data_processed['kiwi'])
        plt.show()
        
       
    
    
    
  
     
 
test_kiwi = Data_processing(csv_dict)
test_kiwi.read_csv()
test_kiwi.kiwi_clean()
# test_kiwi.write_kiwi_processed()
test_kiwi.data_processed["kiwi"].info()
test_kiwi.exploratory_data_analysis_kiwi()

        