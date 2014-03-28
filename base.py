#qpx: QuickPicx
#base.py: basic functions layer
#by Kenneth Feng

import os
import datetime

import EXIF

TYPES = ("jpg", "nef", "bmp")

def decodeArgs(argv):
    li = argv[1:].split(" ")
    li.sort()
    return li


def getExifInfo(file, dir, stop_tag=None):
    """get exif tags of a file"""
    f = open(dir+os.sep+file, 'rb')
    tags = EXIF.process_file(f)
    return tags
    


def lsByType(dir, type):
    """List Files under a directory by type"""
    files = os.listdir(dir)
    list = []
    for file in files:
        if file.split(".")[-1] == type:
            list.append(file)
    return list

def getCreationDate(file, dir):
    """Get the creation date of pictures"""
    tags = getExifInfo(file,dir)
    tag = "EXIF DateTimeOriginal"
    res = tags[tag].values.split(" ")[0]
    da = res.split(":")
    dat = datetime.date(int(da[0]),
                        int(da[1]),
                        int(da[2]))
    return dat

def getCreationTime(file, dir):
    """Get the creation time of pictures"""
    tags = getExifInfo(file,dir)
    tag = "EXIF DateTimeOriginal"
    res = tags[tag].values.split(" ")[1]
    tm = res.split(":")
    tme = datetime.time(int(tm[0]),
                        int(tm[1]),
                        int(tm[2]))
    return tme

def getCreationDateTime(file, dir):
    """Get the creation datetime of pictures"""
    tags = getExifInfo(file, dir)
    f = open(dir+os.sep+file, 'rb')
    tag = "EXIF DateTimeOriginal"
    res = tags[tag].values.split(" ")
    date = res[0].split(":");
    time = res[1].split(":");
    dt = datetime.datetime(int(date[0]), int(date[1]), int(date[2]),
                  int(time[0]), int(time[1]), int(time[2]))
    return dt

if __name__ == "__main__":
    for x in range(4):
        fn = '%d.nef' % (x + 1)
        with open(fn) as f:
            tags = EXIF.process_file(f)        
            for k, v in tags.items():
                print k, v

