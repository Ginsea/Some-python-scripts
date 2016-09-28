#!/usr/bin/env python
#coding=UTF-8
'''
========================Usage=========================
将多个fasta文件合并为一个nexus文件，用于beast和mrbayes分析
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
import random
from Bio import SeqIO
global rd
rd = os.getcwd()

def get_time():
	return time.strftime('%H:%M:%S',time.localtime(time.time()))

def recordcmd():
	out = open("{0}/cmd.sh".format(rd),"w")
	out.write("python {0}".format(" ".join(sys.argv[:])))

def arg_parse():
    parse = argparse.ArgumentParser(usage="%(prog)s[options]")
    parse.add_argument("--path1",help="ids information folder")
    parse.add_argument("--path2",help="fasta format folder")
    return parse.parse_args()

def loadids(path1):
	#导入序列ID信息
	#创建一个空字典
	tmpdir = {}
	#遍历path1中的所有元素
	for ps,ds,fs in os.walk(path1):
		#对path1中的文件进行遍历
		for f in fs:
			#打印信息至标准输出
			sys.stdout.write("[{0}] Load file {1}\n".format(get_time(),f))
			#创建二级字典，键是f文件的前缀
			tmpdir[f.split(".")[0]] = {}
			#for循环分别读取每个f文件
			for line in open("{0}/{1}".format(ps,f),"r"):
				#对读入的行进行tab键分割
				ele = line.strip().split("\t")
				#以第一列为键，第二列为值，存入二级字典
				tmpdir[f.split(".")[0]][ele[0]] = ele[1]
		#本部分分析完成，输出结果至屏幕
		sys.stdout.write("[{0}] Done!\n".format(get_time()))
	return tmpdir

def chandir(strs):
	#对一个字符串进行换行符分割
	#创建一个列表，用于存储本函数的信息
	tmplist = []
	#将字符串的长度赋值给num变量
	num = len(strs)
	#每行60个字符，总共分割成的片段数目，比如 63//60 + 1 = 2
	i = (num//60) + 1
	#给x赋予初始值0
	x = 0
	#当x<i的时候，对应片段长度均为60,；当x=1的时候，对应片段长度为len(strs)%60
	while x <= i:
		if x < i:
			tmplist.append("{0}\n\t\t".format(strs[x*60:(x+1)*60]))
		elif x == i:
			tmplist.append("{0}".format(strs[x*60:]))
		x += 1
	return "".join(tmplist)

def loadfasta(path2):
	#导入fasta文件
	#创建一个新的字典
	tmpdir = {}
	#对path2文件夹中的元素进行遍历
	for ps,ds,fs in os.walk(path2):
		#对path2文件夹中的文件进行遍历
		for f in fs:
			key = f.split(".")[0]
			#创建一个二级字典，键值为所遍历文件的前缀
			tmpdir[key] = {}
			#导出软件运行信息至标准输出
			sys.stdout.write("[{0}] Load file {1}\n".format(get_time(),f))
			#读取文件中的每个fasta文件，若电脑中没有安装Biopython，则这部分需要重写
			for seqs in SeqIO.parse("{0}/{1}".format(ps,f),"fasta"):
				#写入内容至二级字典，键为序列名，值为序列内容
				tmpdir[key][str(seqs.id)] = str(seqs.seq)
		#本函数运行完成
		sys.stdout.write("[{0}] Done!\n".format(get_time()))
	return tmpdir

def getnex(path1,path2):
	#将IDS和OG ID的对应关系字典赋值于idsdir,一级字典的键是OG ID，二级字典的键是序列名称，值是物种名称，每个物种对应多条序列
	idsdir = loadids(path1)
	#将序列信息与OG ID的对应关系字典赋值于fastadir，一级字典的键是OG ID，二级字典的键是序列名称，值是序列信息，每个物种对应多条序列
	fastadir = loadfasta(path2)
	#创建一个临时字典 旨在对上述两个字典进行汇总，生成便于写入文件的信息
	#这也是一个列表嵌套字典的模式，键是物种名称，值是一个有序的列表（按照物种名称排序）
	tmpdir = {}
	for k0 in idsdir.keys():
		# lambda x:x[1] 1表示按照值排序
		for k1 in sorted(idsdir[k0].items(),key=lambda x:x[1]):
			try:
				tmpdir[k1[1]].append(fastadir[k0][k1[0]])
			except:
				tmpdir[k1[1]] = [fastadir[k0][k1[0]]]
	#ntax表示序列的数目
	ntax = len([x for x in fastadir[fastadir.keys()[0]].keys()])
	#ntchar表示每个序列中核苷酸的数目
	nchar = sum(len(x) for x in tmpdir[tmpdir.keys()[random.randint(1,ntax-1)]])
	sys.stdout.write("[{0}] Write Information to Nexus File\n".format(get_time()))
	out = open("{0}/connect.nexus".format(rd),"w")
	out.write("#NEXUS\nBEGIN DATA;\n")
	out.write("\tDIMENSIONS NTAX={0} NCHAR={1};\n".format(ntax,nchar))
	out.write("\tFORMAT DATATYPE = DNA GAP = - MISSING = ?;\n\tMATRIX\n")
	for keys in tmpdir.keys():
		out.write("\t{0}\t{1}\n".format(keys,chandir("".join(tmpdir[keys]))))
	out.write(";\nend;\n")
	out.write("begin assumptions;\n")
	i = 1
	samp = tmpdir[tmpdir.keys()[1]]
	print(sum([len(x) for x in samp]))
	total = len(samp)
	while i <= total:
		if i == 1:
			out.write("\tcharset gene{0} = 1-{1};\n".format(i,len(samp[i-1])))
			i += 1
		elif i > 1:
			starts = sum([len(x) for x in samp[:i-1]]) + 1
			ends = sum([len(x) for x in samp[:i]])
			out.write("\tcharset gene{0} = {1}-{2};\n".format(i,starts,ends))
			i += 1
	out.write("end;\n")
	sys.stdout.write("[{0}] Nexus file producing successfully!\n".format(get_time()))

def main():
	options = arg_parse()
	if options.path1 == None or options.path2== None:
		os.system("python {0} -h".format(sys.argv[0]))
		exit("[{0}] Error: incomplete options".format(get_time()))
	recordcmd()
	path1 = options.path1
	path2 = options.path2
	getnex(path1,path2)

if __name__ == "__main__":
	main()
