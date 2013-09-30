#!/usr/bin/env python
import sys, re, os

frequency = [286527429118,52905544693,119155568598,136017528785,445155370175,85635440629,66615316232,180074687596,269731642485,5657910830,19261229433,144998552911,89506734085,257770795264,272276534337,76112599849,4292916949,223767519675,232082812755,330535289102,97273082907,37532682260,59712390260,8369138754,59331661972,3205398166]
ngrams = 3563505777820.0

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
        s = analysis(text)
        print(['Left','Right'][s>13]+' shift of '+str(s if s<13 else (26-s)))
        print(shift(text,s))
