#!/usr/bin/env python
#coding=UTF-8
'''
========================Usage=========================
assembly stats
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
statsNames = ["name","Total_length","Number","Mean_length","Longest","Shorest","N25","N50","N75",]

def get_time():
	return time.strftime('%H:%M:%S',time.localtime(time.time()))

def recordcmd():
	out = open("{0}/cmd.sh".format(rd),"w")
	out.write("python {0}".format(" ".join(sys.argv[:])))

def sortdict(dicts):
	tmpdir = {}
	for ele in sorted(dicts.items(),key=lambda d:d[1],reverse=True):
		tmpdir[ele[0]] = ele[1]
	return tmpdir

def loadfasta(paths):
	tmpdir = {}
	for ps,ds,fs in os.walk(paths):
		for f in fs:
			if f.endswith(".fa") or f.endswith(".fas") or f.endswith(".fasta"):
				sys.stdout.write("[{0}] Load file {1}\n".format(get_time(),f))
				tmpdir[f] = {}
				for seqs in SeqIO.parse("{0}/{1}".format(ps,f),"fasta"):
					tmpdir[f][str(seqs.description)] = len(str(seqs.seq))
	newdir = sortdict(tmpdir)
	sys.stdout.write("[{0}] File loading complete!\n".format(get_time()))
	return newdir

def getvalues(paths):
	fastadir = loadfasta(paths)
	tmpdir = {}
	for keys in fastadir.keys():
		tmpdir[keys] = {}
		tmpdir[keys]["longest"] = max(fastadir[keys][x] for x in fastadir[keys].keys())
		tmpdir[keys]["shortest"] = min(fastadir[keys][x] for x in fastadir[keys].keys())
		seqsize = sorted([fastadir[keys][x] for x in fastadir[keys].keys()],reverse=True)
		Total = sum(seqsize)
		tmpdir[keys]["total_length"] = Total
		tmpdir[keys]["Number"] = len(fastadir[keys])
		tmpdir[keys]["average"] = Total/len(fastadir[keys])
		tmp = 0
		N25 = 0
		N50 = 0
		N75 = 0
		for i in seqsize:
			tmp += i
			if tmp >= 0.25 * Total and not N75:
				N75 = i
			if tmp >= 0.5 * Total and not N50:
				N50 = i
			if tmp >= 0.75 * Total and not N25:
				N25 = i
		tmpdir[keys]["n25"] = N25
		tmpdir[keys]["n50"] = N50
		tmpdir[keys]["n75"] = N75
	return tmpdir

def write2file(paths):
	allvalues = getvalues(paths)
	out = open("{0}/assembly.stats".format(rd),"w")
	out.write("File\tTotal_length\tNumber\tMean_length\tLongest\tShortest\tN25\tN50\tN75\n")
	for keys in allvalues.keys():
		out.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\n".format(keys,allvalues[keys]["total_length"],
		allvalues[keys]["Number"],allvalues[keys]["average"],allvalues[keys]["longest"],allvalues[keys]["shortest"],
		allvalues[keys]["n25"],allvalues[keys]["n50"],allvalues[keys]["n75"]))

def arg_parse():
    parse = argparse.ArgumentParser(usage="%(prog)s[options]")
    parse.add_argument("--paths",help="The directory of your fasta file")
    return parse.parse_args()

def main():
	options = arg_parse()
	if options.paths == None:
		os.system("python {0} -h".format(sys.argv[0]))
		exit("[{0}] Error: incomplete options".format(get_time()))
	recordcmd()
	paths = options.paths
	if not os.path.dirname(paths):
		sys.stderr.write("[{0}] Error for paths options, you should point a directory".format(get_time()))

	write2file(paths)

if __name__ == "__main__":
	main()
