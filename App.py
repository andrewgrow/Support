import os
from os import listdir
from os.path import isfile, join

# for start open terminal and print
# py -3 App.py




from os import walk

dir_path = os.path.dirname(os.path.realpath(__file__))

files_list = []
for (dirpath, dirnames, filenames) in walk('./incoming'):
    files_list.extend(filenames)
    break

if files_list:
    print("Success")
    for file in files_list:
        print(file)
else:
    print("Wrong")