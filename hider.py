import argparse
from shutil import copyfile
import mmap
import re


class Hider():
    """Object to convert files into other file types"""
    def __init__(self, magic_number_file="magic_numbers.txt"):
        self.magic_numbers = {}
        #Load classes and magic numbers from magic_number file
        for line in open(magic_number_file):
            ext, magic_number = line.strip().split(" ")
            self.magic_numbers[ext] = re.findall("..", magic_number)
            
    def convert_file(self, input_file, output_file):
        """Hides an input file in a new output file, changing the magic number"""
        in_ext = input_file.split(".")[-1].lower() #Extension of the input file
        out_ext = output_file.split(".")[-1].lower() #Extension of the output file
        copyfile(input_file, output_file)
        with open(output_file, "r+b") as outfile:
            mm = mmap.mmap(outfile.fileno(), 0)
            for i,n in enumerate(self.magic_numbers[out_ext]):
                mm[i] = int(n, 16)
            mm.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="The filepath of the file you want to open/hide.")
    parser.add_argument("outfile", help="The filepath of the file you want to save your hidden file to.")
    args = parser.parse_args()
    h = Hider()
    h.convert_file(args.infile, args.outfile)

if __name__ == "__main__":
    main()