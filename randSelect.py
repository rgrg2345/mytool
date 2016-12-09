#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randrange
from sys import argv
def main(arg):
  for item in arg[1:]:
    l=item.split(',')
    print "Random select from %s"%item
    print "Result : %s"%(l[randrange(len(l))])

if __name__ == '__main__':
  assert len(argv)>=2,"Need at least one choice"
  main(argv)

