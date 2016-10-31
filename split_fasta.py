#!/usr/bin/env python
#coding=UTF-8
'''
========================Usage=========================
对较大的fasta文件按照一定序列数目进行分割
========================Author========================
Ginsea Chen
========================E-mail========================
chenzx@biobreeding.com.cn
======================================================
'''
import argparse
import time
import sys
import os
import re
from Bio import SeqIO
global rd
rd = os.getcwd()

def ltime():
	return time.strftime('%H:%M:%S',time.localtime(time.time()))

def arg_parse():
    parse = argparse.ArgumentParser(usage="%(prog)s[options]")
    parse.add_argument("--fasta",help="[FORCE] The input fasta file")
    parse.add_argument("--num",default=1000,help="[OPTION] The sequence number of each file, The default is 1000")
    parse.add_argument("--oudir",help="[FORCE] The output directory")
    return parse.parse_args()
def batch_iterator(iterator,batch_size):
	entry = True
	while entry:
		batch = []
		while len(batch) < batch_size:
			try:
				entry = iterator.next()
			except StopIteration:
				entry = None
			if entry is None:
				break
			batch.append(entry)
		if batch:
			yield batch

def main():
	options = arg_parse()
	if options.fasta == None or options.oudir == None:
		os.system("python {0} -h".format(sys.argv[0]))
		exit("[{0}] Error: incomplete options\n".format(ltime()))

	fasta = options.fasta
	num = int(options.num)
	oudir = options.oudir

	record_iter = SeqIO.parse(open(fasta),"fasta")
	for i, batch in enumerate(batch_iterator(record_iter, num)):
		filename = "{0}/{1}_{2}.fasta".format(oudir,os.path.splitext(os.path.basename(fasta))[0],i+1)
		handle = open(filename, "w")
		count = SeqIO.write(batch, handle, "fasta")
		handle.close()
		sys.stdout.write("[{0}] Wrote {1} records to {2}\n".format(ltime(),count,filename))

if __name__ == "__main__":
	main()
