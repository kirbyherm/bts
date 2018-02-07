from lxml import html
#from mechanize import Browser
from bs4 import BeautifulSoup
import requests
from time import sleep
from tqdm import tqdm
import sys

def get_recent(soup,filename,playerID):
  table = soup.findAll('table')
  try:
    recent_table = table[2]
    for row in recent_table.findAll('tr')[1:]:
      col = row.findAll('td')
      rowname = col[0].string
      AB = int(col[1].string)
      R = int(col[2].string)
      H = int(col[3].string)
      doub = int(col[4].string)
      trip = int(col[5].string)
      HR = int(col[6].string)
      RBI = int(col[7].string)
      BB = int(col[8].string)
      AVG = float(col[9].string)
    
      total = (rowname,str(AB),str(R),str(H),str(doub),str(trip),str(HR),str(RBI),str(BB),str(AVG))
    file1 = open(filename,'a')
    file1.write(str(playerID))
    file1.write('\n')
    file1.close()
  except:
    return 0

  return 1
  header=0 
  i = 0
# for col in recent_table.findAll('th')[1:]:
#   header[i] = col.string
#   i = i+1  
  


def loop_recent():
  filename = ('/home/khermans/Documents/bts/test.txt')
  total = 0
#  bar = progressbar.ProgressBar(maxval=29999,\
#    widgets=[progressbar.Bar('#','[',']'),' ',progressbar.Percentage()])
#  bar.start()
  for x in tqdm(range(int(sys.argv[1]),int(sys.argv[2]))):
#  for x in tqdm(range(1,3000)):
    playerID = x
    playerpage = 'http://www.espn.com/mlb/player/_/id/'+str(x)
    page = requests.get(playerpage)
    soup = BeautifulSoup(page.content,'html.parser')
    y = get_recent(soup,filename,playerID)
#    print(x,'|',y)
    total = total + y
#    bar.update(x)
#    sleep(0.1)
#  bar.finish()
  print(total)


loop_recent()
