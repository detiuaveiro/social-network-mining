import json
import csv
from calendar import monthrange
import numpy as np
from ast import literal_eval

years=['2018','2017','2016','2015','2014','2013','2012','2011']

months=['01','02','03','04','05','06','07','08','09','10','11','12']

clean_data = []

# *************************************
# Get a valid array of text that we can train our model with
# *************************************
def pruneLine(line):
    strippedLine = []
    if(len(line) > 0):
        # Ignore any tweets of Donald Trump quoting other people, we only want to train our model based on things that have actually
        # come out of his mouth.
        if(line[0][0] != '"'):
            txt = line[0].split()
            for word in txt:
                cleanWord = getValidWord(word)
                if(cleanWord != False):
                    if(type(cleanWord) is list):
                        for item in cleanWord:
                            strippedLine.append(item)
                    else:
                        strippedLine.append(cleanWord)
        return strippedLine
    else:
        return False # Love that I can hvae two different return types for this function. Fuck. Yes. Python.

# *************************************
# Blacklist for words that we don't want - links, mentions, ect. As well as lowercase words and separate from punctuation marks.
# *************************************
def getValidWord(word):
    if(word[0] == '@'): # ignore mentions
        return False
    elif(word[:4] == "http"): # ingnore links
        return False
    elif(word == "[removed]" or word == "[deleted]"): # we don't need to include his twitter signature in our model
        return False
    elif(word[len(word) - 1] == "." or word[len(word) - 1] == "!" or word[len(word) - 1] == "?"):
        # separating end of sentence words from their punctuation because we actually want to treat punctuation as it's own word
        # The reason for this is because when we are generating sentences, we will want to terminate the generation when we encounter a puctuation mark.
        punctuation = word[len(word) - 1]
        word = word[:(len(word) - 1)].lower() # <-- don't forget to lowercase
        return [word, punctuation]
    else:
        word = word.strip('"')
        word = word.strip("'")
        word = word.strip(":")
        return word.lower() #lowercase that shit

# *************************************
# Train the first order markov model.
# *************************************
def generateFirstOrderMarkov(cleanData):
    markov_model = {} # <-- this will be a nested dicitonary

    ### first pass - populate markov_model with all words
    for line in cleanData:
        for i in range(0, len(line)):
            markov_model[line[i]] = {}

    ### second pass - count up number of times each unique word transitions to another unique word
    for line in cleanData:
        for i in range(0, len(line) - 1):
            if(line[i+1] in markov_model[line[i]]):
                markov_model[line[i]][line[i+1]] += 1
            else:
                markov_model[line[i]][line[i+1]] = 1

    return markov_model

# *************************************
# Train the second order markov model.
# *************************************
def generateSecondOrderMarkov(cleanData):
    markov_model = {} # <-- this will be a doubly nested dictionary

    ### first pass - populate markov_model with all words
    for line in cleanData:
        for i in range(0, len(line)):
            markov_model[line[i]] = {}

    ### second pass - count up number of times each unique word transitions to another unique word
    for line in cleanData:
        for i in range(0, len(line) - 1):
            markov_model[line[i]][line[i+1]] = {}

    ### third pass - now we go a step further and count up the number of times the previous two words transitioned to the current word in the sequence
    for line in cleanData:
        for i in range(0, len(line) - 2):
            if(line[i+2] in markov_model[line[i]][line[i+1]]):
                markov_model[line[i]][line[i+1]][line[i+2]] += 1
            else:
                markov_model[line[i]][line[i+1]][line[i+2]] = 1

    return markov_model

# *************************************
# Create a dictionary that allows us to see how many times a word occured
# *************************************
def generateOccurenceDictionary(cleanData):
    word_occurences = {}
    for line in cleanData:
        for word in line:
            if(word in word_occurences):
                word_occurences[word] += 1
            else:
                word_occurences[word] = 1

    return word_occurences

# *************************************
# Normalize the first order markov model.
# *************************************
def normalizeFirstOrder(markov_model, word_occurences):
    for word in markov_model:
        for transition_word in markov_model[word]:
            markov_model[word][transition_word] = markov_model[word][transition_word]/word_occurences[word]
    return markov_model

# *************************************
# Normalize the second order markov model.
# *** we will use the first order markov model to get the number of occurences for two words occuring next to eachother.
# *************************************
def normalizeSecondOrder(second_order_markov, first_order_markov):
    for first_word in second_order_markov:
        for second_word in second_order_markov[first_word]:
            for num_transitions in second_order_markov[first_word][second_word]:
                second_order_markov[first_word][second_word][num_transitions] = second_order_markov[first_word][second_word][num_transitions] / first_order_markov[first_word][second_word]
    return second_order_markov

def dateformater(years,months):
    for year in years:
        for month in months:
            (first,last) = monthrange(int(year),int(month))
            days = ranges(last,10)
            for day in days:
                (f,l) = literal_eval(day)
                after=year+"-"+month+"-"+"{0:0=2d}".format(f)
                before=year+"-"+month+"-"+"{0:0=2d}".format(l)
                with open('./redditComments.csv', "w") as c:
                    with open('./data/data({}_{}).json'.format(after,before), buffering=1000) as f:
                        t = json.loads(f.read())
                        print(t)
                        for row in t['data']:
                            filewriter = csv.writer(c, delimiter=',')
                            filewriter.writerow([row['body']])

                        
def ranges(N, nb):
    step = N / nb
    return ["({},{})".format(round(step*i)+1, round(step*(i+1))) for i in range(nb)]

dateformater(years,months)

with open('./redditComments.csv', 'w') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for line in spamreader:
        # Lets go ahead and get rid of all the quoted text by donald trump, we really only just want the things that he has said
        if(len(line) > 0):
            if(line[0][0] != '"'):
                pruned_line = pruneLine(line)
                clean_data.append(pruned_line)


