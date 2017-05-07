#!/usr/bin/env python
#coding=utf-8

'''
convert fasta to paml
'''

import os,sys,argparse
from Bio import SeqIO

def opt():
	args = argparse.ArgumentParser(usage="convert fasta to paml")
	args.add_argument("--ind",help="The input fasta file")
	args.add_argument("--oud",help="The output paml file")
	return args.parse_args()

def fadir(fa):
	tmpdir = {}
	for seqs in SeqIO.parse(fa,"fasta"):
		tmpdir[str(seqs.id)] = str(seqs.seq)
	return tmpdir

def main():
	args = opt()
	if args.ind == None or args.oud == None:
		os.system("python {0} -h".format(sys.argv[0]))
		exit("Error: Incomplete Options")
	
	ind = args.ind 
	oud = args.oud

	try:
		os.stat(oud)
	except:
		os.mkdir(oud)

	for p,ds,fs in os.walk(ind):
		for f in fs:
			if f.endswith("aln"):
				fdir = fadir("{0}/{1}".format(p,f))

				seqsn = len(fdir)
				genen = len(fdir[list(fdir.keys())[0]])

				out = open("{0}/{1}.nuc".format(oud,os.path.splitext(f)[0]),"w")
				out.write("\t{0}\t{1}\n".format(seqsn,genen))

				for keys in fdir.keys():
					out.write("{0}\n{1}\n".format(keys,fdir[keys]))

if __name__ == "__main__":
	main()
