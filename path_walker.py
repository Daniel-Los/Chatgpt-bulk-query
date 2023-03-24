from os import walk
import pandas as pd


f = []
mypath = r"C:\Users\d.los\Berenschot\EXT evaluatie ketenaanpak medicijnresten - General\2. Documentstudie\Vergaderingdocumenten Werkgroep"
mydirs = []
for (dirpath, dirnames, filenames) in walk(mypath):
    mydirs.extend(dirnames)
for dir in mydirs:
    dir = mypath + f'\{dir}'
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend(filenames)
        break

from os import walk

filenames = next(walk(mypath), (None, None, []))[2]

frame = pd.DataFrame()

frame['name'] = f

frame.to_csv('itemlist.csv')

