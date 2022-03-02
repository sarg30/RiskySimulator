import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from userinstruct import  takeinput
#from main import RegisterVals
#print(RegisterVals)
registers=[ "zero","ra","sp","gp","tp","t0","t1","t2","s0","s1","a0",
            "a1","a2","a3","a4","a5","a6","a7","s2","s3","s4","s5",
            "s6","s7","s8","s9", "s10","s11", "t3","t4","t5","t6"]
class Table:
     
    def __init__(self,ws):
         
        # code for creating table
        for i in range(32):
            for j in range(2):
                 
                self.e = Entry(ws, width=30, fg='black',
                               font=('Helvetica',9,'bold'))
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
    ele =""
    count =0
    count2=0
    for i in textsection:
        count=count+1
        ele = ele + str(count) +" "
        for j in i:
            ele = ele+" "+j
        ele = ele +"\n"
        if count==1:
            count2=len(ele)
    txtarea.insert(END, ele)


ws = tk.Tk()

ws.title("Risc-simulator")
ws.geometry("1450x750")
ws['bg'] = '#001233'
tabControl = ttk.Notebook(ws)
style = ttk.Style()
style.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [5, 5] },}})

style.theme_use("MyStyle")
sw = ws.winfo_screenwidth()
sh = ws.winfo_screenheight()
tab1 = Frame(tabControl,width=sw,height=sh,bg="#001233")
tab2 = Frame(tabControl,width=sw,height=sh,bg="#001233")
ws.resizable(0,0)
tabControl.add(tab1, text ='STAGE 1')
tabControl.add(tab2, text ='STAGE 2')
tabControl.grid(column=0,row=0,sticky='nsew')


vsb = tk.Scrollbar(tab1, orient="vertical")
vsb.grid(row=1, column=2, sticky='ns')
txtarea = tk.Text(tab1,font=("Helvetica",11,"bold"), width=70, height=20, yscrollcommand = vsb.set, bd = 7)
txtarea.grid(row=1, column=1,sticky="ns")
ctr_mid = Frame(tab1)
ctr_mid.grid(row=1,column=0,sticky="ns")
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
    text="RUN",
    width=9,
    height=1,
    bd=2
)
vsb.config(command = txtarea.yview)
but.grid(row=3, column=0,sticky='w',padx=10,pady=10)
but2.grid(row=3, column=0,sticky='w',padx=100,pady=10)
ws.mainloop()
