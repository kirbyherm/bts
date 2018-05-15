#!/usr/bin/env python3.6

from lxml import html
#from mechanize import Browser
from bs4 import BeautifulSoup
import requests
from time import sleep
from tqdm import tqdm
import sys
import numpy as np
import h5py


def get_name(soup,filename,playerID):
  print(soup)

def get_recent(soup,filename,playerID):

  table = soup.findAll('table')
#  try:
  recent_table = table[2]
  rowname = []
  AB = []
  R = []
  H = []
  doub = []
  trip = []
  HR = []
  RBI = []
  BB = []
  AVG = []

  for row in recent_table.findAll('tr')[1:]:
    col = row.findAll('td')
    rowname.append(col[0].string)
    AB.append(int(col[1].string))
    R.append(int(col[2].string))
    H.append(int(col[3].string))
    doub.append(int(col[4].string))
    trip.append(int(col[5].string))
    HR.append(int(col[6].string))
    RBI.append(int(col[7].string))
    BB.append(int(col[8].string))
    AVG.append(float(col[9].string))
 
 
    total = (rowname,str(AB),str(R),str(H),str(doub),str(trip),str(HR),str(RBI),str(BB),str(AVG))
#     x = np.array([(AB),(R),(H),(doub),(trip),(HR),(RBI),(BB)],np.dtype('uint32',8))
#     x.dtype
#     hf = h5py.File('data.h5','w')
#     hf.create_dataset('rosario', data=x)
#     hf.close()

    if (playerID == str(31944)):
      print(total)
#    file1 = open(filename,'a')
#    file1.write(str(playerID))
#    file1.write('\n')
#    file1.close()
  name = soup.find("meta", {"property":"og:title"})['content']
  total = [name,rowname,AB,R,H,doub,trip,HR,RBI,BB,AVG]
#  except:
#    return 0

  return total
  header=0 
  i = 0
# for col in recent_table.findAll('th')[1:]:
#   header[i] = col.string
#   i = i+1  
  


def loop_recent():
  filename = ('/home/khermans/Documents/bts/test.txt')
  total = 0
  subset = []
  playertotallist = []  

  with open('test.txt','r') as f:
    for line in f:
      subset.append(str(line).strip())

  
#  for x in tqdm(range(int(sys.argv[1]),int(sys.argv[2]))):
#  for x in tqdm(range(1,3000)):
  for x in tqdm(subset):
    playerID = x
    if (playerID == str(31944)):
      playerpage = 'http://www.espn.com/mlb/player/_/id/'+x
      page = requests.get(playerpage)
      soup = BeautifulSoup(page.content,'html.parser')
      playertotal = get_recent(soup,filename,playerID)
  #    print(x,'|',y)
#      if(name != 0):
#        total = total + 1
#      else:
#        total = total
      playertotallist.append(playertotal)

  names = []
  sd_avgs = []
  m_avgs = []
  home_away_avgs = []  


  print(playertotallist)
  hf = h5py.File('data.h5','w')
  hf.close()
  
#    bar.update(x)
#    sleep(0.1)
#  bar.finish()
#  print(total)

#   with open('test2.txt','w') as g:
#     for x in range(len(subset)):
#       g.write(str(namelist[x]) + ' ' + str(subset[x])+'\n')
#   

loop_recent()
