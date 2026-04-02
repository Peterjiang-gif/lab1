import os 
import re
filewrite=open('CIs_output.txt','a')
sites=[]
with open('wan_CIs.txt','r') as output:
     for line in output: 
         if 'target-sites' in line:
            res=line.split(':')
            re=res[1].split('\n')
            info=re[0].split(',')
            if len(info)>int(0):
               for i in range(0,len(info)):
                   sites.append(info[i])
output.close


with open('wan_CIs.txt','r') as output:    
     for line in output:
        if 'target-sites' not in line:  
           if len(sites)>int(0):
              for i in range(0,len(sites)):
                  if sites[i] in line:
                     filewrite.write(line)                  
output.close 
filewrite.close()                     