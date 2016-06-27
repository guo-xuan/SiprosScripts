'''
Created on Jun 14, 2016

@author: xgo
'''

import sys
import getopt
import operator
import re

# # Version control
def get_version():
    return "5.0.1 (Alpha)"

# # Help message
help_message = '''
Usage:
    python sipros_shuffle_database.py [options]

Inputs:
    database file
    sipros config file
    output filename

Options:
    -h/--help
    -v/--version
    -i/--input-file ./path    
    -p/--prefix
    -o/--output-file ./path

Outputs:
    output file
'''

# # Parse options
def parse_options(argv):

    opts, _args = getopt.getopt(argv[1:], "hvVi:s:p:",
                                    ["help",
                                     "version",
                                     "input-file",
                                     "sequence",
                                     "protein"])

    # Default working dir and config file
    input_file = "./"
    iSequenceIndex = 0
    iProteinNameIndex = 0

    # Basic options
    for option, value in opts:
        if option in ("-h", "--help"):
            print help_message
        if option in ("-v", "-V", "--version"):
            print "sipros_peptides_filtering.py V%s" % (get_version())
            sys.exit(0)
        if option in ("-i", "--input-file"):
            input_file = value
        if option in ("-s", "--sequence"):
            iSequenceIndex = value
        if option in ("-p", "--protein"):
            iProteinNameIndex = value

    return (input_file, iSequenceIndex, iProteinNameIndex)

def fdr(input_file, iSequenceIndex, iProteinNameIndex):
    list_of_pairs=[]
    line_str = ""
    pep_str = ""
    pro_str = ""
    list_split = []
    iSequenceIndex = int(iSequenceIndex)
    iProteinNameIndex = int(iProteinNameIndex)
    with open(input_file) as inputFile:
        next(inputFile)
        for line_str in inputFile:
            list_split = line_str.split()
            if float(list_split[2]) <= 0.01:
                pep_str = list_split[iSequenceIndex]
                pro_str = list_split[iProteinNameIndex]
                list_of_pairs.append((pep_str, pro_str))
            
    list_of_pairs.sort(key = operator.itemgetter(0))
    iNumPepModTotal = 0
    iNumPepModTarget = 0
    pro_str = list_of_pairs[0][1]
    
    if not pro_str.startswith("Dec_"):
        iNumPepModTarget += 1
    iNumPepModTotal += 1
    
    for i in range(1, len(list_of_pairs)):
        if list_of_pairs[i][0] != list_of_pairs[i-1][0]:
            iNumPepModTotal += 1
            pro_str = list_of_pairs[i][1]
            if not pro_str.startswith("Dec_"):
                iNumPepModTarget += 1
    
    dFdr = float(iNumPepModTarget)/float(iNumPepModTotal)
    print dFdr
    print iNumPepModTarget
    print iNumPepModTotal
    
    list_of_pairs2 = []
    for (a, b) in list_of_pairs:
        a = re.sub('[^0-9a-zA-Z]+', '', a)
        list_of_pairs2.append((a, b))
    list_of_pairs2.sort(key = operator.itemgetter(0))
    iNumPepModTotal = 0
    iNumPepModTarget = 0
    pro_str = list_of_pairs2[0][1]
    
    if not pro_str.startswith("Dec_"):
        iNumPepModTarget += 1
    iNumPepModTotal += 1
    
    for i in range(1, len(list_of_pairs)):
        if list_of_pairs2[i][0] != list_of_pairs2[i-1][0]:
            iNumPepModTotal += 1
            pro_str = list_of_pairs2[i][1]
            if not pro_str.startswith("Dec_"):
                iNumPepModTarget += 1
    
    dFdr = float(iNumPepModTarget)/float(iNumPepModTotal)
    print dFdr
    print iNumPepModTarget
    print iNumPepModTotal


def main(argv=None):

        if argv is None:
            argv = sys.argv
        # parse options
        (input_file, iSequenceIndex, iProteinNameIndex) = parse_options(argv)
        # process file
        fdr(input_file, iSequenceIndex, iProteinNameIndex)

if __name__ == '__main__':
    sys.exit(main())