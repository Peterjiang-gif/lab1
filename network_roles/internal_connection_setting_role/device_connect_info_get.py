from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from datetime import datetime

index=[]
device=[]
device_flag=[]
command=[]
with open('index.txt','r') as files:
  for line in files:
      if line!='':
         line=line.strip()
         result=line.split(',') 
         index.append(result[1])
         device.append(result[0])
files.close()

with open('command.txt','r') as files:
     for line in files:
         
            command.append(line)
files.close()  

filewrite=open('device_connect_info.txt','w')
device_connect_list=[]
record_device=[]
n=len(device)
for i in range (0,n): 

    start_word=device[i]+":"
    end_word=device[i]+" end"
    sub_start_word_one="show lldp neighbor"
    sub_start_word_two=command[1]
    sub_start_word_three="show vlan brief"
    start_flag="false"
    sub_start_flag="false"
    to_nei_dev_list=[]
    local_int_to_nei_list=[]
    nei_dev_con_int=""
    result=""
    record_nei_dev_judge_key="ture"
    local_nei_device_judge="ture"
    num=len(device)
    from_device_exist_judge="false"
    to_device_exist_judge="false"
    filewrite.write(device[i]+' local neighbor connection information:'+'\n')
    filewrite.write('if there is no content under a device local neighbor connection information, it means there is no local neighbor device connect to this device  ')
    filewrite.write('\n')
    with open('config_ini.txt','r') as f:
         
         for line in f:
             from_device_exist_judge="false"
             to_device_exist_judge="false"
             record_nei_dev_judge_key="ture"
             local_nei_device_judge="ture"
             if end_word in line :
                start_flag="false"
                
             if start_flag=="ture":
                
                if sub_start_flag=="ture":
                   result=line.split()
                  
                   m=len(to_nei_dev_list)  
                   for j in range(0,len(device)):
                       if result[0]==device[j]:
                          local_nei_device_judge="false"                   
                   if result[0]=="DeviceID" or result[0]=="show" or result[0]=="": 
                      record_nei_dev_judge_key="false"
                   for j in range(0,m): 
                        if to_nei_dev_list[j]==result[1]:               
                            local_nei_device_judge="false"   
                   if record_nei_dev_judge_key=="ture":
                      to_nei_dev_list.append(result[1])
                      
                      
                      if local_nei_device_judge=="ture":
                         filewrite.write(device[i]+' int '+result[1]+' to '+result[0]+' int '+result[4]+'\n')

                      else:
                                
                              m=len(record_device)
                              for j in range(0,m):
                                  if record_device[j]==device[i]: 
                                     from_device_exist_judge="ture"
                              if from_device_exist_judge=="false": 
                                 record_device.append(device[i])
                              for j in range(0,m):
                                  if record_device[j]==result[0]: 
                                     to_device_exist_judge="ture"
                              if to_device_exist_judge=="false": 
                                 record_device.append(result[0])  
                              if from_device_exist_judge=="false" or to_device_exist_judge=="false": 
                                 var=device[i]+" int "+result[1]+" to "+result[0]+" int "+result[4]
                                
                                 device_connect_list.append(var)                             
                if sub_start_word_one in line:   
                   sub_start_flag="ture" 
                                   
                if sub_start_word_three in line:
                   sub_start_flag="false"
                                   
             if start_word in line: 
                start_flag="ture"
                
              
    f.close()
    
filewrite.write('network device connect information:'+'\n' )  
m=len(device_connect_list)
for i in range(0,m):
     filewrite.write(device_connect_list[i]+'\n')
filewrite.close()  