from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException

index=[]
device=[]
command=[]
with open('index.txt','r') as files:
  for line in files:
      if line!='':
         line=line.strip()
         result=line.split(':') 
         index.append(result[1])
         device.append(result[0])
files.close()

with open('command.txt','r') as files:
     for line in files:
         
            command.append(line)
files.close()  
n=len(device)
filewrite=open('device_info.txt','w')
n=len(device)
output=""
interface=["vlan2108","vlan2107","FastEthernet2/0"]
for j in range(0,int(10))
     print("hello\n")
for i in range(0,n):
    filewrite.write(device[i]+' status information:'+'\n')
    
    result=index[i].split(',')
  
    RTR={
     'device_type': result[0],
     'ip': result[1] ,
     'username': result[2],
     'password': result[3],
    }
    net_connect=ConnectHandler(**RTR)
 
    for com in command:
       
        filewrite.write(com+' result:'+'\n')
        output=net_connect.send_command(com)
        
        filewrite.write(output)
        filewrite.write('\n') 
    
filewrite.close()
       