#!/usr/bin/env python

from __future__ import print_function
from optparse import OptionParser
import os
import sys


stdin = ""
for line in sys.stdin.readlines():
    stdin += "%s\n" % line

tmpfile = "%s%s" % (os.environ["TMPDIR"], "script.go")
f = open(tmpfile, 'w')
print(stdin, file=f)
f.close()
os.execlp("go", "", "run", tmpfile)