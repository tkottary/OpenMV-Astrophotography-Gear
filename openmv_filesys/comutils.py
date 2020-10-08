import micropython
micropython.opt_level(2)

import math, pyb
import utime

SENSOR_WIDTH  = micropython.const(2592)
SENSOR_HEIGHT = micropython.const(1944)

PIXELS_PER_DEGREE = micropython.const(875.677409 / 2.9063) # calculated using "OV Cep"
SIDEREAL_DAY_SECONDS = micropython.const(86164.09054)

def angle_diff(x, y):
    x = ang_normalize(x)
    y = ang_normalize(y)
    return ang_normalize(x - y)

def ang_normalize(x):
    while x > 180.0:
        x -= 360.0
    while x < -180.0:
        x += 360.0
    return x

def utc_to_epoch(utc_yr, utc_month, utc_day, utc_hr, utc_min, utc_sec):
    s = utime.mktime((utc_yr, utc_month, utc_day, utc_hr, utc_min, utc_sec, 0, 0))
    return s

def jdn(y, m, d):
    # http://www.cs.utsa.edu/~cs1063/projects/Spring2011/Project1/jdn-explanation.html
    return d + (((153 * m) + 2) // 5) + (356 * y) + (y // 4) - (y // 100) + (y // 400) - 32045

def fmt_time(t):
    return "%04u/%02u/%02u-%02u:%02u:%02u" % (t[0], t[1], t[2], t[3], t[4], t[5])

def vector_between(p1, p2, mag_only = False):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    mag = math.sqrt((dx ** 2) + (dy ** 2))
    if mag_only:
        return mag
    ang = math.degrees(math.atan2(dy, dx))
    return mag, ang

def map_val(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min