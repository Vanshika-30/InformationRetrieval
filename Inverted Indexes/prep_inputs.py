import re
import argparse
import os

def process_file(input, output):
    regex = re.compile("[^a-zA-Z \n]")
    with open(output, 'w') as outfile:
        with open(input, 'r') as infile:
            outfile.write(regex.sub('', infile.read().lower()).replace("\n", " "))


if __name__ == '__main__':

    os.chdir("Corpus") 
    files = []   
    dirname = os.getcwd()
    dirname = os.path.join(dirname, "Docs")
    for filename in os.listdir(dirname):
        in_filepath = os.path.join(dirname, filename)
        out_filepath = os.path.join('PreppedDocs/' +filename)
        files.append(out_filepath.split("/")[1])
        process_file(in_filepath, out_filepath)

    files = sorted(files)
    with open('file.txt', 'w') as outfile:
        for i in files:
            outfile.write(i + " ")
