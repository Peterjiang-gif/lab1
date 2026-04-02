from datetime import datetime
import os 
import re
filewrite=open('wan_output.txt','a')
device=[]
filename=[]
for file in os.listdir():
    if file.endswith(".txt"):
       if 'wan_info' in file:
          rec=file.split('_')
          filename.append(file)
          device.append(rec[0])
m=len(filename)
if m>int(0):
  for i in range(0,m):
      store=[]
      bandw=""
      RT=""
      NRT=""      
      with open(filename[i],'r') as output:
           for line in output: 
               store.append(line)
      output.close
      if len(store)>int(0):
          for l in range(0,len(store)):
              if 'shape (average)' in store[l]:
                 re=store[l].split()
                 if len(re)>int(3):
                    if ',' in re[3]:
                       n=len(re[3])
                       bandw=re[3][:n-1]
                    else:
                       bandw=re[3]
              if '-RT' in store[l] and '-NRT' not in store[l]: 
                  cir_flag="false"
                  if l+int(1)<len(store):
                     if 'cir' in store[l+1] and '%' in store[l+1]:
                        cir_flag="ture"
                        re=store[l+1].split()  
                        if len(re)>int(2):
                           RT=re[1]+re[2] 
                                                     
                  if l+int(2)<len(store):
                     if 'cir' in store[l+2] and '%' in store[l+2]:
                        cir_flag="ture"
                        re=store[l+2].split()  
                        if len(re)>int(2):
                           RT=re[1]+re[2] 
                           
                  if cir_flag=="false":
                     if l+int(1)<len(store):
                        if 'Priority' in store[l+1] and '%' in store[l+1]:
                           re=store[l+1].split()
                           if len(re)>int(1):
                              RT=re[1]  
                             
                     if l+int(2)<len(store):
                        if 'Priority' in store[l+2] and '%' in store[l+2]:
                           re=store[l+2].split()
                           if len(re)>int(1):
                              RT=re[1]  
                                                           
              if '-NRT' in store[l]: 
                  cir_flag="false"
                  if l+int(1)<len(store):
                     if 'cir' in store[l+1] and '%' in store[l+1]:
                        cir_flag="ture"
                        re=store[l+1].split()  
                        if len(re)>int(2):
                           NRT=re[1]+re[2]   
                  if l+int(2)<len(store):
                     if 'cir' in store[l+2] and '%' in store[l+2]:
                        cir_flag="ture"
                        re=store[l+2].split()  
                        if len(re)>int(2):
                           NRT=re[1]+re[2] 
                  if cir_flag=="false":
                     if l+int(1)<len(store):
                        if 'Priority' in store[l+1] and '%' in store[l+1]:
                           re=store[l+1].split()
                           if len(re)>int(1):
                              NRT=re[1]  
                     if l+int(2)<len(store):
                        if 'Priority' in store[l+2] and '%' in store[l+2]:
                           re=store[l+2].split()
                           if len(re)>int(1):
                              NRT=re[1]            
                             
      filewrite.write(device[i]+" "+bandw+" "+RT+" "+NRT) 
      filewrite.write('\n')  
  filewrite.close()      
                 