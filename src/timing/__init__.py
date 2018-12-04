#!/usr/bin/env python3

## System imports
import time

## Constants
DEBUG = False

## Begin function timing.timing
def timing(f):
    def wrap(*args, **kwargs):
        if DEBUG and f.__name__ != 'main':
            time1 = time.time()
        ret = f(*args, **kwargs)
        if DEBUG and f.__name__ != 'main':
            time2 = time.time()
            print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap
## End function timing.timing