#!/usr/bin/env python
#coding=utf-8

'''
get ogs from chlorplast coding sequences fasta file
'''

import os,sys,argparse,re
from Bio import SeqIO

def opt():
	args = argparse.ArgumentParser(usage="get OGs from chloroplast coding sequences fasta file")
	args.add_argument("--inf",help="The input fasta file")
	args.add_argument("--ini",help="The input accids lits")
	args.add_argument("--oud",help="The output prefix")
	return args.parse_args()

def acc2abb(inf):
#	��¼�ź�������д�Ķ�Ӧ��ϵ
	tmpdir = {}
	for line in open(inf,"r"):
		ele = line.strip().split()
		tmpdir[ele[0]] = ele[-1]
	return tmpdir

def test_dir(ind):
#	���ֵ��л�ȡ����������
	tmptup = []
	nametup = [ind[k1] for k1 in ind.keys()]
	for gn in set(nametup):
		if nametup.count(gn) == 1:
			tmptup.append(gn)
		else:
			continue
	return tmptup

def fadir(inf):
	sidsp = re.compile(r"lcl\|([\w]+\.[0-9])")
	gidsp = re.compile(r"_prot_([\w]+\.[0-9])_[0-9]")
	gnamep = re.compile(r"\[gene=([\w]+)\]")
	
	tmpdir = {}
	tmpfa = {}
	for seqs in SeqIO.parse(inf,"fasta"):
		des = str(seqs.description)
		sids = sidsp.match(des).groups()[0]
		gids = gidsp.search(des).groups()[0]
		gname = gnamep.search(des).groups()[0]
		try:
			tmpdir[sids][gids] = gname
		except KeyError:
			tmpdir[sids] = {}
			tmpdir[sids][gids] = gname
		try:
			tmpfa[sids][gids][gname] = str(seqs.seq)
		except KeyError:
			try:
				tmpfa[sids][gids] = {}
				tmpfa[sids][gids][gname] = str(seqs.seq)
			except KeyError:
				tmpfa[sids] = {}
				tmpfa[sids][gids] = {}
				tmpfa[sids][gids][gname] = str(seqs.seq)
				
	tmpset = set(test_dir(tmpdir[list(tmpdir.keys())[0]]))
	for keys in tmpdir.keys():
		tmpset = tmpset & set(test_dir(tmpdir[keys]))

	tmpfa2 = {}

	for keys in tmpfa.keys():
		for k1 in tmpfa[keys].keys():
			for k2 in tmpfa[keys][k1].keys():
				if k2 in tmpset:
					try:
						tmpfa2[k2][keys] = tmpfa[keys][k1][k2]
					except KeyError:
						tmpfa2[k2] = {}
						tmpfa2[k2][keys] = tmpfa[keys][k1][k2]
	return tmpfa2

def main():
	args = opt()
	if args.inf == None or args.ini == None or args.oud == None:
		os.system("python {0} -h".format(sys.argv[0]))
		exit("Error: Incomplete Options")
	
	inf = args.inf
	ini = args.ini
	oud = args.oud
	
	try:
		os.stat(oud)
	except:
		os.mkdir(oud)
	
	accdir = acc2abb(ini)
	fdir = fadir(inf)

	for keys in fdir.keys():
		out = open("{0}/{1}.fa".format(oud,keys),"w")
		for k1 in fdir[keys].keys():
			out.write(">{0}\n{1}\n".format(accdir[k1],fdir[keys][k1]))

if __name__ == "__main__":
	main()
