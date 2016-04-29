'''
Created on Apr 29, 2016

@author: Guo, Xuan
'''

import argparse, os, sys
import platform

parser = argparse.ArgumentParser(description="replace bracket in the protein description",
                                 prog='BracketRemover.py',  # program name
                                 prefix_chars='-',  # prefix for options
                                 fromfile_prefix_chars='@',  # if options are read from file, '@args.txt'
                                 conflict_handler='resolve',  # for handling conflict options
                                 add_help=True,  # include help in the options
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter  # print default values for options in help message
                                 )
# # input files and directories
parser.add_argument("-i", "--input", help="target file/folder", dest='sInput', required=True)
# # process database
parser.add_argument("-f", help="target(s) is/are database", dest='bDatabase', default=False, action="store_true")
# # process sip file
parser.add_argument("-s", help="target(s) is/are sip file(s)", dest='bSip', default=False, action="store_true")
# # output files and directories
parser.add_argument("-o", "--out", help="output file/folder", dest='sOut', required=True)


def main(argv=None):
    # try to get arguments and error handling
    if argv is None:
        args = parser.parse_args()
    
    lInputList = []
    lOutList = []
    sLine = ""
    lLineSplitList = []
    sInput = args.sInput
    sOut = args.sOut
    
    if args.bSip:
        if os.path.isfile(sInput):
            lInputList.append(sInput)
            lOutList.append(sOut)
        else:
            if platform.system() == 'Windows':
                if sInput[-1] != '\\':
                    sInput = sInput + '\\'
                if sOut[-1] != '\\':
                    sOut = sOut + '\\'
            else:
                if sInput[-1] != '/':
                    sInput = sInput + '/'
                if sOut[-1] != '/':
                    sOut = sOut + '/'
        for sFile in os.listdir(sInput):
            if sFile.endswith(".sip"):
                lInputList.append(sInput + sFile)
                lOutList.append(sOut + sFile)
        for iIndex, sFile in enumerate(lInputList):
            sys.stdout.write('Processing '+sFile)
            with open(sFile, 'r') as f:
                with open(lOutList[iIndex], 'w') as w:
                    while(1):
                        sLine = f.readline()
                        if not sLine:
                            break
                        if sLine[0] != '#':
                            lLineSplitList = sLine.split('\t')
                            if lLineSplitList[12].find('[') !=-1 or lLineSplitList[12].find(']') !=-1:
                                lLineSplitList[12] = lLineSplitList[12].replace("[", "(");
                                lLineSplitList[12] = lLineSplitList[12].replace("]", ")");
                                sLine = "\t".join(lLineSplitList)
                        w.write(sLine)
            sys.stdout.write(' -> Done\n')                            
        return
    
    
    if args.bDatabase:
        if os.path.isfile(sInput):
            lInputList.append(sInput)
            lOutList.append(sOut)
        else:
            if platform.system() == 'Windows':
                if sInput[-1] != '\\':
                    sInput = sInput + '\\'
                if sOut[-1] != '\\':
                    sOut = sOut + '\\'
            else:
                if sInput[-1] != '/':
                    sInput = sInput + '/'
                if sOut[-1] != '/':
                    sOut = sOut + '/'
        for sFile in os.listdir(sInput):
            if sFile.endswith(".fasta") or sFile.endswith(".fa") or sFile.endswith(".fna"):
                lInputList.append(sInput + sFile)
                lOutList.append(sOut + sFile)
        for iIndex, sFile in enumerate(lInputList):
            sys.stdout.write('Processing '+sFile)
            with open(sFile, 'r') as f:
                with open(lOutList[iIndex], 'w') as w:
                    while(1):
                        sLine = f.readline()
                        if not sLine:
                            break
                        if sLine[0] == '>':
                            sLine = sLine.replace("[", "(");
                            sLine = sLine.replace("]", ")");
                        w.write(sLine)
            sys.stdout.write(' -> Done\n')
        return
    

if __name__ == '__main__':
    main()
