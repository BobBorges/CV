#!/usr/bin/env python3
"""
Concatinates reads and views from academia/researchgate type social media.
"""
from glob import glob
import os, re, time, sys
import pandas as pd


here = os.path.dirname(__file__)




def clean_up():
    files = glob(f"{here}/tmp-reads/*.tsv")
    for f in files:
        os.remove(f)


def merge():
    with open(f"{here}/tmp-reads/merge-called.txt", "r") as M:
        m = M.read()
        if m.startswith("False"):
            with open(f"{here}/tmp-reads/merge-called.txt", "w+") as MM:
                MM.write("True")

            time.sleep(10)
            dfs = []
            files = glob(f"{here}/tmp-reads/*.tsv")
            print(files)
            for f in files:
                dfs.append(pd.read_csv(f, sep='\t'))
            dfs.append(pd.read_csv(f"{here}/reads.tsv", sep='\t'))
            reads = pd.concat(dfs, ignore_index=True)
            reads.drop_duplicates(
                subset=["message_id", "source", "paper", "reader"],
                inplace=True,
                ignore_index=True)
            reads.to_csv(f"{here}/reads.tsv", sep='\t', index=False)
            with open(f"{here}/tmp-reads/merge-called.txt", "w+") as MMM:
                MMM.write("False")
            clean_up()


def mk_df(row):
    print(row)
    df = pd.DataFrame(row, columns=[
                                "message_id",   # message ID
                                "date",         # date: message arrival
                                "source",       # source: academia, research gate, etc..
                                "paper",        # paper: where was the mention
                                "reader"        # mentioner: who is the mentioner
                            ])
    return df


def write_reads(df, message_id):
    df.to_csv(f"{here}/tmp-reads/{message_id}.tsv", sep='\t', index=False)




def main():
    message_id = sys.argv[1]
    subject = sys.argv[2]
    date = sys.argv[3]
    sender = sys.argv[4]
    #message_id = "abc-123"
    #subject = "Joanna Maryniak read your paper, \"a paper\""
    #date = "today"
    #sender = "test.sender@sender.com"
    if subject is not None and len(subject) > 0:
        print(subject)
        pattern = re.compile(r"(.*)\sread your paper, \"(.*)\"")
        m = pattern.search(subject)
        if m is not None:
            print(m)
            write_reads(mk_df([[message_id,
                                date,
                                sender.split("@")[1][:-1],
                                m[2],
                                m[1]]]), message_id)
    merge()



if __name__ == '__main__':
    main()
