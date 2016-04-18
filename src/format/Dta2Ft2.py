'''
Created on Feb 18, 2016

@author: xgo
'''

import sys, getopt, warnings, os, re
import argparse
from os import listdir
from os.path import isfile, join
from string import split

parser = argparse.ArgumentParser(description="convert dta to ft2 file",
                                 prog='Dta2Ft2.py',  # program name
                                 prefix_chars='-',  # prefix for options
                                 fromfile_prefix_chars='@',  # if options are read from file, '@args.txt'
                                 conflict_handler='resolve',  # for handling conflict options
                                 add_help=True,  # include help in the options
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter  # print default values for options in help message
                                 )
# # input files and directories
parser.add_argument("-i", "--input", help="folder contains dta files", dest='dtafolder', required=True)
# # input files and directories
parser.add_argument("-o", "--out", help="output FT2 file", dest='outputFile', required=True)


def main(argv=None):
    # try to get arguments and error handling
    if argv is None:
        args = parser.parse_args()
        
    sInputFolder = args.dtafolder
    sOutputFile = args.outputFile
    
    fOutputFile = open(sOutputFile, 'w')
    
    #write head for the converter
    fOutputFile.write("H\tExtractor\tRaxport\tv3.3\n")
    fOutputFile.write("H\tm/z\tIntensity\tResolution\tBaseline\tNoise\tCharge\n")
    fOutputFile.write("H\tInstrument Model\tOrbitrap Elite\n")
    print "Start converting..."
    #write info for each scan
    sFakeScanType = "I    ScanType    FT-MS1/FT-MS2 = 000.00 @ CID\n"
    sLine = ""
    dMass = 0.0
    iCharge = 0
    asSplit = []
    iScanId = 1
    for file in listdir(sInputFolder):
        if isfile(join(sInputFolder, file)):
            fInputFile = open(join(sInputFolder, file), 'r')
            sLine = fInputFile.readline().rstrip()
            asSplit = split(sLine, '\t')
            dMass = float(asSplit[0])
            iCharge = int(asSplit[1])
            fOutputFile.write("S\t"+str(iScanId)+"\t"+str(iScanId)+"\t"+str(dMass/iCharge)+"\n")
            iScanId += 1
            if iScanId%100==0:
                print "Converting " + str(iScanId) + " scans"
            fOutputFile.write("Z\t"+asSplit[1]+"\t"+asSplit[0]+"\n")
            fOutputFile.write(sFakeScanType)
            while 1:
                sLine = fInputFile.readline()
                if not sLine:
                    break
                fOutputFile.write(sLine)
            fInputFile.close()
    print "Finish converting."
    
    fOutputFile.flush()
    fOutputFile.close()

if __name__ == '__main__':
    main()
    
