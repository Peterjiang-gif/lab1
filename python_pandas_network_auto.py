import os 
import pandas as pd 
import matplotlib.pyplot as plt
#import pandas np 
import numpy as np

#create site verity command table 
show_commands=["show vlan brief","show run | sec interface","show authetication session","show int trunk","show ip interface"]
colum=["site","device","show"]
df=pd.DataFrame(columns=colum)
#df['show']=show_commands 
df['site']=["site_a","site_a","site_a","site_b","site_b","site_b","site_c","site_c","site_c","site_d","site_d","site_d"]
df['device']=["sw1","sw2","sw3","sw1","sw2","sw3","sw1","sw2","sw3","sw1","sw2","sw3"]
sites=["site_a","site_a","site_a","site_a","site_a","site_a","site_b","site_b","site_b","site_b","site_c","site_c","site_c","site_c","site_d","site_d","site_d","site_d","site_d"] 
ends=["ap1","ap2","ap3","ap4","vg1","vg2","ap1","ap2","ap3","vg1","ap1","ap2","ap3","vg1","ap1","ap2","ap3","ap4","vg1"]
end_auth=[0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0]
ap_trunk_con=[0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0]
ap_access_con=[0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0]
ap_vlan_match=[0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0]
ap_vlan_exist=[0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0]
ap_vlan_comm=[0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0]
wireless_layer3=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ap_vlan_layer3=[0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0]
po_match=[1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
trunk_port_match=[1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
verify=["end_devices","site","end point authentication issue","trunk mode ap config issue on connected switch","access mode ap config issue on connected switch","ap trunk native vlan does not match wireless vlan","ap vlans does not exist in layer 2 trunk traffic to core switch","ap vlans communicate issue in trunk traffic with core switch","wireless vlan does not exist in layer3 traffic","ap vlan does not exist in layer3 traffic","port-channel vlan set does not match physical trunk port","switch redundancy trunk port set does not match"] 
audit=pd.DataFrame(columns=verify)
audit['end_devices']=ends
audit['site']=sites
audit['end point authentication issue']=end_auth 
audit['trunk mode ap config issue on connected switch']=ap_trunk_con
audit['access mode ap config issue on connected switch']=ap_access_con 
#end_devices_access_issue=[]
audit['ap trunk native vlan does not match wireless vlan']=ap_vlan_match 
audit['ap vlans does not exist in layer 2 trunk traffic to core switch']=ap_vlan_exist
audit['ap vlans communicate issue in trunk traffic with core switch']=ap_vlan_comm
#end_devices_vlan_trunk_issue=[]
audit['wireless vlan does not exist in layer3 traffic']=wireless_layer3 
audit['ap vlan does not exist in layer3 traffic']=ap_vlan_layer3
end_devices_vlan_ip_inner_subet_issue=[]
audit['port-channel vlan set does not match physical trunk port']=po_match 
audit['switch redundancy trunk port set does not match']=trunk_port_match 
#site_layer2_trafic_issue=[]




#ap endpoint unavailable issue check list (data analysis and graph)
ap_audit=audit[audit['end_devices'].str.contains('ap')].copy()
ap_audit['issue_summary']=ap_audit['end point authentication issue']
Value=""
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#print(ap_audit)
for i in range(0,ap_audit.shape[0]):
  Value=""
  #print(ap_audit.iloc[i].tolist())
  for j in range(2,(len(verify)-int(4))):
      array=ap_audit.iloc[i].tolist()
      if int(array[j])>int(0):        
         #print(col_name)         
         Value=Value+"  "+verify[j]
  
  ap_audit.loc[i,'issue_summary']=Value 



#site layer2&3 common unavailable issue list (data analysis and graph) 
ap_audit=audit[audit['end_devices'].str.contains('ap')].copy()
#print(ap_audit)
site_issue=pd.pivot_table(ap_audit,index=['site'],values=['end point authentication issue','trunk mode ap config issue on connected switch','access mode ap config issue on connected switch','ap trunk native vlan does not match wireless vlan',
'ap vlans does not exist in layer 2 trunk traffic to core switch','ap vlans communicate issue in trunk traffic with core switch','wireless vlan does not exist in layer3 traffic','ap vlan does not exist in layer3 traffic','port-channel vlan set does not match physical trunk port','switch redundancy trunk port set does not match'],aggfunc='sum')
#print(site_issue)
site_issue['end_devices_access_issue']=site_issue[['end point authentication issue','trunk mode ap config issue on connected switch','access mode ap config issue on connected switch']].sum(axis=1)
site_issue['end_devices_vlan_trunk_issue']=site_issue[['ap trunk native vlan does not match wireless vlan','ap vlans does not exist in layer 2 trunk traffic to core switch','ap vlans communicate issue in trunk traffic with core switch']].sum(axis=1)
site_issue['end_devices_vlan_ip_inner_subet_issue']=site_issue[['wireless vlan does not exist in layer3 traffic','ap vlan does not exist in layer3 traffic']].sum(axis=1)
site_issue['site_layer2_trafic_issue']=site_issue[['port-channel vlan set does not match physical trunk port','switch redundancy trunk port set does not match']].sum(axis=1)

site_issue['end_devices_access_issue']=np.where(site_issue['end_devices_access_issue']>0,1,0) 
site_issue['end_devices_vlan_trunk_issue']=np.where(site_issue['end_devices_vlan_trunk_issue']>0,1,0) 
site_issue['end_devices_vlan_ip_inner_subet_issue']=np.where(site_issue['end_devices_vlan_ip_inner_subet_issue']>0,1,0)
site_issue['site_layer2_trafic_issue']=np.where(site_issue['site_layer2_trafic_issue']>0,1,0)
print(site_issue[['end_devices_access_issue','end_devices_vlan_trunk_issue','end_devices_vlan_ip_inner_subet_issue','site_layer2_trafic_issue']])
site_issue[['end_devices_access_issue','end_devices_vlan_trunk_issue','end_devices_vlan_ip_inner_subet_issue','site_layer2_trafic_issue']].plot(kind="bar",title="sites issue display")





#site unavailable ap list  (data analysis and graph)
ap_audit=audit[audit['end_devices'].str.contains('ap')].copy()
ap_audit.drop(["port-channel vlan set does not match physical trunk port","switch redundancy trunk port set does not match"],axis=1)
ap_audit_new=ap_audit.drop(["site","end_devices"],axis=1)
ap_audit['ap_result']=ap_audit_new.sum(axis=1)
#print(ap_audit['ap_result'])
ap_audit['ap_result']=np.where(ap_audit['ap_result']>0,1,0)
ap_audit=ap_audit.drop(ap_audit[ap_audit['ap_result']<0].index)
#print(ap_audit['ap_result'])
show_table=pd.pivot_table(ap_audit,index=['site'],columns=['end_devices'],values=['ap_result'])
print(show_table)
#.plot(kind="bar",title="site issue end devices display")