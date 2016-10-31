#!/usr/bin/env python
#coding=UTF-8
'''
========================Usage=========================
Get Single Copy Orthology genes from Orthomcl Results
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
global rd
rd = os.getcwd()

def get_time():
	return time.strftime('%H:%M:%S',time.localtime(time.time()))

def arg_parse():
    parse = argparse.ArgumentParser(usage="%(prog)s[options]")
    parse.add_argument("--orthomcl",help="orthomcl results, mclOutput")
    parse.add_argument("--OG",help="The final Orthology genes file")
    parse.add_argument("--num",help="The species number")
    return parse.parse_args()

def main():
	options = arg_parse()
	if options.orthomcl == None or options.OG== None:
		os.system("python {0} -h".format(sys.argv[0]))
		exit("[{0}] Error: incomplete options".format(get_time()))

	orthomcl = options.orthomcl
	OG = options.OG
	num = int(options.num)

	out = open(OG,"w")
	for line in open(orthomcl,"r"):
		ele = line.strip().split()
		tmpdir = []
		for nid in ele:
			tmpdir.append(nid[:2])
		if len(tmpdir) == len(set(tmpdir)) and len(tmpdir) == num:
			out.write("{0}\n".format(line.strip()))

if __name__ == "__main__":
	main()
