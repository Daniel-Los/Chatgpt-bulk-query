def begrippenlijst():
    with open('begrippen.txt', errors = 'ignore') as lijst:
        list = lijst.readlines()
        x = [x.strip('\n') for x in list]
        return x
