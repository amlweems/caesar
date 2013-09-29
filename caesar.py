#!/usr/bin/env python
import sys, re, os

PATH_OF_SCRIPT=os.path.dirname(os.path.realpath(__file__))

PATH_TO_DICT=os.path.join(PATH_OF_SCRIPT, 'words.txt')
dictionary = set(open(PATH_TO_DICT).read().split('\n'))

PATH_TO_FREQ=os.path.join(PATH_OF_SCRIPT, 'frequency.tsv')
frequency = [0]*26
ngrams = 0.0

with open(PATH_TO_FREQ) as f:
    for line in f.read().split('\n'):
        letter, freq = line.split('\t')
        frequency[ord(letter.lower()) - ord('a')]=int(freq)
        ngrams+=int(freq)

def shift(plaintext, s):
    return ''.join([chr(((ord(j)&0x9F)+s-1)%26+1+0x40+(0x20 if ord(j)&0x20 else 0)) if j.isalpha() else j for j in plaintext])

def bruteforce(plaintext):
    return [shift(plaintext,i) for i in range(26)]

def guess(plaintext):
    return max(bruteforce(plaintext), key=lambda x: analyse(x))

def analyse(text):
    words = set([i.lower() for i in re.split('\W',text) if i])
    return len(dictionary.intersection(words))

def analysis(plaintext):
    f = [0]*26
    plaintext = re.sub('\W','',plaintext)
    length = len(plaintext)+0.0
    for l in plaintext:
        f[(ord(l)&0x9F)-1]+=1
    g = [0]*26
    for s in range(26):
        summation = 0
        tmp = f[s:]+f[:s]
        for i in range(26):
            summation += ((tmp[i]/length) / (frequency[i]/ngrams)) ** 2
        g[s] = summation
    return 26-g.index(min(g))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        inp = sys.argv[1]
    else:
        inp = sys.stdin.readline()
    if len(sys.argv) > 2 and sys.argv[2].isdigit():
        print shift(inp,int(sys.argv[2]))
    else:
        s = analysis(inp)
        print ['Left','Right'][s>13]+' shift of '+str(s if s<13 else (26-s))
        print shift(inp,s)
