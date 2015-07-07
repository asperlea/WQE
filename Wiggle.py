__author__ = 'adriana'

import re
import subprocess
import gzip
import glob
import itertools
import pdb

from numpy import array, where, ones

import sys

class Wiggle:
    '''
    Wiggle files (http://genome.ucsc.edu/goldenPath/help/wiggle.html) are files
    contain dense continuous genomic annotation data, like GC content, probabil-
    ity scores and transcriptome data. This class takes a set of wig files or
    or a gzipped set and loads them into iterators. Because it does not store
    then in memory, it is best that the function that uses a wiggle object does
    so sequentially throughout a chromosome instead of jumping around.

    Because this has been slow, I have recently (10/20/11) added a seek feature
    using an index file for each wiggle file. I made these indices with a simple
    bash one-liner.

    The index file looks like:

    line_number \t byte_offset \t chr_pos_start

    where the first column is the position of a header line, such as:
    fixedStep chrom=chr1 start=34045 step=1

    the second column is the byte offset before said line starts, for mmap

    the third column is the chr position (in this case 34045) and the third
    line is the line number for this position.

    the script is:

    for wig in *.gz
    do
        gzcat $wig \
        | grep -nb fixedStep \
        | perl -ne 's/(\d+):(\d+).*start=(\d+).*/$1\t$2\t$3/ && print' \
        > $wig.idx
    done

    (10/28/12 - thanks self from one year ago for writing this down!)

    Adriana 2015 update:
    hg38 data has all the chromosomes in the same file so before using the bash
    one liner above do:

    Unzip the hg38 data
    Run wigSplitByChr from python_utils on it: python wigSplitByChr path_to_hg38_file
    Zip all the .wigFix files: for wig in *.wigFix; do gzip $wig; done
    Run the bash one liner from above to create the .idx files.

    Also, these comments are nice but at some point I should get around to
    writing some proper documentation.
    '''

    def __init__(self, name, wiggle_dir, file_prefix,
                 file_suffix, max_buffer=50):
        self.name = name

        self.lookback_buffers = {}
        self.max_buffer = max_buffer

        glob_components = (wiggle_dir, '/', file_prefix, "*", file_suffix) #(wiggle_dir, '/', file_prefix, '*', file_suffix)

        # put all files into a list
        gzlist = glob.glob(''.join(glob_components))

        # associate files into a dict by chromosome name
        re_components = map(util.to_raw, glob_components)
        re_components[-2] = "(\w+)"

        pattern = re.compile(''.join(re_components))

        self.fnames = \
            dict([(pattern.match(gzfile).group(1), gzfile) \
                  for gzfile in gzlist])
        self.idxnames = \
            dict([(pattern.match(gzfile).group(1), gzfile + r'.idx') \
                  for gzfile in gzlist])
        self.fhandles = \
            dict([(chr, gzip.open(fn)) \
                  for chr, fn in self.fnames.items()])
        self.fidxhandles = \
            dict([(chr, open(fn)) \
                  for chr, fn in self.idxnames.items()])

        # load the indices into a dict of chrs
        self.chridx = {}
        for chr, fidxh in self.fidxhandles.items():
            self.chridx[chr] = [map(int, fl.split()) for fl in fidxh.readlines()]

        wiggle_tracks[name] = self

    def get_region(self, chr, start, end):
        ''' we look through the chromosome index list and we pull out the
            seek position we want by finding the closest chr pos (col 3) that
            does not go over our start. we check to make sure that our end
            is less than the next chr pos (col 3 of next row). col 2 of the
            row is our seek() position. Then we figure out how many lines
            we need to skip, and how many we need to take, and we just return
            them all. no lookback buffer.

        chrom 0 , start 1, end 2, strand 3, value 4.
        '''

        start += 1  # to adjust for pythonic numbering
        end += 2

        next_idx_line = 0
        while (self.chridx[chr][next_idx_line][2] < start) and (next_idx_line < len(self.chridx[chr]) - 2):
            next_idx_line += 1

        if next_idx_line < 1: raise ValueError("START not in wiggle file")

        curr_idx_line = next_idx_line - 1

        next_idx_row = self.chridx[chr][next_idx_line]
        curr_idx_row = self.chridx[chr][curr_idx_line]

        # if the start and end positions are not on the same set of wiggles
        if next_idx_row[2] <= end:
            raise ValueError("This region is not contiguous in the wig file!")

        # if there are not enough lines in this wiggle set
        if next_idx_row[0] - curr_idx_row[0] < end - curr_idx_row[2]:
            raise ValueError("This wiggle set is not large enough!")

        # get seek position, number of lines to jump, and number of lines to keep
        seekpos = curr_idx_row[1]
        jumplines = start - curr_idx_row[2]
        keeplines = end - start

        # tups to keep: chrom 0 , start 1, end 2, strand 3, value 4.
        tups = []

        fh = self.fhandles[chr]
        fh.seek(seekpos)
        for throwaway in range(jumplines):
            fh.readline()

        for keep in range(keeplines):
            # the start/end coords will be pythonic
            tups.append((chr, start + keep - 1, start + keep, '+', float(fh.readline())))

#        if chr not in self.lookback_buffers:
#            self.lookback_buffers[chr] = []
#
#        buffered_iter = \
#            itertools.chain(self.lookback_buffers[chr],self.wigiters[chr])
#        until_start = \
#            itertools.dropwhile(lambda x: x[1] < start - 1,buffered_iter)
#        until_end = \
#            itertools.takewhile(lambda x: x[1] < end, until_start)
#
#        map(tups.append, until_end)
#
#        if len(tups) != end - start + 1:
#            raise WiggleBadRangeSizeException
#
#        to_append = self.max_buffer - len(self.lookback_buffers[chr])
#
#        self.lookback_buffers[chr].extend(tups[-to_append:])

        return tups





