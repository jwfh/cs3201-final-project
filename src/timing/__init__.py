#!/usr/bin/env python3

## System imports
import time

## Constants
DEBUG = True

## Begin function timing.timing
def timing(f):
    def wrap(*args, **kwargs):
        if DEBUG:
            time1 = time.time()
        ret = f(*args, **kwargs)
        if DEBUG:
            time2 = time.time()
            print('\r{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap
## End function timing.timing