import tkinter as tk
from tkinter import *
import os 
import pandas as pd 
one_w_list=""
two_w_entry=""
two_w_radio=""
three_w_entry1=""
three_w_entry2=""
three_w_entry3=""
four_w_list_all=[]
#begin

def read1(next_w,e1,var1):
 global two_w_entry
 global two_w_radio
 two_w_entry=e1.get()
 two_w_radio=var1.get()
 print(str(two_w_entry)+" "+str(two_w_radio))
 next_w.destroy()
 filewrite=open('config_set.txt','w')
 device_trunk=["sw1_int1","sw1_int2","sw3_int1","sw3_int2"]
 vlan=["20","30"]
 device=""
 if two_w_radio==int(1):
   for i in range(0,len(device_trunk)):
     value=device_trunk[i].split('_')
     if device=="":
        device=value[0]
        filewrite.write(device+"\n") 
        filewrite.write("\n")
        filewrite.write("int po"+two_w_entry+"\n")
        filewrite.write("sw trunk encapsulation 802.1q"+"\n")
        filewrite.write("sw mode trunk"+"\n")
        filewrite.write("sw trunk allowed vlan 20,30"+"\n")
        filewrite.write("exit"+"\n")
        filewrite.write("int "+value[1]+"\n")
        filewrite.write("channel-group "+two_w_entry+" mode"+" active"+"\n")
        filewrite.write("exit"+"\n")
        
     else:
        if device!=value[0]:
           device=value[0]
           filewrite.write(device+"\n") 
           filewrite.write("\n")
           filewrite.write("int po"+two_w_entry+"\n")
           filewrite.write("sw trunk encapsulation 802.1q"+"\n")
           filewrite.write("sw mode trunk"+"\n")
           filewrite.write("sw trunk allowed vlan 20,30"+"\n")
           filewrite.write("exit"+"\n")
           filewrite.write("int "+value[1]+"\n")
           filewrite.write("channel-group "+two_w_entry+" mode"+" active"+"\n")
           filewrite.write("exit"+"\n")
        else:
           filewrite.write("int "+value[1]+"\n")
           filewrite.write("channel-group "+two_w_entry+" mode"+" active"+"\n")
           filewrite.write("exit"+"\n")
    
 filewrite.close() 
 
def read2(last_w): 
 global three_w_entry1
 global three_w_entry2
 global three_w_entry3
 global four_w_list_all
 print(four_w_list_all)
 last_w.destroy()
 if len(four_w_list_all)>int(0):
    colum=["section","subnet"]
    df=pd.DataFrame(columns=colum)
    df['section']=["fiance","customer"]
    df['subnet']=["192.168.1.0","192.168.2.0"]
    filewrite=open('config_set.txt','w')
    for i in range(0,len(four_w_list_all)):
      value=four_w_list_all[i].split('+')
      va=value[1].split('_')
      filewrite.write(value[0]+"\n")
      filewrite.write("\n")
      filewrite.write("ip access-list "+three_w_entry1+"\n")
      index=df.loc[df['section']==three_w_entry2].index[0]
      var=df.at[index,'subnet']
      filewrite.write("deny ip "+var+ " any "+three_w_entry3+"\n")
      filewrite.write("exit"+"\n")
      for j in range(0,len(va)):
        if va[j]!="" and va[j]!=" ":
          filewrite.write("int "+va[j]+"\n")
          filewrite.write("access-group "+three_w_entry1+" in"+"\n") 
          filewrite.write("exit"+"\n") 
    filewrite.close()
      
def collect_device(last_w,list2,list3):
 global four_w_list_all

 item=""
 index1=list2.curselection()
 if len(index1)>int(0):
    item=list2.get(index1[0])+"+"
 index2=list3.curselection()
 if len(index2)>int(0):
    selected_items = [list3.get(i) for i in index2]
    for i in range(0,len(selected_items)):
        item=item+"_"+selected_items[i]
    four_w_list_all.append(item)
    list2.selection_clear(0,tk.END) 
    list3.selection_clear(0,tk.END) 
 
def open_last_window(next_w,e1,e2,e3):
 global three_w_entry1
 global three_w_entry2
 global three_w_entry3
 three_w_entry1=e1.get()
 three_w_entry2=e2.get()
 three_w_entry3=e3.get() 
 print(three_w_entry1+"  "+three_w_entry2+" "+three_w_entry3)
 next_w.destroy()
 last_w=tk.Tk()
 last_w.title("fix devices for config")
 last_w.geometry("600x600") 
 tk.Label(last_w,text='select device applied acl').pack(pady=10) 
 scrollbar1=tk.Scrollbar(last_w)
 #scrollbar1.pack(side=RIGHT,fill=Y)
 list2=tk.Listbox(last_w,yscrollcommand=scrollbar1.set,selectmode=tk.MULTIPLE,exportselection=False)
 array2=["sw1","sw2","sw3"]
 for value in array2: 
     list2.insert(tk.END,value)
 #list2.pack(side=LEFT, fill=BOTH)
 scrollbar1.config(command=list2.yview)
 list2.pack(padx=10,pady=5,fill=tk.BOTH, expand=True)
 #list2.grid(row=0,column=0)
 tk.Label(last_w,text='select interface applied acl').pack(pady=10) 
 scrollbar2=tk.Scrollbar(last_w)
 #scrollbar2.pack(side=RIGHT,fill=Y)
 list3=tk.Listbox(last_w,yscrollcommand=scrollbar2.set,selectmode=tk.MULTIPLE,exportselection=False)
 array3=["int1","int2","int3","int4","int5","int6"]
 for value in array3: 
     list3.insert(tk.END,value)
 #list3.pack(side=LEFT, fill=BOTH)
 scrollbar2.config(command=list2.yview)
 list3.pack(padx=10,pady=5,fill=tk.BOTH, expand=True)
 #list3.grid(row=1,column=0)
 button3=tk.Button(last_w,text="add other device",command=lambda: collect_device(last_w,list2,list3))
 button3.pack(pady=10)
 button4=tk.Button(last_w,text="save",command=lambda: read2(last_w))
 button4.pack(pady=10)
 last_w.mainloop()
 
def open_next_window(first_w,list1):
 global one_w_list
    
 index=list1.curselection()
 if len(index)!=int(0):
       one_w_list=list1.get(index[0])
       print(one_w_list)
       first_w.destroy()
       next_w=tk.Tk()
       next_w.title("fix config attribute info")
       next_w.geometry("350x400")
       if one_w_list=="deploy acl security policy":
           tk.Label(next_w,text="input acl name and select worked subnet")
           tk.Label(next_w,text='acl name').grid(row=0)
           tk.Label(next_w,text='acl subnet').grid(row=1)
           tk.Label(next_w,text='acl port').grid(row=2)
           e1=tk.Entry(next_w)
           #e1.pack(pady=5)
           e2=tk.Entry(next_w)
           #e2.pack(pady=5)
           e3=tk.Entry(next_w)
           #e3.pack(pady=5) 
           e1.grid(row=0,column=1)
           e2.grid(row=1,column=1)
           e3.grid(row=2,column=1) 
           button2=tk.Button(next_w,text="save",command=lambda: open_last_window(next_w,e1,e2,e3))
           button2.grid(row=3,column=2)
           #button2.pack(pady=20)
       if one_w_list=="deploy layer 2 trunk port resillence":
           tk.Label(next_w,text='port channel name').pack(pady=10)
           e1=tk.Entry(next_w)
           e1.pack(pady=10)
           var1=tk.IntVar()
           var1.set(1)
           C1 = Checkbutton(next_w, text = "deploy on all switch ", variable = var1, \
              onvalue = 1, offvalue = 0, height=5, \
               width = 20, )
           #check1=tk.Checkbutton(next_w,text='deploy on all switch in layer 2 traffic if no port channel', variable=var1 \
                 #onvalue = 1, offvalue = 0, height=5, \
                # width = 20, )
           C1.pack()
           button2=tk.Button(next_w,text="save",command=lambda: read1(next_w,e1,var1))
           button2.pack(pady=20)
       next_w.mainloop()

def create_first_window():

 first_w=tk.Tk()
 first_w.title("network deploy info input")
 first_w.geometry("350x400")
 
 tk.Label(first_w,text="select deploy operation type").pack(pady=10)
 
 list1=tk.Listbox(first_w,height=6,width=20)
 list1.pack(padx=10,pady=5)

 array1=["deploy acl security policy","deploy layer 2 trunk port resillence"]
 
 for value in array1:
     list1.insert(tk.END,value)
 button1=tk.Button(first_w,text="select",command=lambda: open_next_window(first_w,list1))
 button1.pack(pady=20)
 first_w.mainloop()
 
if __name__== "__main__":
    create_first_window()