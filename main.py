import numpy
from userinstruct import makejumpdict, takeinput

# change it to instructions = userinstruct(file)
datasection,textsection,jumpdict = takeinput('grouping.txt')
memory = numpy.empty(4096, dtype=object)
# counter for instruction
global pc
pc = 0
# initializing the values of  all registers as 0
RegisterVals = []
for i in range(32):
    RegisterVals.append(0)

 # for addi we should know wether they are referring to register or number
def isregister(line): 
    for i in Registers:
        if line == i:
            return True
    return False


def addi(line):
    global pc
    sum = 0
    rd, rs1, rs2 = process_R_type(line)
    if isregister(rs1):
        sum = sum+RegisterVals[Registers[rs1]]
    else:
        sum = sum+int(rs1)
    if isregister(rs2):
        sum = sum+RegisterVals[Registers[rs2]]
    else:
        sum = sum+int(rs2)
    print(sum)
    RegisterVals[Registers[rd]] = sum
    pc = pc+1


def lw(line):
    global pc
    rs1, rs2 = line[1], line[2]
    linelist = [x.strip() for x in rs2.split('(')]
    rs2 = linelist[0]
    linelist = [x.strip() for x in linelist[1].split(')')]
    temp = linelist[0]
    rs2 = int(rs2)+RegisterVals[Registers[temp]]
    pc = pc+1


def beq(line):
    global pc
    rs1, rs2, nextaddress = process_R_type(line) 
    if rs1 == rs2:
        pc = jumpdict[nextaddress]
        print(pc)
    else:
        pc = pc+1


def process_R_type(line):
    """
    This function is to return
    the memory addresses of 
    the registers for R-type instructions
    """
    return line[1], line[2], line[3]


def add(line):
    global pc
    """
    This function processes the
    add instruction of risc-v
    """
    rd, rs1, rs2 = process_R_type(line)
    RegisterVals[Registers[rd]] = RegisterVals[Registers[rs1]] + RegisterVals[Registers[rs2]]
    print( RegisterVals[Registers[rd]])
    pc = pc+1


def sub(line):
    global pc
    """
    This function processes the 
    sub instruction of risc-v
    """
    rd, rs1, rs2 = process_R_type(line)
    RegisterVals[Registers[rd]] = RegisterVals[Registers[rs1]] -  RegisterVals[Registers[rs2]]
    pc = pc+1


def shift_left_logical(line):
    global pc
    """
    This function processes the
    sll instruction of risc-v
    """
    rd, rs1, rs2 = process_R_type(line)
    RegisterVals[Registers[rd]] = (RegisterVals[Registers[rs1]]) << (
        RegisterVals[Registers[rs2]])
    pc = pc+1


Registers = {
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
        else:
            pc = pc+1


# this is the way the register values can be accessed and modified
# s="t0"
# RegisterVals[Registers[s]]=2
# print(RegisterVals[Registers[s]])
processfunction()
# for i in Registers:
#     print(i, RegisterVals[Registers[i]])
