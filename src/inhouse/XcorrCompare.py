'''
Created on Jun 17, 2016

@author: xgo
'''
import sys

def main(argv=None):

    if argv is None:
        argv = sys.argv


    sPinFile = "/home/xgo/ORNL/Sipros/MachineLearning/Experiments/Percolator/AMD_01/CometPercolator/AMD_01.pin"
    sLine = ""
    iScanId = 0
    sPep = ""
    fScore = 0.0
    lListTuper = [[0, "", 0.0] for _i in range(40000)]
    iPosBegin = 0
    iPosEnd = 0
    with open(sPinFile) as inputFile:
        next(inputFile)
        for sLine in inputFile:
            asLine = sLine.split("\t")
            iScanId = int(asLine[2])
            sPep = asLine[-2]
            iPosBegin = sPep.index('.')
            iPosEnd = sPep.find('.', iPosBegin + 1)
            sPep = sPep[iPosBegin + 1:iPosEnd]
            fScore = float(asLine[7])
            lListTuper[iScanId][0] = iScanId
            lListTuper[iScanId][1] = sPep
            lListTuper[iScanId][2] = fScore
            # lListTuper.append((iScanId, sPep, fScore))

    sSipFile = "/home/xgo/ORNL/Sipros/MachineLearning/Experiments/Percolator/AMD_01/XcorrFilter/AMD_HCD_DE10ppm_CS_1000_NCE30_180_01.AMD_Test.sip"
    iNumEqual = 0
    iNumNotEqual = 0

    fTemp = 0.0
    with open(sSipFile) as inputFile:
        for sLine in inputFile:
            if not sLine.startswith("#"):
                break
        for sLine in inputFile:
            asLine = sLine.split("\t")
            iScanId = int(asLine[1])
            sPep = asLine[-3]
            fScore = float(asLine[-4])
            sPep = sPep.replace('!', '#')
            sPep = sPep.replace('~', '*')
            iPosBegin = sPep.index('[')
            iPosEnd = sPep.index(']')
            sPep = sPep[iPosBegin + 1:iPosEnd]
            if lListTuper[iScanId][0] != 0 and sPep == lListTuper[iScanId][1]:
                fTemp = lListTuper[iScanId][2]
                if fScore <= lListTuper[iScanId][2]:
                    fTemp = fScore
                if abs(fScore - lListTuper[iScanId][2]) / (fTemp) < 0.01:
                    iNumEqual += 1
                else:
                    iNumNotEqual += 1
                    print iScanId, sPep, fScore, lListTuper[iScanId][2]

    print "Equal #: " + str(iNumEqual)
    print "Not Equal #: " + str(iNumNotEqual)


if __name__ == '__main__':
    sys.exit(main())
