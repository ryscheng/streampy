#!/usr/bin/env python
import sys

print sys.modules

name = "testdown"

__import__(name)

print "end!"
