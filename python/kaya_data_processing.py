#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 19:37:15 2023

@author: jeffery
"""

import pandas as pd
import datetime
import seaborn as sns
from matplotlib import pyplot as plt


csv_dict = {'kiwi': 'kiwi_data.csv',
    'momondo': 'momondo_data.csv', 'kayak': 'kayak_data.csv'}

class Data_processing:
    
    def __init__ (self, csv_file_dict):
        self.csv_files = csv_file_dict
        self.data = {}
        self.data_processed = {}
        self.departure_date = [2023 , 10 , 22]

    def read_csv(self):

        for key in self.csv_files.keys():
            self.data[key] = pd.read_csv(self.csv_files[key])

        


    def kayak_clean (self):
        
        def clean_departure_time(m_before:str)-> datetime.datetime :
            """ 
            find m in am or pm and chops it off
            
            """
            m_index = m_before.find('m')
            before = m_before [:m_index - 1]
            before = before.strip()
            time_array = []
            if ':' in before :
                time_array.extend([ int (x) for x in before.split(':')]) #split by : and convert to it before extending
            else:
                time_array.append(int (before))
                
            #create date time object
            before = datetime.datetime(*self.departure_date ,*time_array)
            return before
            
                
        def clean_arrival_time (m_before:str) -> datetime.datetime:
            m_index = m_before.find('m')
            str_before = m_before[: m_index -1]
            str_before =str_before.strip()
            time_array = []
            if ':' in str_before :
                time_array.extend([ int (x) for x in str_before.split(':')])
            else:
                time_array.append(int (str_before))
            str_after = m_before [m_index :]
            if '+' in str_after :
                chr_index = str_after.find('+')
                str_after = str_after [chr_index + 1 :].strip() # find +x e.g +2 and teurn integer 2
                str_after = int (str_after)
                #datetime.timedelta
                str_after = datetime.timedelta (days=str_after)
                before = datetime.datetime(*self.departure_date ,*time_array ) + str_after
                return before
            
            before = datetime.datetime(*self.departure_date ,*time_array)
            return before
        
        
        def clean_duration (m_before:str)-> datetime.timedelta:
            before = m_before.split ()
            result =[]
            for x in before :
                result.append(int (x[: -1].strip())) #remove h and m
                
            return datetime.timedelta(hours=result[0] , minutes=result[1]) 
                
            
            
        def clean_price(m_before:str) -> float:
            before = m_before[1:].strip()
            before = float (before)
            return before
        
        
        def clean_number_of_stops (m_before:str) ->int :
            if "nonstop" in  m_before.lower() :
                return 0
            else:
                s_index = m_before.find('s')
                before = m_before[: s_index].strip()
                return int (before)
            
            
        self.data_processed['kayak'] = pd.DataFrame()
        self.data_processed['kayak']["departure_time"] = self.data['kayak']["departure_time"].apply(
            clean_departure_time)
        self.data_processed['kayak']["arrival_time"] = self.data['kayak']["arrival_time"].apply(
            clean_arrival_time)
        self.data_processed['kayak']["duration"] = self.data['kayak']["duration"].apply(
            clean_duration)
        self.data_processed['kayak']["price"] = self.data['kayak']["price"].apply(
            clean_price)
        self.data_processed['kayak']["number_of_stops"] = self.data['kayak']["number_of_stops"].apply(
            clean_number_of_stops)
        self.data_processed['kayak']["airline"] = self.data['kayak']["airline"]
            
            
    def write_kayak_processed(self):
       
       self.data_processed['kayak'].to_csv("kayak_data_cleaned.csv")
       
    
       
    
    def exploratory_data_analysis_kayak (self):
        self.data_processed['kayak'].describe ().to_csv("kayak_summary_statistic")
        print (self.data_processed['kayak'].describe ())
        plt.figure(figsize=(12, 6))
        
        sns.countplot(x = self.data_processed['kayak']["number_of_stops"])  
        sns.countplot(x = self.data_processed['kayak']["price"])
        sns.countplot(x = self.data_processed['kayak']["duration"])
        sns.countplot(x = self.data_processed['kayak']["departure_time"])
        sns.countplot(x = self.data_processed['kayak']["arrival_time"])
        
        
        
        plt.xticks(rotation=90)
        plt.show()
        
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=self.data_processed['kayak'], y='price', hue='number_of_stops')
        plt.show()
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=self.data_processed['kayak'], x='departure_time', y='price')
        plt.show()
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=self.data_processed['kayak'], x="arrival_time", y='price')
        plt.show()
        
        self.data_processed['kayak'].hist (bins=20, figsize=(12, 6))
        plt.show()  
        
        
        plt.figure(figsize=(12, 6))
        self.data_processed['kayak'].boxplot()
        plt.show()
        
        plt.figure(figsize=(12, 6))
        sns.pairplot(self.data_processed['kayak'])
        plt.show()
  
#print (dir (Data_processing)   )  
     
test_kayak = Data_processing(csv_dict)
test_kayak.read_csv()
test_kayak.kayak_clean()
# test_kayak.write_kayak_processed()
test_kayak.exploratory_data_analysis_kayak()