def takeinput(files):

    file = open(files,'r')
    content = file.readlines()
    file.close()

    lines = []

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

    #for i in lines:
        #print(i)


takeinput('grouping.txt')
