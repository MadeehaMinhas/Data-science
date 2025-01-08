import json
from docplex.mp.model import Model
from datetime import datetime

f = open('data.json')
file_contents=json.load(f)

m = Model(name='Airport traffic optimization')
x=[]
wait=[]
for i in range(0,len(file_contents)):
  x.append(m.binary_var(name='node'))   #path exists for a segment/route at a given time
  wait.append(m.binary_var(name='wait'))







no={}
d={}
nodes=[]
times=[]
segments=[]
for file in file_contents:
  node=file['Segment'].split('->')
  time=file['Start_Time']
  
  if time not in times:
    times.append(time)
   
    no[time]=[node[0]]
    

  else:
   
    no[time].append(node[0])
    

    
no
n=[]
for k,v in no.items():
  c=1
  for i in range(0,len(v)-1):
   
    for j in range(i+1,len(v)):
      if v[i]==v[j]:
        print(v[i],v[j])
        c=c+1
        
      
  n.append(c)
  print(n)

no





#Constraints
#2.link occupancy
lo={}
d={}
nodes=[]
flights=[]
segments=[]
for file in file_contents:
  node=file['Segment'].split('->')
  flight=file['Flight']
  
  if flight not in flights:
    flights.append(flight)
   
    lo[flight]=[node[0]]
    

  else:
   
    lo[flight].append(node[0])
    

print(lo)   
l=[]

for k,v in lo.items():
  c=1
  for i in range(0,len(v)-1):
   
    for j in range(i+1,len(v)):
      if v[i]==v[j]:
        print(v[i],v[j])
        c=c+1
        
      
  l.append(c)

lo



# Route and delay choice
ro={}
for file in file_contents:
  if file['Route']!='':
    if file['Delay (min)']>=0:
      ro[file['Route']]=1
    else:
      ro[file['Route']]=0
  else:
    ro[file['Route']]=0



wo=[]
delay=[]
filght=[]
for i in range(0,len(file_contents)-1):
  for j in range(1, len(file_contents)):
    if file_contents[i]['Flight']==file_contents[j]['Flight']:
      res=2**file_contents[j]['Delay (min)']-2**file_contents[i]['Delay (min)']
      d1=0
      d2=0
      for di in range(0,file_contents[i]['Delay (min)']):
        d1+=2**di*wait[j]
      for dj in range(0,file_contents[j]['Delay (min)']):
          d2+=2**dj*wait[j]
      res=res-d1-d2
      wo.append(res)




#Objective function

datetime2=[]
for file in file_contents:
  date_string=file['Start_Time']
  datetime2.append( datetime.strptime(date_string, '%H:%M:%S') )

datetime1=[]
for file in file_contents:
  date_string=file['Dest_time']
  datetime1.append( datetime.strptime(date_string, '%H:%M:%S') )
time=[]
for i in range(0,len(datetime1)):
  time.append((datetime1[i]-datetime2[i]).total_seconds()/3600)
time

delay=[]
for file in file_contents:
  delay.append(file['Delay (min)'])

for i in range(0,len(n)):
    m.add_constraint(n[i]*x[i]<=1)
for i in range(0,len(l)):
    m.add_constraint(l[i]*x[i]<=1)

for file in file_contents:
  m.add_constraint(ro[file['Route']]==1 )

for w in wo:
  m.add_constraint(w==0 )
for i in range(0,len(time)):
  m.maximize((time[i]+delay[i])*x[i] )
m.print_information()
s = m.solve()
m.print_solution()
for i in x:
  print(i.solution_value)


