#!/usr/bin/env python

'''
@Author This script was developed by Ginsea Chen (ginseachen@hotmail.com) in CATAS
@Descriptrion You can use this script to predict pfam domains in peptide sequences
@You need to install pfamscan.pl and HMMSCAN software before script using
@pfam.properties file provided some useful information about script using, you can edit it to suit your file location
@Usage python run_pfam.py
'''

import os,os.path

## Run pfam database searching through pfamscan.pl script
def run_pfamscan(DB,script,query):
    os.system("%s -fasta %s -dir %s -cpu 4 -out %s.pfam"%(script,query,DB,query))

## Delete lines contained "#" in pfam file
def adjust_pfam(pfamfile):
    os.system("grep '^[^#]' %s > %sout "%(pfamfile,pfamfile))

## read some information from pfam out file
def get_seqsnum(pfamfile):
    ids = []
    for line in open(pfamfile,"r"):
        if line.strip().split()[0] not in ids:
            ids.append(line.strip().split()[0])
    return len(ids)

def get_domainnum(pfamfile):
    domain = []
    for line in open(pfamfile,"r"):
        if line.strip().split()[5] not in domain:
            domain.append(line.strip().split()[5])
    return len(domain)

for line in open("pfam.properties","r"):
    if "DB" in line:
        DB = line.strip().split("=")[1]
    elif "SCRIPT" in line:
        script = line.strip().split("=")[1]
    elif "QUERY" in line:
        query = line.strip().split("=")[1]

out = open("%s.pfam.count"%query,"w")

run_pfamscan(DB,script,query)
adjust_pfam("%s.pfam"%query)
out.write("There were %d domains were identified in %d sequences\n%s\n"%(get_domainnum("%s.pfamout"%query),get_seqsnum("%s.pfamout"%query),"="*100))

pfam = dict()
for line in open("%s.pfamout"%query,"r"):
    try:
        pfam[line.strip().split()[5]].append(line.strip().split()[0])
    except KeyError:
        pfam[line.strip().split()[5]] = [line.strip().split()[0]]

for query in pfam:
    out.write("%s\t%d\n"%(query,len(pfam[query])))

out.close()
