#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 13:16:47 2023

@author: jeffery
"""

# The user inputs certain preferences for the flight, e.g., price ranges, trip duration ranges
# (how long from departure to destination), whether the flight is direct or has one or
# more stops (if it has stops then layover duration), flight company from available options
# etc.
import pandas as pd 

dict_of_dataframe = dict()
dict_of_dataframe ['kiwi'] = pd.read_csv("kiwi_data_cleaned.csv")
dict_of_dataframe ['momondo'] = pd.read_csv("momondo_data_cleaned.csv")
dict_of_dataframe ['kayak'] = pd.read_csv("kayak_data_cleaned.csv")




def userInteraction(dict_with_pandas:dict):
    dict_of_filtered_dataframe= dict()
    price_range = []
    duration_range = []
    stops_range = [] #min 0
    flight_company = str()
    userinputcounter = 0
    user_number_of_try = 0
    max_try = 10
    while True :
        user_number_of_try += 1
        if user_number_of_try == max_try : return dict_of_filtered_dataframe
        while True :
            userinputcounter += 1
            if userinputcounter == max_try :return dict_of_filtered_dataframe
            user_price_range = input ("Enter a price range separated by space eg 10 100 or nothing by pressing Enter, minimum is zero: ")
            user_duration_range = input ("Enter a flight duration range in hours separated by space e.g. 0 5 or nothing by pressing Enter minimum is zero :")
            user_stops_range = input ("Enter the range for the number of stops separated by space e.g 0 3 or nothing by pressing Enter minimum is zero :" )
            user_flight_company = input("Enter the name of a flight company or nothing by pressing Enter ")
            user_response = input ("Enter (r or repeat) to repeat the prompt or or  press enter to process data ")
            if user_price_range == "" and user_duration_range =="" and user_stops_range=="" and user_flight_company  == ""  :
                print ("you selected nothing exiting ")
                return
            if user_response.lower().startswith('r'):
                continue
            if userinputcounter == max_try :
                return dict_of_filtered_dataframe
            if user_response == "" :
                break
            if  user_price_range < 0 or  user_duration_range < 0 or user_stops_range < 0  :
                continue
            
        #no user validation just checking if they are not empy before spliting
        #todo user validation later
        if user_price_range != "" :price_range = [float (val) for val in user_price_range.split() ]
        if user_stops_range != "" : stops_range = [int (val) for val in user_stops_range.split() ]
        if user_duration_range != "" : duration_range = [int (val) for val in user_duration_range.split() ]
        if user_flight_company != "" : flight_company = user_flight_company

# airline    departure_time    arrival_time    duration    price    number_of_stops        
         
        for key in  dict_with_pandas.keys():
           
            
            if user_price_range != "" :
                dict_of_filtered_dataframe[key] = dict_with_pandas[key] [ (dict_with_pandas[key]["price"] > price_range[0]) & (dict_with_pandas[key]["price"] < price_range[1])]
             
            
            if user_stops_range != "" : 
                dict_of_filtered_dataframe[key] = dict_of_filtered_dataframe[key] [(dict_of_filtered_dataframe[key]["number_of_stops"] > stops_range[0 ]) &  (dict_of_filtered_dataframe[key]["number_of_stops"] <stops_range[1] ) ]
                
        
            if user_duration_range != "" :
                dict_of_filtered_dataframe[key] = dict_of_filtered_dataframe[key] [(dict_of_filtered_dataframe[key]["duration"] > duration_range [0]) & (dict_of_filtered_dataframe[key]["duration"] < duration_range [1]) ]
        
            if  user_flight_company != "" :
                dict_of_filtered_dataframe[key] = dict_of_filtered_dataframe[key] [dict_of_filtered_dataframe[key]['airline'].apply(lambda airline: (flight_company in airline) or (airline in flight_company))]
            
        
        
        user_response = input ("Enter (r or repeat) to repeat the prompt or or  press enter to quit ")
        if user_response == "":
            return dict_of_filtered_dataframe
result = userInteraction(dict_of_dataframe)

result['kiwi'].head()

