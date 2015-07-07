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
    if len(sys.argv) < 2:
        print("Usage: getConsScores.py <file1>")
        #exit(1)

    MamConserv = Wiggle(name='MamConserv',
                        wiggle_dir='/u/home/a/asperlea/project-ernst/phyloP45way',
                        file_prefix='chr',
                        file_suffix='.phyloP46way.placental.wigFix.gz')

    print "Trying for chr10 region 100042558-100048772:\n"
    regions = MamConserv.get_region('10', 100042558, 100048772)
    print regions[0]
    print regions[-1]

main()
