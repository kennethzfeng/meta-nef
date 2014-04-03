import os
from main import TIFFReader
from datetime import datetime


def test_TIFFReader():
    path = 'test_images/1.nef'
    reader = TIFFReader(open(os.path.join(os.getcwd(), path)))
    dt = reader.getDateTime()
    assert dt == datetime(2009, 6, 3, 19, 57, 29)
