#!/usr/bin/python
#coding=utf-8

'''
treat ncbi info
'''

import os,sys,argparse

def opt():
	args = argparse.ArgumentParser(usage="treat ncbi info")
	args.add_argument("--inf")
	args.add_argument("--ouf")
	return args.parse_args()

def main():
	args = opt()
	if args.inf == None or args.ouf == None:
		os.system("python {0} -h".format(sys.argv[0]))
		exit("Error: Incomplete Options")
	
	inf = args.inf
	ouf = args.ouf
	out = open(ouf,"w")
	
	tmptup = []
	for line in open(inf,"r"):
		if not line.startswith("#"):
			ele = line.strip().split()
			if ele[-1] not in tmptup:
				out.write("{0}\t{1}\n".format(ele[0],ele[-1]))
				tmptup.append(ele[-1])
			else:
				print(line)

if __name__ == "__main__":
	main()
