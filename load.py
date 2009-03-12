#!/usr/bin/env python

## load.py loads a URL specified on the command line and execs it.

import urllib
import sys
import threading

# Eventually you'll get these from apt-run.  
rooturl = "http://code.general-rotors.com/streambin/"
firstsegurl = "streamtest.pyc"
firstsegname = "streamtest"
firstsegpath = "/tmp/streambin/"

# This is so that you can load the new modules.
sys.path.append(firstsegpath)



def erroryank(error):
    return error.message[16:]

def streamrun(segname):
    (seg, headers) = urllib.urlretrieve(rooturl+segname+".pyc", firstsegpath+segname+".pyc");
    try:
        __import__(segname)
    except ImportError, (err):
        name = erroryank(err)
        if name == segname:
            raise
        else:
            streamrun(name)
            streamrun(segname)

streamrun(firstsegname)
    
# This is here as a test -- I want to find a way to get around the common idiom
# if __name__ == '__main__':
#    do_more_stuff()

#exec "import " + firstsegname + " as __main__"
