#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 21:41:36 2019
CS620
HW3
@author: heramb
"""
#--- import librarires
import warnings                                        #--- used to supress warnings
warnings.filterwarnings("ignore")
import pandas as pd
from pandas import DataFrame
#---import xmltodict #--- importing xml as dictionary #----- not working 
import xml.etree.ElementTree as ET

csv_path = 'SP500_ind.csv'
xml_path = 'SP500_symbols.xml'

csv_data = pd.read_csv(csv_path)                        #--- read csv data 
#csv_data.head()
ticker = csv_data.Symbol.unique()                       #--- get the unique tickers from CSV data store it in a list - ticker
ticker

#parser = ET.XMLParser(encoding="utf-8")
tree = ET.parse(xml_path)                               #--- parse the xml using ElementTree.parse
root = tree.getroot()                                   #--- get the root of the xml so that we can parse the remaining data from the root
#etree_to_dict(tree.getroot())
root.tag

"""This function takes in the xml_dict and the list that contains a
Symbol (ticker). Return the name of the ticker
Ex: for ticker “A”, the function returns Agilent Technologies Inc
"""
def ticker_find(xml_dict, ticker):
  name = ''
  for child in xml_dict:                                #--- iterate over xml child elements
    if(child.attrib['ticker'] == ticker):               #--- check if the xml ticker matches with the needed ticker
      #print(child.attrib['name'])
      name = child.attrib['name']                       #--- if matcches update the name variable
      break                                             #--- break the loop once the name is found
    else:
      name = 'No data in SP500'                         #--- update name variable as 'no data in SP500' if ticker not found
  return name

"""This function takes in the csv_data and a ticker.
Return the average opening price for the stock as a float.
"""
def calc_avg_open(csv_data, ticker):
  return csv_data[csv_data['Symbol']==ticker].Open.mean()   #--- returns mean of the ticker found in the dataframe

"""This function takes in the csv_data and a ticker. Return the volume weighted average price (VWAP)
of the stock. In order to do this, first find the average price of the stock on each day. Then, multiply
that price with the volume on that day. Take the sum of these values. Finally, divide that value by the
sum of all the volumes.
(hint: average price for each day = (high + low + close)/3)
"""
def vwap(csv_data, ticker):
  data = csv_data[csv_data['Symbol']==ticker]           #--- gets the matching tiker data from ticker dataframe 
  data1 = data[['High','Low','Close']]                  #--- seperates the required data into another dataframe
  data['mean'] = data1.mean(axis=1)                     #--- calculates mean in horizontal axis
  data['mean_volume'] = data['Volume']*data['mean']     #--- multiply volume of each column with its mean value
  vwa = data['mean_volume'].sum()/data['Volume'].sum()  #--- calculates the sum of each column and divides it with sum of volumne
  #print('Volume weighted average of comapy A is :',vwa)
  return vwa


#----- printing the required data
names=list()
averages=list()
weighted = list()
processedData = dict()
for tick in ticker:
    name = ticker_find(root, tick)
    avg = calc_avg_open(csv_data, tick)
    vwa = vwap(csv_data, tick)
    names.append(name)
    averages.append(avg)
    weighted.append(vwa)
    print(name,', ',avg,', ',vwa)

#--- after printing lets save the data in a csv file for further use
processedData = {'name':names,'avg':averages,'vwap':weighted}
processedDataDF = DataFrame(processedData, columns = ['name','avg','vwap'])
processedDataDF.to_csv('processedData.csv')