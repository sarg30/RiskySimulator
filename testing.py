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
# memory = numpy.empty(4096, dtype=object)
memory = [0 for i in range (4096)]

last_wb = [0 for i in range (32)]                        #stores the latest cc for the wb stage for each register(used when data forwarding is disabled)
last_mem = [0 for i in range (32)]                       #stores the latest cc for the mem stage for each register(used when data forwarding is enabled)

rows,cols = (2000,2000)

df_enabled= [["     " for i in range(cols)] for j in range(rows)]           #stores the pipline stages when data forwarding is enabled
df_disabled = [["     " for i in range(cols)] for j in range(rows)]         #stores the pipline stafes when data forwarding is disabled


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

global inst_counter
inst_counter=1

global  cc_df_enabled
global  cc_df_disabled
cc_df_enabled=0
cc_df_disabled=0

is_stall_dfe = [0 for i in range (2000)]                     # 1 if the cc is a stall else 0
is_stall_dfne = [0 for i in range (2000)]                    # 1 if the cc is a stall else 0
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

# functions related to pipelining implementation for data forwarding disabled
def dfne_R_type(rd,rs1,rs2):
    """
    implements the pipeline stages corresponding to 
    R type instructions when data forwarding is disabled
    """
    global cc_df_disabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i= cc_df_disabled+1
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="IF   "
    cc_df_disabled=i
    i=i+1

    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfne[i]==1 or last_wb[Register_index[rs1]]>=i or last_wb[Register_index[rs2]]>=i:
        df_disabled[inst_counter][i]="STALL"
        is_stall_dfne[i]=1
        i=i+1
    df_disabled[inst_counter][i]="EXE  "
    df_disabled[inst_counter][i+1]="MEM  "
    df_disabled[inst_counter][i+2]="WB   "

    #updating the last WB clock cycle for the destination register
    last_wb[Register_index[rd]]=i+2


def dfne_addi(rd,rs1):
    """
    implements the pipeline stages corresponding to 
    addi instruction when data forwarding is disabled
    """
    global cc_df_disabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i=cc_df_disabled+1
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="IF   "
    cc_df_disabled=i
    i=i+1

    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfne[i]==1 or last_wb[Register_index[rs1]]>=i or last_wb[Register_index[rd]]>=i:
        df_disabled[inst_counter][i]="STALL"
        is_stall_dfne[i]=1
        i=i+1
    df_disabled[inst_counter][i]="EXE  "
    df_disabled[inst_counter][i+1]="MEM  "
    df_disabled[inst_counter][i+2]="WB   "

    #updating the last WB clock cycle for the destination register
    last_wb[Register_index[rd]]=i+2

def dfne_lw(rd,rs2):
    """
    implements the pipeline stages corresponding to lw 
    instructions when data forwarding is disabled
    """
    global cc_df_disabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i=cc_df_disabled+1
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="IF   "
    cc_df_disabled=i
    i=i+1

    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfne[i]==1 or last_wb[Register_index[rs2]]>=i:
        df_disabled[inst_counter][i]="STALL"
        is_stall_dfne[i]=1
        i=i+1
    df_disabled[inst_counter][i]="EXE  "
    df_disabled[inst_counter][i+1]="MEM  "
    df_disabled[inst_counter][i+2]="WB   "

    #updating the last WB clock cycle for the destination register
    last_wb[Register_index[rd]]=i+2



def dfne_sw(rd,rs2):
    """
    implements the pipeline stages corresponding to sw
    instruction when data forwarding is disabled
    """    
    global cc_df_disabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i=cc_df_disabled+1
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="IF   "
    cc_df_disabled=i
    i=i+1

    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfne[i]==1 or last_wb[Register_index[rd]]>=i or last_wb[Register_index[rs2]]>=i:
        df_disabled[inst_counter][i]="STALL"
        is_stall_dfne[i]=1
        i=i+1
    df_disabled[inst_counter][i]="EXE  "
    df_disabled[inst_counter][i+1]="MEM  "
    df_disabled[inst_counter][i+2]="WB   "
      #updating the last WB clock cycle for the destination register
    last_wb[Register_index[rd]]=i+2


def dfne_beq(rd,rs2,checker):
    """
    implements the pipeline stages corresponding to sw
    instruction when data forwarding is disabled
    """    
    global cc_df_disabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i=cc_df_disabled+1
    while is_stall_dfne[i]==1:
        i=i+1
    if checker == True:
        df_disabled[inst_counter][i]="STALL"
        i=i+1
    
    df_disabled[inst_counter][i]="IF   "
    #print(i)
    cc_df_disabled=i
    i=i+1
      
    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="ID/RF"
    #print(i)
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    #print(last_wb[Register_index[rs2]]);
    #print(last_wb[Register_index[rd]]);
    while is_stall_dfne[i]==1 or last_wb[Register_index[rd]]>=i or last_wb[Register_index[rs2]]>=i:
        df_disabled[inst_counter][i]="STALL"
        is_stall_dfne[i]=1
        i=i+1
    df_disabled[inst_counter][i]="EXE  "
    df_disabled[inst_counter][i+1]="MEM  "
    df_disabled[inst_counter][i+2]="WB   "


def dfne_bne(rd,rs2,checker):
    """
    implements the pipeline stages corresponding to sw
    instruction when data forwarding is disabled
    """    
    global cc_df_disabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i=cc_df_disabled+1
    while is_stall_dfne[i]==1:
        i=i+1
    if checker == True:
        df_disabled[inst_counter][i]="STALL"
        i=i+1
    
    df_disabled[inst_counter][i]="IF   "
    cc_df_disabled=i
    i=i+1
      
    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfne[i]==1 or last_wb[Register_index[rd]]>=i or last_wb[Register_index[rs2]]>=i:
        df_disabled[inst_counter][i]="STALL"
        is_stall_dfne[i]=1
        i=i+1
    df_disabled[inst_counter][i]="EXE  "
    df_disabled[inst_counter][i+1]="MEM  "
    df_disabled[inst_counter][i+2]="WB   "


def dfne_ble(rd,rs2,checker):
    """
    implements the pipeline stages corresponding to sw
    instruction when data forwarding is disabled
    """    
    global cc_df_disabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i= cc_df_disabled+1

    while is_stall_dfne[i]==1:
        i=i+1
    if checker == True:
        df_disabled[inst_counter][i]="STALL"
        i=i+1
    
    df_disabled[inst_counter][i]="IF   "
    cc_df_disabled=i
    i=i+1
      
    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfne[i]==1 or last_wb[Register_index[rd]]>=i or last_wb[Register_index[rs2]]>=i:
        df_disabled[inst_counter][i]="STALL"
        is_stall_dfne[i]=1
        i=i+1
    df_disabled[inst_counter][i]="EXE  "
    df_disabled[inst_counter][i+1]="MEM  "
    df_disabled[inst_counter][i+2]="WB   "


def dfne_li(rd):
    """
    implements the pipeline stages corresponding to li
    instruction when data forwarding is disabled
    """    
    global cc_df_disabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i= cc_df_disabled+1
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="IF   "
    cc_df_disabled=i
    i=i+1

    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfne[i]==1 or last_wb[Register_index[rd]]>=i:
        df_disabled[inst_counter][i]="STALL"
        is_stall_dfne[i]=1
        i=i+1
    df_disabled[inst_counter][i]="EXE  "
    df_disabled[inst_counter][i+1]="MEM  "
    df_disabled[inst_counter][i+2]="WB   "
      #updating the last WB clock cycle for the destination register
    last_wb[Register_index[rd]]=i+2


def dfne_la(rd):
    """
    implements the pipeline stages corresponding to la 
    instructions when data forwarding is enabled
    """
    global cc_df_disabled
    global inst_counter

    #searching for which clock cycle to impelement IF stage
    i= cc_df_disabled+1
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="IF   "
    cc_df_disabled=i
    i=i+1

    #searching for the clock cycle to implement the ID/RF stage
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="ID/RF"
    i=i+1

    #checking for stalls and then impelmenting the EXE,MEM,WB stages
    while is_stall_dfne[i]==1:
        df_disabled[inst_counter][i]="STALL"
        is_stall_dfne[i]=1
        i=i+1
    df_disabled[inst_counter][i]="EXE  "
    df_disabled[inst_counter][i+1]="MEM  "
    df_disabled[inst_counter][i+2]="WB   "

    #updating the last MEM clock cycle for the destination register
    last_mem[Register_index[rd]]=i+1


def dfne_jal():
    """
    implements the pipeline stages corresponding to sw
    instruction when data forwarding is disabled
    """    
    global cc_df_disabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i= cc_df_disabled+1
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="IF   "
    cc_df_disabled=i
    i=i+1

    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfne[i]==1:
        i=i+1
    df_disabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfne[i]==1:
        df_disabled[inst_counter][i]="STALL"
        is_stall_dfne[i]=1
        i=i+1
    df_disabled[inst_counter][i]="EXE  "
    df_disabled[inst_counter][i+1]="MEM  "
    df_disabled[inst_counter][i+2]="WB   "



#fucntions related to pipelining implementation for data forwarding enabled


def dfe_R_type(rd,rs1,rs2):
    """
    implements the pipeline stages corresponding to 
    R type instructions when data forwarding is enabled
    """
    global cc_df_enabled
    global inst_counter

    #searching for which clock cycle to impelement IF stage
    i= cc_df_enabled+1
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="IF   "
    cc_df_enabled=i
    i=i+1

    #searching for the clock cycle to implement the ID/RF stage
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="ID/RF"
    i=i+1

    #checking for dependencies and stalls and then impelmenting the EXE,MEM,WB stages
    while is_stall_dfe[i]==1 or last_mem[Register_index[rs1]]>=i or last_mem[Register_index[rs2]]>=i:
        df_enabled[inst_counter][i]="STALL"
        is_stall_dfe[i]=1
        i=i+1
    df_enabled[inst_counter][i]="EXE  "
    df_enabled[inst_counter][i+1]="MEM  "
    df_enabled[inst_counter][i+2]="WB   "

    #updating the last MEM clock cycle for the destination register
    # last_mem[Register_index[rd]]=i+1


def dfe_addi(rd,rs1):
    """
    implements the pipeline stages corresponding to 
    addi instruction when data forwarding is enabled
    """
    global cc_df_enabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i= cc_df_enabled+1
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="IF   "
    cc_df_enabled=i
    i=i+1

    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfe[i]==1:
        i=i+1
    
    df_enabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfe[i]==1 or last_mem[Register_index[rs1]]>=i or last_mem[Register_index[rd]]>=i:
        df_enabled[inst_counter][i]="STALL"
        is_stall_dfe[i]=1
        i=i+1
    df_enabled[inst_counter][i]="EXE  "
    df_enabled[inst_counter][i+1]="MEM  "
    df_enabled[inst_counter][i+2]="WB   "

    #updating the last WB clock cycle for the destination register
    last_mem[Register_index[rd]]=i+2


def dfe_lw(rd,rs2):
    """
    implements the pipeline stages corresponding to lw 
    instructions when data forwarding is enabled
    """
    global cc_df_enabled
    global inst_counter

    #searching for which clock cycle to impelement IF stage
    i = cc_df_enabled+1
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="IF   "
    cc_df_enabled=i
    i=i+1

    #searching for the clock cycle to implement the ID/RF stage
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="ID/RF"
    i=i+1

    #checking for dependencies and stalls and then impelmenting the EXE,MEM,WB stages
    while is_stall_dfe[i]==1 or last_mem[Register_index[rs2]]>=i:
        df_enabled[inst_counter][i]="STALL"
        is_stall_dfe[i]=1
        i=i+1
    df_enabled[inst_counter][i]="EXE  "
    df_enabled[inst_counter][i+1]="MEM  "
    df_enabled[inst_counter][i+2]="WB   "

    #updating the last MEM clock cycle for the destination register
    last_mem[Register_index[rd]]=i+1


def dfe_li(rd):
    """
    implements the pipeline stages corresponding to lw 
    instructions when data forwarding is enabled
    """
    global cc_df_enabled
    global inst_counter

    #searching for which clock cycle to impelement IF stage
    i= cc_df_enabled+1
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="IF   "
    cc_df_enabled=i
    i=i+1

    #searching for the clock cycle to implement the ID/RF stage
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="ID/RF"
    i=i+1

    #checking for dependencies and stalls and then impelmenting the EXE,MEM,WB stages
    while is_stall_dfe[i]==1 or last_mem[Register_index[rd]]>=i:
        df_enabled[inst_counter][i]="STALL"
        is_stall_dfe[i]=1
        i=i+1
    df_enabled[inst_counter][i]="EXE  "
    df_enabled[inst_counter][i+1]="MEM  "
    df_enabled[inst_counter][i+2]="WB   "

    #updating the last MEM clock cycle for the destination register
    last_mem[Register_index[rd]]=i+1


def dfe_jal():
    """
    implements the pipeline stages corresponding to jal
    instruction when data forwarding is enabled
    """    
    global cc_df_enabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i=cc_df_enabled+1
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="IF   "
    cc_df_enabled=i
    i=i+1

    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfe[i]==1:
        df_enabled[inst_counter][i]="STALL"
        is_stall_dfe[i]=1
        i=i+1
    df_enabled[inst_counter][i]="EXE  "
    df_enabled[inst_counter][i+1]="MEM  "
    df_enabled[inst_counter][i+2]="WB   "


def dfe_la(rd):
    """
    implements the pipeline stages corresponding to la 
    instructions when data forwarding is enabled
    """
    global cc_df_enabled
    global inst_counter

    #searching for which clock cycle to impelement IF stage
    i= cc_df_enabled+1
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="IF   "
    cc_df_enabled=i
    i=i+1

    #searching for the clock cycle to implement the ID/RF stage
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="ID/RF"
    i=i+1

    #checking for stalls and then impelmenting the EXE,MEM,WB stages
    while is_stall_dfe[i]==1:
        df_enabled[inst_counter][i]="STALL"
        is_stall_dfe[i]=1
        i=i+1
    df_enabled[inst_counter][i]="EXE  "
    df_enabled[inst_counter][i+1]="MEM  "
    df_enabled[inst_counter][i+2]="WB   "

    #updating the last MEM clock cycle for the destination register
    last_mem[Register_index[rd]]=i+1


def dfe_sw(rd,rs2):
    """
    implements the pipeline stages corresponding to sw 
    instructions when data forwarding is enabled
    """
    global cc_df_enabled
    global inst_counter

    #searching for which clock cycle to impelement IF stage
    i = cc_df_enabled+1
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="IF   "
    cc_df_enabled=i
    i=i+1

    #searching for the clock cycle to implement the ID/RF stage
    while is_stall_dfe[i]:
        i=i+1
    df_enabled[inst_counter][i]="ID/RF"
    i=i+1

    #checking for dependencies and stalls and then impelmenting the EXE,MEM,WB stages
    while is_stall_dfe[i] or last_mem[Register_index[rs2]]>=i or last_mem[Register_index[rd]]>=i:
        df_enabled[inst_counter][i]="STALL"
        is_stall_dfe[i]=1
        #print(i)
        i=i+1
    df_enabled[inst_counter][i]="EXE  "
    df_enabled[inst_counter][i+1]="MEM  "
    df_enabled[inst_counter][i+2]="WB   "

    #updating the last MEM clock cycle for the destination register
    last_mem[Register_index[rd]]=i+1


def dfe_beq(rd,rs2,checker):
    """
    implements the pipeline stages corresponding to beq
    instruction when data forwarding is enabled
    """    
    global cc_df_enabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i= cc_df_enabled+1
    while is_stall_dfe[i]==1:
        i=i+1
    if checker == True:
        df_enabled[inst_counter][i]="STALL"
        i=i+1
    
    df_enabled[inst_counter][i]="IF   "
    cc_df_enabled=i
    i=i+1
      
    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfe[i]==1 or last_mem[Register_index[rd]]>=i or last_mem[Register_index[rs2]]>=i:
        df_enabled[inst_counter][i]="STALL"
        is_stall_dfe[i]=1
        i=i+1
    df_enabled[inst_counter][i]="EXE  "
    df_enabled[inst_counter][i+1]="MEM  "
    df_enabled[inst_counter][i+2]="WB   "


def dfe_bne(rd,rs2,checker):
    """
    implements the pipeline stages corresponding to bne
    instruction when data forwarding is enabled
    """    
    global cc_df_enabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i= cc_df_enabled+1
    while is_stall_dfe[i]==1:
        i=i+1
    if checker == True:
        df_enabled[inst_counter][i]="STALL"
        i=i+1
    
    df_enabled[inst_counter][i]="IF   "
    cc_df_enabled=i
    i=i+1
      
    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfe[i]==1 or last_mem[Register_index[rd]]>=i or last_mem[Register_index[rs2]]>=i:
        df_enabled[inst_counter][i]="STALL"
        is_stall_dfe[i]=1
        i=i+1
    df_enabled[inst_counter][i]="EXE  "
    df_enabled[inst_counter][i+1]="MEM  "
    df_enabled[inst_counter][i+2]="WB   "


def dfe_ble(rd,rs2,checker):
    """
    implements the pipeline stages corresponding to sw
    instruction when data forwarding is disabled
    """    
    global cc_df_enabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i= cc_df_enabled+1
    while is_stall_dfe[i]==1:
        i=i+1
    if checker == True:
        df_enabled[inst_counter][i]="STALL"
        i=i+1
    
    df_enabled[inst_counter][i]="IF   "
    cc_df_enabled=i
    i=i+1
      
    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="ID/RF"
    i=i+1

    # checking for dependencies and stalls and then implementing the EXE, MEM and WB stages
    while is_stall_dfe[i]==1 or last_mem[Register_index[rd]]>=i or last_mem[Register_index[rs2]]>=i:
        df_enabled[inst_counter][i]="STALL"
        is_stall_dfe[i]=1
        i=i+1
    df_enabled[inst_counter][i]="EXE  "
    df_enabled[inst_counter][i+1]="MEM  "
    df_enabled[inst_counter][i+2]="WB   "


#Functions related to processing different types of instructions and returning required registers, labels and constants

def process_R_type(line):
    """
    This function is to return
    the memory addresses of 
    the registers for R-type instructions
    """
    dfne_R_type(line[1],line[2],line[3])
    dfe_R_type(line[1],line[2],line[3])
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
    global pc
    global inst_counter
    rd, rs2 = line[1], line[2]
    dfe_la(rd)
    dfne_la(rd)
    inst_counter=inst_counter+1
    index = memdict[rs2+":"]
    RegisterVals[Register_index[rd]]=index*4
    pc=pc+1

def li(line):
    global pc
    global inst_counter
    rd, rs2 = line[1], line[2]
    dfne_li(rd)
    dfe_li(rd)
    RegisterVals[Register_index[rd]]=int(rs2)
    inst_counter=inst_counter+1
    pc=pc+1
   

def lw(line):
    global pc
    # lw rd, offset_12(base)
    rd, rs2 = line[1], line[2]
    global inst_counter
    linelist = [x.strip() for x in rs2.split('(')]
    offset = linelist[0]
    linelist = [x.strip() for x in linelist[1].split(')')]
    base = linelist[0]
    rs2 = int(offset)//4+int(RegisterVals[Register_index[base]])//4
    dfne_lw(rd,base)
    dfe_lw(rd,base)
    inst_counter=inst_counter+1
    RegisterVals[Register_index[rd]]=memory[rs2]
    pc = pc+1


def sw(line):
    global pc
    #sw rd, offset_12(base)
    rd,rs2=line[1],line[2]
    global inst_counter
    linelist = [x.strip() for x in rs2.split('(')]
    offset = linelist[0]
    linelist = [x.strip() for x in linelist[1].split(')')]
    base = linelist[0]
    dfne_sw(rd,base)
    dfe_sw(rd,base)
    inst_counter=inst_counter+1
    rs2 = int(offset)//4+int(RegisterVals[Register_index[base]])//4
    memory[rs2]=RegisterVals[Register_index[rd]]
    pc=pc+1


#Functions related to processing branching instructions

def beq(line):
    global pc
    global inst_counter
    rs1, rs2, nextaddress = process_B_type(line) 
    predictor = False
    if RegisterVals[Register_index[rs1]] == RegisterVals[Register_index[rs2]]:
        predictor = True
        pc = jumpdict[nextaddress+":"]
    else:
        pc = pc+1
    dfne_beq(rs1,rs2,predictor)
    dfe_beq(rs1,rs2,predictor)
    inst_counter=inst_counter+1


def bne(line):
    global pc
    global inst_counter
    rs1, rs2, nextaddress = process_B_type(line)
    
    predictor = False
    if RegisterVals[Register_index[rs1]] != RegisterVals[Register_index[rs2]] :
        predictor = True
        pc = jumpdict[nextaddress+":"]
    else:
        pc = pc+1
    dfne_bne(rs1,rs2,predictor)
    dfe_bne(rs1,rs2,predictor)
    inst_counter=inst_counter+1


def ble(line):
    global pc
    global inst_counter
    rs1, rs2, nextaddress = process_B_type(line)
    #print(RegisterVals[Register_index[rs1]])
    #print(RegisterVals[Register_index[rs2]])
    predictor = False
    #print(memory[0:mem])
    if int(RegisterVals[Register_index[rs1]])<= int(RegisterVals[Register_index[rs2]]):
        predictor = True
        pc = jumpdict[nextaddress+":"]
    else:
        pc = pc+1
    dfne_ble(rs1,rs2,predictor)
    dfe_ble(rs1,rs2,predictor)
    inst_counter=inst_counter+1
    
# Funtions related to processing Instructions related to arithmetic operations

def add(line):
    global pc
    """
    This function processes the
    add instruction of risc-v
    """
    global inst_counter
    rd, rs1, rs2 = process_R_type(line)
    RegisterVals[Register_index[rd]] = int(RegisterVals[Register_index[rs1]]) + (RegisterVals[Register_index[rs2]])
    inst_counter=inst_counter+1
    pc = pc+1


def sub(line):
    global pc
    """
    This function processes the 
    sub instruction of risc-v
    """
    global inst_counter
    rd, rs1, rs2 = process_R_type(line)
    inst_counter=inst_counter+1
    RegisterVals[Register_index[rd]] = int(RegisterVals[Register_index[rs1]]) -  int(RegisterVals[Register_index[rs2]])
    pc = pc+1


def addi(line):
    global pc
    global inst_counter
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
    dfne_addi(rd,rs1)
    dfe_addi(rd,rs1)
    inst_counter=inst_counter+1
    #print(sum)
    RegisterVals[Register_index[rd]] = sum
    pc = pc+1


def shift_left_logical(line):
    global pc
    global inst_counter
    """
    This function processes the
    sll instruction of risc-v
    """
    rd, rs1, rs2 = process_R_type(line)
    inst_counter=inst_counter+1
    RegisterVals[Register_index[rd]] = (RegisterVals[Register_index[rs1]]) << (
        RegisterVals[Register_index[rs2]])
    pc = pc+1


#Functions related to jump instructions

def jal(line):
    global pc
    global inst_counter
    nextaddress=line[1]+":"
    pc=jumpdict[nextaddress]
    dfne_jal()
    dfe_jal()
    inst_counter=inst_counter+1

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



# def print_register_vals():
#     for i in Register_index:
#         print(i, RegisterVals[Register_index[i]])

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
global dfe_cycles,dfne_cycles,dfe_stalls,dfne_stalls
dfe_cycles=0            # the number of clock cycles taken when data forwarding is enabled
dfne_cycles=0           # the number of clock cycles taken when data forwarding is disabled
dfe_stalls=0            # the number of stalls when data forwarding is enabled
dfne_stalls=0           # the number of stalls when data forwarding is disabled



def dopipeline():
    global dfe_cycles,dfne_cycles,dfe_stalls,dfne_stalls
    for i in range(cols):
        if df_disabled[inst_counter-1][i]!="     ":
            dfne_cycles=i
        if df_enabled[inst_counter-1][i]!="     ":
            dfe_cycles=i
        if is_stall_dfe[i]==1:
            dfe_stalls=dfe_stalls+1
        if(is_stall_dfne[i]==1):
            dfne_stalls=dfne_stalls+1



def printnondataforwarding():
    global dfne_cycles,dfne_stalls
    for i in range(inst_counter+1):
        for j in range(1,dfne_cycles):
            if i==0:
                cc= str(j)
                while(len(cc)<5):
                    cc="0"+cc
                df_disabled[i][j]=cc
            txtarea4.insert(END,df_disabled[i][j]+"\t")
        txtarea4.insert(END,"\n")


def printdataforwarding():
    global dfe_cycles,dfe_stalls
    for i in range(inst_counter+1):
        for j in range(1,dfe_cycles):
            if i==0:
                cc= str(j)
                while(len(cc)<5):
                    cc="0"+cc
                df_enabled[i][j]=cc
            txtarea5.insert(END,df_enabled[i][j]+"\t")
        txtarea5.insert(END,"\n")    
        


def printCycles():
    global dfe_cycles,dfne_cycles,dfe_stalls,dfne_stalls
    #printing the pipeline for data forwarding disabled
    txtarea3.insert(END,"The pipeline for data forwarding disabled is as follows: ")
    txtarea3.insert(END,"\n")
    txtarea3.insert(END,"The number of stalls is: ")
    txtarea3.insert(END,dfne_stalls)
    txtarea3.insert(END,"\n")
    txtarea3.insert(END,"IPC value is: ")
    txtarea3.insert(END,(inst_counter-1)/dfne_cycles)

    txtarea3.insert(END,"\n")
    txtarea3.insert(END,"\n")
    txtarea3.insert(END,"\n")

    #printing the pipeline for data forwarding enabled
    txtarea3.insert(END,"The pipeline for data forwarding enabled is as follows: ")
    txtarea3.insert(END,"\n")
    txtarea3.insert(END,"The number of stalls is: ")
    txtarea3.insert(END,dfe_stalls)
    txtarea3.insert(END,"\n")
    txtarea3.insert(END,"IPC value is: ")
    txtarea3.insert(END,(inst_counter-1)/dfe_cycles)

#---------------------------------------------------------------------------------------------------#        
#GUI SECTION UTILITY FUNCTIONS TO LOAD GUI 
prevVal = RegisterVals.copy()


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
        global prevVal
        for i in range(32):
            for j in range(2):
                 
                self.e = Entry(root, width=27, fg='black',
                               font=('Helvetica',8,'bold'))
                if j == 0:
                    self.e.grid(row=i, column=j)
                    if prevVal[i]!=RegisterVals[i]:
                        self.e.insert(END, registers[i])
                        self.e.config(bg="lightblue")
                    else:
                        self.e.insert(END, registers[i])
                if j == 1:
                    self.e.grid(row=i, column=j)
                    if prevVal[i]!=RegisterVals[i]:
                        self.e.insert(END, RegisterVals[i])
                        self.e.config(bg="lightblue")
                    else:
                        self.e.insert(END, RegisterVals[i])
        prevVal = RegisterVals.copy()

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
root.resizable(True,True)

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
tab3 = Frame(tabControl,width=swi,height=sh,bg="#001233")


tabControl.add(tab1, text ='SIMULATOR')
tabControl.add(tab2, text ='DATA NON-FORWARDING')
tabControl.add(tab3, text ='DATA FORWARDING')
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

paned_window3 = tk.PanedWindow(tab2, orient = tk.HORIZONTAL)
paned_window3.grid(row=3,column=0,sticky=NS)
paned_window4 = tk.PanedWindow(tab2, orient = tk.VERTICAL)
paned_window4.grid(row=4,column=0,sticky=EW)

paned_window5 = tk.PanedWindow(tab3, orient = tk.HORIZONTAL)
paned_window5.grid(row=3,column=0,sticky=NS)
paned_window6 = tk.PanedWindow(tab3, orient = tk.VERTICAL)
paned_window6.grid(row=4,column=0,sticky=EW)

vsb4 = tk.Scrollbar(paned_window3, orient="vertical")
vsb5 = tk.Scrollbar(paned_window4, orient="horizontal")
txtarea4 = tk.Text(paned_window3,font=("Helvetica",11,"bold"), width=151, height=34, yscrollcommand = vsb4.set,xscrollcommand=vsb5.set,wrap = "none", bd = 7)

vsb6 = tk.Scrollbar(paned_window5, orient="vertical")
vsb7 = tk.Scrollbar(paned_window6, orient="horizontal")
txtarea5 = tk.Text(paned_window5,font=("Helvetica",11,"bold"), width=151, height=34, yscrollcommand = vsb6.set,xscrollcommand=vsb7.set,wrap ="none",bd = 7)

head = Label(tab1, text="CONSOLE", font=("Helvetica", 14),bg='gray')
head.grid(row=4,column=0,sticky='nsew')
head = Label(tab1, text="INPUT AND MEMORY SECTION", font=("Helvetica", 14),bg='gray')
head.grid(row=2,column=0,sticky='nsew')
head = Label(tab1, text="REGISTERS", font=("Helvetica", 14),bg='gray')
head.grid(row=2,column=1,sticky='nsew')

vsb.config(command = txtarea.yview)
vsb2.config(command = txtarea2.yview)
vsb3.config(command = txtarea3.yview)
vsb4.config(command = txtarea4.yview)
vsb5.config(command = txtarea4.xview)
vsb6.config(command = txtarea5.yview)
vsb7.config(command = txtarea5.xview)



paned_window1.add(txtarea)
paned_window1.add(vsb)
paned_window1.add(txtarea2)
paned_window1.add(vsb2)

paned_window2.add(txtarea3)
paned_window2.add(vsb3)

paned_window3.add(txtarea4)
paned_window3.add(vsb4)
paned_window4.add(vsb5)

paned_window5.add(txtarea5)
paned_window5.add(vsb6)
paned_window6.add(vsb7)

ctr_mid = Frame(tab1)
ctr_mid.grid(row=3,column=1,rowspan=3,sticky=NS)
t = Table(ctr_mid)

def loadi():
    for i in range(32):
        RegisterVals[i]=0
    global prevVal
    prevVal = RegisterVals.copy()
    global t
    t=Table(ctr_mid)

def reload():
    processfunction()
    dopipeline()
    printnondataforwarding()
    printdataforwarding()
    printCycles()
    txtarea2. delete("1.0", "end") 
    ele2=memsecloader()
    txtarea2.insert(END, ele2)
    global t
    t=Table(ctr_mid)

def reload2():
    global pc
    single_step_execution()
    txtarea2.delete("1.0", "end") 
    ele2=memsecloader()
    txtarea2.insert(END, ele2)
    txtarea.tag_remove("blue", "1.0", "end")
    str1 = str(pc) +".0"
    str2 = str(pc) +".0 lineend" 
   
    txtarea.tag_configure("blue", background="lightblue")
    txtarea.tag_add("blue", str1, str2)

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


##

