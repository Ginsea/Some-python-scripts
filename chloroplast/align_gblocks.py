#!/usr/bin/env python
#coding=utf-8

import os,sys,argparse

global gblocks
gblocks = "/home/ginsea/soft/Gblocks_0.91b/Gblocks"

def opt():
	args = argparse.ArgumentParser(usage="align sequences and Gblocks treat")
	args.add_argument("--ind",help="The input directory")
	args.add_argument("--ous",help="The output shell script")
	return args.parse_args()

def main():
	args = opt()
	if args.ind == None or args.ous == None:
		os.system("python {0} -h".format(sys.argv[0]))
		exit("Error: Incomplete Options")
	ind = args.ind
	ous = args.ous

	try:
		os.stat("align")
	except:
		os.mkdir("align")

	out = open(ous,"w")
	for p,ds,fs in os.walk(ind):
		for f in fs:
			if f.endswith(".fa"):
				out.write("mafft --auto {0}/{1} > {3}/align/{2}.aln && {4} {3}/align/{2}.aln -t=c\n".format(p,f,os.path.splitext(f)[0],os.getcwd(),gblocks))

if __name__ == "__main__":
	main()