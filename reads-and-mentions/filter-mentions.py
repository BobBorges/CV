#!/usr/bin/env python3
"""
Concatinates 'mentions / citations' from academia/researchgate type social media
"""
import sys
import os
import pandas as pd
import re

here = os.path.dirname(__file__)

def read_in_mentions():
    try:
        df = pd.read_csv(f"{here}/mentions.csv")
    except:
        df = pd.DataFrame(columns=[
            "message_id",           # message ID
            "date",                 # date: message arrival
            "source",               # source: academia, research gate, etc..
            "paper",                # paper: where was the mention
            "mentioner"             # mentioner: who is the mentioner
            ])
    return df

def write_mentions(mentions):
    mentions.to_csv(f"{here}/mentions.csv", index=False)



def main():

    #message_id = sys.argv[1]
    #subject = sys.argv[2]
    #date = sys.argv[3]
    #sender = sys.argv[4]
    message_id = "01000186fc8e7d56-f8d7ee35-af8f-454c-b4b6-409e737907aa-000000@email.amazonses.com"
    subject = 'Richard Parkinson read your paper, "The Life of Language: dynamics of language contact in Suriname"'
    date = "Fri Mar 08 2024 23:08:43 GMT+0100 (centraleuropeisk normaltid)"
    sender = '"Read by Parkinson, Richard" <updates@academia-mail.com>'


    if subject is not None and len(subject) > 0:
        mentions = read_in_mentions()
        if message_id not in mentions['message_id'].unique():
            print(subject)
            pattern = re.compile(r"(.*)\sread your paper, \"(.*)\"")
            m = pattern.search(subject)
            if m is not None:
                mentions.loc[len(mentions)] = [message_id, date, sender.split("@")[1][:-1], m[1], m[1]]
            print(m[1], '--', m[2])
            #print(date)
            #print(sender)
        print(mentions)



        #write_mentions(mentionns)




if __name__ == '__main__':
    main()
