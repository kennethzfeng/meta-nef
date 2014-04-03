#!/usr/bin/python2
import datetime
from exifread import process_file


INTERESTING_TAGS = (
    'EXIF DateTimeOriginal',
    'Image DateTimeOriginal',
    'Image DateTime',
    'EXIF DateTimeDigitized'
)

def to_datetime(datetime_string):
    FORMAT = '%Y:%m:%d %H:%M:%S'
    return datetime.datetime.strptime(datetime_string, FORMAT)

def get_datetime_from_tags(tags):
    datetime_dict = {key: to_datetime(tags[key].values) 
                    for key in tags if key in INTERESTING_TAGS}
    return datetime_dict 


if __name__ == "__main__":
    import os
    import sys
    if len(sys.argv) <= 1:
        print "Error"
    else:
        f = sys.argv[1]
        tags = process_file(open(os.path.join(os.getcwd(), f)))
        print get_datetime_from_tags(tags)
