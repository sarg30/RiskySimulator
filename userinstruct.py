lines = []
each = []
textsection = []
datasection = []
jumpdict = {}


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


def makejumpdict(each):
    counter = 0
    for i in each:
        counter = counter+1
        if i[0].find(":") != -1:
            s = i[0]
            # print(s)
            jumpdict[s] = counter
    return jumpdict


def decodeinstruct(line):
    linelist = [x.strip() for x in line.split(',')]
    res = []
    for i in linelist:
        i = [x.strip() for x in i.split(' ')]
        for k in i:
            if len(k) > 0:
                res. append(k)
    each.append(res)


def takeinput(files):

    file = open(files, 'r')
    content = file.readlines()
    file.close()

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
    for i in lines:
        decodeinstruct(i)
    sepeartedatasec(each)
    makejumpdict(textsection)
    return datasection, textsection, jumpdict


#takeinput('grouping.txt')
#print(jumpdict)
# for i in textsection:
#     print(i)
# for i in datasection:
#     print(i)
