#!/opt/intel/oneapi/intelpython/latest/bin/python

from lxml import html
#from mechanize import Browser
from bs4 import BeautifulSoup
import requests
from time import sleep
from tqdm import tqdm
import sys
import numpy as np
import pandas as pd

team_dict = [
    "Yankees",
    "Blue Jays",
    "Rays",
    "Orioles",
    "Red Sox",
    "Twins",
    "Guardians",
    "White Sox",
    "Royals",
    "Tigers",
    "Astros",
    "Mariners",
    "Rangers",
    "Angels",
    "Athletics",
    "Mets",
    "Braves",
    "Phillies",
    "Marlins",
    "Nationals",
    "Brewers",
    "Cardinals",
    "Cubs",
    "Reds",
    "Pirates",
    "Dodgers",
    "Padres",
    "Giants",
    "Rockies",
    "D-backs"
]

def probables():

    probables = 'http://www.mlb.com/probable-pitchers'
    pageprobables = requests.get(probables)
    soupprobables = BeautifulSoup(pageprobables.content,'html.parser')
    divs = soupprobables.find_all('div', {'class': "probable-pitchers__container"})
    games = soupprobables.find_all('div', {'class': "probable-pitchers__game"})
    pitchers = soupprobables.find_all('div', {'class': "probable-pitchers__pitchers"})
    df = pd.DataFrame()
    for i in range(len(games)):
        home_playing = True
        away_playing = True
        gametime = pd.Timestamp(games[i].find('div',{'class':'probable-pitchers__game-date-time'}).time['datetime']) - pd.Timedelta('4h')
        if (gametime.hour > 17):
            gametime = 'Night'
        else:
            gametime = 'Day'
        # Away
        field = str(games[i].find('div',{'class':'probable-pitchers__game-location'}).string.strip()[3:]) 
        bad_chars = [' ',',','-','#','/','.']
        for char in bad_chars:
          field = field.replace(char,'')
        away_team = str(games[i].find('span',{'class':'probable-pitchers__team-name--away'}).string.strip()) 
        try:
            away_pitcher_name = (pitchers[i].find_all('div',{'class':'probable-pitchers__pitcher-name'}))[0].string.strip()
        except:
            away_pitcher_name = (pitchers[i].find_all('a',{'class':'probable-pitchers__pitcher-name-link'}))[0].string.strip()
        if away_pitcher_name == "TBD":
            away_playing=False
            away_pitcher_hand = False
            away_pitcher_era = float(5.00)
        else:
            away_pitcher_hand = (pitchers[i].find_all('span',{'class':'probable-pitchers__pitcher-pitch-hand'}))[0].string.strip()
            if away_pitcher_hand == "RHP":
                away_pitcher_hand = False
            elif away_pitcher_hand == "LHP":
                away_pitcher_hand = True
            else:
                print(away_pitcher_hand)
            try:
                away_pitcher_era = float((pitchers[i].find_all('span',{'class':'probable-pitchers__pitcher-era'}))[0].string.strip().split()[0])
            except:
                away_pitcher_era = float(5.00)
        home_team = str(games[i].find('span',{'class':'probable-pitchers__team-name--home'}).string.strip()) 
        try:
            home_pitcher_name = (pitchers[i].find_all('div',{'class':'probable-pitchers__pitcher-name'}))[1].string.strip()
        except:
            home_pitcher_name = (pitchers[i].find_all('a',{'class':'probable-pitchers__pitcher-name-link'}))[-1].string.strip()
        if home_pitcher_name == "TBD":
            home_playing=False
            home_pitcher_hand = False
            home_pitcher_era = float(5.00)
        else:
            home_pitcher_hand = str((pitchers[i].find_all('span',{'class':'probable-pitchers__pitcher-pitch-hand'}))[-1].string.strip())
            if home_pitcher_hand == "RHP":
                home_pitcher_hand = False
            elif home_pitcher_hand == "LHP":
                home_pitcher_hand = True
            else:
                print(home_pitcher_hand)
            try:
                home_pitcher_era = float((pitchers[i].find_all('span',{'class':'probable-pitchers__pitcher-era'}))[-1].string.strip().split()[0])
            except:
                home_pitcher_era = float(5.00)
        print(gametime, field, away_team, away_pitcher_hand, away_pitcher_era)
        print(gametime, field, home_team, home_pitcher_hand, home_pitcher_era)
        df_temp = pd.DataFrame({"Team":pd.Series([away_team,home_team]), "Home":pd.Series([False,True]), "Opponent":pd.Series([home_team,away_team]), "Field":pd.Series([field,field]), "GameTime":pd.Series([gametime,gametime]), "PitcherLeftHand":pd.Series([home_pitcher_hand,away_pitcher_hand]), "PitcherERA":pd.Series([home_pitcher_era,away_pitcher_era]), "Playing":pd.Series([home_playing,away_playing])})
#        df_temp = df_temp.append({"Team":home_team, "Home":True, "Opponent":away_team, "Field":field, "GameTime":gametime, "PitcherLeftHand":away_pitcher_hand, "PitcherERA":away_pitcher_era},ignore_index=True)
        df = df.append(df_temp,ignore_index=True)
    print(df)
    for j in range(len(team_dict)):
        df_temp = pd.DataFrame({"Team":pd.Series([team_dict[j]]), "Home":pd.Series([True]), "Opponent":pd.Series([team_dict[j]]), "Field":pd.Series([field]), "GameTime":pd.Series(['Night']), "PitcherLeftHand":pd.Series([False]), "PitcherERA":pd.Series([0.0]), "Playing":pd.Series([False])})
        if df.loc[df["Team"]==team_dict[j]].shape[0]==0:
            df = df.append(df_temp,ignore_index=True)
    print(df)
    return df
    

def main():
    df = probables()
    print(df)

if __name__ == "__main__":
    main()
