'''
Created on Mar 14, 2016

@author: xgo
'''

import argparse, os
from os import listdir
from os.path import isfile, join
from string import split

parser = argparse.ArgumentParser(description="convert mgf file with fragment charge to ft2 file",
                                 prog='Mgf2Ft2_wFragmentCharge.py',  # program name
                                 prefix_chars='-',  # prefix for options
                                 fromfile_prefix_chars='@',  # if options are read from file, '@args.txt'
                                 conflict_handler='resolve',  # for handling conflict options
                                 add_help=True,  # include help in the options
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter  # print default values for options in help message
                                 )
# # input files and directories
parser.add_argument("-i", "--input", help="folder contains mgf files", dest='sMgfFolder', required=True)
# # input files and directories
parser.add_argument("-o", "--out", help="output folder for the FT2 files", dest='sFt2Folder', required=True)


def main(argv=None):
    # try to get arguments and error handling
    if argv is None:
        args = parser.parse_args()
        
    sInputFolder = args.sMgfFolder
    sOutputFolder = args.sFt2Folder
    
    # write info for each scan
    sFakeScanType = "I    ScanType    FT-MS1/FT-MS2 = 000.00 @ CID\n"
    sLine = ""
    dPepMassZ = 0.0
    iPepCharge = 0
    iFragmentCharge = 0
    dFragmentMassZ = 0.0
    dFragmentIntensity = 0.0
    asSplit = []
    print "Start converting..."
    for sFileInput in listdir(sInputFolder):
        if isfile(join(sInputFolder, sFileInput)) and sFileInput.endswith('.mgf'):
            fOutputFile = open(sOutputFolder + "/" + os.path.splitext(sFileInput)[0] + ".FT2", 'w')
            # write head for the converter
            fOutputFile.write("H\tExtractor\tRaxport\tv3.3\n")
            fOutputFile.write("H\tm/z\tIntensity\tResolution\tBaseline\tNoise\tCharge\n")
            fOutputFile.write("H\tInstrument Model\tOrbitrap Elite\n")
            
            fInputFile = open(join(sInputFolder, sFileInput), 'r')
            
            iScanId = 1
            while 1:
                sLine = fInputFile.readline().rstrip()
                if not sLine:
                    break
                if sLine.startswith('BEGIN'):
                    iPepCharge = 0
                    dPepMassZ = 0
                    if iScanId % 100 == 0:
                        print "Converting " + str(iScanId) + " scans"
                elif sLine.startswith("END"):
                    iScanId += 1
                elif sLine.startswith('CHARGE'):
                    iPepCharge = int(sLine[7:-1])
                elif sLine.startswith('PEPMASS'):
                    dPepMassZ = float(sLine[8:])
                    fOutputFile.write("S\t" + str(iScanId) + "\t" + str(iScanId) + "\t" + str(dPepMassZ) + "\n")
                    if iPepCharge > 0:
                        fOutputFile.write("Z\t" + str(iPepCharge) + "\t" + str(dPepMassZ * iPepCharge) + "\n")
                    fOutputFile.write(sFakeScanType)
                elif sLine.startswith('TITLE') or sLine.startswith('RTINSECONDS'):
                    continue
                else:
                    asSplit = split(sLine, ' ')
                    iFragmentCharge = int(asSplit[2])
                    dFragmentMassZ = float(asSplit[0])
                    dFragmentIntensity = float(asSplit[1])
                    if iFragmentCharge > 1:
                        dFragmentMassZ = (dFragmentMassZ + (iFragmentCharge - 1) * 1.007276)
                        dFragmentMassZ = dFragmentMassZ / float(iFragmentCharge)
                        
                    fOutputFile.write(str(dFragmentMassZ) + "\t" + str(dFragmentIntensity) + "\t0\t0\t0\t" + str(iFragmentCharge) + "\n")
            fInputFile.close()
            fOutputFile.flush()
            fOutputFile.close()
    print "Finish converting."
    
    
if __name__ == '__main__':
    main()
    
