from lxml import html


def get_recent(soup):
  table = soup.findAll('table')
  recent_table = table[2]
  header=0 
  i = 0
# for col in recent_table.findAll('th')[1:]:
#   header[i] = col.string
#   i = i+1  
  
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
    print(str.join('|',total))

