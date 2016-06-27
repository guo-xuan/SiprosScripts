#!/usr/bin/python


## Import Python package modules
import sys, getopt, os

def parse_options(argv):

    opts, _args = getopt.getopt(argv[1:], "hi:o:",
                                    ["help",
                             	     "input-file",
	                			     "output-file"])

    output_filename = ""
    input_filename  = ""

    # Basic options
    for option, value in opts:
        if option in ("-h", "--help"):
            print "-i input-file, -o output-file"
            sys.exit(1)
        if option in ("-i", "--input-file"):
            input_filename = value
        if option in ("-o", "--output-file"):
            output_filename = value

    if (input_filename == "") :
        print "Please specify -i"
        sys.exit(1)
    if (output_filename == "") :
        (inputFileNameRoot, inputFileNameExt) = os.path.splitext(input_filename)
        output_filename = inputFileNameRoot + "_CFR" + inputFileNameExt
    return (input_filename, output_filename)


def ReverseSeq(inputFileName, outputFileName) :
    outputFile = open(outputFileName, "w")
    id_str = ""
    seq_str = ""
    seq_new_str = ""
    inputFile = open(inputFileName, "r")
    line_str = ""
    for line_str in inputFile:
        if line_str[0] == '>':
            if seq_str != "":
                seq_new_str = (seq_str[::-1])
                outputFile.write(id_str)
                outputFile.write(seq_str)
                outputFile.write(">Rev_")
                outputFile.write(id_str[1:])
                outputFile.write(seq_new_str[1:])
                outputFile.write("\n")
            id_str = line_str
            seq_str = ""
        else:
            seq_str += line_str
    if seq_str != "":
        seq_new_str = (seq_str[::-1])
        outputFile.write(id_str)
        outputFile.write(seq_str)
        outputFile.write(">Rev_")
        outputFile.write(id_str[1:])
        outputFile.write(seq_new_str[1:])
        outputFile.write("\n")
        
    inputFile.close()
    outputFile.close()


def main(argv=None):

    # try to get arguments and error handling
    if argv is None:
        argv = sys.argv
        # parse options
        (inputFileName, outputFileName) = parse_options(argv)
        ReverseSeq(inputFileName, outputFileName)


## If this program runs as standalone, then go to main.
if __name__ == "__main__":
    main()




