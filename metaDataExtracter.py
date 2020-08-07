from climateDataPreprocessor import avg_aqi
from constants import get_path
import sys
import requests
import os
import csv
import pandas as pd
from bs4 import BeautifulSoup

def meta_data(month, year):
  file_html = open('assets/climate-data/{}/{}.html'.format(year, month), 'rb')
  text = file_html.read()

  temp_data = []
  final_data = []

  soup = BeautifulSoup(text, 'lxml')
  for table in soup.findAll('table', { 'class': 'medias mensuales numspan' }):
    for tbody in table:
      for tr in tbody:
        data = tr.get_text()
        temp_data.append(data)

  rows = len(temp_data) / 15  #15 is column count in data

  for _row in range(round(rows)):
    new_data = []
    for _i in range(15):
      new_data.append(temp_data[0])
      temp_data.pop(0)
    final_data.append(new_data)

  final_data_len = len(final_data)
  final_data.pop(final_data_len-1)
  final_data.pop(0)

  for i in range(len(final_data)):
    final_data[i].pop(6)
    final_data[i].pop(13)
    final_data[i].pop(12)
    final_data[i].pop(11)
    final_data[i].pop(10)
    final_data[i].pop(9)
    final_data[i].pop(0)

  return final_data

def combine_processed_data(year, chunksize):
  for data in pd.read_csv('assets/processed-data/processed_{}.csv'.format(year), chunksize=chunksize):
    df = pd.DataFrame(data=data)
    lst = df.values.tolist()
  return lst

if __name__ == "__main__":
  path = get_path()
  if not os.path.exists('{}/assets/processed-data'.format(path)):
    os.makedirs('{}/assets/processed-data'.format(path))

  for year in range(2013, 2019):
    final_data = []
    with open('{}/assets/processed-data/processed_{}.csv'.format(path, year), 'w') as csvfile:
      writer = csv.writer(csvfile, dialect='excel')
      writer.writerow(['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])

    for month in range(1, 13):
      temp_data = meta_data(month, year)
      final_data = final_data + temp_data

    aqi_year = avg_aqi(year)
    if len(aqi_year) == 364:
      aqi_year.insert(364, '-')
    
    for i in range(len(final_data)-1):
      final_data[i].insert(8, aqi_year[i])

    with open('{}/assets/processed-data/processed_{}.csv'.format(path, year), 'a') as csvfile:
      writer = csv.writer(csvfile, dialect='excel')
      for row in final_data:
        valid_flag = True
        for element in row:
          if element == '-' or element == '':
            valid_flag = False
        if valid_flag:
          writer.writerow(row)

  data_2013 = combine_processed_data(2013, 500)
  data_2014 = combine_processed_data(2014, 500)
  data_2015 = combine_processed_data(2015, 500)
  data_2016 = combine_processed_data(2016, 500)
  data_2017 = combine_processed_data(2017, 500)

  total_data = data_2013 + data_2014 + data_2015 + data_2016 + data_2017

  with open('{}/assets/processed-data/combined-processed-data.csv'.format(path), 'w') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
    writer.writerows(total_data)

    