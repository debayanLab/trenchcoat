#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 17:14:28 2020

@author: alicia
"""

#key = 'WhiteBirds', answer = 'e3cfgya1w3'


import string
import random

commonwords = [line.rstrip('\n') for line in open("The_Oxford_3000.txt")]
commonwords[0] = 'a'


def memorypalace(key):
#    print(key)        
    if len(key)%2 != 0:
        # changes for every person
        key+= 'r'
     
    letter_groups = []
    for i in range(0,len(key),2):
        letter_groups.append(key[i:i+2])
    
    alphabets = {}
    for i in range(len(string.ascii_lowercase)):
        alphabets[string.ascii_lowercase[i]] = i+1
        alphabets[string.ascii_uppercase[i]] = i+1
    
    letterstoalphabets = {}
    for i in range(len(string.ascii_lowercase)):
        letterstoalphabets[i+1] = string.ascii_lowercase[i]
        
    concatenated = []
    for group in letter_groups:
        concatenate = alphabets[group[0]]+alphabets[group[1]]
        if concatenate > 26:
            concatenate = concatenate - 26
        concatenated.append(letterstoalphabets[concatenate])
    
    # whether they choose number or symbol changes with every person
    symbol_to_right = {'q':'2',
    'w':'3',
    'r':'5',
    't':'6',
    'y':'7',
    'p':'-',
    's':'e',
    'd':'r',
    'f':'t',
    'g':'y',
    'h':'u',
    'j':'i',
    'k':'o',
    'l':'p',
    'z':'s',
    'x':'d',
    'c':'f',
    'v':'g',
    'b':'h',
    'n':'j',
    'm':'k'}
    
    
    vowel_to_left = {'a':'1',
    'e':'3',
    'u':'7',
    'i':'8',
    'o':'9'}
    
    password = []
    for letter in concatenated:
        if letter in ['a', 'e', 'i', 'o', 'u']:
            encode = vowel_to_left[letter]
            password.append(letter+encode)
        else:
            encode = symbol_to_right[letter]
            password.append(letter+encode)
        
    return ''.join(password)

def single_key(number1, number2):
    key = commonwords[number1] + commonwords[number2]
    for letter in key:
        if letter not in string.ascii_letters:
            key = key.replace(letter, '')
    return key, memorypalace(key)

def collision_test(number):
    keyandpass = []
    allpasses = []
    keys = []
    i = 0
    while i < number:
        number1 = random.randrange(len(commonwords))
        number2 = random.randrange(len(commonwords))
        key, password = single_key(number1, number2)
        allpasses.append(password)
        keys.append(key)
        keyandpass.append((key, password))
        i+=1
    return keys, allpasses, keyandpass

allkeys,allpasswords,keysandpasses = collision_test(50000)

import numpy
# create an array of all passwords
x=numpy.array(allpasswords)
uniquepasswords = numpy.unique(x)

# check if all keys are unique
len(allkeys) == len(numpy.unique(allkeys))
# check if all passwords are unique
# True if they are, false if not
len(x) == len(uniquepasswords)


import hashlib
def sha_hash(number1, number2):
    key = commonwords[number1] + commonwords[number2]
    return key, shasymbolfreq(key)

def shasymbolfreq(key):
#    print(key)        
    h = hashlib.sha3_256()
    # update hash with key, which is converted to bytes from ascii encoding 
    h.update(bytes(key, 'ascii'))
    secret = h.digest().decode('latin-1')
    return secret



def makepasswords(numberofpasswords):
    keyandpass = []
    allpasses = []
    i = 0
    while i < numberofpasswords:
        number1 = random.randrange(len(commonwords))
        number2 = random.randrange(len(commonwords))
        key, password = sha_hash(number1, number2)
        allpasses.append(password)
        keyandpass.append((key, password))
        i+=1
    return keyandpass, allpasses
 
def getcharfrequencies(allpasses):
    concatenatedpasswords = ''.join(allpasses)
    totalnumberofcharacters = len(concatenatedpasswords)
    
    # publicly available string of symbols extracted
    printable = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~£’”€₹'
#    singleapostrophechar = '\''
    # find any characters entered that aren't in printable
    # double check that we have all characters
    notprintable = []
    for symbol in concatenatedpasswords:
        if (symbol not in printable) and (symbol not in notprintable):
            notprintable.append(symbol)
    
    # calculate frequency of each symbol in printable
    frequencies = []
    for character in printable:
        freq_character = concatenatedpasswords.count(character)
        frequencies.append(freq_character)
    
#    frequencies.append(concatenatedpasswords.count(singleapostrophechar))
    
    freq_out_of_range_characters = 0
    # error handling in case a character can be printed
    for character in notprintable:
        # find the frequency of the character not in printable
        freq_character = concatenatedpasswords.count(character)
        freq_out_of_range_characters += freq_character
    
    frequencies.append(freq_out_of_range_characters)
    
    allsymbols = printable+ ' out of range character '
    # the below line is used because it rescales frequencies, since some methods have more passwords than others
    # numpy.array(frequencies)/totalnumberofcharacters * 10000
    # * 10000 is used since * 100 produces very long decimals 
    return allsymbols, numpy.array(frequencies)/totalnumberofcharacters * 10000

# extract SHA256 hashes and treat them as passwords   
keyandpass, allpasses = makepasswords(50)
allchars, frequencies = getcharfrequencies(allpasses)