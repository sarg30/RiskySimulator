each = []
lines = []
jumpdict = {}
def decodeinstruct(line):
    linelist = [x.strip() for x in line.split(',')]
    res = []
    for i in linelist:
       i = [x.strip() for x in i.split(' ')]
       for k in i :
           if len(k)>0:
               res. append(k)
    each.append(res)

def makejumpdict(each):
    counter =0
    for i in each:
        counter=counter+1
        if i[0].find(":")!=-1:
            s=i[0]
            #print(s)
            jumpdict[s]=counter

def takeinput(files):

    file = open(files,'r')
    content = file.readlines()
    file.close()

    

    for line in content:
        line  = line.strip()
        if len(line)!=0 and line[0]!='#':
            seperate = ''
            for i in line:
                if i =='#':
                    break
                else:
                    seperate = seperate+i
            if len(seperate)!=0:
                seperate  = seperate.strip()
                lines.append(seperate)
    for i in lines:
        decodeinstruct(i)
    return each
    
    #for i in lines:
        #print(i)

#takeinput('grouping.txt')
#makejumpdict(each)
#print(jumpdict)
# for i in each:
#     print(i)

