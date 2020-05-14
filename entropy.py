#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2020 hulikalruthu
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Created on Fri Apr 10 21:05:46 2020

@author: Ruthu Hulikal
"""
import string, math

def determine_charpool(password):
    charpool = []
    for char in password:
        if (char in string.ascii_lowercase):
            if ("ascii_lowercase" not in charpool):
                charpool.append("ascii_lowercase")
        elif (char in string.ascii_uppercase):
            if ("ascii_uppercase" not in charpool):
                charpool.append("ascii_uppercase")
        elif (char in string.digits):
            if ("numeric" not in charpool):
                charpool.append("numeric")
        elif (char in string.printable):
            if ("asciiprintable" not in charpool):
                charpool.append("asciiprintable")
        else:
            print("this character is not in any charpool",char, charpool)
    return charpool

def determine_entropy(charpool, password):
    passlen = len(password)
    symbolcount = 0
    if "numeric" in charpool:
        symbolcount += 10
    if "ascii_lowercase" in charpool:
        symbolcount += 26
    if "ascii_uppercase" in charpool:
        symbolcount += 26
    if "asciiprintable" in charpool:
        symbolcount = 95
    entropy = passlen*math.log2(symbolcount)
    return entropy

def get_length(passwords):
    """
    returns list of mappings: length of password in passwords to password
    """
    lengths = []
    for password in passwords:
        lengths.append(len(password))
    return lengths

import numpy
import matplotlib.pyplot as plt 


def get_length_frequencies(lengths,x):
    frequencies = []
    for l in x:
        freq_l= lengths.count(l)
        frequencies.append(freq_l)
    return frequencies

def get_clean_passwords(filename):
    file = open(filename, 'r') 
    passwords = file.readlines() 
    file.close()
    passwords.pop(0)

    for i in range(len( passwords)):
        passwords[i] = passwords[i][1:-2]
    return passwords

def plot_the_graph(filename,methodname):
    passwords = get_clean_passwords(filename)
    lengths = get_length(passwords)
    # remove repeated length values
    x = list(numpy.unique(lengths))
    y = get_length_frequencies(lengths,x)
    plt.plot(x, y) 
    plt.xlabel('Length') 
    # naming the y axis 
    plt.ylabel('frequency of length') 
    plt.title('length vs freq: '+methodname)
    plt.show()
    
def getxy(filename):
    passwords = get_clean_passwords(filename)
    lengths = get_length(passwords)
    # remove repeated length values
    x = list(numpy.unique(lengths))
    y = get_length_frequencies(lengths,x)
    return x,y

def getcharfrequencies(filename):
    passwords = get_clean_passwords(filename)
    concatenatedpasswords = ''.join(passwords)
    
    printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[\]^_`{|}~ '
    singleapostrophechar = '\''
    # find any characters entered that aren't in string.printable
    notinprintable = []
    for symbol in concatenatedpasswords:
        if (symbol not in string.printable) and (symbol not in notinprintable):
            notinprintable.append(symbol)
    
    # calculate frequency of each symbol in string.printable
    frequencies = []
    for character in printable:
        freq_character = concatenatedpasswords.count(character)
        
        frequencies.append(freq_character)
    
    frequencies.append(concatenatedpasswords.count(singleapostrophechar))
    
    for character in notinprintable:
        freq_character = concatenatedpasswords.count(character)
        frequencies.append(freq_character)
    
    allsymbols = printable+singleapostrophechar+''.join(notinprintable)
    return allsymbols, frequencies


def plotbargraph(symbols,frequencies):
    symbols = list(symbols)
    # Make fake dataset
    height = frequencies
    bars = symbols
    y_pos = numpy.arange(len(bars))
     
    f, ax = plt.subplots(figsize=(18,5)) # set the size that you'd like (width, height)
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    ax.legend(fontsize = 14)


#plot_the_graph('memorypalacem1passwords.csv','memory palace method 1')
#plot_the_graph('memorypalacem2passwords.csv','memory palace method 2')
#plot_the_graph('internalmethodpasswords.csv','internal method')
#plot_the_graph('songmethodpasswords.csv','song method')
#plot_the_graph('scrambledstoryboxmethodpasswords.csv','scrambled storybox method')
#
#
#x,y = getxy('memorypalacem1passwords.csv')
#plt.plot(x, y, label = 'memory palace method 1')
#x,y = getxy('memorypalacem2passwords.csv')
#plt.plot(x, y, label = 'memory palace method 2')
#x,y = getxy('internalmethodpasswords.csv')
#plt.plot(x, y, label = 'internal method')
#x,y = getxy('songmethodpasswords.csv')
#plt.plot(x, y, label = 'song method')
#x,y = getxy('scrambledstoryboxmethodpasswords.csv')
#plt.plot(x, y, label = 'scrambled storybox method')
#plt.xlabel('Length') 
## naming the y axis 
#plt.ylabel('frequency of length') 
#plt.title('length vs freq')
#plt.legend()
#plt.show()



def haspasswords(passwords, prime):
    intpasswords = []
    for password in passwords:
        convertoint = 0
        for char in password:
            convertoint+=ord(char)
        intpasswords.append(convertoint)
    intpasswords = numpy.array(intpasswords)
    return (intpasswords%prime)
    
def plotpasswordhashfrequencies(filename,prime):
    passwords = get_clean_passwords(filename)
    hashes = haspasswords(passwords, prime)
    x,y = numpy.unique(hashes, return_counts=True)
    
    plt.plot(x, y, label = 'mod'+str(prime))
    plt.xlabel('hash value') 
    # naming the y axis 
    plt.ylabel('frequency of hash value') 
    plt.title('frequency of password hashes for ' + filename)
    plt.legend()
    plt.figure(figsize=(20,10))

def frequenciespersymbol(filename):
    passwords = get_clean_passwords(filename)
    concatenatedpasswords = ''.join(passwords)
    allprintable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[]^_`{|}~ €£’\\₹”'
    # find any characters entered that aren't in string.printable    
    # calculate frequency of each symbol in string.printable
    frequencies = []
    for character in allprintable:
        freq_character = concatenatedpasswords.count(character)
        frequencies.append(freq_character)
        
    return frequencies


#### Find out if password characters are evenly distributed
#prime = 73
#plotpasswordhashfrequencies('memorypalacem1passwords.csv',prime)
#plotpasswordhashfrequencies('memorypalacem2passwords.csv',prime)
#plotpasswordhashfrequencies('internalmethodpasswords.csv',prime)
#plotpasswordhashfrequencies('songmethodpasswords.csv',prime)
#plotpasswordhashfrequencies('scrambledstoryboxmethodpasswords.csv',prime)


#height = y
#bars = x
#y_pos = numpy.arange(len(bars))
#f, ax = plt.subplots(figsize=(18,5)) # set the size that you'd like (width, height)
#plt.bar(y_pos, height)
#plt.xticks(y_pos, bars)
#ax.legend(fontsize = 14)



### plot bar graph of symbols vs their frequencies
#allsymbols, frequencies = getcharfrequencies('memorypalacem1passwords.csv')
#plotbargraph(allsymbols,frequencies)
#allsymbols, frequencies = getcharfrequencies('memorypalacem2passwords.csv')
#plotbargraph(allsymbols,frequencies)
#allsymbols, frequencies = getcharfrequencies('internalmethodpasswords.csv')
#plotbargraph(allsymbols,frequencies)
#allsymbols, frequencies = getcharfrequencies('songmethodpasswords.csv')
#plotbargraph(allsymbols,frequencies)
#allsymbols, frequencies = getcharfrequencies('scrambledstoryboxmethodpasswords.csv')
#plotbargraph(allsymbols,frequencies)

## this package has heatmap generation abolity, incase we need it
#import seaborn as sns
## getting frequenices for a common symbol set
#allprintable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[]^_`{|}~ €£’\\₹”'
#mempalace1frequencies = frequenciespersymbol('memorypalacem1passwords.csv')
#mempalace2frequencies = frequenciespersymbol('memorypalacem2passwords.csv')
#internalfrequencies = frequenciespersymbol('internalmethodpasswords.csv')
#songfrequencies = frequenciespersymbol('songmethodpasswords.csv')
#scrambledfrequencies = frequenciespersymbol('scrambledstoryboxmethodpasswords.csv')



def create_entropylist(filename):
    passwords = get_clean_passwords(filename)
    passwordentropys = []
    for password in passwords:
        charpool = determine_charpool(password)
        entropy = determine_entropy(charpool, password)
        passwordentropys.append((password,entropy))
    return passwordentropys
    

def writeentropystofile(inputname, outputname):
    passwordentropys = create_entropylist(inputname)
    file = open(outputname, "w") 
    for entry in passwordentropys:
        password = entry[0]
        entropy = entry[1]
        file.write(password + "\t" + str(entropy))
        file.write("\n")
    file.close()
    
##### heatmap of password length, entropy, method
def lengthsentropys(filename):
    passwords = get_clean_passwords(filename)
    passwordentropys = []
    passwordlengths = []
    for password in passwords:
        passwordlengths.append(len(password))
        charpool = determine_charpool(password)
        entropy = determine_entropy(charpool, password)
        passwordentropys.append((password,entropy))
    return passwordentropys, passwordlengths

entropys,lengths = lengthsentropys('memorypalacem1passwords.csv')
mempalace2 = lengthsentropys('memorypalacem2passwords.csv')
internal = lengthsentropys('internalmethodpasswords.csv')
song = lengthsentropys('songmethodpasswords.csv')
scrambled = lengthsentropys('scrambledstoryboxmethodpasswords.csv')


#writeentropystofile('memorypalacem1passwords.csv', 'memorypalacem1entropys.tsv')
#writeentropystofile('memorypalacem2passwords.csv', 'memorypalacem2entropys.tsv')
#writeentropystofile('internalmethodpasswords.csv', 'internalmethodentropys.tsv')
#writeentropystofile('songmethodpasswords.csv', 'songmethodentropys.tsv')
#writeentropystofile('scrambledstoryboxmethodpasswords.csv', 'scrambledstoryboxmethodentropys.tsv')
