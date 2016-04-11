#!/usr/bin/env python

'''
This script can be used to add taxon to multiple fasta files in orthomcl analysis
You need add orthomclAdjustFasta to your path
Usage: python add_taxon_orthomcl.py path
'''
from Bio import SeqIO
import sys
import os,os.path

try:
    sys.argv[1]
except IndexError:
    print "Please input path of multiple fasta files"
    exit(1)

path = sys.argv[1]

os.system("mkdir %s/complaintFasta"%path)

for parent, dirnames, filenames in os.walk(path):
    for filename in filenames:
        if filename.split(".")[1] == "fa" and len(filename.split(".")[0]) == 5:
             os.system("cd %s/complaintFasta"%path)
             os.system("orthomclAdjustFasta %s %s/%s 1"%(filename.split(".")[0], path, filename))
