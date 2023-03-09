# # Follow this instructions after watching all videos:
# # 1. Find All PDF files (nested dir inclusive) with system arguments that receives at 
# invoking python script and store files with key value pairs format where key is path 
# to the file and value is array of PDF names in the path. For instance, 
# path = /Users/jooyonwon/Downloads/Jobs/H1-B/2/Joy and value = [I94_wife.pdf, Joy-Visa.pdf, Passport_wife.pdf]
# #     - Edge Case, if file name has whitespace or any keyword included that would 
# # break pdf merge, change the name of the file at step 1.

# # 2. Iterate and print out each file name with number in front, for instance, 
# # "1: sample.pdf" with appending path+"/"+filename combination into array.



# # 4. iterate user input array and change each string number into number type to grab 
# # specific index of file from array created in step 2 by paths[int(input)-1]

# # 5. using PyPDF2 function, merge all files into one PDF with asking user to provide name of combined name

# # 6. test run

# At 5, “combined name” meaning combined file name like if user put “sample” then it 
# generates aggregated file with “sample.pdf”. In the case of whitespace had been detected 
# in input, generate aggregated file for “sample test” input as “sample_test.pdf”. 
# Same for if there is any unacceptable character in input, remove them and generate 
# without those characters. It apply similar to step 1 edge cases part. 

import os
import json
import shutil
from subprocess import PIPE, run
import sys
import re
import PyPDF2

PDF_EX = ".pdf"

def find_all_pdf_path(source):
    pdf_paths = {}
    for root, dirs, files in os.walk(source):
        pdf_paths[root] = []
        filepath = pdf_paths[root]
        for file in files:
            if PDF_EX in file.lower():
                tempf = re.sub('\s+', '_', file)
                filepath.append(tempf)
                orig_name = os.path.join(root, file)
                fin_name = os.path.join(root, tempf)
                os.rename(orig_name, fin_name)
    return pdf_paths


def store_paths(pdf_paths):
    paths = []
    i = 1

    for key in pdf_paths:
        for value in pdf_paths[key]:
            if (len(pdf_paths[key]) > 0):
                value_path = os.path.join(key, value)
                paths.append(value_path)
                i += 1
    return paths


def get_input_n(numbers):
    to_print_pdf = input("Pick the numbers of the pdf you wish to print. ex) 1 2.  ")
    to_print = to_print_pdf.split()
    to_print_arr = list(map(int, to_print))
    return to_print_arr


def pdf_merge(numbers, paths):
    merger = PyPDF2.PdfMerger()
    paths_to_print = []
    for i in numbers:
        paths_to_print.append(paths[i - 1])
    for file in paths_to_print:
        merger.append(file)
    name = input("Please write the name.  ")
    merger.write(name + ".pdf")


def main(source):

    pdf_paths = find_all_pdf_path(source)
    numbers = store_paths(pdf_paths)
    i = 1
    for key in pdf_paths:
        for val in pdf_paths[key]:
            print(str(i) + ": " + val)
            i += 1
    number_to_print = get_input_n(numbers)
    all_stored_paths = store_paths(pdf_paths)
    pdf_merge(number_to_print, all_stored_paths)
    

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 2:
        raise Exception("you must pass a target directory")
    source = args[1]

    main(source)
