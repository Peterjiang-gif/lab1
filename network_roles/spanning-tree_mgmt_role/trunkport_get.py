from datetime import datetime
import os 
import re

switch_name=[]
with open('siteswitch_name.txt','r') as output:
     for line in output: 
         re=line.split() 
         if len(re)>int(0): 
            switch_name.append(re[0])
output.close 
re=[]
vlan_access_collect=[]
vlan_trunk_collect=[]
filewrite=open('trunkport_info.csv','a')
if len(switch_name)>int(0):
  for i in range(0,len(switch_name)):
     
     device_name=i
     trunk_int=[]
     port_channel=[]
     vlan_port_info=[]
     extra_con_int=[]
     start_flag="false"
     sub_start_flag="false"
     end_flag="false"
     section_flag="false"
     interface_store=""
     port_channel_int=[]
     trunk_config_port=[]
     access_up_port=[]
     with open(switch_name[i]+'_csw_vlan_brief.txt','r') as output:   
       vlan_id=""
       vlan_port=""     
       for line in output:
         if 'active' in line or 'ACTIVE' in line: 
             re=line.split()
             if len(re)>int(1):
                if re[0]=="vlan" or re[0]=="VLAN" or re[0]=="Vlan":
                   if vlan_id!="":
                      vlan_value=vlan_id+":"+vlan_port
                      vlan_port_info.append(vlan_value)                        
                   vlan_id=re[1]
                   vlan_port=""
                   if 'active' in line: 
                      info=line.split('active')
                      if len(info)>int(1):
                         info[1]=info[1].strip()
                         info[1]=info[1].strip('\n')
                         vlan_port=vlan_port+info[1]
                         
                   if 'ACTIVE' in line: 
                      info=line.split('ACTIVE')
                      if len(info)>int(1):
                         info[1]=info[1].strip()
                         info[1]=info[1].strip('\n')
                         vlan_port=vlan_port+info[1]
                      
                else:
                      
                        if 'vlan' in re[0]:
                           re[0]=re[0].strip('vlan')
                        if 'VLAN' in re[0]:
                           re[0]=re[0].strip('VLAN')                     
                        if 'Vlan' in re[0]:
                           re[0]=re[0].strip('Vlan')            
                        if 'vl' in re[0]:
                           re[0]=re[0].strip('vl')
                        if 'Vl' in re[0]:
                           re[0]=re[0].strip('Vl')
                        if vlan_id!="":
                          
                           vlan_value=vlan_id+":"+vlan_port
                           vlan_port_info.append(vlan_value)                        
                        vlan_id=re[0]
                        vlan_port=""
                        if 'active' in line: 
                          info=line.split('active')
                          if len(info)>int(1):
                             info[1]=info[1].strip()
                             info[1]=info[1].strip('\n')
                             vlan_port=vlan_port+info[1] 
                         
                        if 'ACTIVE' in line: 
                           info=line.split('ACTIVE')
                           if len(info)>int(1):
                              info[1]=info[1].strip()
                              info[1]=info[1].strip('\n') 
                              vlan_port=vlan_port+info[1]
                              
                              
         if 'active' not in line and 'ACTIVE' not in line: 
            if 'Te' in line or 'te' in line or 'Gi' in line or 'gi' in line or 'Fa' in line or 'fa' in line or 'Eth' in line or 'eth' in line: 
               line=line.strip('\n')  
               line=line.strip()   
               vlan_port=vlan_port+","+line        
       if vlan_id!="":
          vlan_value=vlan_id+":"+vlan_port
          vlan_port_info.append(vlan_value)
     output.close
        
     #print(vlan_port_info)
     Le=len(vlan_port_info)
     
     
     
     start_flag="false" 
     with open(switch_name[i]+'_switch_int_config.txt','r') as output:
        for line in output: 
            if start_flag=="ture":
               if 'channel-group' in line: 
                  re=line.split()
                  if len(re)>int(1) and re[0]=="channel-group": 
                     Va="interface "+interface+" in port channel-group "+re[1]
                     port_channel_int.append(Va)
               if 'switchport mode trunk' in line: 
                  re=line.split()
                  if len(re)==int(3):
                     trunk_config_port.append(interface)
            if 'interface' in line: 
               re=line.split()
               if len(re)==int(2) and re[0]=="interface":
                  start_flag="ture"
                  if re[1]!="":
                     interface=re[1]      
     output.close                    
     #print("port-channel info:")
     #print(port_channel_int)
     
     #print("trunk ports:")
     #print(trunk_config_port)
     
     
     
    
     vlan_up_count=[] 
     #show_value="vlan24 up port:"
     Leng=len(vlan_port_info)
     if Leng>int(0): 
      for j in range (0,Leng):
       up_num="0"
       
       record=vlan_port_info[j].split(':')
       if len(record)>int(1) and record[0]!="": 
          v_id=record[0]
          trunkp_con=switch_name[i]+":"
          accessp_con=switch_name[i]+":"
          show_value="vlan"+record[0]+" up port:"
          if ',' in record[1]:
             info=record[1].split(',')
             L=len(info)
             for k in range (0,L):
                 info[k]=info[k].strip()
                
                 with open (switch_name[i]+'_switch_interface_status.txt','r') as out:
                      for queue in out:
                          if info[k] in queue:
                             result=queue.split()
                             if len(result)>int(4):
                                if result[0]==info[k] and result[4]=="up":
                                   up_num=str(int(up_num)+int(1))     
                                   show_value=show_value+info[k]+","
                 out.close                  
          if ',' not in record[1]:
             record[1]=record[1].strip()
             with open (switch_name[i]+'_switch_interface_status.txt','r') as out:
                  for queue in out:
                      if record[1] in queue:
                         result=queue.split()
                         if len(result)>int(4):
                            if result[0]==record[1] and result[4]=="up":
                               up_num=str(int(up_num)+int(1)) 
                               show_value=show_value+record[1]                             
          Va=record[0]+"_"+up_num
          vlan_up_count.append(Va)
          vlan_re=show_value.split(':') 
          if vlan_re[1]!="":
             vlan_va=vlan_re[1].split(',')
             num=len(vlan_va)
             for k in range(0,num):
                 trunk_num=len(trunk_config_port)
                 w_flag="ture"
                 for l in range(0,trunk_num):
                     if 'Te' in trunk_config_port[l] and 'gab' in trunk_config_port[l]:
                         trunk_config_port[l]=trunk_config_port[l].replace('TenGigabitEthernet','Te') 
                     if 'Gi' in trunk_config_port[l] and 'gab' in trunk_config_port[l]:
                         trunk_config_port[l]=trunk_config_port[l].replace('GigabitEthernet','Gi')  
                     if 'Fa' in trunk_config_port[l] and 'eth' in trunk_config_port[l]:
                         trunk_config_port[l]=trunk_config_port[l].replace('Fastethernet','Fa')
                     if 'Eth' in trunk_config_port[l] and 'ernet' in trunk_config_port[l]:
                         trunk_config_port[l]=trunk_config_port[l].replace('Ethernet','Eth')   
                     if trunk_config_port[l]==vlan_va[k] or 'Po' in vlan_va[k] or 'po' in vlan_va[k]:
                        w_flag="false"
                 if w_flag=="ture":
                    if vlan_va[k]!="":
                       access_up_port.append(vlan_va[k])
                       accessp_con=accessp_con+"_"+vlan_va[k]
                 if w_flag=="false":
                    if vlan_va[k]!="":
                       trunkp_con=trunkp_con+"_"+vlan_va[k] 
                  
          leng=len(vlan_access_collect)
          if leng==int(0):
             content=v_id+","+accessp_con
             vlan_access_collect.append(content)
          if leng>int(0):
             Flag="false"
             num_re=""
             for l in range(0,leng):
                 sep=vlan_access_collect[l].split(',')
                 if sep[0]!="" and sep[0]==v_id:
                    Flag="ture"
                    num_re=str(l)
             if Flag=="ture":
                vlan_access_collect[int(num_re)]=vlan_access_collect[int(num_re)]+","+accessp_con
             if Flag=="false":
                content=v_id+","+accessp_con
                vlan_access_collect.append(content)
          leng=len(vlan_trunk_collect)
          if leng==int(0):
             content=v_id+","+trunkp_con
             vlan_trunk_collect.append(content)
          if leng>int(0):
             Flag="false"
             num_re=""
             for l in range(0,leng):
                 sep=vlan_trunk_collect[l].split(',')
                 if sep[0]!="" and sep[0]==v_id:
                    Flag="ture"
                    num_re=str(l)
             if Flag=="ture":
                vlan_trunk_collect[int(num_re)]=vlan_trunk_collect[int(num_re)]+","+trunkp_con
             if Flag=="false":
                content=v_id+","+trunkp_con
                vlan_trunk_collect.append(content)

#filewrite.write("vlan collect information:")
#filewrite.write("\n")
if len(switch_name)>int(0):
   #filewrite.write("note:")
   filewrite.write(" ,")
   for i in range(0,len(switch_name)):
       filewrite.write(switch_name[i]+",")
   filewrite.write("\n")
#filewrite.write("\n")
#filewrite.write("vlans access ports:")
#filewrite.write("\n") 
for i in range(0,len(vlan_trunk_collect)): 
    filewrite.write(vlan_trunk_collect[i]+",")   
    filewrite.write("\n")  
filewrite.write("\n") 
  
