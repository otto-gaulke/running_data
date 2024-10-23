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
  parsed_files = parse_read.read().split(',')

del parsed_files[0]

cols = ['date', 'time', 'latitude', 'longitude',
        'elevation_meters', 'elevation_feet', 'elevation_change_feet',
        'distance_meters', 'distance_feet', 'distance_miles', 'heart_rate']

if 'running_data.csv' not in host_files:
  df = pd.DataFrame(columns=cols)
else:
  df = pd.read_csv('running_data.csv')

os.chdir(os.getcwd() + '\\tcx')
tcx_files = os.listdir(os.getcwd())

files_parse = [x for x in tcx_files if x not in parsed_files and x[-4:] == '.tcx']

for parse in files_parse:
  print(f'Processing {parse}...')
  
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

  elevation_ft_delta = []

  for index, item in enumerate(elevation_ft):
    if index == 0:
      elevation_ft_delta.append(0.000)
    else:
      elevation_ft_delta.append(elevation_ft[index] - elevation_ft[index - 1])

  data_set = {'date': date, 'time': time, 'latitude': latitude, 'longitude': longitude,
              'elevation_meters': elevation_m, 'elevation_feet': elevation_ft, 'elevation_change_feet': elevation_ft_delta,
              'distance_meters': distance_m, 'distance_feet': distance_ft, 'distance_miles': distance_mi, 'heart_rate': hr}

  df_temp = pd.DataFrame(data_set)

  df = pd.concat([df, df_temp])

os.chdir('..')

df['date'] = pd.to_datetime(df['date'])
df['time'] = pd.to_timedelta(df['time'])

df = df.sort_values(by=['date', 'time'], ignore_index=False)

df.to_csv('running_data.csv', index=False)

parsed_files_string = ''

for file in files_parse:
  parsed_files_string += ',' + file

with open('parse_history.txt', 'a') as f:
  f.write(parsed_files_string)
