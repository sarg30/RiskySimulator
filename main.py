import numpy
from userinstruct import makejumpdict, takeinput

# change it to instructions = userinstruct(file)
datasection,textsection,jumpdict = takeinput('grouping.txt')
memdict = {}
mem=0
memory = numpy.empty(4096, dtype=object)



global pc
pc = 0

def insertdatatomemory(datasection):
    global mem
    for i in datasection:
        if len(i)>2 and i[0].find(":") != -1 and (i[1]==".word" or i[1]==".string"):
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
    global pc
    rd, rs2 = line[1], line[2]
    index = memdict[rs2+":"]
    RegisterVals[Register_index[rd]]=index*4
    pc=pc+1

def li(line):
    global pc
    rd, rs2 = line[1], line[2]
    RegisterVals[Register_index[rd]]=int(rs2)
    pc=pc+1

def lw(line):
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
        else:
            pc = pc+1
        s="t2"
        #print(pc)
        

# this is the way the register values can be accessed and modified

# RegisterVals[Register_index[s]]=2

insertdatatomemory(datasection)
print(jumpdict)
processfunction()
#print(jumpdict)

# for i in Register_index:
#     print(i, RegisterVals[Register_index[i]])