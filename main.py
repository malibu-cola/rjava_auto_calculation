import pyautogui
import pyperclip
import sys
import time
import threading
import schedule
import datetime
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


# # １０等分した値
# vYe0_0 = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
# vYe0_1 = ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
# vYe0_2 = ["20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]

# vT0_9 = ["1e9", "2e9", "3e9", "4e9", "5e9", "6e9", "7e9", "8e9", "9e9"]
# vT0_10 = ["1e10", "2e10", "3e10", "4e10", "5e10", "6e10", "7e10", "8e10", "9e10"]
# vT0_11 = ["1e11", "2e11", "3e11", "4e11", "5e11", "6e11", "7e11", "8e11", "9e11"]

# vrho0_10 = ["1e10","2e10","3e10", "4e10", "5e10","6e10","7e10", "8e10", "9e10"]
# vrho0_11 = ["1e11", "2e11", "3e11", "4e11","5e11","6e11", "7e11", "8e11", "9e11"]
# vrho0_12 = ["1e12", "2e12", "3e12", "4e12", "5e12", "6e12", "7e12", "8e12", "9e12"]
# vrho0_13 = ["1e13", "2e13", "3e13", "4e13", "5e13", "6e13", "7e13", "8e13", "9e13"]

# 初期化の仕方
# r-javaをデフォルトの状態、デフォルトのディレクトリで開いておく
# またテキストファイルも同様にデフォルトで開いてい置く
# DataモジュールのdisplayをGeneralDataだけにしておく

# T0 = "1e11"
# rho0 = "5e11"
# Ye0 = "021"
update = "500"
PolyIndex = "1"
P0 = "1e-4"
Vexp = "1e4"
R0 = "2"


# Ye = 09は終わったので消すよ
vYe0_0 = ["10", "13","16","19"\
        "20","23","26","29", "30", "01","03","06"]# 12こ

vT0_9 = ["4e9", "7e9",\
     "1e10", "4e10", "7e10",\
         "1e11", "4e11", "7e11", "1e12"] # 10こ

vrho0_10 = ["1e10","4e10", "7e10",\
    "1e11", "4e11", "7e11",\
        "1e12", "4e12", "7e12",\
            "1e13", "4e13"] # 11こ


cnt = 0
for Ye0 in vYe0_0:
    for T0 in vT0_9:
        for rho0 in vrho0_10:
            # 現在の時刻を表示
            now = datetime.datetime.now()
            print(now)

            print(cnt, "回目, Ye0:", Ye0,"  T0:", T0,"rho0",rho0)
            cnt+=1 #何回目か
            
            filename = "Ye_0" + Ye0 + "_T0_" + T0 + "_rho0_" + rho0
            if filename == "Ye_010_T0_7e10_rho0_7e13" or filename == "Ye_010_T0_7e10_rho0_1e14":
                continue
            rjava.opdf() #デフォルトを開く
            time.sleep(10)
            rjava.saveas(filename) #filenameで保存
            rjava.yesbotton() # 上書きする
            rjava.NSE(T0, rho0, "0." + Ye0) # NSEの条件を入力
            rjava.calculate()# 計算ボタンを押す
            time.sleep(5)# ５秒待つ
            rjava.Replot() # Replotを押す。
            screenshot = pyautogui.screenshot()
            path10 = "../進捗/0910to0917/pic/"+ filename + ".png"
            screenshot.save(path10)
            
            rjava.Data()# dataを開く
            txtdata1 = "elementdata__NSE_" + filename + ".txt"
            rjava.DtSv(txtdata1)# 一度データとして保存
            rjava.yesbotton()#上書き保存

            # テキストデータをこのpythonで開く
            path1 = "../進捗/0910to0917/data/" + txtdata1
            with open(path1) as f:
                line = f.readlines()
            print(line[1])
            # target_line = linecache.getline(path1,5)
            element, Z, A, N, mass, solarMF, MF,InitialMF = line[1].split( ) # １行目（水素１）のデートを読み込む            print(line[1], " MF:", MF)
            if MF == "NaN":# Nanだったら計算終了
                rjava.save()
                time.sleep(10)

            else:# NaNではなかったらr-processを実行する。
                rjava.graph2()
                rjava.setInital()
                time.sleep(2)
                rjava.rprocess(T0,rho0,update,PolyIndex,P0,Vexp,R0)
                rjava.calculate()
                time.sleep(10)
                rjava.Data()# dataを開く
                txtdata2 = "elementdata_freezeout_" + filename + ".txt"
                rjava.DtSv(txtdata2)
                rjava.yesbotton() # 上書き保存
                path2 = "../進捗/0910to0917/data/" + txtdata2
                with open(path2) as f:
                    line = f.readlines()
                print(line[1])
                # target_line = linecache.getline(path1,5)
                element, Z, A, N, mass, solarMF, MF,InitialMF = line[1].split( )
                if MF == "NaN":# Nanだったら計算終了
                    rjava.save()
                    time.sleep(10)
                else:   
                    time.sleep(1500)
                    rjava.graph2()
                    rjava.Replot()
                    screenshot2 = pyautogui.screenshot()
                    path11 = "../進捗/0910to0917/pic/elementdata_last_" + filename + ".png"
                    screenshot2.save(path11)
                    rjava.Data()# dataを開く
                    rjava.calstop()
                    txtdata3 = "elementdata_last_" + filename + ".txt"
                    rjava.DtSv(txtdata3)
                    rjava.save()
                    time.sleep(10)
