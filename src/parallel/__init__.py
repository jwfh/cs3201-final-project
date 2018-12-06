#!/usr/bin/env python3

## System imports
import multiprocessing as mp 
import numpy as np
import pathos.multiprocessing as pmp

def func(f, q_in, q_out, unpack=False):
    while True:
        i, x = q_in.get()
        if i is None:
            break
        if unpack:
            q_out.put((i, f(*x)))
        else:
            q_out.put((i, f(x)))


def parallel_map(f, X, nprocs: int=mp.cpu_count(), unpack: bool=False) -> map:
    q_in = mp.Queue(1)
    q_out = mp.Queue()

    proc = [mp.Process(target=func, args=(f, q_in, q_out, unpack)) for _ in range(nprocs)]
    for p in proc:
        p.daemon = True
        p.start()
    sent = [q_in.put((i, x)) for i, x in enumerate(X)]
    for _ in range(nprocs):
        q_in.put((None, None))
    res = [q_out.get() for _ in range(len(sent))]
    for p in proc:
        p.join()

    for (i, x) in sorted(res):
        yield x 

