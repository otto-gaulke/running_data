import os
import pandas as pd
import tcxreader as tr

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('..')
host_files = os.listdir(os.getcwd())

if 'parse_history.txt' not in host_files:
  with open('parse_history.txt', 'w') as parse_write:
    pass

with open('parse_history.txt', 'r') as parse_read:
  parsed_files = parse_read.read().splitlines()

cols = ['date', 'time', 'latitude', 'longitude',
        'elevation_meters', 'distance_meters', 'heart_rate']

if 'running_data.csv' not in host_files:
  df = pd.DataFrame(columns=cols)
else:
  df = pd.read_csv('running_data.csv')

os.chdir(os.getcwd() + '\\tcx')
tcx_files = os.listdir(os.getcwd())

files_parse = [x for x in tcx_files if x not in parsed_files and x[-4:] == '.tcx']

for parse in files_parse:
  data = tr.TCXReader().read(parse)
  trackpoints = data.trackpoints

  date = []
  time = []
  latitude = []
  longitude = []
  elevation_m = []
  distance_m = []
  hr = []

  for point in trackpoints:
    date.append(str(point.time)[:10])
    time.append(str(point.time)[11:19])
    latitude.append(point.latitude)
    longitude.append(point.longitude)
    elevation_m.append(point.elevation)
    distance_m.append(point.distance)
    hr.append(point.hr_value)

  elevation_ft = [x * 3.28084 for x in elevation_m]
  distance_ft = [x * 3.28084 for x in distance_m]
  distance_mi = [x * 0.000621371 for x in distance_m]

x = 1
