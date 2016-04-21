#!/usr/bin/env python

'''
@Description You can used this script to download sra file from NCBI
@You need install Aspera plugins in you PC
@Author This script was developed by Ginsea Chen in CATAS
'''

import os
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--sra",help="A txt file which contained sra ids such as SRR**")
    parser.add_argument("--out",help="The storage folder of sra file")
    parser.add_argument("--aspera",help="The dir of aspera software")
    parser.add_argument("--addr",help="You can input the ncbi ftp address of you target file, just like 'ftp://ftp.ncbi.nlm.nih.gov/**'")
    return parser.parse_args()

def test_aspera(aspera):
    if not os.stat(aspera):
        print "You need install aspera!"
        exit(1)

def clean_aspera_path(aspera):
    aspera_path = ""
    if aspera[-1] == "/":
        aspera_path += aspera[0:-1]
    else:
        aspera_path += aspera
    return aspera_path


def down_sra_file(sra,out,aspera):
    for line in open(sra,"r"):
        folder1 = line[0:3]
        folder2 = line[0:6]
        aspera_path = clean_aspera_path(aspera)
        if os.stat(out):
            if out[-1] == "/":
                os.system("%s/connect/bin/ascp -i %s/connect/etc/asperaweb_id_dsa.openssh -k 1 -QT -l 200m anonftp@ftp-trace.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/%s/%s/%s/%s.sra %s"%(aspera_path,aspera_path,folder1,folder2,line.strip(),line.strip(),out))
            elif out[-1] != "/":
                os.system("%s/connect/bin/ascp -i %s/connect/etc/asperaweb_id_dsa.openssh -k 1 -QT -l 200m anonftp@ftp-trace.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/%s/%s/%s/%s.sra %s/"%(aspera_path,aspera_path,folder1,folder2,line.strip(),line.strip(),out))
        else:
            print "There were no folder which located on %s"%out
            exit(1)

def down_sra_screen(out,aspera):
    ids = raw_input("Enter a sra ids such as SRR**:\n")
    folder1 = ids.strip()[0:3]
    folder2 = ids.strip()[0:6]
    aspera_path = clean_aspera_path(aspera)
    if os.stat(out):
        if out[-1] == "/":
            os.system("%s/connect/bin/ascp -i %s/connect/etc/asperaweb_id_dsa.openssh -k 1 -QT -l 200m anonftp@ftp-trace.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/%s/%s/%s/%s.sra %s"%(aspera_path,aspera_path,folder1,folder2,ids.strip(),ids.strip(),out))
        elif out[-1] != "/":
            os.system("%s/connect/bin/ascp -i %s/connect/etc/asperaweb_id_dsa.openssh -k 1 -QT -l 200m anonftp@ftp-trace.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/%s/%s/%s/%s.sra %s/"%(aspera_path,aspera_path,folder1,folder2,ids.strip(),ids.strip(),out))
    else:
        print "There were no folder which located on %s"%out
        exit(1)

def down_file_addre(addre,out,aspera):
    point = addre.find(".gov")
    sub_addre = addre[point+4:]
    aspera_path = clean_aspera_path(aspera)
    if os.stat(out):
        if out[-1] == "/":
            os.system("%s/connect/bin/ascp -i %s/connect/etc/asperaweb_id_dsa.openssh -k 1 -QT -l 200m anonftp@ftp-trace.ncbi.nlm.nih.gov:%s %s"%(aspera_path,aspera_path,sub_addre,out))
        elif out[-1] != "/":
            os.system("%s/connect/bin/ascp -i %s/connect/etc/asperaweb_id_dsa.openssh -k 1 -QT -l 200m anonftp@ftp-trace.ncbi.nlm.nih.gov:%s %s/"%(aspera_path,aspera_path,sub_addre,out))
    else:
        print "There were no folder which located on %s"%out
        exit(1)


def main():
    argser = parse_args()

    if argser.out == None or argser.aspera == None:
        os.system("python %s -h"%sys.argv[0])
        exit(1)

    if argser.sra != None and argser.addr != None:
        print "You can't use sra and addre options one time!"
        exit(1)

    test_aspera(argser.aspera)

    if argser.sra == None:
        if argser.addr == None:
            down_sra_screen(argser.out,argser.aspera)
        else:
            down_file_addre(argser.addr,argser.out,argser.aspera)
    else:
        down_sra_file(argser.sra,argser.out,argser.aspera)

if __name__ == "__main__":
    main()
