#!/usr/bin/env python

## load.py loads a URL specified on the command line and execs it.

import urllib
import sys

urllib.urlcleanup()
firstsegurl = "http://code.general-rotors.com/streambin/streamtest.pyc"
firstsegname = "testdown"
firstsegpath = "/tmp/streambin/"

sys.path.append(firstsegpath)

(firstseg, headers) = urllib.urlretrieve(firstsegurl, firstsegpath+firstsegname+".pyc");

__import__(firstsegname)

