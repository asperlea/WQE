__author__ = 'adriana'

import sys
from Wiggle import Wiggle

'''
Head of true.ss.fasta for reference:
>.|chr10|100042558|100048772|-|1|2
GCGGAACCAACGTTGGTGAGTTAGGCTGAGCTTTTTTTCTTCCAGGTTAACTTCCACCTC
>.|chr10|100048861|100054361|-|2|2
ATGATGTCACTTCAGGTAGGTGGTCACTGCCTTTGTGACTTTCAGGTGACCATGGTGATT
>.|chr10|100054431|100057027|-|3|2
CAGTTCCTGGAACAGGTAAAATCTCATTTGTACTTGTTCCTGCAGGTTCACCAGGGCATC
>.|chr10|100057137|100063628|-|4|2
ATTCTCTCAGCAAGGGTAAGGGGAGTCCTGCCCTCTTTCCCTTAGGAATGCAAGACTTTA
>.|chr10|100063710|100065202|-|5|2
AAGCTCTTCCAGAAGGTATGTGGAGAAGCACTGCTTTTCCTCTAGCTGGCCAAGGTCTAC
'''

def main():
    if len(sys.argv) < 3:
        print("Usage: getConsScores.py <input file> <output file>")
        exit(1)
    exonsFile = open(sys.argv[1], "r")
    consScores = open(sys.argv[2], "w")

    MamConserv = Wiggle(name='MamConserv',
                        wiggle_dir='/u/home/a/asperlea/project-ernst/phyloP45way',
                        file_prefix='chr',
                        file_suffix='.phyloP46way.placental.wigFix.gz')

    for line in exonsFile:
        if line[0] == '>':
            parsedLine = line.split("|")
            chrom = parsedLine[1][3:]
            chromStart = int(parsedLine[2])
            chromEnd = int(parsedLine[3])
            region = MamConserv.get_region(chrom, chromStart, chromEnd)

            print region[0], region[1]

main()
