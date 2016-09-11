#!/usr/bin/env python
#-*- coding:utf-8 -*-


#========================Usage=========================
#对提供序列进行blast，并根据最佳匹配提取出对应的区域，保存为fasta文件
#你需要在你的PC上安装blast
#========================Author========================
#Ginsea Chen
#========================E-mail========================
#chenzx@biobreeding.com.cn
#======================================================


import argparse
import time
import sys
import os
import re
global rootdir
rootdir = os.getcwd()

def ltime():
	return time.strftime('%H:%M:%S',time.localtime(time.time()))

def arg_parse():
    parse = argparse.ArgumentParser(usage="%(prog)s[options]")
    parse.add_argument("--qs",help="[FORECE] query file, fasta format")
    parse.add_argument("--dbs",help="[FORECE] a folder with all target seqs, all file should be fasta format")
    return parse.parse_args()

def credir():

	try:
		os.stat("{0}/Analysis/db".format(rootdir))
		os.stat("{0}/Analysis/blast".format(rootdir))
		os.stat("{0}/Analysis/results".format(rootdir))
	except:
		os.makedirs("{0}/Analysis/db".format(rootdir))
		os.makedirs("{0}/Analysis/blast".format(rootdir))
		os.makedirs("{0}/Analysis/results".format(rootdir))
	
def blast(dbs,qs):
	for ps,ds,fs in os.walk(dbs):
		for f in fs:
			if f.endswith("fa") or f.endswith("fas") or f.endswith("fasta"):
				try:
					os.stat("{0}/Analysis/db/{1}".format(rootdir,os.path.splitext(f)[0]))
					os.stat("{0}/Analysis/blast/{1}".format(rootdir,os.path.splitext(f)[0]))
				except:
					os.mkdir("{0}/Analysis/db/{1}".format(rootdir,os.path.splitext(f)[0]))
					os.mkdir("{0}/Analysis/blast/{1}".format(rootdir,os.path.splitext(f)[0]))

				sys.stdout.write("[{0}] Copy {1} to {2}/Analysis/db/{3}\n".format(ltime(),f,rootdir,os.path.splitext(f)[0]))
				out = open("{0}/Analysis/db/{1}/{2}".format(rootdir,os.path.splitext(f)[0],f),"w")
				for line in open("{0}/{1}".format(ps,f),"r"):
					out.write("{0}\n".format(line.strip()))
				out.close()

				sys.stdout.write("[{0}] Run makeblastdb for {1}\n".format(ltime(),f))
				os.chdir("{0}/Analysis/db/{1}".format(rootdir,os.path.splitext(f)[0]))
				sys.stdout.write("[{0}] makeblastdb -in {1} -dbtype nucl\n".format(ltime(),f))
				os1 = os.system("makeblastdb -in {0} -dbtype nucl".format(f))
				if os1:
					sys.stderr.write("[{0}] Please Check makeblastdb".format(ltime()))
					sys.exit(1)
				else:
					sys.stdout.write("[{0}] makeblastdb analysis is finished\n".format(ltime()))

				sys.stdout.write("[{4}] blastn -query {0} -db {1}/Analysis/db/{2}/{3} -outfmt 6 -evalue 1e-5 -max_target_seqs 1 -out {1}/Analysis/blast/{2}/{2}.outfmt6\n".format(qs,rootdir,os.path.splitext(f)[0],f,ltime()))
				os2 = os.system("blastn -query {0} -db {1}/Analysis/db/{2}/{3} -outfmt 6 -evalue 1e-5 -max_target_seqs 1 -out {1}/Analysis/blast/{2}/{2}.outfmt6".format(qs,rootdir,os.path.splitext(f)[0],f))
				if os2:
					sys.stderr.write("[{0}] Please Check blastn".format(ltime()))
					sys.exit(1)
				else:
					sys.stdout.write("[{0}] blastn analysis is finished, result was {1}/Analysis/blast/{2}/{2}.outfmt6\n".format(ltime(),rootdir,os.path.splitext(f)[0]))

def getfasta(dbs):
	fadir = {}
	for ps,ds,fs in os.walk(dbs):
		for f in fs:
			if f.endswith("fa") or f.endswith("fas") or f.endswith("fasta"):
				sys.stdout.write("[{0}] Load file {1}\n".format(ltime(),f))
				ks = os.path.splitext(f)[0]
				fadir[ks] = {}
				r = open("{0}/{1}".format(ps,f),"r").read()
				es = r.split(">")
				for ids in es:
					if len(ids) > 1:
						si = ids.split("\n")[0].split()[0]
						ss = "".join(ids.split("\n")[1:])
						fadir[ks][si] = ss
	return fadir

def DNA_complement(sequence):
    sequence = sequence.upper()
    sequence = sequence.replace('A', 't')
    sequence = sequence.replace('T', 'a')
    sequence = sequence.replace('C', 'g')
    sequence = sequence.replace('G', 'c')
    return sequence.upper()
 
def DNA_reverse(sequence):
    sequence = sequence.upper()
    return sequence[::-1]

def getseqs(dbs):
	fadir = getfasta(dbs)
	for ps,ds,fs in os.walk("{0}/Analysis/blast".format(rootdir)):
		for f in fs:
			if f.endswith("outfmt6"):
				sys.stdout.write("[{0}] Load file {1}\n".format(ltime(),f))
				out = open("{0}/Analysis/results/{1}.fa".format(rootdir,os.path.splitext(f)[0]),"w")
				for line in open("{0}/{1}".format(ps,f),"r"):
					ele = line.strip().split("\t")
					query = ele[0]
					targets = ele[1]
					sp = int(ele[8])
					ep = int(ele[9])
					if sp < ep:
						seqs = fadir[os.path.splitext(f)[0]][targets][sp -1:ep]
						out.write(">{0}\t{1}\t{2}\t{3}\n{4}\n".format(query,targets,sp,ep,seqs))
					elif sp > ep:
						seqs =  DNA_reverse(DNA_complement(fadir[os.path.splitext(f)[0]][targets][ep -1:sp]))
						out.write(">{0}\t{1}\t{2}\t{3}\n{4}\n".format(query,targets,sp,ep,seqs))

def main():
	options = arg_parse()
	if options.qs == None or options.dbs== None:
		sys.stdout.write('''Description:run blast, and then get hit regions
		Author: chenzx
		E-mail: chenzx@biobreeding.com.cn
		Date: 2016/9/11
		''')
		os.system("python {0} -h".format(sys.argv[0]))
		exit("[{0}] Error: incomplete options".format(ltime()))
	
	qs = options.qs
	dbs = options.dbs

	credir()
	blast(dbs,qs)
	getseqs(dbs)

if __name__ == "__main__":
	main()
