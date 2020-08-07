import os
import sys
import requests
import time
from constants import get_path

def scrape_climate_data():
  path = get_path()
  for year in range(2013, 2019):
    for month in range(1, 13):
      if month < 10:
        url = 'https://en.tutiempo.net/climate/0{}-{}/ws-421820.html'.format(month, year)
      else:
        url = 'https://en.tutiempo.net/climate/{}-{}/ws-421820.html'.format(month, year)

      data = requests.get(url)
      data_utf = data.text.encode('utf=8')

      if not os.path.exists('{}/assets/climate-data/{}'.format(path,year)):
        os.makedirs('{}/assets/climate-data/{}'.format(path,year))

      with open('{}/assets/climate-data/{}/{}.html'.format(path,year, month), 'wb') as result:
        result.write(data_utf)

      sys.stdout.flush()

if __name__ == '__main__':
  start = time.time()
  scrape_climate_data()
  end = time.time()

  print('Time taken = {}'.format(end-start))