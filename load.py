#!/usr/bin/env python

## load.py loads a URL specified on the command line and execs it.

import urllib
import sys

# Eventually you'll get these from apt-run.  
firstsegurl = "http://code.general-rotors.com/streambin/streamtest.pyc"
firstsegname = "testdown"
firstsegpath = "/tmp/streambin/"

# This is so that you can load the new modules.
sys.path.append(firstsegpath)

(firstseg, headers) = urllib.urlretrieve(firstsegurl, firstsegpath+firstsegname+".pyc");

__import__(firstsegname)

# This is here as a test -- I want to find a way to get around the common idiom
# if __name__ == '__main__':
#    do_more_stuff()

#exec "import " + firstsegname + " as __main__"
