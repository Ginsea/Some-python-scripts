#!/usr/bin/env python
#coding=utf-8

'''
perform codeml analysis
'''

import os,sys,argparse,re

def opt():
	args = argparse.ArgumentParser(usage="perfrom codeml analysis")
	args.add_argument("--nuc",help="The directory contained nuc files which used in codeml analysis")
	args.add_argument("--tre",help="The guided tree file with newick format")
	args.add_argument("--ctl",help="The control file of codeml")
	args.add_argument("--model",help="The analysis model, which should be free, site or bs")
	args.add_argument("--ous",help="The output shell script")
	return args.parse_args()

def change_ctl(ctl,model,opath,nuc,tre):
	if model == "free":
		out = open("{0}/codeml.ctl".format(opath),"w")
		for line in open(ctl,"r"):
			if line.strip().startswith("seqfile"):
				seqfile = "seqfile = {0}".format(nuc)
				out.write("{0}\n".format(seqfile))
			elif line.strip().startswith("treefile"):
				treefile = "treefile = {0}".format(tre)
				out.write("{0}\n".format(treefile))
			elif line.strip().startswith("seqtype"):
				out.write("seqtype = 1\n")
			elif line.strip().startswith("model"):
				out.write("model = 1\n")
			else:
				out.write(line.strip()+"\n")
	elif model == "site":
		out = open("{0}/codeml.ctl".format(opath),"w")
		for line in open(ctl,"r"):
			if line.strip().startswith("seqfile"):
				seqfile = "seqfile = {0}".format(nuc)
				out.write("{0}\n".format(seqfile))
			elif line.strip().startswith("treefile"):
				treefile = "treefile = {0}".format(tre)
				out.write("{0}\n".format(treefile))
			elif line.strip().startswith("model"):
				out.write("model = 0\n")
			elif line.strip().startswith("NSsites"):
				out.write("NSsites = 0 1 2 3 7 8\n")
			else:
				out.write("{0}\n".format(line.strip()))
	elif model == "bs":
		try:
			os.path("{0}/modela".format(opath))
		except IndexError:
			os.mkdir("{0}/modela".format(opath))
		try:
			os.path("{0}/modelanull".format(opath))
		except IndexError:
			os.mkdir("{0}/modelanull".format(opath))
		out = open("{0}/modela/codeml.ctl".format(opath),"w")
		out1 = open("{0}/modelanull/codeml.ctl".format(opath,"w"))
		for line in open(ctl,"r"):
			if line.strip().startswith("seqfile"):
				out.write("seqfile = {0}\n".format(nuc))
				out1.write("seqfile = {0}\n".format(nuc))
			elif line.strip().startswith("treefile"):
				out.write("treefile = {0}\n".format(tre))
				out1.write("treefile = {0}\n".format(tre))
			elif line.strip().startswith("model"):
				out.write("model = 2\n")
				out1.write("model = 2\n")
			elif line.strip().startswith("NSsites"):
				out.write("NSsites = 2\n")
				out1.write("NSsites = 2\n")
			elif line.strip().startswith("fix_omega"):
				out.write("fix_omega = 0\n")
				out1.write("fix_omega = 1\n")
			elif line.strip().startswith("omega"):
				out1.write("omega = 1\n")
				out.write("{0}\n".format(line.strip()))
			else:
				out.write("{0}\n".format(line.strip()))
				out1.write("{0}\n".format(line.strip()))
	else:
		exit("model option should be free, site or bs")

def main():
	args = opt()
	if args.nuc == None or args.tre == None or args.ctl == None or args.model == None or args.ous == None:
		os.system("python {0} -h".format(sys.argv[0]))
		exit("Error: Incomplete Options")
	
	nuc = args.nuc
	tre = args.tre
	ctl = args.ctl
	model = args.model
	ous = args.ous

	out = open(ous,"w")
	
	try:
		os.stat("{0}/paml".format(os.getcwd()))
	except:
		os.mkdir("{0}/paml".format(os.getcwd()))

	for p,ds,fs in os.walk(nuc):
		for f in fs:
			if f.endswith("nuc"):
				opath = "{0}/paml/{1}".format(os.getcwd(),os.path.splitext(f)[0])
				try:
					os.path(opath)
				except:
					os.mkdir(opath)
				change_ctl(ctl,model,opath,"{0}/{1}".format(p,f),tre)
				if model in ["free","site"]:
					out.write("cd {0} && codeml\n".format(opath))
				else:
					out.write("cd {0}/modela && codeml && cd {0}/modelanull && codeml\n")

if __name__ == "__main__":
	main()