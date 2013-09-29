#!/usr/bin/env python
import sys, re, os

PATH_OF_SCRIPT=os.path.dirname(os.path.realpath(__file__))

PATH_TO_FREQ=os.path.join(PATH_OF_SCRIPT, 'frequency.tsv')
frequency = [0]*26
ngrams = 0.0

with open(PATH_TO_FREQ) as f:
    for line in f.read().split('\n'):
        letter, freq = line.split('\t')
        frequency[ord(letter.lower()) - ord('a')]=int(freq)
        ngrams+=int(freq)

def shift(plaintext, s):
    """Returns plaintext with all alpha characters shifted to the right by s"""
    return ''.join([chr(((ord(j)&0x9F)+s-1)%26+1+0x40+(0x20 if ord(j)&0x20 else 0)) if j.isalpha() else j for j in plaintext])

def bruteforce(plaintext):
    """Returns an array of plaintext shifted by each possible shift"""
    return [shift(plaintext,i) for i in range(26)]

def analysis(plaintext):
    """Performs frequency analysis on plaintext to determine the best shift"""
    freq = [0]*26
    plaintext = re.sub('\W','',plaintext)
    length = float(len(plaintext))
    for letter in plaintext:
        freq[ord(letter.lower()) - ord('a')]+=1
    g = [0]*26
    for shift in range(26):
        summation = 0
        shifted_freq = freq[shift:]+freq[:shift]
        for i in range(26):
            summation += ((shifted_freq[i]/length) / (frequency[i]/ngrams)) ** 2
        g[shift] = summation
    return 26-g.index(min(g))

if __name__ == '__main__':
    """Enter your text followed by ^D to perform frequency analysis"""
    text = ""
    for line in sys.stdin:
        text += line
    if text:
        shift = analysis(text)
        print(['Left','Right'][shift>13]+' shift of '+str(shift if shift<13 else (26-shift)))
        print(shift(text,shift))
