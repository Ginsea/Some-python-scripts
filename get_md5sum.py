#!/usr/bin/env python
#coding=UTF-8
'''
========================Usage=========================
get md5 value for all files in specific folder
========================Author========================
get md5 for data backup
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

def recordcmd():
	out = open("{0}/run_{1}.sh".format(rd,sys.argv[0]),"w")
	out.write("python {0}".format(" ".join(sys.argv[:])))

def arg_parse():
    parse = argparse.ArgumentParser(usage="%(prog)s[options]")
    parse.add_argument("--inf1",help="Your work directory")
    return parse.parse_args()

def getmd5(folder):
	tmp = {}
	for ps,ds,fs in os.walk(folder):
		for f in fs:
			sys.stdout.write("[{0}] Get md5 from file {1}\n".format(get_time(),f))
			x = os.popen("md5sum {0}/{1}".format(ps,f))
			try:
				tmp[ps][f] = x.strip().split()[0]
			except:
				tmp[ps] = {}
				tmp[ps][f] = x.strip().split()[0]
	return tmp

def write2file(folder):
	out = open("md5sum.txt","w")
	md5dir = getmd5(folder)
	sys.stdout.write("[{0}] Write results to file md5sum.txt\n".format(get_time()))
	for keys in md5dir.keys():
		out.write("{0}\n".format(keys))
		for k1 in md5dir[keys].keys():
			out.write("\t{0}\t{1}\n".format(k1,md5dir[keys][k1]))
	sys.stdout.write("[{0}] Done!\n".format(get_time()))

def main():
	options = arg_parse()
	if options.inf1 == None:
		os.system("python {0} -h".format(sys.argv[0]))
		exit("[{0}] Error: incomplete options".format(get_time()))
	recordcmd()
	inf1 = options.inf1
	write2file(inf1)

if __name__ == "__main__":
	main()
