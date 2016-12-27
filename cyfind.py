#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from sys import argv
searchlen=200

def h2ord(h):
   h=h[2:]
   lens=len(h)/2
   s=""
   for i in range(lens):
       s=h[i*2:(i+1)*2]+s
   return s.decode('hex')

bofstr=cyclic(searchlen)
dst=h2ord(argv[1])
for i in range(0,searchlen,4):
    #print "compare :%s with %s"%(bofstr[i:i+4],dst)
    if dst==bofstr[i:i+4]:
        print argv[1],"found at offset:",i if i>0 else 0
        break
