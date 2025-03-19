import sys
import struct
import glob
import pandas as pd
import numpy as np


def parse_pfd(filename):
    header_params = [
        "ndms","nperiods","npdots","nsubs","nparts","proflen","nchans","pstep"
        ,"pdstep","dmstep","ndmfact","npfact","filname","candname","telescope","plotdev"
        ,"rastr","decstr","dt","tstart","tend","tepoch","bepoch","avgvoverc","lofreq"
        ,"chan_wid","best_dm","topo_pow","topo_p1","topo_p2","topo_p3","bary_pow","bary_p1"
        ,"bary_p2","bary_p3","fold_pow","fold_p1","fold_p2","fold_p3","orb_p","orb_e","orb_x"
        ,"orb_w","orb_t","orb_pd","orb_wd"]
    f = open(filename,"rb")
    values = {}
    count = 0
    for ii in range(12):
        values[header_params[count]] = struct.unpack("I",f.read(4))[0]
        count += 1
    for ii in range(4):
        val_len = struct.unpack("I",f.read(4))[0]
        values[header_params[count]] = b"".join([char for char in struct.unpack("c"*val_len,f.read(val_len))]).decode("utf-8")
        count += 1
    for ii in range(2):
        values[header_params[count]] = b"".join([char for char in struct.unpack("c"*13,f.read(13))]).decode("utf-8")
        f.seek(3,1)
        count += 1
    for ii in range(9):
        values[header_params[count]] = struct.unpack("d",f.read(8))[0]
        count += 1
    for ii in range(3):
        values[header_params[count]] = struct.unpack("f",f.read(4))[0]
        count += 1
        f.seek(4,1)
        for ii in range(3):
            values[header_params[count]] = struct.unpack("d",f.read(8))[0]
            count += 1
    f.close()
    return values


def p_to_f(p, pd, pdd=None):
    """
    p_to_f(p, pd, pdd=None):
       Convert period, period derivative and period second
       derivative to the equivalent frequency counterparts.
       Will also convert from f to p.
    """
    f = 1.0 / p
    fd = -pd / (p * p)
    if (pdd is None):
        return [f, fd]
    else:
        if (pdd == 0.0):
            fdd = 0.0
        else:
            fdd = 2.0 * pd * pd / (p ** 3.0) - pdd / (p * p)
        return [f, fd, fdd]




pfd = sys.argv[1]
values = parse_pfd(pfd)

f,fd,fdd = p_to_f(float(values['bary_p1']), float(values['bary_p2']), float(values['bary_p3']))
print("PSRJ {}".format(sys.argv[2]))
print("RAJ {}".format(values['rastr']))
print("DECJ {}".format(values['decstr']))
print("PEPOCH {}".format(values['bepoch']))
print("DM {}".format(values['best_dm']))
print("F0 {}".format(f))
print("F1 {}".format(fd))
print("F2 {}".format(fdd))


