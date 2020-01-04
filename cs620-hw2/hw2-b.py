"""
CS 620
HW2-b
@author: Heramb
"""
import pandas as pd
import glob
import gc
import os
import numpy as np

import datetime
currentyear = datetime.date.today().year


"""
Function : getDataFrame(fileName)
	- Returns a dataframe with a added year column from the fileName 
""" 
def getDataFrame(fileName):
  yobdf = pd.read_csv(fileName, delimiter=',', header=None)
  yobdf['year'] = fileName[-8:-4]
  return yobdf


"""
Function : getAge(birthyear)
	- Returns the age based on birth year 
"""
def getAge(birthyear):
  return currentyear - birthyear
  

"""
Function : getDataFrame(fileName)
	- Returns a dataframe with a added year column from the fileName 
"""
def checkAlive(data_p):
  Tdata = data_p['age']
  #print(Tdata)
  Tlife = data_p['F']
  #print(Tlife)
  return Tdata < Tlife

#part I
path = r'wrangling/yob-names' # use your path
yobPath = 'yob-names.csv'
all_files = glob.glob(path + "/*.txt")
data = pd.DataFrame()

print('No of Files : ',len(all_files))

allData = list(map(getDataFrame, all_files))

data = pd.concat(allData)

data.columns = ['name','sex','frequency','year']

data = data[['year','name','sex','frequency']]

data.to_csv('wrangling/'+yobPath, index=False)

print('--> number of rows on csv : ',data.name.count())

print(data.head())

data['year'] = pd.to_numeric(data['year'])                                        #--- Changing the year column to numeric
# Part II
# a)	What is the most popular boys name in year 1980?
data_b = data[(data['sex'] == "M") & (data['year'] == 1980)]                      #--- Creating a seperate dataframe for the problem when we have data where sex = 'M' and year = 1980

popular_count = data_b['frequency'].max()                                         #--- Getting popular count by taking max of frequency

print('--> post popular count is : ',popular_count)                   

popular_boy = data_b.loc[data_b['frequency'] == popular_count,'name'].iloc[0]     #--- Getting name of a popular boy based on popular count

print('--> Most popular boy name of 1980 is : ',popular_boy)

# b)	How many girls were born between 1990 and 2000?

data_a = data[(data['sex'] == "F") & (data['year'] >= 1990) & (data['year'] <= 2000)] #--- Creating a seperate dataframe for the problem when we have data where sex = 'F' and year >= 1990 & <= 2000

print('--> No of girls born between 1990 and 2000 : ',data_a['frequency'].sum())          #--- Number of girls born between 1990 and 2000

#c)	How many female Benjamin's are alive today (year 2019)? 
"""
(15 pts) Estimate the number of female Benjamin’s alive today (year 2019) who were born on or after 1950. For this particular query, use the given “cdclife-expectancy.csv” file to generate this result. We can interpret the data from
this file as, “The average life expectancy of U.S. babies born in each year, for Males and Females” and so on.
"""
lifeExpectancy = pd.read_csv("wrangling/cdc-life-expectancy.csv")

lifeExpectancy_c = lifeExpectancy[lifeExpectancy['year']>=1950]                      #--- Creating a seperate dataframe for the problem when we have data where year >= 1950

data_c = data[(data['name'] == 'Benjamin') & (data['sex'] == "F") & (data['year'] >= 1950)] #--- Creating a seperate dataframe for the problem when we have data where sex = 'F' and year = 1950 and #name = 'Benjamin'

#data_c['age'] = data_c['year'].apply(getAge)                                         #--- Creating a column age calculated based on the current year and brith year
data_c['age'] = data_c.loc[:, ('year')].apply(getAge)

data_c_byAge = data_c.sort_values('year', ascending = False)                         #--- sorting the dataframe by year

data_c_byAge = data_c_byAge[data_c_byAge['year'] <= 2012]                            #--- based on the life expectancy we have only data upto 2012 so we are slicing tremaining rows that have year > 2012

data_c_byAge = data_c_byAge.reset_index(drop=True)                                   #--- resetting he index as we have previous index so far.

data_c_byAge = data_c_byAge.merge(lifeExpectancy_c[['year','F']],on = 'year')        #--- merging the 2 dataframes as to compare and get result

data_c_byAge['alive'] = checkAlive(data_c_byAge[['age','F']])                        #--- use check alive function to create a column 'alive' that has true if current age is less than life expectancy, false if current age is greater than life expectancy

#print(data_c_byAge.head())

data_final = data_c_byAge[data_c_byAge['alive'] == True]                             #--- Creating a final dataframe where we have only benjamin's who are alive based on the life expectancy from 1950 - 2012

print('--> Rows : ',data_final['frequency'].count())                                 

print('--> Estimated Female Benjamin\'s alive today who were born from 1950 - 2012 : ',data_final['frequency'].sum()) #--- Printing the number of female benjamin's alive today.

#--- For Benjamin's born after 2012 we donot have a ny life expectency and it has been only 6 years so we can assume that most of them will be alive
data_12_2_19 = data_c[(data_c['year'] > 2012) & (data_c['year'] < 2019)]

print('--> Estimated Female Benjamin\'s alive today who were born from 1950 - 2019 : ',data_final['frequency'].sum()+data_12_2_19.frequency.sum())

