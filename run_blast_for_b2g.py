#!/usr/bin/env python
'''
@Description This script can be used to run blast against nr database for GO annotation analysis
@The corresponding parameters of blast were obtained from web of blast2go
@Author This script was developed by Ginsea Chen (ginseachen@hotmail.com) in CATAS
@Usage python run_blast_for_b2g.py --query query.fa --db path to nr --num_threads [NUM] --out query.xml --dbtype prot
'''
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--query",default="query.fa",help = "query file")
    parser.add_argument("--db", help="path to nr database in your server")
    parser.add_argument("--num_threads",default=10,type=int,help="Number of threads you want to process")
    parser.add_argument("--out",default="query.xml",help="The outfile of blast with xml format")
    parser.add_argument("--dbtype",default="prot",help="The type of your query file, prot means protein, nucl means transcripts")
    return parser.parse_args()

def run_blast(query,db,num,out,dbtype):
    if dbtype == "prot":
        os.system("blastp -query %s -db %s -outfmt 5 -evalue 1e-5 -word_size 3 -show_gis -num_alignments 20 -max_hsps 20 -num_threads %d -out %s"%(query,db,num,out))
    elif dbtype == "nucl":
        os.system("blastx -query %s -db %s -outfmt 5 -evalue 1e-5 -word_size 3 -show_gis -num_alignments 20 -max_hsps 20 -num_threads %d -out %s"%(query,db,num,out))

def main():
    argser = parse_args()

    if argser.dbtype not in ["prot","nucl"]:
        print "Please type available type: prot or nucl"
        exit(1)

    run_blast(argser.query,argser.db,int(argser.num_threads),argser.out,argser.dbtype)

if __name__ == "__main__":
    main()
