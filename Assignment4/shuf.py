#!/usr/bin/python

import random
import sys
import argparse
import string



class shuf:
    def __init__(self,min_,max_,n_count_,repeat_,file_list_):
        self.min = min_
        self.max = max_
        self.n_count = n_count_
        self.repeat = repeat_
        self.file_list = file_list_
        
    def output(self):
        #if -r flag used
        if self.repeat == True:
            #if -i flag not used
            if self.min == -1 and self.max == -1:
                #if -i not used but -r is, go forever.. basically
                for i in range(self.n_count):
                    j = random.randint(0,len(self.file_list) - 1)
                    print(self.file_list[j])
            #if -i flag is used
            else:
                for i in range(self.n_count):
                    j = random.randint(self.min, self.max)
                    print(j)
        #if -r flag is not used
        else:   
            #if -i flag not used
            if self.min == -1 and self.max == -1:
                #in case the file has less lines than the lines desired
                if self.n_count > len(self.file_list):
                    self.n_count = len(self.file_list)
                for i in range(self.n_count):
                    j = random.randint(0,len(self.file_list) - 1)
                    print(self.file_list[j])
                    del self.file_list[j]
            else:
                #if -i flag is used, create array with vals from min->max
                i_list = []
                for k in range(self.min,self.max + 1):
                    i_list.append(k)
                #if file has less lines than the num of lines desired
                if self.n_count > len(i_list):
                    self.n_count = len(i_list)
                #iterate as many times as needed and delete from list to make sure no repeats
                for i in range(self.n_count):
                    j = random.randint(0, len(i_list) - 1)
                    print(i_list[j])
                    del i_list[j]
                
                    
def main():
    parser = argparse.ArgumentParser(description="Write a random permutation of the input lines to standard output.", \
        prog="shuf.py",\
        usage="%(prog)s [OPTION]... [FILE]\n  or:  %(prog)s -i LO-HI [OPTION]...")
    
    #input range argument
    parser.add_argument("-i", "--input-range", \
        help="treat each number LO through HI as an input line", \
        action="store", \
        dest="LO_HI", \
        default="")

    #head-count argument
    parser.add_argument("-n", "--head-count", \
        help="output at most COUNT lines", \
        action="store", \
        dest="count", \
        default=sys.maxsize)

    #repeat argument
    parser.add_argument("-r", "--repeat", \
        help="output lines can be repeated", \
        action="store_true", \
        dest="repeat", \
        default=False)

    #file/stdin argument
    parser.add_argument("FILE", \
        help="with no FILE, or when FILE is -, read standard input", \
        nargs="?", \
        action="store", \
        default="")

    args = parser.parse_args()

    #exception handling for -i, --input-range
    if not args.LO_HI == "":   #needed bc default LO_HI="", causes error 
        input = []
        try:
            LO = int(args.LO_HI.split("-", 1)[0])
            HI = int(args.LO_HI.split("-", 1)[1])
        except:
            parser.error("Invalid LO-HI: {}, LO-HI must be an integer range".format(args.LO_HI))
        
        if LO < 0:
            parser.error("Invalid LO-HI: {}, LO cannot be less than 0".format(args.LO_HI))
        if LO > HI:
            parser.error("Invalid LO-HI: {}, LO cannot be greater than HI".format(args.LO_HI))
        if not args.FILE == "":
            parser.error("Extra FILE operand: {}, cannot include FILE with -i/--input-range".format(args.FILE))
    else:
        #to signify no -i flag, set LO, HI = -1
        LO=-1
        HI=-1
        #exception handling for FILE
        if args.FILE == "" or args.FILE == "-":
            input = sys.stdin.readlines()
        else:
            try:
                f = open(args.FILE, "r")
                input = (f.readlines())
                f.close()
            except:
                parser.error("Invalid FILE: {} could not opened/read".format(args.FILE))
        input = [x.replace('\n','') for x in input]

    #exception handling for -n, --head-count
    try:
        num_lines = int(args.count)
    except:
        parser.error("Invalid COUNT: {}, COUNT must be an integer".format(args.count))

    if num_lines < 0:
        parser.error("Invalid COUNT: {}, COUNT cannot be less than 0".format(args.count))

    #shuf class object and output() function
    try:
        generator = shuf(LO, HI, num_lines, args.repeat, input)
        generator.output()
    except IOError as err:
        errno, strerror = err.args
        print("I/O error({0}): {1}".format(errno, strerror))



if __name__ == "__main__":
    main()