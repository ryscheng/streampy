#!/usr/bin/env python

## load.py loads a URL specified on the command line and execs it.

import urllib
import sys
import threading
import os
import glob
import time

# Eventually you'll get these from apt-run.  
rooturl = "http://code.general-rotors.com/streambin/"
firstsegurl = "streamtest.pyc"
firstsegname = "streamtest"
firstsegpath = "/tmp/streambin/"

# This is so that you can load the new modules.
sys.path.append(firstsegpath)

# Create a lock to stop the background thread getting stuff while the
# foreground thread needs it right away

netlock = threading.Condition()

## the BackgroundStream grabs the remaining modules while the
## foreground thread is running the program.

class BackgroundStream(threading.Thread):
    """It downloads pyc files in the background.  You must tell it the
    root url from which to get a modlist.txt and the folder (segment
    path) into which the pyc files are to be downloaded."""
    def __init__(self, rooturl, segpath):
        self.rooturl = rooturl
        self.segpath = segpath
        self.modules = []
        threading.Thread.__init__(self)
    def run(self):
        # even things out a little -- let the lazy loader work
        time.sleep(0.5)
        print("STREAMBIN: Background thread started downloading.")
        modlist = urllib.urlopen(rooturl+"modlist.txt")
        self.modules = [m.rstrip('\n') + ".pyc" for m in modlist.readlines()]
        print "STREAMBIN: Got all the modules:", self.modules
        for m in self.modules:
            print "STREAMBIN: Checking module", m
            # This checks if we've already downloaded the module.
            globs = glob.glob(self.segpath+"*.pyc")
            print "STREAMBIN: globs are", globs
            if [os.path.basename(g) for g in glob.glob(self.segpath+"*.pyc")].count(m) == 0:
                print "waiting for netlock"
                netlock.acquire()
                print "got the netlock"
                urllib.urlretrieve(self.rooturl+m, self.segpath+m)
                netlock.release()
                print "STREAMBIN: Background thread got", m, "in the background."
            # else go on to the next module.  They should be in order.
            else:
                print "STREAMBIN: Skipped module", m, "since it was already downloaded."
        print "STREAMBIN: All done!  Rejoining main thread."

def erroryank(error):
    return error.message[16:]

def streamrun(segname):
    netlock.acquire()
    (seg, headers) = urllib.urlretrieve(rooturl+segname+".pyc", firstsegpath+segname+".pyc");
    netlock.release()
    try:
        __import__(segname)
    except ImportError, (err):
        name = erroryank(err)
        if name == segname:
            raise
        else:
            streamrun(name)
            streamrun(segname)

background = BackgroundStream(rooturl, firstsegpath)
background.start()
print "STREAMBIN: Created background task; now running main task"
streamrun(firstsegname)
background.join()
    
# This is here as a test -- I want to find a way to get around the common idiom
# if __name__ == '__main__':
#    do_more_stuff()

#exec "import " + firstsegname + " as __main__"
