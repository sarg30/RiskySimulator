import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import numpy

lines = [] #initial data processing array to remove comments
each = [] #after stripping each line of commas and whitespace
datasection=[] #seperate data section
textsection=[] #seperate text section
jumpdict = {} # used to keep track of all labels and their line number

#function to seperate data and text section
def sepeartedatasec(each):
    global datasection, textsection
    count = 0
    for i in each:
        if i[0] == '.text':
            break
        else:
            count = count+1
    datasection = each[:count]
    textsection = each[count:]

#function to make jumpdict
def makejumpdict(each):
    counter = 0
    for i in each:
        counter = counter+1
        if i[0].find(":") != -1:
            s = i[0]
            # print(s)
            jumpdict[s] = counter
    return jumpdict

#function to remove commas and whitespace
def decodeinstruct(line):
    linelist = [x.strip() for x in line.split(',')]
    res = []
    for i in linelist:
        i = [x.strip() for x in i.split(' ')]
        for k in i:
            if len(k) > 0:
                res. append(k)
    each.append(res)

#function to take input
def takeinput(files):
    global mem,pc
    mem =0
    pc=0
    file = open(files, 'r')
    content = file.readlines()
    file.close()
    lines.clear()
    for line in content:
        line = line.strip()
        if len(line) != 0 and line[0] != '#':
            seperate = ''
            for i in line:
                if i == '#':
                    break
                else:
                    seperate = seperate+i
            if len(seperate) != 0:
                seperate = seperate.strip()
                lines.append(seperate)
    each.clear()
    for i in lines:
        decodeinstruct(i)
    sepeartedatasec(each)
    makejumpdict(textsection)
    return datasection, textsection, jumpdict


memdict = {} # keeps track of memory labels and their indices in memory
mem=0 # mem variable to keep track of memory size occupied till now
memory = numpy.empty(4096, dtype=object)#memory section

registers=[ "zero","ra","sp","gp","tp","t0","t1","t2","s0","s1","a0",
            "a1","a2","a3","a4","a5","a6","a7","s2","s3","s4","s5",
            "s6","s7","s8","s9", "s10","s11", "t3","t4","t5","t6"]

#Assigning indices to each register
Register_index = {
    "zero": 0,"ra": 1,"sp": 2,"gp": 3,"tp": 4,"t0": 5,"t1": 6,"t2": 7,"s0": 8,
    "fp": 8,"s1": 9,"a0": 10,"a1": 11,"a2": 12,"a3": 13,"a4": 14,"a5": 15,"a6": 16,
    "a7": 17,"s2": 18,"s3": 19,"s4": 20,"s5": 21,"s6": 22,"s7": 23,"s8": 24,"s9": 25,
    "s10": 26, "s11": 27,"t3": 28,"t4": 29,"t5": 30,"t6": 31,
}
global pc
pc = 0
#function to insert data section to memory
def insertdatatomemory(datasection):
    global mem
    for i in datasection:
        if len(i)>2 and i[0].find(":") != -1 and i[1]==".word":
            memdict[i[0]]=mem
            for j in range(len(i)):
                if j>1:
                    memory[mem]=i[j]
                    mem=mem+1

#Functions related to processing different types of instructions and returning required registers, labels and constants
def process_R_type(line):
    """
    This function is to return
    the memory addresses of 
    the registers for R-type instructions
    """
    return line[1], line[2], line[3]

def process_I_type(line):
    """
    This function is to return the registers and
    the constants given with I type instructions
    """
    return line[1],line[2],line[3]

def process_B_type(line):
    """
    This function is to return the registers and labels
    corresponding to the B type instructions
    """
    return line[1],line[2],line[3]

def process_J_type(line):
    """
    returns labels related to J type instructions
    """
    return line[1]



#Functions related to processing load and save instructions
def la(line):
    """
    This function is to return the start address
    of the variable stored in memory
    """
    global pc
    rd, rs2 = line[1], line[2]
    index = memdict[rs2+":"]
    RegisterVals[Register_index[rd]]=index*4
    pc=pc+1

def li(line):
    """
    This function is to load the integer into memory
    """
    global pc
    rd, rs2 = line[1], line[2]
    RegisterVals[Register_index[rd]]=int(rs2)
    pc=pc+1

def lw(line):
    """
    This function loads word from memory into register
    """
    global pc
    # lw rd, offset_12(base)
    rd, rs2 = line[1], line[2]
    linelist = [x.strip() for x in rs2.split('(')]
    offset = linelist[0]
    linelist = [x.strip() for x in linelist[1].split(')')]
    base = linelist[0]
    rs2 = int(offset)//4+RegisterVals[Register_index[base]]//4
    RegisterVals[Register_index[rd]]=memory[rs2]
    pc = pc+1


def sw(line):
    """
    This function loads word from register into memory
    """
    global pc
    #sw rd, offset_12(base)
    rd,rs2=line[1],line[2]
    linelist = [x.strip() for x in rs2.split('(')]
    offset = linelist[0]
    linelist = [x.strip() for x in linelist[1].split(')')]
    base = linelist[0]
    rs2 = int(offset)//4+RegisterVals[Register_index[base]]//4
    memory[rs2]=RegisterVals[Register_index[rd]]
    pc=pc+1


#Functions related to processing branching instructions

def beq(line):

    global pc
    rs1, rs2, nextaddress = process_B_type(line) 
    if RegisterVals[Register_index[rs1]] == RegisterVals[Register_index[rs2]]:
        pc = jumpdict[nextaddress+":"]
    else:
        pc = pc+1


def bne(line):

    global pc
    rs1, rs2, nextaddress = process_B_type(line)
    if RegisterVals[Register_index[rs1]] != RegisterVals[Register_index[rs2]] :
        pc = jumpdict[nextaddress+":"]
    else:
        pc = pc+1

def ble(line):

    global pc
    rs1, rs2, nextaddress = process_B_type(line)
    #print(RegisterVals[Register_index[rs1]])
    #print(RegisterVals[Register_index[rs2]])
    print(memory[0:mem])
    if int(RegisterVals[Register_index[rs1]])<= int(RegisterVals[Register_index[rs2]]) :
        pc = jumpdict[nextaddress+":"]
    else:
        pc = pc+1
    
# Funtions related to processing Instructions related to arithmetic operations

def add(line):
    global pc
    """
    This function processes the
    add instruction of risc-v
    """
    rd, rs1, rs2 = process_R_type(line)
    RegisterVals[Register_index[rd]] = RegisterVals[Register_index[rs1]] + RegisterVals[Register_index[rs2]]
    print( RegisterVals[Register_index[rd]])
    pc = pc+1


def sub(line):
    global pc
    """
    This function processes the 
    sub instruction of risc-v
    """
    rd, rs1, rs2 = process_R_type(line)
    RegisterVals[Register_index[rd]] = RegisterVals[Register_index[rs1]] -  RegisterVals[Register_index[rs2]]
    pc = pc+1


def addi(line):

    global pc
    sum = 0
    rd, rs1, rs2 = process_I_type(line)
    if is_register(rs1):
        sum = sum+RegisterVals[Register_index[rs1]]
    else:
        sum = sum+int(rs1)
    if is_register(rs2):
        sum = sum+RegisterVals[Register_index[rs2]]
    else:
        sum = sum+int(rs2)
    #print(sum)
    RegisterVals[Register_index[rd]] = sum
    pc = pc+1


def shift_left_logical(line):
    global pc
    """
    This function processes the
    sll instruction of risc-v
    """
    rd, rs1, rs2 = process_R_type(line)
    RegisterVals[Register_index[rd]] = (RegisterVals[Register_index[rs1]]) << (
        RegisterVals[Register_index[rs2]])
    pc = pc+1


#Functions related to jump instructions

def jal(line):
    global pc
    nextaddress=line[1]+":"
    pc=jumpdict[nextaddress]


# checks whether the input is a register or a constant word
def is_register(line): 
    for registers in Register_index:
        if line == registers:
            return True
    return False


# initializing the values in all registers as 0
RegisterVals = []
for i in range(32):
    RegisterVals.append(0)



def print_register_vals():
    for i in Register_index:
        print(i, RegisterVals[Register_index[i]])

#to perform single step execution of the code
def single_step_execution():
    global pc
    line = textsection[pc]
    if line[0] == 'add':
        add(line)
    elif line[0] == 'addi':
        addi(line)
    elif line[0]=='sub':
        sub(line)
    elif line[0]=='jal':
        jal(line)
    elif line[0]=='bne':
        bne(line)
    elif line[0]=='lw':
        lw(line)
    elif line[0]=='sw':
        sw(line)
    elif line[0]=='la':
        la(line)
    elif line[0]=='ble':
        ble(line)
    elif line[0]=='li':
        li(line)
    elif line[0]=='beq':
        beq(line)
    elif line[0]=='sll':
        shift_left_logical(line)
    else:
        pc = pc+1
    #print_register_vals()

#to execute the whole code at once
def processfunction():
    global pc
    while pc != len(textsection):
        line = textsection[pc]
        if line[0] == 'add':
            add(line)
        elif line[0] == 'addi':
            addi(line)
        elif line[0]=='sub':
            sub(line)
        elif line[0]=='jal':
            jal(line)
        elif line[0]=='bne':
            bne(line)
        elif line[0]=='lw':
            lw(line)
        elif line[0]=='sw':
            sw(line)
        elif line[0]=='la':
            la(line)
        elif line[0]=='ble':
            ble(line)
        elif line[0]=='li':
            li(line)
        elif line[0]=='beq':
           beq(line)
        elif line[0]=='sll':
            shift_left_logical(line)
        else:
            pc = pc+1
        s="t2"
        #print(pc)
    #print_register_vals()
        

#---------------------------------------------------------------------------------------------------#        
#GUI SECTION UTILITY FUNCTIONS TO LOAD GUI 

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


def memsecloader():
    ele=""
    base=10010000
    for i in range(0,mem):
        ele = ele+"[0x"+str(base+4*i)+"]"+":  "+str(memory[i])
        ele = ele +"\n"
    return ele

class Table:
     
    def __init__(self,root):
         
        # code for creating table
        for i in range(32):
            for j in range(2):
                 
                self.e = Entry(root, width=27, fg='black',
                               font=('Helvetica',8,'bold'))
                if j == 0:
                    self.e.grid(row=i, column=j)
                    self.e.insert(END, registers[i])
                if j == 1:
                    self.e.grid(row=i, column=j)
                    self.e.insert(END, RegisterVals[i])


def settingvariables(tf):
    global  datasection,textsection,jumpdict
    datasection,textsection,jumpdict = takeinput(tf)
    insertdatatomemory(datasection)

              
def openFile():
    tf = filedialog.askopenfilename(
        initialdir="C:/Users/MainFrame/Desktop/",
        title="Open Text file",
        filetypes=(("Text Files", "*.txt"),)
    )
  
    settingvariables(tf)
    loadi()
    txtarea.delete("1.0", "end") 
    ele = convertostring(textsection)
    txtarea.insert(END, ele)
    txtarea2.delete("1.0", "end") 
    ele2=memsecloader()
    txtarea2.insert(END, ele2)
    


root = tk.Tk()
root.title("Risc-simulator")
root.geometry("1250x690")
root['bg'] = '#001233'


tabControl = ttk.Notebook(root)
style = ttk.Style()
style.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] ,"background": "gray"} },
        "TNotebook.Tab": {"configure": {"padding": [5, 5] }}})
style.theme_use("MyStyle")
swi = root.winfo_screenwidth()
sh = root.winfo_screenheight()
tab1 = Frame(tabControl,width=swi,height=sh,bg="#001233")
tab2 = Frame(tabControl,width=swi,height=sh,bg="#001233")


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
txtarea = tk.Text(paned_window1,font=("Helvetica",11,"bold"), width=65, height=17, yscrollcommand = vsb.set, bd = 7)
txtarea2 = tk.Text(paned_window1,font=("Helvetica",11,"bold"), width=40, height=17, yscrollcommand = vsb2.set, bd = 7)
txtarea3 = tk.Text(paned_window2,font=("Helvetica",11,"bold"), width=109, height=10, yscrollcommand = vsb3.set, bd = 7)



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

def loadi():
    for i in range(32):
        RegisterVals[i]=0
    global t
    t=Table(ctr_mid)

def reload():
    processfunction()
    txtarea2. delete("1.0", "end") 
    ele2=memsecloader()
    txtarea2.insert(END, ele2)
    global t
    t=Table(ctr_mid)

def reload2():
    single_step_execution()
    txtarea2.delete("1.0", "end") 
    ele2=memsecloader()
    txtarea2.insert(END, ele2)
    global t
    t=Table(ctr_mid)

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
    command=reload,
    width=20,
    height=1,
    bd=2
)
but3 = tk.Button(
   tab1,
    text="STEP BY STEP EXECUTION",
    command=reload2,
    width=20,
    height=1,
    bd=2
)

but.grid(row=1, column=0,sticky=W,padx=15,pady=10)
but2.grid(row=1, column=0,sticky=W,padx=120,pady=10)
but3.grid(row=1, column=0,sticky=W,padx=300,pady=10)
root.mainloop()




