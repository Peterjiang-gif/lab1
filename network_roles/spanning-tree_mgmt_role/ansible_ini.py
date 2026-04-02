from datetime import datetime
import os 
import re

filewrite=open('cellular_inventory.txt','a')
with open('device_ip.txt','r') as output: 
     for line in output: 
         res=line.split()
         if len(res)==int(2):
            value=res[0]+" ansible_host="+res[1]
            filewrite.write(value)
            filewrite.write('\n')
output.close
filewrite.close()
            