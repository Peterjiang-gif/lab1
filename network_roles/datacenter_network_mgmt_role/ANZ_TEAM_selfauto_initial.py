from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from datetime import datetime
import os 
import re


         
voice_site_switch=[]
voice_site_router=[]
filewrite=open('check_output_detail.txt','a')
with open ('voice_site_device_info.txt','r') as files: 
   for line in files: 
     result=line.split()
     res=result[0].split('-')
     m=len(res)
     for i in range(0,m): 
       if i==(m-int(2)): 
          if res[i]=="r" or res[i]=="R":
             voice_site_router.append(result[0]+"_"+result[1])
          if res[i]=="sw" or res[i]=="csw" or res[i]=="CSW" or res[i]=="dsw" or res[i]=="DSW" or res[i]=="core" or res[i]=="ss" or res[i]=="bs": #extend switch identify
             voice_site_switch.append(result[0]+"_"+result[1])     
files.close

m=len(voice_site_switch)
n=len(voice_site_router)  

switch_eigrp_num=""
switch_vlan_info=[]
vlan_no=""
device_name=""
csw_group=[]
vlan_in_csw=""
vlan_layer3_csw=[]
lay2to3_flag="false"
switch_output="" 
with open('ini_info.txt','r') as output: 
     for line in output: 
        if 'device' in line:      
            re=line.split() 
            if len(re)>int(1): 
               device_name=re[1]
        if 'vlan_id' in line: 
           re=line.split() 
           if len(re)> int(1): 
              vlan_no=re[1]
output.close    
if 'CORE' in device_name or 'core' in device_name or 'CSW' in device_name or 'csw' in device_name: 
   vlan_in_csw=device_name  


for i in range(0,m):  
    res=voice_site_switch[i].split('_')
    csw_log=res[0]+":"
    protocol_set="false"
    site_switch_check="false"
    vlan=[]
    with open(res[0]+'_switch_ip_des.txt','r') as output:  
      for line in output:    
          result=line.split()
          if len(result)>3: 
             le=len(result)
             for k in range(0,le): 
                 if '-R' in result[k] or '-r' in result[k]: 
                    if 'm-' in result[k] or 'M-' in result[k]: 
                       if 'cs' in res[0] or 'CS' in res[0] or 'core' in res[0] or 'CORE' in res[0]:
                          site_switch_check="ture"            
    output.close
   
    if site_switch_check=="ture": 
          csw_group.append(res[0])
          filewrite.write("\n")
          filewrite.write("\n")
          filewrite.write(res[0]+" layer 3 info:")
          with open(res[0]+'_switch_eigrp_a.txt','r') as output: 
            router_eigrp_flag="false"
            for line in output:
                result=line.split()
                if 'router eigrp' in line:
                   if len(result)>int(2) and result[2]!="":                
                      router_eigrp_flag="ture"
                      csw_log=csw_log+"has eigrp running "+"and"
                   if switch_eigrp_num=="":
                      switch_eigrp_num=result[2]
                   if switch_eigrp_num!="":
                      if switch_eigrp_num!=result[2]: 
                         csw_log=csw_log+"eigrp num may be incorrect should be "+switch_eigrp_num+"and" 
            if router_eigrp_flag=="ture":
               protocol_set="ture"            
          output.close                    
        
          vlan_name=[]
          
          with open(res[0]+'_csw_vlan_brief.txt','r') as output:          
            for line in output: 
              if line!=''or line!="/n": 
                 line=line.strip()
                 if 'active' in line:
                     result=line.split()
                     if len(result)>int(1):
                        if result[0]=="vlan":
                           if result[2]=="active":
                              vlan_name.append(result[1])
                              
                           else:
                                result[1]=result[1].strip('vl')
                                value=result[1]+"+"+result[2]
                                vlan_name.append(value)
                        if result[0]!="vlan" and result[0]!="VLAN" and result[0]!="Vlan":
                           result[0]=result[0].strip('vl')
                           value=result[0]+"+"+result[1]
                           vlan_name.append(value)
                                   
                 else:
                      if '/' not in line and 'access port' not in line and 'Po' not in line and '-' not in line:
                         result=line.split()
                         if len(result)>int(0):
                            if result[0]=="vlan": 
                               if len(result)==int(2):                     
                                  vlan_name.append(result[1])
                                 
                               if len(result)>int(2):
                                  result[2]=result[2].strip('(')
                                  result[2]=result[2].strip(')')
                                  value=result[1]+"+"+result[2]
                                  vlan_name.append(value)
                                 
                            else:
                               if len(result)==int(1):
                                  result[0]=result[0].strip('vl')
                                  vlan_name.append(result[0]) 
                                  
                                                            
                               if len(result)>int(1): 
                                  result[0]=result[0].strip('vl')
                                  result[1]=result[1].strip('(')
                                  result[1]=result[1].strip(')')
                                  value=result[0]+"+"+result[1]
                                  vlan_name.append(value)
                                 
          output.close 
          l=len(vlan_name)
          for j in range(0,l):
            if '(' in vlan_name[j]:
               value=re.sub(r"\([^()]*\)", "",vlan_name[j])
               n=len(value)
               result=vlan_name[j][n:]
               result=result.strip('(')
               result=result.strip(')')
               vlan.append(value)
            if '+' in vlan_name[j]: 
               result=vlan_name[j].split('+')
               vlan.append(result[0])   
          svi_vlan=[]
          local_eigrp_vlan=[] 
          local_eigrp_vlan_value=""
          l=len(vlan)
          for j in range(0,l):        
             eigrp_vlan="false"  
             interface_store=""        
             with open(res[0]+'_switch_int_config.txt','r') as output:  
              vrf_flag="false"
              vlan_ip="no-ip"
              eigrp_vlan_in="false"
              vlan_info=""
              start_flag="false"
              shutdown_flag="false"
              for line in output: 
                if start_flag=="ture":
                
                  result=line.split()
                  if 'ip address' in line and len(result)>int(2): 
                    vlan_ip=result[2]
                    vlan_layer3="ture"
                    csw_log=csw_log+"has vlan "+vlan[j]+"SVI "+"and"
                    Va=vlan[j]+"+"+result[2]
                    eigrp_vlan="ture"  
                  if 'ip vrf forwarding' in line and result[3]!="": 
                     vrf_flag="ture"
                     csw_log=csw_log+"vlan "+vlan[j]+" set vrf "+result[3]+" and"
                  if 'shutdown' in line and 'no' not in line and interface_store==vlan[j]:
                     if Va!="":
                        Va=Va+"+"+"shutdown"
                        svi_vlan.append(Va)
                        shutdown_flag="ture"
                  if 'interface' in line: 
                        re=line.split()
                        if len(re)==int(2) and re[0]=="interface":
                           if Va!="":
                              if shutdown_flag=="false": 
                                 Va=Va+"+"+"up"
                                 svi_vlan.append(Va) 
                           start_flag="false"    
                           interface_store=""  
                           Va=""      
                if 'interface' in line and vlan[j] in line: 
                     re=line.split()
                     if len(re)==int(2):
                        if re[1]=="Vlan"+vlan[j]:
                           start_flag="ture" 
                           interface_store=vlan[j]
                           Va=""
             output.close  
          
          #print(svi_vlan)
          Leng=len(svi_vlan)
          for j in range(0,Leng):
              record=svi_vlan[j].split('+')
              eigrp_exist_flag=""
              if record[1]!="":
                 if '/' in record[1]:
                    sub_record=record[1].split('/')
                    if len(sub_record)>int(0):
                       if sub_record[0]!="":
                          record[1]=sub_record[0]
                 eigrp_exist_flag="false"
                 with open(res[0]+'_switch_eigrp_a.txt','r') as output: 
                    for line in output:
                       if 'network' in line: 
                          re=line.split()
                          if len(re)==int(3) and re[0]=="network":
                             network=[]
                             mask=[]
                             vlanip=[]
                             com_start_flag="false"
                             sub_re=re[1].split('.') 
                             l=len(sub_re)
                             for k in range(0,l):
                                 network.append(sub_re[k])
                             sub_re=re[2].split('.')
                             l=len(sub_re)
                             for k in range(0,l):
                                 Va=int(255)-int(sub_re[k])
                                 mask.append(str(Va))
                             sub_re=record[1].split('.')
                             l=len(sub_re)
                             for k in range(0,l):
                                 vlanip.append(sub_re[k])
                             if len(network)==int(4) and len(mask)==int(4) and len(vlanip)==int(4):
                                com_start_flag="ture"
                                sec_com_flag="ture"
                                l=len(network)
                                for k in range(0,l):
                                    if (int(network[k])&int(mask[k]))!=(int(vlanip[k])&int(mask[k])):
                                       sec_com_flag="false"
                             if com_start_flag=="ture" and sec_com_flag=="ture": 
                                eigrp_exist_flag="ture"

                 output.close 
                 
                 vlan_info="vlan"+record[0]+"+"+"in eigrp network "+eigrp_exist_flag
                 local_eigrp_vlan.append(vlan_info)
                 q=len(switch_vlan_info) 
                 if(int(q)>int(0)):
                    count_flag="false"
                    for k in range (0,q): 
                        info=switch_vlan_info[k].split('+') 
                        if info[0]=="vlan"+record[0]:
                           count_flag="ture"
                           if info[1]=="false": 
                              if eigrp_exist_flag=="ture":
                                 switch_vlan_info[k]=vlan_info
                    if count_flag=="false": 
                       switch_vlan_info.append(vlan_info)  
                 else: 
                       switch_vlan_info.append(vlan_info) 
          value=""                     
          for n in range(0,len(local_eigrp_vlan)):
              value=value+local_eigrp_vlan[n]+", "   
          filewrite.write("\n")             
          filewrite.write("svi vlan in layer 3:"+"\n")
          filewrite.write(value)
          for l in range(0,len(local_eigrp_vlan)):
              if vlan_no in local_eigrp_vlan[l] and 'ture' in local_eigrp_vlan[l]:
                 vlan_layer3_csw.append(res[0])
          r_con_int=[]
          r_con_int_back=[]
      
          with open(res[0]+'_switch_ip_des.txt','r')as output:
            start_flag="false"
            end_flag="false" 
            count="false"
            for line in output: 
          
             if start_flag=="ture": 
               Info=line.split()
                           
               if '--------' in line and endready_flag=="false": 
                 
                 if count=="ture":
                    start_flag="false"
                 if count=="false":
                    count="ture"  
               if '--------' in line and endready_flag=="ture": 
                  start_flag="false"
                  count="false"
               if '--------' not in line:
                    
                    endready_flag="ture"
                    
                       
                    if '-cs' in line or '-core-' in line or '-dsw-' in line or '-sw' in line or '-r'in line or '-R' in line:
                 #condition define                           
                                                             
                                                             line=line.strip()
                                                             result=line.split()
                                                             l=len(result)
                                                             for k in range(0,l):
                                                                  if 'm-anz-' in result[k] or 'M-ANZ-' in result[k] or 'm-sgt-' in result[k] or 'M-SGT-' in result[k] : 
                                                                       R=result[k].split('-')
                                                                       L=len(R)
                                                                       if 'r' in R[L-1] or 'R' in R[L-1]:
                                                                          value=result[0]+"(to "+result[k]+")"
                                                                          r_con_int.append(value)
                                                                          r_con_int_back.append(result[0])
                                                                       if 'r' in R[L-2] or 'R' in R[L-2]:
                                                                          value=result[0]+"(to "+result[k]+")"
                                                                          r_con_int.append(value)
                                                                          r_con_int_back.append(result[0]) 
                                                  
             if 'Port' in line and 'Type' in line and 'Speed' in line and 'Description' in line:
                 start_flag="ture"
                 endready_flag="false"
                 count="false"
             if 'port' in line and 'type' in line and 'speed' in line and 'description' in line:
                 start_flag="ture"
                 endready_flag="false"
                 count="false"
             if 'interface' in line and 'status' in line and 'protocol' in line and 'description' in line: 
                 start_flag="ture"
                 endready_flag="false"
                 count="false" 
             if 'Interface' in line and 'Status' in line and 'Protocol' in line and 'Description' in line: 
                 start_flag="ture"
                 endready_flag="false"
                 count="false"      
          output.close
          value=""                     
          for n in range(0,len(r_con_int)):
              value=value+r_con_int[n]+", " 
          filewrite.write("\n")              
          filewrite.write("router connected interface in switch:"+"\n")
          filewrite.write(value)
             #print(r_con_int_back)
             
          csw_layer3_con=[] 
          Leng=len(r_con_int)                        
          for j in range(0,Leng):
             r_con_int  
             with open(res[0]+'_switch_int_config.txt','r') as output: 
                  start_flag=="false"
                  switch_flag="false"
                  for line in output: 
                      if start_flag=="ture":
                         if 'switchport mode trunk' in line:
                             switch_flag="ture"
                         if 'switchport trunk allowed' in line and switch_flag=="ture": 
                             Va=r_con_int[j]+': '+"traffic to router:"+line+' ' 
                             csw_layer3_con.append(Va)
                         if 'ip address' in line and switch_flag=="false": 
                             record=line.split()
                             if len(record)>int(2) and record[2]!="": 
                                exist_flag="false"
                                with open('eigrp_int.txt','r') as info:
                                     for queue in info: 
                                         if r_con_int_back[j] in queue:
                                            sub_re=queue.split()
                                            if len(sub_re)>int(0):
                                               if sub_re[0]==r_con_int_back[j]:
                                                  exist_flag="ture"
                                if exist_flag=="ture": 
                                   Va=r_con_int[j]+': '+"traffic to router: the interface is ip interface to connected router , interface in eigrp"
                                   csw_layer3_con.append(Va)
                                if exist_flag=="false": 
                                   Va=r_con_int[j]+': '+"traffic to router: the interface is ip interface to connected router , interface not in eigrp"    
                                   csw_layer3_con.append(Va)

                         if 'interface' in line: 
                             re=line.split()
                             if len(re)==int(2) and re[0]=="interface": 
                                start_flag="false"
                      if 'interface' in line:
                         if r_con_int_back[j].replace('Eth','Ethernet') in line or r_con_int_back[j].replace('Gi','GigabitEthernet') in line or r_con_int_back[j].replace('Fa','Fastethernet')in line or r_con_int_back[j].replace('Te','TenGigabitEthernet')in line:
                           
                            re=line.split()
                            if len(re)==int(2):
                               start_flag="ture"
          value=""                     
          for n in range(0,len(csw_layer3_con)):
              value=value+csw_layer3_con[n]+", "
          filewrite.write("\n")
          filewrite.write(value)



          
       
#print("in whole site, svi vlan in layer 3 :") 
#print(switch_vlan_info) 
vlan_in_dsw=[]          
trun_int_in_port_channel_record=[]
vlan_allowed_record=[]             
m=len(voice_site_switch)
for i in range(0,m): 
     res=voice_site_switch[i].split('_') 
     con_int=[]
     con_int_back=[]
     trunk_int=[]
     port_channel=[]
     vlan_allowed=res[0]
     trun_int_in_port_channel=res[0]
     extra_con_int=[]
     start_flag="false"
     sub_start_flag="false"
     end_flag="false"
     section_flag="false"
     interface_store=""
     port_channel_int=[]
     trunk_config_port=[]
     access_up_port=[]
     filewrite.write("\n")
     filewrite.write("\n")
     filewrite.write(res[0]+" layer2 info:")
     
     vlan_result=[] 
     vlan_spa_sum=[]
     with open(res[0]+'_switch_spanning_sum.txt','r') as output: 
       start_flag="false"
       for line in output: 
         if start_flag=="ture":
            if '-----' not in line:
               re=line.split()
               if len(re)>int(2): 
                  if 'vlan' in re[0]:  
                     re[0]=re[0].strip('vlan')
                     re[0]=re[0].lstrip('0') 
                     value=re[0]+"_"+re[4] 
                     vlan_spa_sum.append(value)
                  if 'VLAN' in re[0]: 
                     re[0]=re[0].strip('VLAN')
                     re[0]=re[0].lstrip('0') 
                     value=re[0]+"_"+re[4]
                     vlan_spa_sum.append(value)
                  if 'Vlan' in re[0]:
                     re[0]=re[0].strip('Vlan')
                     re[0]=re[0].lstrip('0') 
                     value=re[0]+"_"+re[4]
                     vlan_spa_sum.append(value)
                               
         if 'Block' in line and 'Listen' in line and 'Forward' in line: 
            start_flag="ture"
         if 'block' in line and 'listen' in line and 'forward' in line: 
            start_flag="ture"   
            
     output.close 
     #print(vlan_spa_sum)
     vlan_port_info=[]
     with open(res[0]+'_csw_vlan_brief.txt','r') as output:   
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
     with open(res[0]+'_switch_int_config.txt','r') as output:
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
     show_value="vlan24 up port:"
     Leng=len(vlan_port_info)
     if Leng>int(0): 
      for j in range (0,Leng):
       up_num="0"
       record=vlan_port_info[j].split(':')
       if len(record)>int(1) and record[0]=="24": 
          if ',' in record[1]:
             info=record[1].split(',')
             L=len(info)
             for k in range (0,L):
                 info[k]=info[k].strip()
                
                 with open (res[0]+'_switch_interface_status.txt','r') as out:
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
             with open (res[0]+'_switch_interface_status.txt','r') as out:
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
     value=""                     
     for n in range(0,len(access_up_port)):
         value=value+access_up_port[n]+", "
     filewrite.write("\n")         
     filewrite.write("vlan 24 up access port:") 
     filewrite.write(value)    
     #print(vlan_up_count) 
     #print(show_value)
     if len(vlan_up_count)>int(0):
        find_flag="false" 
        record=vlan_up_count[0].split('_')
        if record[0]=="24": 
          Le=len(vlan_spa_sum)     
          for k in range(0,Le): 
              com_vlan=vlan_spa_sum[k].split('_')  
              if com_vlan[0]==record[0]:
                 find_flag="ture"
                 if int(record[1])>int(com_vlan[1]): 
                    Num=len(vlan_port_info)
                    
                    Va="vlan"+record[0]+"'s access port may has spanning-tree block issue"+"("+show_value+")"
                    
                    vlan_result.append(Va)  
                 if int(record[1])==int(com_vlan[1]) or int(record[1])<int(com_vlan[1]):
                    Va="vlan"+record[0]+"'s access port has no spanning-tree block issue"
                    vlan_result.append(Va)
          if find_flag=="false":
             
             Va="vlan"+result[0]+"'s access port may has spanning-tree block issue"+"("+show_value+")"
             vlan_result.append(Va)  
        #print("refered vlan layer 2 spanning-tree traffic:")
        #print(vlan_result)
     
     
     
     
     
     
     
     
     with open(res[0]+'_switch_ip_des.txt','r')as output:
       start_flag="false"
       end_flag="false" 
       count="false"
       for line in output: 
          
           if start_flag=="ture": 
              Info=line.split()
                           
              if '--------' in line and endready_flag=="false": 
                 
                 if count=="ture":
                    start_flag="false"
                 if count=="false":
                    count="ture"  
              if '--------' in line and endready_flag=="ture": 
                 start_flag="false"
                 count="false"
              if '--------' not in line:
                    
                    endready_flag="ture"
                    
                       
                    if '-cs' in line or '-core-' in line or '-dsw-' in line or '-sw' in line or '-ss' in line or '-us' in line or '-bs' in line  or '-CS' in line or '-CORE-' in line or '-DSW-' in line or '-SW' in line or '-SS' in line or '-SS' in line or '-BS' in line:
                 #condition define                           
                                                             
                                                             line=line.strip()
                                                             result=line.split()
                                                             l=len(result)
                                                             for k in range(0,l):
                                                                  if 'm-anz-' in result[k] or 'M-ANZ-' in result[k] or 'm-sgt-' in result[k] or 'M-SGT-' in line : 
                                                                       R=result[k].split('-')
                                                                       L=len(R)
                                                                       if 'CORE' in R[L-1] or 'core' in R[L-1] or 'CS' in R[L-1] or 'cs' in R[L-1] or 'DS' in R[L-1]  or 'ds' in R[L-1]:
                                                                                                           
                                                                            value=result[0]+"(to "+result[k]+")"
                                                                            con_int.append(value)
                                                                            con_int_back.append(result[0])
                                                                       if 'CORE' in R[L-2] or 'core' in R[L-2] or 'CS' in R[L-2] or 'cs' in R[L-2] or 'DS' in R[L-2]  or 'ds' in R[L-2]:
                                                                                                           
                                                                            value=result[0]+"(to "+result[k]+")"
                                                                            con_int.append(value)
                                                                            con_int_back.append(result[0])#write_flag
           if 'Port' in line and 'Type' in line and 'Speed' in line and 'Description' in line:
               start_flag="ture"
               endready_flag="false"
               count="false"
           if 'port' in line and 'type' in line and 'speed' in line and 'description' in line:
               start_flag="ture"
               endready_flag="false"
               count="false"
           if 'interface' in line and 'status' in line and 'protocol' in line and 'description' in line: 
               start_flag="ture"
               endready_flag="false"
               count="false" 
           if 'Interface' in line and 'Status' in line and 'Protocol' in line and 'Description' in line: 
               start_flag="ture"
               endready_flag="false"
               count="false"      
     output.close
    
     #print("switch connect int:")
     #print(con_int_back)
       
     
                        
                        
     with open (res[0]+'_eigrp_int_tru.txt','r') as output: 
      section_flag="false"
      for line in output: 
          if '-------' in line: 
            section_flag="ture"
     output.close
     if section_flag=="false":
         with open (res[0]+'_eigrp_int_tru.txt','r') as output:
           for line in output: 
             result=line.split()#isolate character define 
             if len(result)> int(1):
                if 'Te' in result[0] or 'te' in result[0] or 'Gi' in result[0] or 'gi' in result[0] or 'Fa' in result[0] or 'fa' in result[0] or 'Eth' in result[0] or 'eth' in result[0]:
                    description=""                
                    with open(res[0]+'_switch_ip_des.txt','r') as info: 
                       for queue in info: 
                           if result[0] in queue: 
                              description=queue
                    info.close          
                    value=result[0]+"\n"+"description "+description+"\n"+"allowed vlan="+result[1]
                    if 'CORE' in decription or 'core' in description or 'CSW' in description or 'csw' in description or 'DSW' in description or 'dsw' in description: 
                         vlan_allowed=vlan_allowed+value+"\n"+"\n"
                    if res[0]==device_name and vlan_in_csw=="":
                       for l in range(0,len(csw_group)):
                           if csw_group[l] in description or csw_group[l].replace('CSW','NX-CORE') in description:
                              if '-' in result[1]:  
                                 rec=result[1].split(',')
                                 for m in range(0,len(rec)):
                                     if '-' in rec[m]: 
                                        nums=re[m].split('-')
                                        if len(nums)==int(2):
                                           if int(nums[0])<=int(vlan_no)<=int(nums[1]):
                                              vlan_in_dsw.append(csw_group[l])  
                                     else: 
                                          if vlan_no==rec[m]:
                                             vlan_in_dsw.append(csw_group[l]) 

                              else:
                                   if vlan_no in result[1]:
                                      vlan_in_dsw.append(csw_group[l])                         
                    trunk_int.append(result[0])
                if 'po' in line or 'Po' in line: 
                    description=""                
                    with open(res[0]+'_switch_ip_des.txt','r') as info: 
                       for queue in info: 
                           if result[0] in queue: 
                              description=queue
                    info.close   
                    value=result[0]+" allowed vlan= "+result[1] 
                    if 'CORE' in decription or 'core' in description or 'CSW' in description or 'csw' in description or 'DSW' in description or 'dsw' in description: 
                          vlan_allowed=vlan_allowed+result[0]+"\n"+"description "+description+"allowed vlan="+result[1]+"\n"+"\n"
                     
                    port_channel.append(value) 
         output.close           
     if section_flag=="ture": 
         start_flag="false"
         end_flag="false" 
         sub_start_flag="false"
         with open (res[0]+'_eigrp_int_tru.txt','r') as output:
            for line in output: 
              if start_flag=="ture":           
               if '--------' in line : 
                  end_flag="ture"
                  start_flag="false"
                  sub_start_flag="false"
               if start_flag=="ture" and end_flag=="false":
                  result=line.split()#isolate character define 
                  if len(result)> int(1):
                     if 'Te' in result[0] or 'te' in result[0] or 'Gi' in result[0] or 'gi' in result[0] or 'Fa' in result[0] or 'fa' in result[0] or 'Eth' in result[0] or 'eth' in result[0]:
                       description=""                
                       with open(res[0]+'_switch_ip_des.txt','r') as info: 
                         for queue in info: 
                           if result[0] in queue: 
                              description=queue
                       info.close  
                                              
                       value=result[0]+"\n"+"description "+description+"allowed vlan="+result[1]
                       if 'CORE' in description or 'core' in description or 'CSW' in description or 'csw' in description or 'DSW' in description or 'dsw' in description: 
                          vlan_allowed=vlan_allowed+value+"\n"+"\n" 
                       if res[0]==device_name and vlan_in_csw=="":
                          for l in range(0,len(csw_group)):
                              if csw_group[l] in description or csw_group[l].replace('CSW','NX-CORE') in description:
                                 if '-' in result[1]:  
                                    rec=result[1].split(',')
                                    for m in range(0,len(rec)):
                                        if '-' in rec[m]: 
                                           nums=rec[m].split('-')
                                           
                                           if len(nums)==int(2):
                                             
                                              if int(nums[0])<=int(vlan_no) and int(num)<=int(nums[1]):
                                                 vlan_in_dsw.append(csw_group[l]) 
                                        else: 
                                             if vlan_no==rec[m]:
                                                vlan_in_dsw.append(csw_group[l]) 

                                        
                                 else:
                                      if vlan_no in result[1]:
                                         vlan_in_dsw.append(csw_group[l])      
                       trunk_int.append(result[0])
                     if 'po' in line or 'Po' in line: 
                       description=""                
                       with open(res[0]+'_switch_ip_des.txt','r') as info: 
                         for queue in info: 
                           if result[0] in queue: 
                              description=queue
                       info.close   
                       value=result[0]+" allowed vlan= "+result[1] 
                       if 'CORE' in description or 'core' in description or 'CSW' in description or 'csw' in description or 'DSW' in description or 'dsw' in description: 
                          vlan_allowed=vlan_allowed+result[0]+"\n"+"description "+description+"allowed vlan="+result[1]+"\n"+"\n" 
                        
                       port_channel.append(value) 
              if 'interface allowed vlan' in line or 'Vlans Allowed on Trunk' in line or 'vlans allowed on trunk'in line:
                #condition define 
                  sub_start_flag="ture" 
                  
              if '--------' in line and sub_start_flag=="ture":  
                 start_flag="ture"                   
         output.close 
       
     if vlan_allowed!=res[0]:
        vlan_allowed_record.append(vlan_allowed)
     filewrite.write("\n")   
     filewrite.write("layer 2 trunk info:")
     filewrite.write(vlan_allowed)
     value=""                     
     for n in range(0,len(trunk_int)):
         value=value+trunk_int[n]+", "
     filewrite.write("\n")    
     filewrite.write("trunk physical int:")
     filewrite.write(value)
     #print("trunk port-channel :")
     #print(port_channel)
     l=len(port_channel_int)
     Leng=len(trunk_int)
     for k in range (0,l): 
        flag="false"
        record=port_channel_int[k].split()
        if len(record)>int(1):
           store=record[1]
              
        for o in range(0,Leng): 
            if 'Te' in trunk_int[o] and 'gab' not in trunk_int[o]:
                        trunk_int[o]=trunk_int[o].replace('Te','TenGigabitEthernet') 
            if 'Gi' in trunk_int[o] and 'gab' not in trunk_int[o]:
                        trunk_int[o]=trunk_int[o].replace('Gi','GigabitEthernet')  
            if 'Fa' in trunk_int[o] and 'eth' not in trunk_int[o]:
                        trunk_int[o]=trunk_int[o].replace('Fa','Fastethernet')  
            if 'Eth' in trunk_int[o] and 'ernet' not in trunk_int[o]:
                        trunk_int[o]=trunk_int[o].replace('Eth','Ethernet')
            if trunk_int[o]==store:
               flag="ture"             
        if flag=="false": 
           extra_con_int.append(port_channel_int[k])
        
     l=len(extra_con_int)
     for k in range(0,l): 
         if extra_con_int[k]!="":
            trun_int_in_port_channel=trun_int_in_port_channel+extra_con_int[k]+"\n"
     if trun_int_in_port_channel!=res[0]: 
        trun_int_in_port_channel=trun_int_in_port_channel+"(above info shows "+res[0]+" interface that are not in int trunk record but are in port-channel )"
        trun_int_in_port_channel_record.append(trun_int_in_port_channel)
        #print("trunk interface in port channel extra :")
        #print(trun_int_in_port_channel)
#print(vlan_in_dsw)
#print(vlan_layer3_csw)
if vlan_in_csw=="":
         for l in range(0,len(vlan_in_dsw)):
            for m in range(0,len(vlan_layer3_csw)):
                if vlan_in_dsw[l]==vlan_layer3_csw[m]:
                   lay2to3_flag="ture"
if vlan_in_csw!="":
         for m in range(0,len(vlan_layer3_csw)):
             if vlan_in_csw==vlan_layer3_csw[m]:
                lay2to3_flag="ture"

if lay2to3_flag=="ture":
    switch_output=switch_output+"target vlan"+vlan_no+" is available to go trunk to core switch and join layer 3 in core switch "+'\n'
if lay2to3_flag=="false":
   switch_output=switch_output+"target vlan"+vlan_no+" may be not available to go trunk to core switch and join layer 3 in core switch, need to check detail info "+'\n'


 

n=len(voice_site_router)      
ping_result=[]       
vlan_dot1q="false"


for i in range(0,n):
    res=voice_site_router[i].split('_')    
    log=res[0]+":"   
    result=res[0].split('-')
    name=res[0]+"_"+"config"
    sw_r_int_record=[]
    sub_int_ture_record=[]
    sw_r_flag="ture"
    router_output=""
    filewrite.write("\n")
    filewrite.write("\n")
    filewrite.write(res[0]+" ip traffic info:")
    print(res[0]+" ip traffic info summary:")
    csw_cdp=[]    
    with open(res[0]+'_ip_des.txt','r') as output:
         for line in output:   
             result=line.split()
             if len(result)>3: 
       
                 
                 le=len(result)
                 for k in range(0,le): 
                                if 'csw' in result[k] or 'CSW' in result[k] or 'core' in result[k] or 'CORE' in result[k]: 
                                     if'm-' in result[k] or 'M-' in result[k]:  
                                      csw_cdp.append(result[0])
    #print("csw_cdp")  
    #print(csw_cdp)    
    output.close
    eigrp_record=[]
    eigrp_num=res[0]+"eigrp_no:"
    with open(res[0]+'_eigrp_nei.txt','r') as output:
      for line in output:
           if line!='': 
                line=line.strip()
                
                if '/' in line:
                   result=line.split()
                   L=len(result)
                   router_cdp_write_value=""
                   for k in range(0,L):
                       if '/' in result[k]: 
                           if 'Te' in result[k] or 'te' in result[k] or 'Fa' in result[k] or 'fa' in result[k] or 'Gi' in result[k] or 'gi' in result[k]: 
                                                              if router_cdp_write_value=="":
                                                                 router_cdp_write_value=result[k]
                   if router_cdp_write_value!="": 
                      eigrp_record.append(router_cdp_write_value)  
                                       
    output.close
   
    with open(res[0]+'_eigrp_vrf_nei.txt','r') as output:
      for line in output:
           if line!='': 
                line=line.strip()
                result=line.split()
                if '/' in line:
                   L=len(result)
                   router_cdp_write_value=""
                   for k in range(0,L):
                       if '/' in result[k]: 
                           if 'Te' in result[k] or 'te' in result[k] or 'Fa' in result[k] or 'fa' in result[k] or 'Gi' in result[k] or 'gi' in result[k]: 
                                                              if router_cdp_write_value=="":
                                                                 router_cdp_write_value=result[k]
                   if router_cdp_write_value!="": 
                      eigrp_record.append(router_cdp_write_value)          
    output.close
    p=len(eigrp_record) 
    q=len(csw_cdp) 
   
    eigrp_flag="ture"    
    for k in range(0,q): 
        flag="false"
        for o in range(0,p): 
            if eigrp_record[o]==csw_cdp[k]:
               flag="ture" 
               
        if flag=="false": 
           if '.' in csw_cdp[k]:
              eigrp_flag="false"
              log=log+"core switch connected port "+csw_cdp[k]+" not in "+res[0]+" eigrp interface and "
           if '.' not in csw_cdp[k]:
              com_value=csw_cdp[k]
              num=len(csw_cdp)
              record_flag="ture"
              for m in range(0,num):
                  if '.' in csw_cdp[m] and com_value in csw_cdp[m]:
                     record_flag="false"
                         
              if record_flag=="ture": 
                 eigrp_flag="false"
                 log=log+"core switch connected port "+csw_cdp[k]+" not in "+res[0]+" eigrp interface and "    
    if eigrp_flag=="ture": 
       log=log+"all core switch connected port are in eigrp interface and "    
    if eigrp_flag=="false":
       log=log+"eigrp nei established may not completed , need to ensure the neighbor core sw of this router is the eigrp nei or not "+"and" 
    #print(log)
   
    tu_int=[]
    tu_vrf=[]
    with open(res[0]+'_r_ip_int.txt','r') as output:
       for line in output: 
           result=line.split()  #character isolate coloum fot output fpr split
           if 'tunnel' in line or 'Tunnel' in line or 'Tu' in line or 'tu' in line:
              if 'tunnel' in result[0] or 'Tunnel' in result[0] or 'Tu' in result[0] or 'tu' in result[0]:
                 tu_int.append(result[0])
    output.close
    #print(tu_int)
    l=len(tu_int)
    if l>int(0):
      for k in range(0,l):
          vrf_exist_flag="false"   
          with open(res[0]+'_r_int_config.txt','r') as output:
             start_flag="false"
             for line in output: 
                 if start_flag=="ture":
                    if 'ip vrf forwarding' in line: 
                       vrf_exist_flag="ture"
                       vrf_record=line.split() 
                       vrf=tu_int[k]+"+"+vrf_record[3]
                       tu_vrf.append(vrf) 
                    if 'interface' in line: 
                        re=line.split()
                        if len(re)==int(2) and re[0]=="interface":
                           start_flag="false" 
                           if vrf_exist_flag=="false":
                              vrf=tu_int[k]+"+"+"no_vrf"
                              tu_vrf.append(vrf)                            
                 if 'interface' in line and tu_int[k] in line: 
                     re=line.split()
                     if len(re)==int(2):
                        start_flag="ture"     
                  
          output.close 
    #print("router vrf:")  
    #print(tu_vrf)
    l=len(tu_vrf)
    if l>int(0):
       value=res[0] 
       for k in range(0,l): 
                  
            result=tu_vrf[k].split('+')  
            vrf=result[0]    
                      
            if result[1]=="ANZ_BRANCH":           
              with open(res[0]+'_eigrp_vrf_nei.txt','r') as eigrp_nei:
                Flag="false"
                for Que in eigrp_nei:
                  if Que!="":
                     if vrf in line or vrf.replace('nnel','') in Que:   
                        Flag="ture"  
                                        
                if Flag=="false":
                  value=value+"+"+"vlan outside protocol: "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei unestablished "
                  log=log+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei unestablished "+"and"
                  
                  router_output=router_output+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei unestablished "+"and"
                if Flag=="ture": 
                  value=value+"+"+"vlan outside protocol: "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei established "
                  log=log+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei established "+"and"
                  
                  router_output=router_output+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei established "+"and"          
              eigrp_nei.close
            if result[1]=="INTL_BRANCH":   
              with open(res[0]+'_eigrp_vrf_INTL_nei.txt','r') as eigrp_nei:
                Flag="false"
                for Que in eigrp_nei:
                  if Que!="":
                     if vrf in line or vrf.replace('nnel','') in Que:   
                        Flag="ture"  
                                        
                if Flag=="false":
                  value=value+"+"+"vlan outside protocol: "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei unestablished "
                  log=log+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei unestablished "+"and"
                  
                  router_output=router_output+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei unestablished "+"and"
                if Flag=="ture": 
                  value=value+"+"+"vlan outside protocol: "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei established "
                  log=log+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei established "+"and"
                  
                  router_output=router_output+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei established "+"and"          
              eigrp_nei.close
            if result[1]=="no_vrf":           
              with open(res[0]+'_eigrp_nei.txt','r') as eigrp_nei:
                Flag="false"
                for Que in eigrp_nei:
                  if Que!="":
                     if vrf in line or vrf.replace('nnel','') in Que:   
                        Flag="ture"  
                                        
                if Flag=="false":
                  value=value+"+"+"vlan outside protocol: "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei unestablished "
                  log=log+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei unestablished "+"and"
                  
                  router_output=router_output+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei unestablished "+"and"
                if Flag=="ture": 
                  value=value+"+"+"vlan outside protocol: "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei established "
                  log=log+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei established "+"and"
                  
                  router_output=router_output+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei established "+"and"          
              eigrp_nei.close 
            if result[1]!="ANZ_BRANCH" and result[1]!="INTL_BRANCH" and result[1]!="no_vrf":
              with open(res[0]+'_eigrp_vrf_all_nei.txt','r') as eigrp_nei:
                Flag="false"
                start_flag="false"
                for Que in eigrp_nei: 
                    if start_flag=="ture":
                       if Que!="":
                          if vrf in Que or vrf.replace('nnel','') in Que: 
                             Flag="ture"
                       if 'Neighbors' in Que:
                          rec=Que.split()
                          if len(rec)==int(5):
                             start_flag="false"
                    if 'Neighbors' in Que and result[1] in Que:
                       rec=Que.split()
                       if len(rec)==int(5): 
                          start_flag="ture"
  

                if Flag=="false":
                   value=value+"+"+"vlan outside protocol: "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei unestablished "
                   log=log+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei unestablished "+"and"
                  
                   router_output=router_output+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei unestablished "+"and"
                if Flag=="ture":
                   value=value+"+"+"vlan outside protocol: "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei established "
                   log=log+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei established "+"and"
                  
                   router_output=router_output+"+"+"vlan outside protocol "+" DMVPN eigrp vrf "+tu_vrf[k]+" nei established "+"and"          
              eigrp_nei.close

              
            #voice_site_router_dmvpn_eigrp.append(value)
    #print(log)
    router_output=router_output+'\n'    
    bgp_num=""
    ebgp_flag="false"
    ebgp_num=[]
    num_back=[]
    redist="65697"
    with open(res[0]+'_bgp_config.txt','r') as output:   
      for line in output: 
        result=line.split() #character isolate coloum fot output fpr split
        if len(result)==3:
           if result[1]=="bgp": 
              bgp_num=result[2]
        if len(result)==4:
           if result[0]=="neighbor" and result[2]=="remote-as": 
              if result[3]!="" and bgp_num!="" and result[3]!=bgp_num: 
                ebgp_flag="ture"
                write_flag="ture"
                for m in range (0,len(ebgp_num)):
                    if result[3]==ebgp_num[m]:
                       write_flag="false" 
                if write_flag=="ture":                      
                   ebgp_num.append(result[3])
                   num_back.append(result[3])
    output.close
   
    if bgp_num!="" and ebgp_flag=="ture":
       count=int(0)
       with open(res[0]+'_r_bgp_sum.txt','r') as output:   
          ebgp_nei_tag="false"
          start_flag="false"
          find_flag="false"
          
          for line in output: 
            if line!="" and start_flag=="ture":
              result=line.split() 
              if len(result)>int(2):
                if result[2]!=bgp_num and result[2]!="": 
                  L=len(ebgp_num)
                  for k in range(0,L):
                     if result[2]==ebgp_num[k]:
                        num_back[k]=""
                        find_flag="ture" 
                        count=count+int(1)                
                  if find_flag=="ture":                  
                    ebgp_nei_tag="ture"
                    value=res[0]+"+"+"vlan outside protocol "+"ebgp "+result[2]+" established"
                    log=log+"vlan outside protocol "+"ebgp "+result[2]+" established"+" and"     
                    
            if 'Neighbor' in line or 'neighbor' in line: 
                 start_flag="ture"             
       output.close  
       if count==len(ebgp_num): 
         router_output=router_output+"created ebgp neighbor all established,can see detail "+'\n'
       if count!=len(ebgp_num):  
         router_output=router_output+"not all created ebgp neighbor established,can see detail "+'\n' 
             
       Le=len(num_back)
       if Le>int(0):
          for n in range(0,Le):
              if num_back[n]!="":
                 value=res[0]+"+"+"vlan outside protocol "+"ebgp "+num_back[n]+" unestablished"
                 log=log+"vlan outside protocol "+"ebgp "+num_back[n]+" unestablished"+"and" 
                  
    #print("eigrp, vrf DMVPN, bgp nei established ") 
    filewrite.write("\n")    
    filewrite.write(log) 
    eigrp_edge_record=""   
    vrf=""#for eigrp redistribute check
    with open(res[0]+'_r_eigrp.txt','r') as eigrp_info:
            
            for Que in eigrp_info: 
                if line !="":
                   if 'router eigrp' in Que:
                      R=Que.split()
                      eigrp_num=eigrp_num+R[2]
                if "vrf" in Que: 
                   R=Que.split()
                   if len(R)==4: 
                      vrf=R[3]                   
                if "redistribute" in Que: 
                    if ebgp_num!="":
                       R=Que.split()
                    if vrf!="":
                       if R[2]==bgp_num:
                          eigrp_edge_record=eigrp_edge_record+"+"+"bgp "+bgp_num+" redistribute into eigrp vrf "+vrf+" correctly"
                       if R[2]!=bgp_num:
                          eigrp_edge_record=eigrp_edge_record+"+"+"bgp "+bgp_num+" redistribute into eigrp vrf "+vrf+" incorrectly (bgp num may be incorrect) "
                    if vrf=="":
                       if R[2]==bgp_num:
                          eigrp_edge_record=eigrp_edge_record+"+"+"bgp "+bgp_num+" redistribute into eigrp (not vrf table) "+" correctly"
                       if R[2]!=bgp_num:
                          eigrp_edge_record=eigrp_edge_record+"+"+"bgp "+bgp_num+" redistribute into eigrp (not vrf table)"+" incorrectly (bgp num may be incorrect) "
                    if vrf!="":
                       vrf="" 
    eigrp_info.close
    log=log+eigrp_edge_record+"  "
    filewrite.write("\n")
    filewrite.write("eigrp redistribute info:")
    filewrite.write(eigrp_edge_record)
    csw_des=[]
    with open(res[0]+'_ip_des.txt','r') as output:  
            for line in output: 
                result=line.split()#specical character to isolate
                
                if len(result)>3: 
                  if '-cs' in line or '-CS' in line or '-core' in line or '-CORE' in line:
                     csw_des.append(line)
    output.close                 
    #le=len(csw_des) 
    #for m in range(0,le):
        #print(csw_des[m])    
    interface_with_sub=[]                   
    with open(res[0]+'_r_ip_int.txt','r') as output:  
      for line in output: 
           
           result=line.split()#character isolate coloum fot output fpr split
           if len(result)>int(0): 
              R=result[0].split('.')
              if result[0]!=R[0]: 
                 interface_with_sub.append(result[0])
                 vrf=""
                 with open(res[0]+'_r_int_config.txt','r') as interface_info:
                   start_flag="false"     
                   if 'Te' in result[0] and 'gab' not in result[0]:
                        result[0]=result[0].replace('Te','TenGigabitEthernet') 
                   if 'Gi' in result[0] and 'gab' not in result[0]:
                        result[0]=result[0].replace('Gi','GigabitEthernet')  
                   if 'Fa' in result[0] and 'eth' not in result[0]:
                        result[0]=result[0].replace('Fa','fastethernet')                          
                   for queue in interface_info: 
                     
                     if start_flag=="ture":
                       if 'ip address' in queue: 
                          ip_info=queue.split()
                          interface_to_sub_ip=ip_info[2] 
                       if 'ip vrf forwarding' in queue: 
                          vrf_record=queue.split()
                          vrf=vrf_record[3]
                       if 'interface' in queue : 
                          re=queue.split()
                          if len(re)==int(2) and re[0]=="interface":
                             start_flag="false"            
                     if 'interface' in queue and result[0] in queue: 
                        re=queue.split()
                        if len(re)==int(2):
                           start_flag="ture" 
                          
                 interface_info.close        
                 with open(res[0]+'_r_int_config.txt','r') as sub_interface_info:
                   start_flag="false"
                   if 'Te' in result[0] and 'gab' not in result[0]:
                        result[0]=result[0].replace('Te','TenGigabitEthernet') 
                   if 'Gi' in result[0] and 'gab' not in result[0]:
                        result[0]=result[0].replace('Gi','GigabitEthernet')  
                   if 'Fa' in result[0] and 'eth' not in result[0]:
                        result[0]=result[0].replace('Fa','Fastethernet')  
                   for queue in sub_interface_info:
                     if start_flag=="ture":
                       
                      
                        if 'encapsulation dot1Q' in queue or 'encapsulation dot1q' in queue:
                           dot1q_info=queue.split()
                           y=len(switch_vlan_info)
                           for x in range(0,y):   
                              W=switch_vlan_info[x].split('+')
                              if W[0]=="vlan"+dot1q_info[2]:
                                 sw_vlan_add="false"
                                 Le=len(csw_cdp)
                                 for m in range(0,Le):
                                     if csw_cdp[m]==result[0].replace('TenGigabitEthernet','Te') or csw_cdp[m]==result[0].replace('GigabitEthernet','Gi') or csw_cdp[m]==result[0].replace('Fastethernet','Fa'):
                                        sw_vlan_add="ture"
                                 if sw_vlan_add=="ture":       
                                    vlan_dot1q="ture"  
                                   
                                    if "+layer2 to router" in switch_vlan_info[x] :
                                       switch_vlan_info[x]=switch_vlan_info[x]
                                    if"+layer2 to router" not in switch_vlan_info[x] :
                                       switch_vlan_info[x]=switch_vlan_info[x]+"+"+"layer2 to router"
                                    if vrf!="" and vrf not in switch_vlan_info[x]:
                                       switch_vlan_info[x]=switch_vlan_info[x]+"_vrf:"+vrf   
                        if 'interface' in queue: 
                          re=queue.split()
                          if len(re)==int(2) and re[0]=="interface":
                             start_flag="false"            
                     if 'interface' in queue and result[0] in queue: 
                        re=queue.split()
                        if len(re)==int(2):
                           start_flag="ture"  
                                                  
                 sub_interface_info.close                  
    output.close
    
   #here need to extend for case if encapsuation int in different router come with different vrf  
    csw_con_edge_record=res[0]+"(csw connect int status):"
    vlan_layer3="ture"
    if vlan_layer3=="ture":
       core_switch_con_int=[]
       core_switch_con_int_sta="down"
       core_switch_con_vrf=""
       core_switch_con_int_ip=""
       with open(res[0]+'_ip_des.txt','r') as output:  
            for line in output: 
                result=line.split()#specical character to isolate
                
                if len(result)>3: 
                
                 
                  le=len(result)
                  write_flag="false"
                  for k in range(0,le): 
                                if 'csw' in result[k] or 'CSW' in result[k] or 'core' in result[k] or 'CORE' in result[k]: 
                                     if'm-' in result[k] or 'M-' in result[k]:  
                      
                                        l=len(interface_with_sub)
                                        flag="false"
                                        for m in range(0,l): 
                                            if interface_with_sub[m]==result[0]:
                                               flag="ture"
                                        R=result[0].split('.')
                                        if R[0]!=result[0]:
                                           flag="ture"
                                        if flag=="false" and write_flag=="false": 
                                           core_switch_con_int.append(result[0]) 
                                           write_flag="ture"                                           
                        
       output.close
       #print(interface_with_sub)
       #print(core_switch_con_int)
       l=len(core_switch_con_int)
       for k in range(0,l):
          core_switch_con_int_sta="down"
          core_switch_con_vrf=""
          core_switch_con_int_ip=""
          core_switch_con_ip_flag="false"
          core_switch_con_vrf_flag="false"
          #r_int_egirp_exist_flag="false" 
          #x_connect="false"
          #x_connect_value=""
          #encap_value=""
          with open(res[0]+'_ip_des.txt','r') as output:
            for line in output: 
                result=line.split()
                if len(result)>int(0):
                   if result[0]==core_switch_con_int[k]:
                      core_switch_con_int_sta=result[1]+"(status)"+"and"+result[2]+"(protocol)"
          output.close
          core_upade=interface_with_sub[k]
          if 'Te' in core_switch_con_int[k] and 'gab' not in core_switch_con_int[k]:
             core_upade=core_switch_con_int[k].replace('Te','TenGigabitEthernet') 
          if 'Gi' in core_switch_con_int[k] and 'gab' not in core_switch_con_int[k]:
             core_upade=core_switch_con_int[k].replace('Gi','GigabitEthernet')  
          if 'Fa' in core_switch_con_int[k] and 'eth' not in core_switch_con_int[k]:
             core_upade=core_switch_con_int[k].replace('Fa','Fastethernet') 
          with open(res[0]+'_r_int_config.txt','r') as output: 
            start_flag="false"
            for line in output: 
              if start_flag=="ture":
                result=line.split()
                if len(result)>int(0):          
                   if 'ip address' in line and '.' in line: 
                          ip_info=line.split()
                          core_switch_con_int_ip=ip_info[2] 
                   #if 'encapsulation dot1q' in line:
                       #encap_info=line.split()
                       #encap_value=encap_info[2]
                   #if 'xconnect' in line: 
                       #xcon_info=line.split()
                       #if xcon_info[0]=="xconnect" and len(xcon_info)>int(2):
                          #x_connect="ture"
                          #x_connect_value="router-id:"+xcon_info[1]+"_"+"vcid:"+xcon_info[2]
                   if 'ip vrf forwarding' in line: 
                          vrf_record=line.split()
                          core_switch_con_vrf=vrf_record[3]
                   if 'interface' in line: 
                          re=line.split()
                          if len(re)==int(2) and re[0]=="interface":
                             start_flag="false"            
              if 'interface' in line and core_upade in line and '.' not in line: 
                        re=line.split()
                        if len(re)==int(2):
                           start_flag="ture"  
                                                
          output.close
         
          if  core_switch_con_vrf=="":   
              with open(res[0]+'_eigrp_int.txt','r') as output: 
                for line in output: 
                    if core_switch_con_int[k] in line: 
                       result=line.split()
                       if len(result)>int(0):
                          if core_switch_con_int[k]==result[0]:                       
                             core_switch_con_ip_flag="ture"                     
              output.close            
              with open(res[0]+'_eigrp_nei.txt','r') as output: 
               for line in output: 
                  if core_switch_con_int[k] in line: 
                        result=line.split()
                        if len(result)>int(2):
                         if core_switch_con_int[k]==result[2]:   
                            core_switch_con_vrf_flag="ture"  
              output.close
          
          if  core_switch_con_vrf!="":          
              with open(res[0]+'_eigrp_vrf_int.txt','r') as output: 
                for line in output: 
                    if core_switch_con_int[k] in line:
                       result=line.split()
                       if len(result)>int(0):
                          if core_switch_con_int[k]==result[0]:                       
                             core_switch_con_ip_flag="ture"                    
              output.close            
              with open(res[0]+'_eigrp_vrf_nei.txt','r') as output: 
               for line in output: 
                   if core_switch_con_int[k] in line: 
                      result=line.split()
                      if len(result)>int(2):
                         if core_switch_con_int[k]==result[2]:   
                            core_switch_con_vrf_flag="ture"   
              output.close  
          #if core_switch_con_int_ip!="":    
               
             #with open(res[0]+'_r_eigrp.txt','r') as output: 
               #for line in output:
                 #if 'network' in line: 
                    #re=line.split()
                    #if len(re)==int(3) and re[0]=="network":
                       #network=[]
                       #mask=[]
                       #vlanip=[]
                       #com_start_flag="false"
                       #sub_re=re[1].split('.') 
                       #l=len(sub_re)
                       #for k in range(0,l):
                           #network.append(sub_re[k])
                       #sub_re=re[2].split('.')
                       #l=len(sub_re)
                       #for k in range(0,l):
                           #Va=int(255)-int(sub_re[k])
                           #mask.append(str(Va))
                       #sub_re=core_switch_con_int_ip.split('.')
                       #l=len(sub_re)
                       #for k in range(0,l):
                           #vlanip.append(sub_re[k])
                       #if len(network)==int(4) and len(mask)==int(4) and len(vlanip)==int(4):
                          #com_start_flag="ture"
                          #sec_com_flag="ture"
                          #l=len(network)
                          #for k in range(0,l):
                              #if (int(network[k])&int(mask[k]))!=(int(vlanip[k])&int(mask[k])):
                                 #sec_com_flag="false"
                       #if com_start_flag=="ture" and sec_com_flag=="ture": 
                          #r_int_eigrp_exist_flag="ture"

             #output.close            
          if core_switch_con_vrf_flag=="ture" and  core_switch_con_ip_flag=="ture" and core_switch_con_int_sta=="up(status)andup(protocol)":
             value=core_switch_con_int[k]+"_ture"
             sw_r_int_record.append(value)
             csw_con_edge_record=csw_con_edge_record+"+ "+"get layer3 traffic to outside ready for site vlan via "+core_switch_con_int[k]
             if core_switch_con_vrf!="":
                csw_con_edge_record=csw_con_edge_record+"( vrf:"+core_switch_con_vrf+")"  
             if core_switch_con_vrf=="":
                csw_con_edge_record=csw_con_edge_record+"(no vrf )"  
          #if x_connect=="ture":
             #csw_con_edge_record=csw_con_edge_record+"+ "+core_switch_con_int[k]+"go xconnect for connected csw:" +x_connect_value
             #if encap_value!="":
                #csw_con_edge_record=csw_con_edge_record+" encapsulation dot1q"+encap_value  
             #if core_switch_con_vrf!="":
                #csw_con_edge_record=csw_con_edge_record+"( vrf:"+core_switch_con_vrf+")"  
             #if core_switch_con_vrf=="":
                #csw_con_edge_record=csw_con_edge_record+"(no vrf )"                  
          else: 
               value=core_switch_con_int[k]+"_false"
               sw_r_int_record.append(value)
               if core_switch_con_vrf_flag=="false": 
                   csw_con_edge_record=csw_con_edge_record+"+ "+" fail to get layer3 traffic to outside ready for site vlan :"+ core_switch_con_int[k]+"  eigrp nei may not established"
                   if core_switch_con_vrf!="":
                      csw_con_edge_record=csw_con_edge_record+"(eigrp nei vrf "+core_switch_con_vrf+" )"  
               if  core_switch_con_ip_flag=="false": 
                   csw_con_edge_record=csw_con_edge_record+"+ "+"fail to get layer3 traffic to outside ready for site vlan: "+"interface "+core_switch_con_int[k]+"may not in device eigrp protocol rightly"              

               if core_switch_con_int_sta!="up(status)andup(protocol)": 
                  csw_con_edge_record=csw_con_edge_record+"+ "+"fail to get layer3 traffic to outside ready for site vlan "+core_switch_con_int[k]+":protocol, status is down"  
               #if r_int_egirp_exist_flag=="false":
                  #csw_con_edge_record=csw_con_edge_record+core_switch_con_int[k]+" ip not in router eigrp"               
             
                     
    if vlan_dot1q=="ture":
       l=len(interface_with_sub)
       for k in range(0,l):
         start_flag="false"
         sub_upade=interface_with_sub[k]
         if 'Te' in interface_with_sub[k] and 'gab' in interface_with_sub[k]:
             sub_upade=interface_with_sub[k].replace('TenGigabitEthernet','Te') 
         if 'Gi' in interface_with_sub[k] and 'gab' in interface_with_sub[k]:
             sub_upade=interface_with_sub[k].replace('GigabitEthernet','Gi')  
         if 'Fa' in interface_with_sub[k] and 'eth' in interface_with_sub[k]:
             sub_upade=interface_with_sub[k].replace('Fastethernet','Fa')
         Le=len(csw_cdp)
         for m in range(0,Le):
              if csw_cdp[m]==sub_upade:
                 start_flag="ture"  
                          
         if start_flag=="ture": 
          #print(sub_upade)
          interface_with_sub_int_sta="down"
          interface_with_sub_vrf=""
          interface_with_sub_int_ip=""
          interface_with_sub_ip_flag="false"
          interface_with_sub_vrf_flag="false"
          #r_int_egirp_exist_flag="false"
          #x_connect="false"
          #x_connect_value=""
          #encap_value=""
          with open(res[0]+'_ip_des.txt','r') as output:
            for line in output: 
                result=line.split()
                if len(result)>int(0):
                   if result[0]==sub_upade:
                      interface_with_sub_int_sta=result[1]+"(status)"+"and"+result[2]+"(protocol)"
          output.close
          core_upade=interface_with_sub[k]
          if 'Te' in interface_with_sub[k] and 'gab' not in interface_with_sub[k]:
             core_upade=interface_with_sub[k].replace('Te','TenGigabitEthernet') 
          if 'Gi' in interface_with_sub[k] and 'gab' not in interface_with_sub[k]:
             core_upade=interface_with_sub[k].replace('Gi','GigabitEthernet')  
          if 'Fa' in interface_with_sub[k] and 'eth' not in interface_with_sub[k]:
             core_upade=interface_with_sub[k].replace('Fa','Fastethernet') 
          #print(core_update)
          with open(res[0]+'_r_int_config.txt','r') as output: 
            start_flag="false"
            for line in output: 
              if start_flag=="ture":
                result=line.split()
                if len(result)>int(0):          
                   if 'ip address' in line: 
                          ip_info=line.split()
                          interface_with_sub_int_ip=ip_info[2] 
                   #if 'encapsulation dot1q' in line:
                       #encap_info=line.split()
                       #encap_value=encap_info[2]
                   #if 'xconnect' in line: 
                       #xcon_info=line.split()
                       #if xcon_info[0]=="xconnect" and len(xcon_info)>int(2):
                          #x_connect="ture"
                          #x_connect_value="router-id:"+xcon_info[1]+"_"+"vcid:"+xcon_info[2]
                   if 'ip vrf forwarding' in line: 
                          vrf_record=line.split()
                          interface_with_sub_vrf=vrf_record[3]
                   if 'interface' in line: 
                          re=line.split()
                          if len(re)==int(2) and re[0]=="interface":
                             start_flag="false"            
              if 'interface' in line and core_upade in line : 
                        re=line.split()
                        if len(re)==int(2):
                           start_flag="ture"               
          output.close
          #print(sub_upade+":"+interface_with_sub_vrf)
          if  interface_with_sub_vrf=="":   
              with open(res[0]+'_eigrp_int.txt','r') as output: 
                for line in output: 
                    if sub_upade in line: 
                        result=line.split()
                        if len(result)>int(0):
                          if sub_upade==result[0]:                       
                             interface_with_sub_ip_flag="ture"                     
              output.close            
              with open(res[0]+'_eigrp_nei.txt','r') as output: 
               for line in output: 
                   if sub_upade in line: 
                      result=line.split()
                      if len(result)>int(2):
                          if sub_upade==result[2]:    
                             interface_with_sub_vrf_flag="ture"  
              output.close
          if  interface_with_sub_vrf!="":          
              with open(res[0]+'_eigrp_vrf_int.txt','r') as output: 
                for line in output: 
                    if sub_upade in line: 
                       result=line.split()
                       if len(result)>int(0):
                          if sub_upade==result[0]:                       
                             interface_with_sub_ip_flag="ture"                   
              output.close            
              with open(res[0]+'_eigrp_vrf_nei.txt','r') as output: 
               for line in output: 
                   if sub_upade in line: 
                      result=line.split()
                      if len(result)>int(2):
                          if sub_upade==result[2]:    
                             interface_with_sub_vrf_flag="ture"    
              output.close
          #if interface_with_sub_int_ip!="":    
                
             #with open(res[0]+'_r_eigrp.txt','r') as output: 
               #for line in output:
                 #if 'network' in line: 
                    #re=line.split()
                    #if len(re)==int(3) and re[0]=="network":
                       #network=[]
                       #mask=[]
                       #vlanip=[]
                       #com_start_flag="false"
                       #sub_re=re[1].split('.') 
                       #l=len(sub_re)
                       #for k in range(0,l):
                           #network.append(sub_re[k])
                       #sub_re=re[2].split('.')
                       #l=len(sub_re)
                       #for k in range(0,l):
                           #Va=int(255)-int(sub_re[k])
                           #mask.append(str(Va))
                       #sub_re=interface_with_sub_int_ip.split('.')
                       #l=len(sub_re)
                       #for k in range(0,l):
                           #vlanip.append(sub_re[k])
                       #if len(network)==int(4) and len(mask)==int(4) and len(vlanip)==int(4):
                          #com_start_flag="ture"
                          #sec_com_flag="ture"
                          #l=len(network)
                          #for k in range(0,l):
                              #if (int(network[k])&int(mask[k]))!=(int(vlanip[k])&int(mask[k])):
                                 #sec_com_flag="false"
                       #if com_start_flag=="ture" and sec_com_flag=="ture": 
                          #r_int_eigrp_exist_flag="ture"

             #output.close  
          if interface_with_sub_vrf_flag=="ture" and  interface_with_sub_ip_flag=="ture" and  interface_with_sub_int_sta=="up(status)andup(protocol)":
              value=interface_with_sub[k]+"_ture"
              sw_r_int_record.append(value)   
              csw_con_edge_record= csw_con_edge_record+"+ "+"get layer2&layer3 traffic to outside ready for site vlan via "+interface_with_sub[k]
              if interface_with_sub_vrf!="":
                csw_con_edge_record=csw_con_edge_record+"( vrf:"+interface_with_sub_vrf+")"  
              if interface_with_sub_vrf=="":
                csw_con_edge_record=csw_con_edge_record+"(no vrf )" 
          #if x_connect=="ture":
             #csw_con_edge_record=csw_con_edge_record+"+ "+interface_with_sub[k]+"go xconnect for connected csw:" +x_connect_value
             #if encap_value!="":
                #csw_con_edge_record=csw_con_edge_record+" encapsulation dot1q"+encap_value  
             #if core_switch_con_vrf!="":
                #csw_con_edge_record=csw_con_edge_record+"( vrf:"+core_switch_con_vrf+")"  
             #if core_switch_con_vrf=="":
                #csw_con_edge_record=csw_con_edge_record+"(no vrf )"                        
          else: 
               value=interface_with_sub[k]+"_false"
               sw_r_int_record.append(value)  
               if interface_with_sub_vrf_flag=="false": 
                  csw_con_edge_record= csw_con_edge_record+"+ "+"fail to get layer2&layer3 traffic to outside ready for site vlan :"+ interface_with_sub[k]+" eigrp nei  not established"
                  if interface_with_sub_vrf!="":
                       csw_con_edge_record= csw_con_edge_record+"(eigrp nei vrf "+interface_with_sub_vrf+" )" 
                   
               if interface_with_sub_ip_flag=="false": 
                    csw_con_edge_record= csw_con_edge_record+"+ "+"fail to get layer2&layer3 traffic to outside ready for site vlan: "+" interface "+interface_with_sub[k]+" not in device eigrp protocol rightly"              

               if interface_with_sub_int_sta!="up(status)andup(protocol)": 
                   csw_con_edge_record= csw_con_edge_record+"+ "+"fail to get layer2 traffic to outside ready for site vlan "+interface_with_sub[k]+":protocol status is down"
               #if r_int_egirp_exist_flag=="false":
                   #csw_con_edge_record=csw_con_edge_record+interface_with_sub[k]+" ip not in router eigrp"       
          log=log+csw_con_edge_record+"   "
          
    #edge_deivce_for_sitevlan_outside.append( csw_con_edge_record)   
    filewrite.write("\n")
    filewrite.write("router to connected csw traffic: ")
    filewrite.write(csw_con_edge_record)
    
    for l in range(0,len(sw_r_int_record)):
        if '.' in sw_r_int_record[l] and '_ture' in sw_r_int_record[l]:
           re=sw_r_int_record[l].split('_')
           if len(re)>int(1): 
              sub_int_ture_record.append(re[0]) 
   
    for l in range(0,len(sub_int_ture_record)):
        re=sub_int_ture_record[l].split('.')
        comp=""
        if len(re)>int(1): 
           comp=re[0]
        for m in range(0,len(sw_r_int_record)):
            if comp !=""  and 'false' in sw_r_int_record[m]:
               if comp in sw_r_int_record[m] or comp.replace('GigabitEthernet','Gi') in sw_r_int_record[m] or comp.replace('TenGigabitEthernet','Te') in sw_r_int_record[m] or comp.replace('Fastethernet','Fa') in sw_r_int_record[m]:
                 if '.' in sw_r_int_record[m]:             
                   sw_r_int_record[m]=sw_r_int_record[m] 
                 else: 
                   sw_r_int_record[m]=sw_r_int_record[m].replace('false','ture') 
    sw_r_flag="ture"             
    for l in range(0,len(sw_r_int_record)):
        if 'false' in sw_r_int_record[l]:
           sw_r_flag="false" 
          
    if sw_r_flag=="ture":
         router_output=router_output+"core switch to this router traffic all ok "
    if sw_r_flag=="false":
         router_output=router_output+"core switch to this router traffic may have issue , can see detail "    
    print(router_output)         
    #print(eigrp_num)
      
value=""
for n in range(0,len(switch_vlan_info)):
    value=value+switch_vlan_info[n]+", " 
filewrite.write("\n")
filewrite.write("\n")   
filewrite.write("svi vlan in layer 2&3:")
filewrite.write(value)
filewrite.close()


for l in range(0,len(switch_vlan_info)):
    if vlan_no in switch_vlan_info[l] and 'layer2 to router' in switch_vlan_info[l]:
       
       switch_output=switch_output+"target vlan"+vlan_no+" can go both layer2&layer3 to outside network via router"+'\n'   
print(switch_output)

