#!/usr/bin/python
# -*- coding: utf-8 -*-

owner = "ojahnn"        # Name des Accounts, an den Fehlermeldungen gesendet werden
import HP_config
import tweepy
import sqlite3

def login():
    # for info on the tweepy module, see http://tweepy.readthedocs.org/en/

    # Authentication is taken from F3_config.py
    consumer_key = HP_config.consumer_key
    consumer_secret = HP_config.consumer_secret
    access_token = HP_config.access_token
    access_token_secret = HP_config.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api

def stick_together_output():
    folge = ""
    connection = sqlite3.connect("daten.sqlite")
    c = connection.cursor()
    firstNounQuery = 'select Features, Wort from Morph natural join Wort where Features like "Masc_Nom_%" or Features like "Fem_Nom_%" or Features like "Neut_Nom_%" order by random() limit 1'
    firstNounFeats, firstNoun = c.execute(firstNounQuery).fetchone()
    secondNounQuery = 'select Features, Wort from Morph natural join Wort where Features like "Masc_Gen_%" or Features like "Fem_Gen_%" or Features like "Neut_Gen_%" order by random() limit 1'
    secondNounFeats, secondNoun = c.execute(secondNounQuery).fetchone()
    if firstNounFeats.endswith("Pl") or firstNounFeats.startswith("Fem"):
        folge += "die "
    elif firstNounFeats.startswith("Neut"):
        folge += "das "
    else:
        folge += "der "

    folge += firstNoun

    if secondNounFeats == "Neut_Gen_Sg" or secondNounFeats == "Masc_Gen_Sg":
        folge += " des "
        cont = True
    elif secondNounFeats.endswith("Pl") or secondNounFeats.startswith("Fem"):
        folge += " der "
        cont = True

    if cont:
        folge += secondNoun
        output = "Harry Potter und "+folge
        return output

def tweet_something(debug):
    api = login()
    output = stick_together_output()
    if debug:
        print(output)
    else:
        api.update_status(status=output)
        print(output)

tweeted = False
while not tweeted:
    try:
        tweet_something(False)
        tweeted = True
    except:
        pass
