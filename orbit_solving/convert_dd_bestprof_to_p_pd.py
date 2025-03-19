import sys
import glob
import pandas as pd
import numpy as np


bestprofs = sorted(glob.glob(str(sys.argv[1])))


with open(sys.argv[2],"a") as f:
    for bestprof in bestprofs:
        print(bestprof)
        data = pd.read_csv(bestprof)
        mjd = data.iloc[3][0].split('=')[1]
        period_uncertainty = "{:.9f}".format(float(data.iloc[16][0].split('=')[1].split('+/-')[1]))
        period = float(data.iloc[16][0].split('=')[1].split('+/-')[0])
        pder_uncertainty = "{:.15f}".format(float(data.iloc[17][0].split('=')[1].split('+/-')[1]))
        pder = float(data.iloc[17][0].split('=')[1].split('+/-')[0])
        #f.write("{} {} {} {} {}\n".format(mjd, period, period_uncertainty, pder, pder_uncertainty))
        f.write("{} {} {} {}\n".format(mjd, period, pder, pder_uncertainty))
f.close()
 
