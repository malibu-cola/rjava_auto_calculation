import pyautogui
import pyperclip
import sys
import time
import threading
import schedule
from action import rjava
from action import analysis

import os
import glob
import linecache
import seaborn as sns;
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from matplotlib.ticker import MaxNLocator

# T0 = "1e11"
# rho0 = "5e11"
# Ye0 = "021"
update = "500"
PolyIndex = "1"
P0 = "1e-4"
Vexp = "1e4"
R0 = "2"

# rjava.opdf()
# filename = "Ye_" + Ye0 + "_T0_" + T0 + "_rho0_" + rho0
# time.sleep(10)
# rjava.saveas(filename)
# rjava.NSE(T0, rho0, Ye0)
# rjava.calculate()
# rjava.setInital()
# time.sleep(2)
# rjava.rprocess(T0,rho0,update,PolyIndex,P0,Vexp,R0)
# rjava.save()
# rjava.calculate()

vYe0_0 = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
vYe0_1 = ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
vYe0_2 = ["20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]

vT0_9 = ["1e9", "2e9", "3e9", "4e9", "5e9", "6e9", "7e9", "8e9", "9e9"]
vT0_10 = ["1e10", "2e10", "3e10", "4e10", "5e10", "6e10", "7e10", "8e10", "9e10"]
vT0_11 = ["1e11", "2e11", "3e11", "4e11", "5e11", "6e11", "7e11", "8e11", "9e11"]

vrho0_10 = ["1e10","2e10","3e10", "4e10", "5e10","6e10","7e10", "8e10", "9e10"]
vrho0_11 = ["1e11", "2e11", "3e11", "4e11","5e11","6e11", "7e11", "8e11", "9e11"]
vrho0_12 = ["1e12", "2e12", "3e12", "4e12", "5e12", "6e12", "7e12", "8e12", "9e12"]
vrho0_13 = ["1e13", "2e13", "3e13", "4e13", "5e13", "6e13", "7e13", "8e13", "9e13"]

cnt = 0
for Ye0 in vYe0_0:
    for T0 in vT0_9:
        for rho0 in vrho0_10:
            print(cnt, "回目, Ye0:", Ye0,"  T0:", T0,"rho0",rho0)
            cnt+=1
            rjava.opdf()
            filename = "Ye_0" + Ye0 + "_T0_" + T0 + "_rho0_" + rho0
            time.sleep(10)
            rjava.saveas(filename)
            rjava.yesbotton()
            rjava.NSE(T0, rho0, "0." + Ye0)
            rjava.calculate()
            time.sleep(5)
            rjava.setInital()
            time.sleep(2)
            rjava.rprocess(T0,rho0,update,PolyIndex,P0,Vexp,R0)
            rjava.calculate()
            time.sleep(10)
            rjava.Data()
            txtdata = "elementdata_" + filename + ".txt"
            rjava.DtSv(txtdata)
            rjava.yesbotton()
            path = "../進捗/0826to0902/" + txtdata
            with open(path) as f:
                line = f.readlines()
            print(line[1])
            # target_line = linecache.getline(path,5)
            element, Z, A, N, mass, solarMF, MF,InitialMF = line[1].split( )
            print(line[1], " MF:", MF)
            if MF == "NaN" or InitialMF == "NaN":
                rjava.save()
                time.sleep(10)
            else:
                time.sleep(1800)
                rjava.save()
                # Nanではなかった計算のElement dataを保存しないと
                time.sleep(10)
