'''
Created on Jun 6, 2016

@author: xgo
'''

import sys
import getopt
from random import shuffle

## Import Sipros package modules
import sipros_post_module
import parseconfig

## Version control
def get_version():
    return "5.0.1 (Alpha)"

## Help message
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
    -c/--configuration-file SiprosConfig.cfg    # SIPROS config file
    -o/--output-file ./path

Outputs:
    output file
'''

## Global variables
pep_iden_str            = '[Peptide_Identification]'
cleave_after_str        = 'Cleave_After_Residues'
cleave_before_str       = 'Cleave_Before_Residues'
pro_iden_str            = '[Protein_Identification]'
decoy_prefix_str        = 'Decoy_Prefix'
aa_after_cleave_str     = ""
aa_before_cleave_str    = ""
decoy_str               = ""


## check_file_exist
check_file_exist = sipros_post_module.check_file_exist
## Import classes and definitions in the Sipros module
## Class Usage
Usage = sipros_post_module.Usage


## Parse options
def parse_options(argv):

    try:
        opts, _args = getopt.getopt(argv[1:], "hvVi:c:o:",
                                    ["help",
                                     "version",
                                     "input-file",
                                     "configuration-file",
                                     "output-file"])

    # Error handling of options
    except getopt.error, msg:
        raise Usage(msg)

    # Default working dir and config file
    input_file = "./"
    config_file = "SiprosConfig.cfg"
    output_file = ""

    # Basic options
    for option, value in opts:
        if option in ("-h", "--help"):
            raise Usage(help_message)
        if option in ("-v", "-V", "--version"):
            print "sipros_peptides_filtering.py V%s" % (get_version())
            sys.exit(0)
        if option in ("-i", "--input-file"):
            input_file = value
        if option in ("-c", "--configuration-file"):
            config_file = value
        if option in ("-o", "--output-file"):
            output_file = value

    return (input_file, config_file, output_file)

def ShufflePep(seq_str):
    start = 0
    end = 1
    seq_new_str = ""
    pep_str = ""
    i = 0
    for i in range(0, len(seq_str)-2):
        if seq_str[i] in aa_before_cleave_str and seq_str[i+1] in aa_after_cleave_str:
            end = i
            pep_str = list(seq_str[start:end])
            shuffle(pep_str)
            seq_new_str += "".join(pep_str)
            seq_new_str += "".join(seq_str[i])
            start = end + 1
    if seq_str[i+1] not in aa_after_cleave_str or seq_str[i] not in aa_before_cleave_str:
        pep_str = list(seq_str[start:])
        shuffle(pep_str)
        seq_new_str += "".join(pep_str)
    return seq_new_str

def ReverseSeq(inputFileName, outputFileName, config_dict) :
    outputFile = open(outputFileName, "w")
    id_str = ""
    seq_str = ""
    seq_new_str = ""
    inputFile = open(inputFileName)
    line_str = ""
    for line_str in inputFile:
        if line_str[0] == '>':
            if not id_str.startswith(decoy_str) and seq_str != "":
                seq_str = seq_str.rstrip()
                seq_new_str = ShufflePep(seq_str)
                outputFile.write(id_str)
                outputFile.write(seq_str)
                outputFile.write("\n>Dec_")
                outputFile.write(id_str[1:])
                outputFile.write(seq_new_str)
                outputFile.write("\n")
            else:
                if id_str.startswith(decoy_str) and seq_str != "":
                    outputFile.write(id_str)
                    outputFile.write(seq_str)
            id_str = line_str
            seq_str = ""
        else:
            seq_str += line_str
    if not id_str.startswith(decoy_str) and seq_str != "":
        seq_str = seq_str.rstrip()
        seq_new_str = ShufflePep(seq_str)
        outputFile.write(id_str)
        outputFile.write(seq_str)
        outputFile.write("\n>Dec_")
        outputFile.write(id_str[1:])
        outputFile.write(seq_new_str)
        outputFile.write("\n")
    else:
        if id_str.startswith(decoy_str) and seq_str != "":
            outputFile.write(id_str)
            outputFile.write(seq_str)
        
    inputFile.close()
    outputFile.close()
    
## Parse config file
def parse_config(config_filename):

    # Save config values to dictionary
    config_dict = {}    # initialize dictionay

    # Call Yinfeng's parseconfig.py module
    check_file_exist(config_filename)
    # Save all config values to dictionary
    all_config_dict = parseconfig.parseConfigKeyValues(config_filename)

    # valiables were defined in global
    # pep_iden_str      = '[Protein_Identification]'
    # cleave_after_str  = 'Decoy_Prefix'
    # cleave_before_str = 'FDR_Filtering'
    # FDR_threshold_str = 'FDR_Threshold'

    # only save protein_identification config info to config_dict
    for key, value in all_config_dict.items():
        if key == (pep_iden_str + cleave_after_str):
            config_dict[cleave_after_str] = value
        elif key == (pep_iden_str + cleave_before_str):
            config_dict[cleave_before_str] = value
        elif key == (pro_iden_str + decoy_prefix_str):
            config_dict[decoy_prefix_str] = value
        else:
            continue

    # return config dictionary
    return config_dict

def main(argv=None):
    
    # try to get arguments and error handling
    try:
        if argv is None:
            argv = sys.argv
        try:
            # parse options
            (input_file, config_filename, output_file) = parse_options(argv)
            # Call parse_config to open and read config file
            config_dict = parse_config(config_filename)
            global aa_after_cleave_str
            aa_after_cleave_str = config_dict[cleave_before_str]
            global aa_before_cleave_str
            aa_before_cleave_str = config_dict[cleave_after_str]
            global decoy_str
            decoy_str = ">" + config_dict[decoy_prefix_str]
            # random shuffle database
            ReverseSeq(input_file, output_file, config_dict)
            
        # Error handling
        except Usage, err:
            print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
            return 2
    
    # Error handling
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "for help use -h/--help"
        return 2

if __name__ == '__main__':
    sys.exit(main())
