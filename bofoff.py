#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

from sys import argv
host = "10.211.55.9"
port = 8888

#r=remote(host,port)
print cyclic(int(argv[1]))

