'''
Created on Jun 14, 2016

@author: xgo
'''

import sys
import getopt

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

    opts, _args = getopt.getopt(argv[1:], "hvVi:p:o:",
                                    ["help",
                                     "version",
                                     "input-file",
                                     "prefix",
                                     "output-file"])

    # Default working dir and config file
    input_file = "./"
    prefix_string = ""
    output_file = ""

    # Basic options
    for option, value in opts:
        if option in ("-h", "--help"):
            print help_message
        if option in ("-v", "-V", "--version"):
            print "sipros_peptides_filtering.py V%s" % (get_version())
            sys.exit(0)
        if option in ("-i", "--input-file"):
            input_file = value
        if option in ("-p", "--prefix"):
            prefix_string = value
        if option in ("-o", "--output-file"):
            output_file = value

    return (input_file, prefix_string, output_file)

def extract(input_file, prefix_string, output_file):
    outputFile = open(output_file, "w")
    id_str = ""
    seq_str = ""
    inputFile = open(input_file)
    line_str = ""
    for line_str in inputFile:
        if line_str[0] == '>':
            if not id_str.startswith(prefix_string) and seq_str != "":
                outputFile.write(id_str)
                outputFile.write(seq_str)
            id_str = line_str
            seq_str = ""
        else:
            seq_str += line_str
    if not id_str.startswith(prefix_string) and seq_str != "":
        outputFile.write(id_str)
        outputFile.write(seq_str)
    
    inputFile.close()
    outputFile.close()


def main(argv=None):

        if argv is None:
            argv = sys.argv
        # parse options
        (input_file, prefix_string, output_file) = parse_options(argv)
        if not prefix_string.startswith(">"):
            prefix_string = ">" + prefix_string
        # process file
        extract(input_file, prefix_string, output_file)


if __name__ == '__main__':
    sys.exit(main())
