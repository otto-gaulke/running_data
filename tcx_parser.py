import os
import pandas as pd
import tcxreader as tr

os.chdir(os.path.dirname(os.path.abspath(__file__)))
files = os.listdir(os.getcwd())

if 'parse_history.txt' not in files:
  with open('parse_history.txt', 'w') as f:
    pass

with open('parsed_history.txt', 'r') as f:
  parsed_files = f.read().splitlines()

files_parse = [x for x in files if x not in parsed_files and x[-4:] == '.tcx']

if 'running_data.csv' not in files:
  df_empty = pd.DataFrame()
  pd.to_csv('running_data.csv', index=False)

df = pd.read_csv('running_data.csv')

for parse in files_parse:
  data = tr.TCXReader(parse).read()

  for workout in data.workouts():
    for track in workout.track:
      for point in track.track_points:
        
