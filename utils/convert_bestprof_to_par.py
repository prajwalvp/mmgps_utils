import sys
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
    f = open(filename,"r")
    values = {}
    count = 0
    for ii in range(12):
        values[header_params[count]] = struct.unpack("I",f.read(4))[0]
        count += 1
    for ii in range(4):
        val_len = struct.unpack("I",f.read(4))[0]
        values[header_params[count]] = ''.join([char for char in struct.unpack("c"*val_len,f.read(val_len))])
        count += 1
    for ii in range(2):
        values[header_params[count]] = ''.join([char for char in struct.unpack("c"*13,f.read(13))])
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
        return f, fd, 0.0 
    else:
        if (pdd == 0.0):
            fdd = 0.0
        else:
            fdd = 2.0 * pd * pd / (p ** 3.0) - pdd / (p * p)
        return f, fd, fdd


bestprof = sys.argv[1]


with open(sys.argv[2],"w") as ff:
    data = pd.read_csv(bestprof)
    mjd = data.iloc[3][0].split('=')[1]
    period = float(data.iloc[17][0].split('=')[1].split('+/-')[0]) 
    period_uncertainty = "{:.15f}".format(float(data.iloc[17][0].split('=')[1].split('+/-')[1]))
    pder = float(data.iloc[18][0].split('=')[1].split('+/-')[0]) 
    pder_uncertainty = "{:.15f}".format(float(data.iloc[18][0].split('=')[1].split('+/-')[1]))
    pdd = float(data.iloc[19][0].split('=')[1].split('+/-')[0]) 
    pder_uncertainty = "{:.15f}".format(float(data.iloc[19][0].split('=')[1].split('+/-')[1]))
    dm = float(data.iloc[13][0].split('=')[1])
    f,fd,fdd = p_to_f(period, pder, pdd)  
    print('PSRJ {}'.format(sys.argv[3]))
    print('RAJ {}')    


ff.close()
