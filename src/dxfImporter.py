# -*- coding: utf-8 *-*


def read(filename):
    print "Opening file: {0}".format(filename)
    file = open(filename)

    # skip to entities section
    s = file.next()
    while s.strip() != "ENTITIES":
        s = file.next()

    inLine = False

    ptList = []

    for line in file:
        line = line.strip()  # Stip out the white space
        if line == 'ENDSEC':
            break
        elif inLine == True:
            dd = dict.fromkeys(['10', '20', '30', '11', '21', '31'], 0.0)
            while True:
                if line in dd:
                    dd[line] = float(file.next().strip())
                    # Found the last Z value, so kick out of loop
                    if line == '31':
                        break
                line = file.next().strip()
            ptList.append([[dd['10'], dd['20'], dd['30']], [dd['11'], dd['21'],
                        dd['31']]])
            inLine = False
        else:
            if line == 'LINE':
                inLine = True

    file.close()

    return ptList
