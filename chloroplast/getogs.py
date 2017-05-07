#!/usr/bin/env python
#coding=utf-8

'''
loading coding sequences and protein sequences of multiple chloroplast genomes, and then produce single copy orthologous pairs.
These gene pairs were saved as fasta format, then conserved alignment domains was extracted through pal2nal 
The author of this script is ginsea(cginsea@gmail.com)
Version: 0.1
Date: 2017-05-07
'''

import os
import sys
from optparse import OptionParser
import time
import re

def ltime():
    return time.strftime("%H:%M:%S",time.localtime(time.time()))

def readfa(fa):
    sys.stdout.write("[{0}] Loading {1}\n".format(ltime(),os.path.basename(fa)))
    starts = time.time()
    tmpdir = {}
    ids = ""
    with open(fa,"r") as inf:
        for line in inf:
            if line.startswith(">"):
                ids = line.lstrip(">")
                tmpdir[ids] = ""
            else:
                tmpdir[ids] += line.strip()
    sys.stdout.write("[{0}] File loading finished, you have spent {1} minutes\n".format(ltime(),(time.time() - starts)/60))
    return tmpdir

class GetOgs(object):
    def __init__(self,inp,inn):
        self.inp = inp
        self.inn = inn

    def regpattern(self):
        sidsp = re.compile(r"lcl\|([\w]+\.[0-9])")
        gidsp = re.compile(r"_cds_([\w]+\.[0-9])_[0-9]")
        pidsp = re.compile(r"_prot_([\w]+\.[0-9])_[0-9]")
        gnamep = re.compile(r"\[gene=([\w]+)\]")
        return sidsp,gidsp,pidsp,gnamep

    def treatcoding(self):

        fadir = readfa(self.inn)

        tmpdir = {}
        tmpfa = {}

        regp = self.regpattern()
        sidsp,gidsp,pidsp,gnamep = regp

        for keys in fadir.keys():
            sids = sidsp.search(keys).groups()[0]
            gids = gidsp.search(keys).groups()[0]
            gname = gnamep.search(keys).groups()[0]





