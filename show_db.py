#!/usr/bin/env python3

#from mechanize import Browser
from time import sleep
from tqdm import tqdm
import sys
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
team_dict = {
    "New York Yankees": "Yankees",
    "Toronto Blue Jays": "Blue Jays",
    "Tampa Bay Rays": "Rays",
    "Baltimore Orioles": "Orioles",
    "Boston Red Sox": "Red Sox",
    "Minnesota Twins": "Twins",
    "Cleveland Guardians": "Guardians",
    "Chicago White Sox": "White Sox",
    "Kansas City Royals": "Royals",
    "Detroit Tigers": "Tigers",
    "Houston Astros": "Astros",
    "Seattle Mariners": "Mariners",
    "Texas Rangers": "Rangers",
    "Los Angeles Angels": "Angels",
    "Oakland Athletics": "Athletics",
    "New York Mets": "Mets",
    "Atlanta Braves": "Braves",
    "Philadelphia Phillies": "Phillies",
    "Miami Marlins": "Marlins",
    "Washington Nationals": "Nationals",
    "Milwaukee Brewers": "Brewers",
    "St. Louis Cardinals": "Cardinals",
    "Chicago Cubs": "Cubs",
    "Cincinnati Reds": "Reds",
    "Pittsburgh Pirates": "Pirates",
    "Los Angeles Dodgers": "Dodgers",
    "San Diego Padres": "Padres",
    "San Francisco Giants": "Giants",
    "Colorado Rockies": "Rockies",
    "Arizona Diamondbacks": "D-backs"
}

def make_float(x):
    try: 
        return float(x)
    except:
        return 0

def loop_recent(filename,playername):
  subset = []
  playertotallist = []  
  features = ['AllSplits_H','homeaway_H','hand_H','AllSplits_AVG','homeaway_AVG','hand_AVG','pitcher_ERA','Last7Days_H','Last15Days_H','Last30Days_H','Last7Days_AVG','Last15Days_AVG','Last30Days_AVG','daynight_H','daynight_AVG']
  features = features[:-2]
  today = pd.Timestamp(pd.Timestamp.today().year,pd.Timestamp.today().month,pd.Timestamp.today().day)
  today = today - pd.Timedelta('1d')
  dateID = int(today.year*1e9 + today.month*1e7 + today.day*1e5)
#  df = pd.read_hdf('{}.h5'.format(dateID))
  df = pd.read_hdf(filename)
  df_orig = df.copy()
  print(df.loc[df.Name==playername])
  df['PitcherERA'].apply(lambda x : make_float(x))
#  print(df.sort_values(by='PitcherERA', ascending=False))

def main():
    script, filename, playername = sys.argv
    loop_recent(filename, playername)

if __name__ == "__main__":
    main()
