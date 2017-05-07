#!/usr/bin/env python
#coding=utf-8

import os,sys,argparse
from Bio import SeqIO

def opt():
	args = argparse.ArgumentParser(usage="merge fasta file")
	args.add_argument("--ind",help="input directory")
	args.add_argument("--ouf",help="The output file")
	return args.parse_args()

def fadir(infa):
	tmpdir = {}
	for seqs in SeqIO.parse(infa,"fasta"):
		tmpdir[seqs.id] = seqs.seq
	return tmpdir

def main():
	args = opt()
	if args.ind == None or args.ouf == None:
		os.system("python {0} -h".format(sys.argv[0]))
		exit("Error: Incomplete Options")
	
	ind = args.ind
	ouf = args.ouf 

	out = open("{0}.fa".format(ouf),"w")
	out1 = open("{0}.phy".format(ouf),"w")
	out2 = open("{0}.nex".format(ouf),"w")

	tmpdir = {}

	for p,ds,fs in os.walk(ind):
		for f in fs:
			if f.endswith("aln-gb"):
				gn = os.path.splitext(f)[0]
				fdir = fadir("{0}/{1}".format(p,f))
				for keys in fdir.keys():
					try:
						tmpdir[keys][gn] = fdir[keys]
					except KeyError:
						tmpdir[keys] = {}
						tmpdir[keys][gn] = fdir[keys]
	
	tmpdir1 = {}
	for keys in tmpdir.keys():
		for k1 in sorted(tmpdir[keys].keys()):
			try:
				tmpdir1[keys] += str(tmpdir[keys][k1])
			except:
				tmpdir1[keys] = "{0}".format(str(tmpdir[keys][k1]))

	for keys in tmpdir1.keys():
		out.write(">{0}\n{1}\n".format(keys,tmpdir1[keys]))
	
	seqsn = len(tmpdir1)
	genen = len(tmpdir1[list(tmpdir1.keys())[0]])
	out1.write("{0}\t{1}\n".format(seqsn,genen))
	out2.write("#NEXUS\nbegin data;\ndimensions ntax={0} nchar={1};\nformat datatype=dna interleave=yes gap=- missing=?;\nmatrix\n".format(seqsn,genen))
	for keys in tmpdir1.keys():
		out1.write("{0}\t{1}\n".format(keys,tmpdir1[keys]))
		out2.write("{0}\t{1}\n".format(keys,tmpdir1[keys]))
	out2.write(";\nend;\n")

if __name__ == "__main__":
	main()