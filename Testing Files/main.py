from mailbox import linesep
from re import T
from traceback import print_tb
import numpy
from userinstruct import makejumpdict, takeinput

# change it to instructions = userinstruct(file)
datasection,textsection,jumpdict = takeinput('grouping.txt')
memdict = {}
mem=0
# memory = numpy.empty(4096, dtype=object)
memory = [0 for i in range (4096)]

last_wb = [0 for i in range (32)]                        #stores the latest cc for the wb stage for each register(used when data forwarding is disabled)
last_mem = [0 for i in range (32)]                       #stores the latest cc for the mem stage for each register(used when data forwarding is enabled)

rows,cols = (2000,2000)

df_enabled= [["     " for i in range(cols)] for j in range(rows)]           #stores the pipline stages when data forwarding is enabled
df_disabled = [["     " for i in range(cols)] for j in range(rows)]         #stores the pipline stafes when data forwarding is disabled

global pc
pc = 0

global inst_counter
inst_counter=1

global  cc_df_enabled
global  cc_df_disabled
cc_df_enabled=0
cc_df_disabled=0

is_stall_dfe = [0 for i in range (cols)]                     # 1 if the cc is a stall else 0
is_stall_dfne = [0 for i in range (cols)]                    # 1 if the cc is a stall else 0

def insertdatatomemory(datasection):
    global mem
    for i in datasection:
        if len(i)>2 and i[0].find(":") != -1 and (i[1]==".word" or i[1]==".string"):
            memdict[i[0]]=mem
            for j in range(len(i)):
                if j>1:
                    memory[mem]=i[j]
                    mem=mem+1
    


# check for updation of inst_counter in the functions



# functions related to pipelining implementation for data forwarding disabled


def dfne_R_type(rd,rs1,rs2):
    """
    implements the pipeline stages corresponding to 
    R type instructions when data forwarding is disabled
    """
    global cc_df_disabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i=int(cc_df_disabled+1)
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
    i=int(cc_df_disabled+1)
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
    i=int(cc_df_disabled+1)
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
    i=int(cc_df_disabled+1)
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


def dfne_beq(rd,rs2,checker):
    """
    implements the pipeline stages corresponding to sw
    instruction when data forwarding is disabled
    """    
    global cc_df_disabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i=int(cc_df_disabled+1)
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


def dfne_bne(rd,rs2,checker):
    """
    implements the pipeline stages corresponding to sw
    instruction when data forwarding is disabled
    """    
    global cc_df_disabled
    global inst_counter

    # searching for which clock cycle implement IF stage
    i=int(cc_df_disabled+1)
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
    i=int(cc_df_disabled+1)
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
    i=int(cc_df_disabled+1)
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


def dfne_la(rd):
    """
    implements the pipeline stages corresponding to la 
    instructions when data forwarding is enabled
    """
    global cc_df_disabled
    global inst_counter

    #searching for which clock cycle to impelement IF stage
    i= int(cc_df_disabled+1)
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
    i=int(cc_df_disabled+1)
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
    i= int(cc_df_enabled+1)
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
    i=int(cc_df_enabled+1)
    while is_stall_dfe[i]==1:
        i=i+1
    df_enabled[inst_counter][i]="IF   "
    cc_df_enabled=i
    i=i+1

    # searching for which clock cycle to implement ID/RF stage 
    while is_stall_dfne[i]==1:
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
    i= int(cc_df_enabled+1)
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
    i= int(cc_df_enabled+1)
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
    i=int(cc_df_enabled+1)
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
    i= int(cc_df_enabled+1)
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
    i= int(cc_df_enabled+1)
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
    i=int(cc_df_enabled+1)
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
    df_disabled[inst_counter][i]="ID/RF"
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
    i=int(cc_df_enabled+1)
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
    i=int(cc_df_enabled+1)
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
        is_stall_dfne[i]=1
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
    print(memory[0:mem])
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


#Assigning indices to each register
Register_index = {
    "zero": 0,
    "ra": 1,
    "sp": 2,
    "gp": 3,
    "tp": 4,
    "t0": 5,
    "t1": 6,
    "t2": 7,
    "s0": 8,
    "fp": 8,
    "s1": 9,
    "a0": 10,
    "a1": 11,
    "a2": 12,
    "a3": 13,
    "a4": 14,
    "a5": 15,
    "a6": 16,
    "a7": 17,
    "s2": 18,
    "s3": 19,
    "s4": 20,
    "s5": 21,
    "s6": 22,
    "s7": 23,
    "s8": 24,
    "s9": 25,
    "s10": 26,
    "s11": 27,
    "t3": 28,
    "t4": 29,
    "t5": 30,
    "t6": 31,
}

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
    # print_register_vals()



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
    # print_register_vals()
        

insertdatatomemory(datasection)

x=1

while(x!=3 or pc!=len(textsection)):

    print("What operation do you want to perform\n1 --> Run/Continue\n2 --> Single Step Execution\n3 --> Terminate Program/Exit\nPlease enter the corresponding number")
    x=int(input())
    if x==1:
        processfunction()
        break
    elif x==2:
        single_step_execution()
    elif x==3:
        break
    else:
        print("Invalid input")



dfe_cycles=0            # the number of clock cycles taken when data forwarding is enabled
dfne_cycles=0           # the number of clock cycles taken when data forwarding is disabled
dfe_stalls=0            # the number of stalls when data forwarding is enabled
dfne_stalls=0           # the number of stalls when data forwarding is disabled

for i in range(cols):
    if df_disabled[inst_counter-1][i]!="     ":
        dfne_cycles=i
    if df_enabled[inst_counter-1][i]!="     ":
        dfe_cycles=i
    if is_stall_dfe[i]==1:
        dfe_stalls=dfe_stalls+1
    if(is_stall_dfne[i]==1):
        dfne_stalls=dfne_stalls+1

# print(dfe_cycles)
# print(dfne_cycles)
# print(dfne_stalls)
# print(dfe_stalls)
# print(inst_counter)


#printing the pipeline for data forwarding disabled
print("The pipeline for data forwarding disabled is as follows: ")
for i in range(inst_counter+30):
    for j in range(1,30):
        if i==0:
            cc= str(j)
            while(len(cc)<5):
                cc="0"+cc
            df_disabled[i][j]=cc
            
        print (df_disabled[i][j],end=" ")
    print()
print("The number of stalls is: ",end=" ")
print(dfne_stalls)
print("IPC value is: ",end=" ")
print((inst_counter-1)/dfne_cycles)

print()

#printing the pipeline for data forwarding enabled
print("The pipeline for data forwarding enabled is as follows: ")
for i in range(inst_counter+30):
    for j in range(1,20):
        if i==0:
            cc= str(j)
            while(len(cc)<5):
                cc="0"+cc
            df_enabled[i][j]=cc
            
        print (df_enabled[i][j],end=" ")
    print()
print("The number of stalls is: ",end=" ")
print(dfe_stalls)
print("IPC value is: ",end=" ")
print((inst_counter-1)/dfe_cycles)
# for i in range (0,31):
#     print(last_mem[i],end=" ")
