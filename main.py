#!/usr/bin/python2
import sys
import datetime
FIELD_TYPES = (
    (0, 'X', 'Proprietary'), # no such type
    (1, 'B', 'Byte'),
    (1, 'A', 'ASCII'),
    (2, 'S', 'Short'),
    (4, 'L', 'Long'),
    (8, 'R', 'Ratio'),
    (1, 'SB', 'Signed Byte'),
    (1, 'U', 'Undefined'),
    (2, 'SS', 'Signed Short'),
    (4, 'SL', 'Signed Long'),
    (8, 'SR', 'Signed Ratio'),
    )
EXIF_TAGS = {
    0x0100: ('ImageWidth', ),
    0x0101: ('ImageLength', ),
    0x0102: ('BitsPerSample', ),
    0x0103: ('Compression',
             {1: 'Uncompressed',
              2: 'CCITT 1D',
              3: 'T4/Group 3 Fax',
              4: 'T6/Group 4 Fax',
              5: 'LZW',
              6: 'JPEG (old-style)',
              7: 'JPEG',
              8: 'Adobe Deflate',
              9: 'JBIG B&W',
              10: 'JBIG Color',
              32766: 'Next',
              32769: 'Epson ERF Compressed',
              32771: 'CCIRLEW',
              32773: 'PackBits',
              32809: 'Thunderscan',
              32895: 'IT8CTPAD',
              32896: 'IT8LW',
              32897: 'IT8MP',
              32898: 'IT8BL',
              32908: 'PixarFilm',
              32909: 'PixarLog',
              32946: 'Deflate',
              32947: 'DCS',
              34661: 'JBIG',
              34676: 'SGILog',
              34677: 'SGILog24',
              34712: 'JPEG 2000',
              34713: 'Nikon NEF Compressed',
              65000: 'Kodak DCR Compressed',
              65535: 'Pentax PEF Compressed'}),
    0x0106: ('PhotometricInterpretation', ),
    0x0107: ('Thresholding', ),
    0x010A: ('FillOrder', ),
    0x010D: ('DocumentName', ),
    0x010E: ('ImageDescription', ),
    0x010F: ('Make', ),
    0x0110: ('Model', ),
    0x0111: ('StripOffsets', ),
    0x0112: ('Orientation',
             {1: 'Horizontal (normal)',
              2: 'Mirrored horizontal',
              3: 'Rotated 180',
              4: 'Mirrored vertical',
              5: 'Mirrored horizontal then rotated 90 CCW',
              6: 'Rotated 90 CW',
              7: 'Mirrored horizontal then rotated 90 CW',
              8: 'Rotated 90 CCW'}),
    0x0115: ('SamplesPerPixel', ),
    0x0116: ('RowsPerStrip', ),
    0x0117: ('StripByteCounts', ),
    0x011A: ('XResolution', ),
    0x011B: ('YResolution', ),
    0x011C: ('PlanarConfiguration', ),
#    0x011D: ('PageName', make_string),
    0x0128: ('ResolutionUnit',
             {1: 'Not Absolute',
              2: 'Pixels/Inch',
              3: 'Pixels/Centimeter'}),
    0x012D: ('TransferFunction', ),
    0x0131: ('Software', ),
    0x0132: ('DateTime', ),
    0x013B: ('Artist', ),
    0x013E: ('WhitePoint', ),
    0x013F: ('PrimaryChromaticities', ),
    0x0156: ('TransferRange', ),
    0x0200: ('JPEGProc', ),
    0x0201: ('JPEGInterchangeFormat', ),
    0x0202: ('JPEGInterchangeFormatLength', ),
    0x0211: ('YCbCrCoefficients', ),
    0x0212: ('YCbCrSubSampling', ),
    0x0213: ('YCbCrPositioning',
             {1: 'Centered',
              2: 'Co-sited'}),
    0x0214: ('ReferenceBlackWhite', ),
    
    0x4746: ('Rating', ),
    
    0x828D: ('CFARepeatPatternDim', ),
    0x828E: ('CFAPattern', ),
    0x828F: ('BatteryLevel', ),
    0x8298: ('Copyright', ),
    0x829A: ('ExposureTime', ),
    0x829D: ('FNumber', ),
    0x83BB: ('IPTC/NAA', ),
    0x8769: ('ExifOffset', ),
    0x8773: ('InterColorProfile', ),
    0x8822: ('ExposureProgram',
             {0: 'Unidentified',
              1: 'Manual',
              2: 'Program Normal',
              3: 'Aperture Priority',
              4: 'Shutter Priority',
              5: 'Program Creative',
              6: 'Program Action',
              7: 'Portrait Mode',
              8: 'Landscape Mode'}),
    0x8824: ('SpectralSensitivity', ),
    0x8825: ('GPSInfo', ),
    0x8827: ('ISOSpeedRatings', ),
    0x8828: ('OECF', ),
#    0x9000: ('ExifVersion', make_string),
    0x9003: ('DateTimeOriginal', ),
    0x9004: ('DateTimeDigitized', ),
    0x9101: ('ComponentsConfiguration',
             {0: '',
              1: 'Y',
              2: 'Cb',
              3: 'Cr',
              4: 'Red',
              5: 'Green',
              6: 'Blue'}),
    0x9102: ('CompressedBitsPerPixel', ),
    0x9201: ('ShutterSpeedValue', ),
    0x9202: ('ApertureValue', ),
    0x9203: ('BrightnessValue', ),
    0x9204: ('ExposureBiasValue', ),
    0x9205: ('MaxApertureValue', ),
    0x9206: ('SubjectDistance', ),
    0x9207: ('MeteringMode',
             {0: 'Unidentified',
              1: 'Average',
              2: 'CenterWeightedAverage',
              3: 'Spot',
              4: 'MultiSpot',
              5: 'Pattern'}),
    0x9208: ('LightSource',
             {0: 'Unknown',
              1: 'Daylight',
              2: 'Fluorescent',
              3: 'Tungsten',
              9: 'Fine Weather',
              10: 'Flash',
              11: 'Shade',
              12: 'Daylight Fluorescent',
              13: 'Day White Fluorescent',
              14: 'Cool White Fluorescent',
              15: 'White Fluorescent',
              17: 'Standard Light A',
              18: 'Standard Light B',
              19: 'Standard Light C',
              20: 'D55',
              21: 'D65',
              22: 'D75',
              255: 'Other'}),
    0x9209: ('Flash',
             {0: 'No',
              1: 'Fired',
              5: 'Fired (?)', # no return sensed
              7: 'Fired (!)', # return sensed
              9: 'Fill Fired',
              13: 'Fill Fired (?)',
              15: 'Fill Fired (!)',
              16: 'Off',
              24: 'Auto Off',
              25: 'Auto Fired',
              29: 'Auto Fired (?)',
              31: 'Auto Fired (!)',
              32: 'Not Available'}),
    0x920A: ('FocalLength', ),
    0x9214: ('SubjectArea', ),
    0x927C: ('MakerNote', ),
#    0x9286: ('UserComment', make_string_uc),
    0x9290: ('SubSecTime', ),
    0x9291: ('SubSecTimeOriginal', ),
    0x9292: ('SubSecTimeDigitized', ),
    
    # used by Windows Explorer
    0x9C9B: ('XPTitle', ),
    0x9C9C: ('XPComment', ),
    0x9C9D: ('XPAuthor', ), #(ignored by Windows Explorer if Artist exists)
    0x9C9E: ('XPKeywords', ),
    0x9C9F: ('XPSubject', ),

#    0xA000: ('FlashPixVersion', make_string),
    0xA001: ('ColorSpace',
             {1: 'sRGB',
              2: 'Adobe RGB',
              65535: 'Uncalibrated'}),
    0xA002: ('ExifImageWidth', ),
    0xA003: ('ExifImageLength', ),
    0xA005: ('InteroperabilityOffset', ),
    0xA20B: ('FlashEnergy', ),               # 0x920B in TIFF/EP
    0xA20C: ('SpatialFrequencyResponse', ),  # 0x920C
    0xA20E: ('FocalPlaneXResolution', ),     # 0x920E
    0xA20F: ('FocalPlaneYResolution', ),     # 0x920F
    0xA210: ('FocalPlaneResolutionUnit', ),  # 0x9210
    0xA214: ('SubjectLocation', ),           # 0x9214
    0xA215: ('ExposureIndex', ),             # 0x9215
    0xA217: ('SensingMethod',                # 0x9217
             {1: 'Not defined',
              2: 'One-chip color area',
              3: 'Two-chip color area',
              4: 'Three-chip color area',
              5: 'Color sequential area',
              7: 'Trilinear',
              8: 'Color sequential linear'}),             
    0xA300: ('FileSource',
             {1: 'Film Scanner',
              2: 'Reflection Print Scanner',
              3: 'Digital Camera'}),
    0xA301: ('SceneType',
             {1: 'Directly Photographed'}),
    0xA302: ('CVAPattern', ),
    0xA401: ('CustomRendered',
             {0: 'Normal',
              1: 'Custom'}),
    0xA402: ('ExposureMode',
             {0: 'Auto Exposure',
              1: 'Manual Exposure',
              2: 'Auto Bracket'}),
    0xA403: ('WhiteBalance',
             {0: 'Auto',
              1: 'Manual'}),
    0xA404: ('DigitalZoomRatio', ),
    0xA405: ('FocalLengthIn35mmFilm', ),
    0xA406: ('SceneCaptureType',
             {0: 'Standard',
              1: 'Landscape',
              2: 'Portrait',
              3: 'Night)'}),
    0xA407: ('GainControl',
             {0: 'None',
              1: 'Low gain up',
              2: 'High gain up',
              3: 'Low gain down',
              4: 'High gain down'}),
    0xA408: ('Contrast',
             {0: 'Normal',
              1: 'Soft',
              2: 'Hard'}),
    0xA409: ('Saturation',
             {0: 'Normal',
              1: 'Soft',
              2: 'Hard'}),
    0xA40A: ('Sharpness',
             {0: 'Normal',
              1: 'Soft',
              2: 'Hard'}),
    0xA40B: ('DeviceSettingDescription', ),
    0xA40C: ('SubjectDistanceRange', ),
    0xA500: ('Gamma', ),
    0xC4A5: ('PrintIM', ),
    0xEA1C:	('Padding', ),
    }


def getByte(f, offset, length):
    f.seek(offset)
    return f.read(length)

def decode_motorola(string):
    x = 0
    for c in string:
        x = (x << 8) | ord(c)
    return x

class TIFFReader(object):
    ENDIANNESS = { 'I': 'INTEL', 'M':'MOTOROLA' }
    DECODE_FUNC = { 'I': None, 'M' : decode_motorola }
    def __init__(self, f):
        self.f = f
        self.endian = getByte(self.f, 0, 1)
        self.func = self.DECODE_FUNC[self.endian]

    def getEndianString(self):
        return self.ENDIANNESS[self.endian]
    
    def getFirstIFD(self):
        return self.s2n(4, 4)

    def getNextIFD(self, ifd):
        entries = self.s2n(ifd, 2)
        return self.s2n(ifd+2+(12*entries), 4)

    def s2n(self, offset, length):
        return self.func(getByte(self.f, offset, length))

    def getIFDs(self):
        i = self.getFirstIFD()
        a = []
        while i:
            a.append(i)
            i = self.getNextIFD(i)
        return a

    def dump_IFD(self, ifd):
        entries = self.s2n(ifd, 2)
        for i in range(entries):
            entry = ifd + 2 + 12 * i
            tag = self.s2n(entry, 2)
            tag_name = EXIF_TAGS.get(tag)
            field_type = self.s2n(entry + 2, 2)
            typelen = FIELD_TYPES[field_type][0]
            count = self.s2n(entry + 4, 4)
            offset = entry + 8

            print tag_name, typelen, count, offset

    def getDateTime(self):
        self.f.seek(234)
        typelen = 1
        count = 20
        offset = self.s2n(234, 4)
        self.f.seek(offset)
        values = []
        for i in range(count):
            val = self.s2n(offset + i * typelen, typelen)
            values.append(chr(val))

        date, time = "".join(values[:-1]).split(" ")
        dt_str = date.split(':') + time.split(':')
        return datetime.datetime(*[int(v) for v in dt_str])
        


if len(sys.argv) <= 1:
    print "Error"
else:
    f = sys.argv[1]
    dt = TIFFReader(open(os.path.join(os.getcwd(), f))).getDateTime()
    print dt
