import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from turtle import bgcolor
from userinstruct import  takeinput
#from main import RegisterVals
#print(RegisterVals)
registers=[ "zero","ra","sp","gp","tp","t0","t1","t2","s0","s1","a0",
            "a1","a2","a3","a4","a5","a6","a7","s2","s3","s4","s5",
            "s6","s7","s8","s9", "s10","s11", "t3","t4","t5","t6"]
def convertostring(textsection):
    ele =""
    count =0
    count2=0
    for i in textsection:
        count=count+1
        ele = ele + str(count) +":"+" "
        for j in i:
            ele = ele+" "+j
        ele = ele +"\n"
    if count==1:
        count2=len(ele)
    return ele
class Table:
     
    def __init__(self,root):
         
        # code for creating table
        for i in range(32):
            for j in range(4):
                 
                self.e = Entry(root, width=31, fg='black',
                               font=('Helvetica',8,'bold'))
                if j == 0:
                    self.e.grid(row=i, column=j)
                    self.e.insert(END, registers[i])
                if j == 1:
                    self.e.grid(row=i, column=j)
              
def openFile():
    tf = filedialog.askopenfilename(
        initialdir="C:/Users/MainFrame/Desktop/",
        title="Open Text file",
        filetypes=(("Text Files", "*.txt"),)
    )
    datasection,textsection,jumpdict = takeinput(tf)
    ele = convertostring(textsection)
    txtarea.insert(END, ele)
    ele2=convertostring(datasection)
    txtarea2.insert(END, ele2)
    


root = tk.Tk()
root.title("Risc-simulator")
root.geometry("1450x700")
root['bg'] = '#001233'


tabControl = ttk.Notebook(root)
style = ttk.Style()
style.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [5, 5] }}})
style.theme_use("MyStyle")
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
tab1 = Frame(tabControl,width=sw,height=sh,bg="#001233")
tab2 = Frame(tabControl,width=sw,height=sh,bg="#001233")


tabControl.add(tab1, text ='STAGE 1')
tabControl.add(tab2, text ='STAGE 2')
tabControl.grid(column=0,row=0,sticky='nsew')



paned_window1 = tk.PanedWindow(tab1, orient = tk.HORIZONTAL)
paned_window1.grid(row=3,column=0,sticky=NS)
paned_window2 = tk.PanedWindow(tab1, orient = tk.HORIZONTAL)
paned_window2.grid(row=5,column=0,sticky='nsew')
vsb = tk.Scrollbar(paned_window1, orient="vertical")
vsb2 = tk.Scrollbar(paned_window1, orient="vertical")
vsb3 = tk.Scrollbar(paned_window2, orient="vertical")
txtarea = tk.Text(paned_window1,font=("Helvetica",11,"bold"), width=80, height=20, yscrollcommand = vsb.set, bd = 7)
txtarea2 = tk.Text(paned_window1,font=("Helvetica",11,"bold"), width=44, height=20, yscrollcommand = vsb2.set, bd = 7)
txtarea3 = tk.Text(paned_window2,font=("Helvetica",11,"bold"), width=128, height=9, yscrollcommand = vsb3.set, bd = 7)

head = Label(tab1, text="CONSOLE", font=("Helvetica", 14),bg='gray')
head.grid(row=4,column=0,sticky='nsew')
head = Label(tab1, text="INPUT AND MEMORY SECTION", font=("Helvetica", 14),bg='gray')
head.grid(row=2,column=0,sticky='nsew')
head = Label(tab1, text="REGISTERS", font=("Helvetica", 14),bg='gray')
head.grid(row=2,column=1,sticky='nsew')
vsb.config(command = txtarea.yview)
vsb2.config(command = txtarea2.yview)
vsb3.config(command = txtarea3.yview)




paned_window1.add(txtarea)
paned_window1.add(vsb)
paned_window1.add(txtarea2)
paned_window1.add(vsb2)

paned_window2.add(txtarea3)
paned_window2.add(vsb3)
ctr_mid = Frame(tab1)
ctr_mid.grid(row=3,column=1,rowspan=3,sticky=NS)
t = Table(ctr_mid)
#tk.t.grid(row=0,column=1,sticky="ns")



but = tk.Button(
   tab1,
    text="OPEN FILE",
    command=openFile,
    width=9,
    height=1,
    bd=2
)
but2 = tk.Button(
   tab1,
    text="ONE STEP EXECUTION",
    width=20,
    height=1,
    bd=2
)
but3 = tk.Button(
   tab1,
    text="STEP BY STEP EXECUTION",
    width=20,
    height=1,
    bd=2
)

but.grid(row=1, column=0,sticky=W,padx=15,pady=10)
but2.grid(row=1, column=0,sticky=W,padx=120,pady=10)
but3.grid(row=1, column=0,sticky=W,padx=300,pady=10)
root.mainloop()
