__author__ = 'adriana'
import gzip
import sys
from collections import defaultdict

def main():
    if len(sys.argv) < 2:
        print "Usage: python parseWig.py <file1>"
        exit(1)
    wigFile = sys.argv[1]
    f = gzip.open(wigFile, 'rb')
    
    # Create chromData dictionary which will contain the intervals for which we have data
    chromData = defaultdict(list)
    curInt = (0, 0)
    prevChrom = ""
    curChrom = ""
    chromList = []
    
    for line in f:
        if len(line) > 7:
            if curChrom != "":
                chromData[curChrom].append(curInt)
            splitLine = line.split(" ")
            start = int(splitLine[2].split("=")[1])
            curInt = (start, start)
            prevChrom = curChrom
            curChrom = splitLine[1].split("=")[1]

            if curChrom != prevChrom:
                ofile = open("consChrom " + str(prevChrom) + ".wigFix
        else:
            curInt = (curInt[0], curInt[1] + 1) 
    f.close()

    ofile = open("consPerChrom.txt", "w")
    for chrom in chromData:
        ofile.write(chrom + "\n")
        for interval in chromData[chrom]:
            ofile.write(str(interval) + "\n")
    ofile.close()

main()
