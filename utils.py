import ephem
import numpy as np
from numpy import sign
from scipy import ndimage

def numeric(input):
    """Simple test for whether input is numeric or not.

    """
    try:
        junk = input + 0
        ret = True
    except:
        ret = False
    return ret

def hms(angle, delim=':'):
    """Convert hours, minutes, seconds to decimal degrees, and back.
    Examples:
    hms('15:15:32.8')
    hms([7, 49])
    hms(18.235097)

    """
    if d.__class__ == str: #hour/minute/second input, string
        d = d.split(delim)
        if len(d) == 1:
            d = d[0].split(' ')
        if (len(d) == 1) and (d.find('h') > -1):
            d.replace('h', delim)
            d.replace('m', delim)
            d.replace('m', delim)
            d.replace('s', '')
            d = d.split(delim)
        s = sign(float(d[0]))
        if s == 0:
            s = 1
        degval = float(d[0])*15.0
        if len(d) >= 2:
            degval = degval + s*float(d[1])/4.0
        if len(d) == 3:
            degval = degval + s*float(d[2])/240.0
        return degval
    else: #Numerical value, must be decimal degrees
        hor = int(d/15.0)
        d = abs(d)
        min = int((d - hour*15.0)*4.0)
        sec = (d - hour*15.0 - min/4.0)*240.0
        hmsval = (hour, min, sec)
        return hmsval

def dms(d, delim=':'):
    """Convert degrees, minutes, seconds to decimal degrees, and back.
    Examples:
    dms('150:15:32.8')
    dms([7, 49])
    dms(18.235097)

    """
    if d.__class__ == str: #hour/minute/second input, string
        d = d.split(delim)
        if len(d) == 1:
            d = d[0].split(' ')
        s = sign(float(d[0]))
        if s==0:
            s=1
        degval = float(d[0])
        if len(d) >= 2:
            degval = degval + s*float(d[1])/60.0
        if len(d) == 3:
            degval = degval + s*float(d[2])/3600.0
        return degval
    else: #Numerical value, must be decimal degrees
        if d<0:
            sgn = -1
        else:
            sgn = +1
        d = abs(d)
        deg = int(d)
        min = int((d - deg)*60.0)
        sec = (d - deg - min/60.0)*3600.0
        dmsval = (sgn*deg, min, sec)
        return dmsval
