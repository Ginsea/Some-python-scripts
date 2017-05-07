#!/usr/bin/env python
#coding=utf-8

'''
get information from fasta file which containd chloroplast information(source from NCBI)
'''

import os,sys,argparse,re
from Bio import SeqIO

def opt():
	args = argparse.ArgumentParser(usage="get info from NCBI chloroplast fasta file")
	args.add_argument("--inf",help="The input fasta file with fasta format")
	args.add_argument("--ouf",help="The output file")
	return args.parse_args()

def main():
	args = opt()
	if args.inf == None or args.ouf == None:
		os.system("python {0} -h".format(sys.argv[0]))
		exit("Error: Incomplete Options")
	
	aid = re.compile(r"(^[\w]+\.[0-9])")

	inf = args.inf
	out = open(args.ouf,"w")

	tmptup = []
	for seqs in SeqIO.parse(inf,"fasta"):
		des = seqs.description
		ids = aid.search(des).groups()[0]
		sname = des.split("chloroplast")[0].lstrip(ids).strip()
#		if sname not in tmptup:
#			out.write("{0}\t{1}\n".format(ids,sname))
#			tmptup.append(sname)
#		else:
#			continue
		out.write("{0}\t{1}\n".format(ids,sname))
		
if __name__ == "__main__":
	main()

