from userinstruct import takeinput
Instructions= takeinput('grouping.txt') #change it to instructions = userinstruct(file)
RegisterVals=[]

#initializing the values of  all registers as 0
for i in range(32):
    RegisterVals.append(0)

def process_R_type(line):
    """
    This function is to return
    the memory addresses of 
    the registers for R-type instructions
    """
    return line[0],line[1],line[2]


def add(line):
    """
    This function processes the
    add instruction of risc-v
    """
    rd,rs1,rs2=process_R_type(line)
    RegisterVals[Registers[rd]]=RegisterVals[Registers[rs1]]+RegisterVals[Registers[rs2]]


def sub(line):
    """
    This function processes the 
    sub instruction of risc-v
    """
    rd,rs1,rs2=process_R_type(line)
    RegisterVals[Registers[rd]]=RegisterVals[Registers[rs1]]-RegisterVals[Registers[rs2]]

def shift_left_logical(line):
    """
    This function processes the
    sll instruction of risc-v
    """
    rd,rs1,rs2=process_R_type(line)
    RegisterVals[Registers[rd]]=(RegisterVals[Registers[rs1]])<<(RegisterVals[Registers[rs2]])

Registers= {
    "zero":0,
    "ra":1,
    "sp":2,
    "gp":3,
    "tp":4,
    "t0":5,
    "t1":6,
    "t2":7,
    "s0":8,
    "fp":8,
    "s1":9,
    "a0":10,
    "a1":11,
    "a2":12,
    "a3":13,
    "a4":14,
    "a5":15,
    "a6":16,
    "a7":17,
    "s2":18,
    "s3":19,
    "s4":20,
    "s5":21,
    "s6":22,
    "s7":23,
    "s8":24,
    "s9":25,
    "s10":26,
    "s11":27,
    "t3":28,
    "t4":29,
    "t5":30,
    "t6":31,
}

#this is the way the register values can be accessed and modified
for i in Instructions:
    if len(i)>2:
        #print(i)
        print(process_R_type(i))
s="t0"
RegisterVals[Registers[s]]=2
print(RegisterVals[Registers[s]])