#!/usr/bin/env python3

from lxml import html
#from mechanize import Browser
from bs4 import BeautifulSoup
import requests
from time import sleep
from tqdm import tqdm
import sys
import numpy as np
import pandas as pd
from probables import probables
import warnings
warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning)
sys.setrecursionlimit(2000)

default_DIR = '/home/khermans/code/bts/'
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

def get_name(soup,playerID):
  print(soup)

def get_text_only(soup):
  col = soup.findAll('td')
  return_text = []
  for i in range(len(col)):
    return_text.append(col[i].string) 
  return return_text

def get_text_only_header(soup):
  col = soup.findAll('th')
  return_text = []
  for i in range(len(col)):
    return_text.append(col[i].string) 
  return return_text


def check_log(soup,playerID):

  today = pd.Timestamp(pd.Timestamp.today().year,pd.Timestamp.today().month,pd.Timestamp.today().day)
  divs = soup.find_all('div', {'class': "Table__Title"})
  good_log = 0
  try:
    year = int(divs[0].string.split()[0])
  except:
    good_log = 1
    return good_log
  if year < today.year:
    good_log = 2
    return good_log
  table = soup.findAll('table')
  if len(table) > 0:
      name_table = table[0]
      name_table_rows = name_table.findAll('tr')
  else:
    good_log = 3
    return good_log

  return good_log

def check_splits(soup,playerID):

  good_splits = 0
  table = soup.findAll('table')
  if len(table) > 1:
    name_table = table[0]
    stat_table = table[1]
    name_table_rows = name_table.findAll('tr')
    stat_table_rows = stat_table.findAll('tr')
  else:
    good_splits=1
    return good_splits

  assert len(name_table_rows) == len(stat_table_rows), "tables should have same number of rows, instead name_table = {}, stat_table = {}".format(len(name_table_rows), len(stat_table_rows))

  fixed_stat_name = get_text_only(stat_table_rows[0])
  if 'ERA' in fixed_stat_name:
    good_splits=2
    return good_splits
  teamname = soup.find("a", {"class":"AnchorLink clr-black"})
  if teamname ==None:
    good_splits=3
    return good_splits
  status = soup.find("span", {"class":"TextStatus"}).string
  if status ==None:
    good_splits=4
    return good_splits
  return good_splits


def get_log(df,soup,playerID):

  today = pd.Timestamp(pd.Timestamp.today().year,pd.Timestamp.today().month,pd.Timestamp.today().day)
  divs = soup.find_all('div', {'class': "Table__Title"})
  name = str(soup.find("meta", {"property":"og:title"})['content'])
  fullname = name[:name.index('Stat')-1]
  dateID = int(today.year*1e9 + today.month*1e7 + today.day*1e5)
  rowID = dateID + int(playerID)
  year = int(divs[0].string.split()[0])
  table = soup.findAll('table')
  name_table = table[0]
  name_table_rows = name_table.findAll('tr')

  rowname = []
  fixed_stat_name = get_text_only_header(name_table_rows[0])
  colname = []
  stat = []
  hitbool = False
  for i in range(len(name_table_rows)):
    if i > 1: 
      break
    col = get_text_only_header(name_table_rows[i])
    name_table_cols = get_text_only(name_table_rows[i])
    for j in range(len(name_table_cols)): 
      if j == fixed_stat_name.index('H'):
        if name_table_cols[j] != 'H':
          if int(name_table_cols[j]) > 0:
            hitbool = True
      elif j == fixed_stat_name.index('Date'):
        if name_table_cols[j] != 'Date':
          last_game = name_table_cols[j].strip().split()
#          print(last_game)
          last_game_date = pd.Timestamp(today.year, int(last_game[1].split("/")[0]), int(last_game[1].split("/")[1]))
#          print(last_game_date)
      else:
        continue
  yesterday = today - pd.Timedelta('1d')
  dateID = int(yesterday.year*1e9 + yesterday.month*1e7 + yesterday.day*1e5)
  rowID = dateID + int(playerID)
  if (today - last_game_date).round('1d') == pd.Timedelta('1d'): 
    if (rowID in df.index):
      df.at[rowID,'played']=True
      df.at[rowID, 'hitbool']=hitbool
#    df.at[rowID, 'playerID'] = int(playerID)

  return df 

def get_splits(df,df_probables,soup,playerID):

  table = soup.findAll('table')
#  print(table)
  if len(table) > 1:
    name_table = table[0]
    stat_table = table[1]
    name_table_rows = name_table.findAll('tr')
    stat_table_rows = stat_table.findAll('tr')

  rowname = []
  fixed_stat_name = get_text_only(stat_table_rows[0])
  colname = []
  stat = []
#  print(fixed_stat_name)
  for i in range(len(name_table_rows)):
    col = get_text_only(name_table_rows[i])
    rown = (col[0].strip()) 
#    print(rown)
    bad_chars = [' ',',','-','#','/','.']
    for char in bad_chars:
      rown = rown.replace(char,'')
#    print(rown)
    rowname.append(rown)
    stat_table_cols = get_text_only(stat_table_rows[i])
    for j in range(len(stat_table_cols)): 
      if j == fixed_stat_name.index('H'):
        if stat_table_cols[j] != 'H':
          colname.append("{}_{}".format(rowname[-1], 'H'))
          stat.append(int(stat_table_cols[j]))
      elif j == fixed_stat_name.index('AVG'):
        if stat_table_cols[j] != 'AVG':
          colname.append("{}_{}".format(rowname[-1], 'AVG'))
          stat.append(float(stat_table_cols[j]))
      else:
        continue
  stat = np.array(stat)        
#  stat = np.append(stat, np.zeros(len(stat)))
  stat = stat.reshape((1,len(colname)))
#  print(stat)
  name = str(soup.find("meta", {"property":"og:title"})['content'])
  status = str(soup.find("span", {"class":"TextStatus"}).string)
#  print(status)
  teamname = str(soup.find("a", {"class":"AnchorLink clr-black"}).string)
  teamname = team_dict[teamname]
#  print(teamname)
  fullname = name[:name.index('Stat')-1]
#  print(fullname)
  today = pd.Timestamp(pd.Timestamp.today().year,pd.Timestamp.today().month,pd.Timestamp.today().day)
  dateID = int(today.year*1e9 + today.month*1e7 + today.day*1e5)
  rowID = dateID + int(playerID)
  temp_df = pd.DataFrame(stat, columns = colname, index=[rowID])
  if df.shape[0] == 0:
    df = pd.DataFrame(stat, columns = colname, index=[rowID])
  temp_df['Name'] = fullname
  temp_df['Date'] = today
  temp_df['played'] = False
  temp_df['playerID'] = playerID 
  temp_df['hitbool'] = False
  temp_df['status'] = status
  new_cols = []
  for i in range(df_probables.shape[1]):
#      print(df_probables.columns[i], df_probables.loc[df_probables['Team']==teamname])
      if df_probables.columns[i] in df.columns:
          temp_df[df_probables.columns[i]] = df_probables.at[df_probables.index[df_probables['Team'] == teamname][0],df_probables.columns[i]]
      else:
          new_cols.append(df_probables.columns[i])
#      try:
#        temp_df[df_probables.columns[i]] = df_probables.at[df_probables.index[df_probables['Team'] == teamname][0],df_probables.columns[i]]
#      except:
#        temp_df[df_probables.columns[i]] = np.nan
  temp_df = temp_df.loc[:,~temp_df.columns.duplicated()].copy()
#  print(df, temp_df.loc[rowID,:])
#  print(df.loc[~df.index.duplicated(keep='first')], temp_df.loc[~temp_df.index.duplicated(keep='first')])
#  print(df.loc[~df.index.duplicated(keep='last')], temp_df.loc[~temp_df.index.duplicated(keep='last')])
#  df = df.loc[~df.index.duplicated(keep='first')]
#  temp_df = temp_df.loc[~temp_df.index.duplicated(keep='first')]
  df.loc[rowID] = temp_df.loc[rowID, :]#, ignore_index=True)
  if len(new_cols) > 0:
      for i in range(len(new_cols)):
          df.loc[rowID, new_cols[i]] = temp_df.loc[rowID, new_cols[i]]
#  df = pd.join([df, temp_df])#, ignore_index=True)

  return df 

def get_all(df,df_probables,playerID):

    playersplits = 'http://www.espn.com/mlb/player/splits/_/id/'+playerID
    playerlog = 'http://www.espn.com/mlb/player/gamelog/_/id/'+playerID
    pagesplits = None
    soupsplits = None
    pagelog = None
    souplog = None
    good_log = 0
    good_splits=0

    try:
        pagesplits = requests.get(playersplits)
        soupsplits = BeautifulSoup(pagesplits.content,'html.parser')
        pagelog = requests.get(playerlog)
        souplog = BeautifulSoup(pagelog.content,'html.parser')
        good_splits = check_splits(soupsplits,playerID) 
        good_log = check_log(souplog,playerID) 
    except:
        print("{} ID error, log = {}, splits = {}".format(playerID,good_log,good_splits))
        return df 
    if(good_log + good_splits >0):
        print("{} ID error, log = {}, splits = {}".format(playerID,good_log,good_splits))
        return df 
#    print(playerID, good_log, good_splits)
    df = get_splits(df,df_probables,soupsplits,playerID)
    df.fillna(0,inplace=True)
    df = get_log(df,souplog,playerID)
    return df

def scrape_new():

  total = 0
  subset = []
  playertotallist = []  
  df_probables = probables()

#  with open('test.txt','r') as f:
#    for line in f:
#      subset.append(str(line).strip())
#
#  for i in range(int(subset[-1]),44000):
#    subset.append(str(i))
#  
#  for x in tqdm(range(int(sys.argv[1]),int(sys.argv[2]))):
#  for x in tqdm(range(1,3000)):
#  subset = ['28841']
#  df = pd.DataFrame()
  success = False
  yesterday = pd.Timestamp(pd.Timestamp.today().year,pd.Timestamp.today().month,pd.Timestamp.today().day) - pd.Timedelta('1d')
#  yesterday = pd.Timestamp(2022, 9, 26)
  dateID = int(yesterday.year*1e9 + yesterday.month*1e7 + yesterday.day*1e5)
  df = pd.read_hdf('{}{}.h5_proc.h5'.format(default_DIR,dateID))
#  df = pd.read_hdf('2022092600000.h5_proc.h5')
#  df["Date"] = yesterday
#  df = pd.DataFrame() 
  uniqueID = (df.playerID.unique())
  for i in range(len(uniqueID)):
    try:
      subset.append(int(uniqueID[i]))
    except:
      continue
#  print(uniqueID, len(uniqueID), subset)
  i = 0
  for x in tqdm(subset):
#  for x in subset:
    playerID = str(x)
#    if (playerID == str(39572)):
    if df.shape[0] == 0:    
        df = get_all(df,df_probables,playerID)
    else:
        df = get_all(df,df_probables,playerID)
    
  today = pd.Timestamp.today()
  dateID = int(today.year*1e9 + today.month*1e7 + today.day*1e5)
  df.to_hdf("{}{}.h5".format(default_DIR,dateID), key='df')
#  print(df)
  return "{}{}.h5".format(default_DIR,dateID)

def main():
    scrape_new()

if __name__ == "__main__":
    main()
