import pandas as pd
import matplotlib.pyplot as plt
from constants import get_path

def avg_aqi(year):
  average = []
  for rows in pd.read_csv('assets/aqi/aqi{}.csv'.format(year), chunksize=24):
    avg = 0.0
    sum = 0
    count = 0
    data = []
    df = pd.DataFrame(data=rows)
    for _index,row in df.iterrows():
      data.append(row['PM2.5'])
    for item in data:
      if type(item) is float or type(item) is int:
        sum += item
        count += 1
      if type(item) is str:
        if item != 'NoData' and item != 'PwrFail' and item != '---' and item != 'InVld':
          sum += float(item)
          count += 1
    if count:
      avg = sum/count
    average.append(avg)

  return average

def avg_aqi_years(years):
  avgs = []
  for year in years:
    avgs.append(avg_aqi(year))

  return avgs

if __name__=='__main__':
  averages = avg_aqi_years([2013, 2014, 2015, 2016, 2017, 2018])
  plt.plot(range(0,365), averages[0], label='2013 AQI')
  plt.plot(range(0,364), averages[1], label='2014 AQI')
  plt.plot(range(0,365), averages[2], label='2015 AQI')
  plt.savefig('dynamic/aqi.png')