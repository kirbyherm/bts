#!/usr/bin/env python

#from mechanize import Browser
from time import sleep
from tqdm import tqdm
import sys
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score
from sklearn.model_selection import cross_val_score, GridSearchCV
import warnings
warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

layers = []

for i in range(0,11):
    for j in range(7,12):
        if i == 0:
            layers.append((j,))
        elif i < j:
            layers.append((j, i))
print(layers)
parameters = {"hidden_layer_sizes":layers}

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
        return 5.00

def loop_recent(filename):
  subset = []
  playertotallist = []  
  features = ['pitcher_ERA','AllSplits_H','homeaway_H','hand_H','Last7Days_H','Last15Days_H','Last30Days_H','daynight_H','AllSplits_AVG','homeaway_AVG','hand_AVG','Last7Days_AVG','Last15Days_AVG','Last30Days_AVG','daynight_AVG']
#  features = features[:8]
  today = pd.Timestamp(pd.Timestamp.today().year,pd.Timestamp.today().month,pd.Timestamp.today().day)
#  today = today - pd.Timedelta('1d')
  dateID = int(today.year*1e9 + today.month*1e7 + today.day*1e5)
#  df = pd.read_hdf('{}.h5'.format(dateID))
  df = pd.read_hdf(filename)
  print(df.index.duplicated)
  df['PitcherERA'] = df['PitcherERA'].apply(lambda x: make_float(x))
  df_orig = df.copy()
  df['pitcher_ERA'] = df['PitcherERA'].apply(lambda x: make_float(x))
#  df['hand_H'] = 0
  df.loc[df['PitcherLeftHand'] == True, 'hand_H'] = df['vsLeft_H']
  df.loc[df['PitcherLeftHand'] == False, 'hand_H'] = df['vsRight_H']
  df['homeaway_H'] = 0
  df.loc[df['GameTime'] == 'Day', 'homeaway_H'] = df['Day_H']
  df.loc[df['GameTime'] == 'Night', 'homeaway_H'] = df['Night_H']
  df['daynight_H'] = 0
  df.loc[df['Home'] == True, 'daynight_H'] = df['Home_H']
  df.loc[df['Home'] == False, 'daynight_H'] = df['Away_H']
  df['hand_AVG'] = 0
  df.loc[df['PitcherLeftHand'] == True, 'hand_AVG'] = df['vsLeft_AVG']
  df.loc[df['PitcherLeftHand'] == False, 'hand_AVG'] = df['vsRight_AVG']
  df['homeaway_AVG'] = 0
  df.loc[df['Home'] == True, 'homeaway_AVG'] = df['Home_AVG']
  df.loc[df['Home'] == False, 'homeaway_AVG'] = df['Away_AVG']
  df['daynight_AVG'] = 0
  df.loc[df['GameTime'] == 'Day', 'daynight_AVG'] = df['Day_AVG']
  df.loc[df['GameTime'] == 'Night', 'daynight_AVG'] = df['Night_AVG']
  df['hit'] = 0
  df.loc[df['hitbool'] == True, 'hit'] = 1
#  print(df_train)
  df_played_count = (df.loc[(df['status'] == "Active") & (df['Playing']==True) & (df['played']==True) & (df['Date']<today)]).fillna(0)
  df_played_count = df_played_count.groupby(['playerID']).sum()['played']
  print(df_played_count)
  df.drop(['played_count'])
  df =df.join(df_played_count,'playerID',rsuffix='_count')
  print(df[['played_count','played']])
  df_train = (df.loc[(df['status'] == "Active") & (df['Playing']==True) & (df['played']==True) & (df['Date']<today) & (df.played_count>(df.played_count.max()*0.3)),features]).fillna(0)
#  print(df_train)
  X = np.array(df_train)
  y = np.array((df.loc[(df['status'] == 'Active') & (df['Playing']==True) & (df['played']==True) & (df['Date']<today) & (df.played_count>(df.played_count.max()*0.3)), 'hit'])).reshape((len(X),))
  df1 = df_train[df_train.isna().any(axis=1)]
  scaler = StandardScaler()
  X = scaler.fit_transform(X)
#  print(pd.DataFrame(X),pd.DataFrame(y))
#  print(np.sum(y))
  clf = MLPClassifier(
                solver='lbfgs', 
                    alpha=1e-5,
                    hidden_layer_sizes=(8,), 
                    random_state=1,
                    max_iter=int(1e5))
  clf.fit(X,y)
#  grid = GridSearchCV(clf, parameters)
#  grid.fit(X,y)
#  print(grid.best_index_, grid.best_score_)
#  clf = MLPClassifier(
#                solver='lbfgs', 
#                    alpha=1e-5,
#                    hidden_layer_sizes=layers[grid.best_index_], 
#                    random_state=1,
#                    max_iter=int(1e5))
#  clf.fit(X,y)
#  print(grid.cv_results_)
#  print(cross_val_score(clf, X, y, cv=4, scoring='precision'))
  predictions_train = clf.predict(X)
  predictions_proba = clf.predict_proba(X)[:,1].reshape((X.shape[0],1))
  df_train['predict_proba'] = clf.predict_proba(X)[:,1].reshape((X.shape[0],1))
#  print(df_train.sort_values(by='predict_proba'))
  y_weights = np.zeros((len(y),))
  for i in range(y.shape[0]):
    if predictions_proba[i] > 0.6:
      y_weights[i] = 1
  train_score = precision_score(y, predictions_train)
  print(train_score)
#  print(today)
#  print(np.sum(clf.predict(X)))
  X = np.array(df.loc[(df['status'] == 'Active') & (df['Playing']==True) & (df['Date']==today) & (df.played_count>(df.played_count.max()*0.3)),features].fillna(0))
  y = np.array(df.loc[(df['status'] == 'Active') & (df['Playing']==True) & (df['Date']==today) & (df.played_count>(df.played_count.max()*0.3)),'hit'])
#  print(X,y)
  X = scaler.fit_transform(X)
  clf.predict(X)
#  print(clf.predict_proba(X)[:,1])
  df['predict_hit'] = 0
  df_predict = df.loc[(df['status'] == 'Active') & (df['Playing']==True) & (df['Date']==today) & (df.played_count>(df.played_count.max()*0.3))]
#  print(df_predict.shape, clf.predict_proba(X)[:,1].shape)
  df_predict.loc[(df_predict['status'] == 'Active') & (df_predict['Playing']==True) & (df_predict['Date']==today), 'predict_hit'] = (clf.predict_proba(X)[:,1]).reshape((df_predict.shape[0],1))
#  print(df_predict.sort_values(by=['predict_hit'], ascending=False)[['Name','predict_hit','Team']])
#  df_orig['predict_hit'] = 0
#  df_orig['predict_hit_proba'] = 0
  df_orig.loc[(df['status'] == 'Active') & (df['Playing']==True) & (df['Date']==today) & (df.played_count>(df.played_count.max()*0.3)), 'predict_hit'] = df_predict['predict_hit'].sort_values(ascending=False).rank(method='first',ascending=False)
  df_orig.loc[(df['status'] == 'Active') & (df['Playing']==True) & (df['Date']==today) & (df.played_count>(df.played_count.max()*0.3)), 'predict_hit_proba'] = df_predict['predict_hit']
#  print(df_orig.sort_values(by='predict_hit'))
  df_orig =df_orig.join(df_played_count,'playerID',rsuffix='_count')
  df_orig = df_orig.fillna(0)
  df_orig.to_hdf('{}_proc.h5'.format(dateID),key='df')
  print(df_orig.loc[(df_orig.predict_hit>0) & (df_orig.predict_hit<10),['Name','Date','Team','predict_hit','predict_hit_proba','hitbool','Last7Days_AVG','Last15Days_AVG','Last30Days_AVG']].sort_values(by=['Date','predict_hit']))
  print(df_orig.loc[(df_orig.predict_hit>0) & (df_orig.predict_hit<3) & (df_orig.Date < today),['hitbool']].sum()/df_orig.loc[(df_orig.predict_hit>0) & (df_orig.predict_hit<3) & (df_orig.Date < today)].shape[0])

def main():
    script, filename = sys.argv
    loop_recent(filename)

if __name__ == "__main__":
    main()
