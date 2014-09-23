from os import listdir
from os.path import isfile, join
mypath = "C:\\Users\\Admin\\Desktop\\fantasy_game"
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
lines = 0
for f in onlyfiles:
    x = f.split(".")
    print x
    if x[1] == "pyc" or x[1] == "txt":
        pass
    else:
        for line in open(f):
            lines += 1
print lines
