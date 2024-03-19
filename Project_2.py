# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 13:13:02 2023

@author: Melanie Navarrete
"""
##Added append to merge dataframes
####changed the dataframe layout to minimize the number of dataframes used

##Next update-
###added a new columns and calculated the antiobiotic resistance rate, change 
###### in antibiotic resistance and difference in infection rate  
###### for California and NYC  
 


#Next update changed the order of some of the comparison statistics to make S
###more sense added the infection rate difference for California
###worked some of the graphs


##Entered charts/comparisons


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import csv



#importing the dataframes from my the respective csv files
stats_ca = pd.read_csv(r'C:\Users\Brine\OneDrive\Documents\Spring_2023\Project\tb_in_ca.csv')
stats_nyc = pd.read_csv(r'C:\Users\Brine\OneDrive\Documents\Spring_2023\Project\DOHMH_Tuberculosis_Surveillance__Data_from_the_Tuberculosis_Control_Annual_Summary.csv')
stats_us = pd.read_csv(r'C:\Users\Brine\OneDrive\Documents\Spring_2023\Project\Tuberculosis_Cases_and_Percentages_by_multidurg_resistance_and_origin.csv')

#filtering out extra data (about 100 years worth)  in the New York City cases before merge
stats_nyc=( stats_nyc[(stats_nyc['Year'] >= 2005) & (stats_nyc['Year'] <= 2016 )])
stats_us = (stats_us[(stats_us['Year'] >= 2005) & (stats_us['Year'] <= 2016 )])
#stats_us = (stats_us[(stats_us['Year' : 'Multidrug Resistant TB Cases Total MDR No Previous TB Percent'])])
stats_us = stats_us.filter(items=['Year','All MDR', 'Multidrug Resistant TB Cases Total MDR Previous TB Percentage', 'Multidrug Resistant TB Cases Total MDR No Previous TB Percent' ])

#Adding a column to the NYC info to show the city to compliment the California 
####information
stats_nyc["location"] = "New York City"

#getting rid of duplicate/broken down by demographics 
#information from the california data set
stats_ca =( stats_ca[(stats_ca['Strata'] == 'All cases') ])
stats_ca["location"] = "California"
stats_ca=(stats_ca[stats_ca['Year']<=2016])


#Append the dataframes since the merge is across columns
total_stats = stats_nyc.append(stats_ca)
total_stats = total_stats.append(stats_us)

total_stats['difference_mdr'] = total_stats['All MDR']-total_stats['Multidrug-resistance cases']

####Create a new column to house and calculate the antibiotic resistance percentage per population. 
#Tuberculosis is treated with 4 antibiotics so mar= a/b where a is 

total_stats['antibiotic_resistance_per_100,000'] = total_stats['Multidrug-resistance cases'] / total_stats['Culture-positive cases']*100


####create a column and calculate difference in infection rate for California and NYC 
total_stats['infection_rate_difference_NYC'] = total_stats['NYC Rate per 100,000'].diff()

##Making 'Rate per 100,000 population a float
total_stats['Rate per 100,000 population'] = pd.to_numeric(total_stats['Rate per 100,000 population'], errors = 'coerce')
#total_stats['infection_rate_difference_Ca'] = total_stats['Rate per 100,000 population'].diff()

#calculating the difference between the infection rates in NYC and California
total_stats['infection_rate_difference'] = total_stats['Rate per 100,000 population'] - total_stats['NYC Rate per 100,000']

#Calculate percent infection for both us and nyc, subtract and graph
total_stats['antibiotic_resistance_rate_percentage'] = total_stats['Multidrug-resistance cases'] / total_stats['NYC Number of TB cases']
total_stats.plot(x="Year", y=["antibiotic_resistance_rate_percentage"])

##plot the yearly infection rate for nyc and california with the  
## antibiotic-resistance rate
total_stats.plot(x="Year", y=["NYC Rate per 100,000", "antibiotic_resistance_per_100,000"])
plt.show()


#plot the antibiotic resistance rate for nyc
total_stats.plot(x="Year", y=["antibiotic_resistance_per_100,000"])
plt.show()

##plot the yearly infection rate for nyc and california
total_stats.plot(x="Year", y=["NYC Rate per 100,000", "Rate per 100,000 population"])
plt.show()

##plot the antibiotic rate percentage against the infection rate for NYC

 
#Saving the dataframe to a csv file
total_stats.to_csv(r'C:\Users\Brine\OneDrive\Documents\Spring_2023\Project\total_stats2.csv')

