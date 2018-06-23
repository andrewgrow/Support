import os

# for start open terminal and print
# py -3 App.py


from os import walk

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = dir_path + '\input'
output_path = dir_path + '\output'

files_list = []
for (dirpath, dirnames, filenames) in walk(input_path):
    files_list.extend(filenames)
    break


if files_list:
    print("Incoming path = ", input_path)
    print(files_list)


else:
    print("Wrong")
