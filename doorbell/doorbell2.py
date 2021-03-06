#!/usr/bin/python
import RPi.GPIO as GPIO
import os
import time
import random
import pdb

confFile="/etc/doorbell.cfg"

##############################################################################
def processConf(fileName,fileList):
    """
    To check the config file and send back the results.
    An empty string if there is no mp3 to play all the time or else
    the name of the file to play always
    """
    playString=""
    f = open(fileName.strip())
    try:
        for rawline in f:
            line=rawline.strip()
            print "################ %s #######################" % (line)
            if line in fileList:
                playString=line
                return playString
            pass
    finally:
        f.close()
    
    return playString
###########################################################################


# set up the gpio stuff
GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.IN)



# get the list of mp3 files we have
fileList=os.listdir('thesounds/')

# remove any that aren't mp3s
for thefile in fileList:
    if(not thefile.endswith('.mp3')):
        fileList.remove(thefile)


# to achieve very simple configuration we will look at a file and if 
#  that file has the name of one of the files in the dir then we will only play that
playString=processConf(confFile,fileList)

cstat=os.stat(confFile)
confTime=cstat.st_mtime # remember the last time the file was changed

#pdb.set_trace()
state = 0
while 1:
    button = GPIO.input(17)

    # we will not need to do much with debounce as the playing of the
    # mp3 file will delay things more than enough to cope with anything 
    if button == 1:
        #print "button pressed"
        if playString=="":
            """
            Then we randomise which file to play from the mp3s in  the main directory
            """
            rawRandom=random.random()
            randomNum=int(rawRandom * len(fileList))
            randomSoundFile=fileList[randomNum]
            os.system('mpg123 thesounds/%s' % (randomSoundFile))
        else:
            os.system('mpg123 thesounds/%s' % (playString))
        
    # check the conf file
    ccstat=os.stat(confFile)
    checkConfTime=ccstat.st_mtime
    if(checkConfTime != confTime):
        playString=processConf(confFile,fileList)
        confTime=checkConfTime
        
    data=None
