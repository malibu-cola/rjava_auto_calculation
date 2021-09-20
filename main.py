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

update = "500"
PolyIndex = "1"
P0 = "1e-4"
Vexp = "1e4"
R0 = "2"

vYe0_0 = ["09", "10", "13","16","19"\
        "20","23","26","29", "30", "01","03","06"]# 12こ

vT0_9 = ["7e11", "4e9", "7e9",\
     "1e10", "4e10", "7e10",\
         "1e11", "4e11",  "1e12"] # 10こ

vrho0_10 = ["4e13","1e10","4e10", "7e10",\
    "1e11", "4e11", "7e11",\
        "1e12", "4e12", "7e12",\
            "1e13"] # 11こ

cnt = 0
for Ye0 in vYe0_0:
    for T0 in vT0_9:
        for rho0 in vrho0_10:
            # 現在の時刻を表示
            now = datetime.datetime.now()
            print(now)

            # 何回目、初期条件を表示
            print(cnt, "回目, Ye0:", Ye0,"  T0:", T0,"rho0",rho0)
            cnt+=1 #何回目か
            
            filename = "Ye_0" + Ye0 + "_T0_" + T0 + "_rho0_" + rho0

            # デフォルトを開く
            rjava.opdf()
            time.sleep(10)

            # filenameで上書き保存
            rjava.saveas(filename)
            rjava.yesbotton()

            # NSEを開き、条件を入力
            rjava.NSE(T0, rho0, "0." + Ye0)

            # 計算ボタンを押し、NSEでの分布を表示
            rjava.calculate()
            time.sleep(5)
            rjava.Replot()

            # screenshotを撮り、保存
            screenshot = pyautogui.screenshot()
            path_pic_NSE = "../進捗/0916to0924/sample/pic/NSE_"+ filename + ".png"
            screenshot.save(path_pic_NSE)
            
            # Dataモジュールを開き、NSEでの分布をtxtdataとして保存
            rjava.Data()
            txtdata_NSE = "NSE_" + filename + ".txt"
            rjava.DtSv(txtdata_NSE)

            # テキストデータをこのpythonで開く
            path_open_NSE = "../進捗/0916to0924/sample/data/" + txtdata_NSE
            with open(path_open_NSE) as f:
                line = f.readlines()
            print(line[1]) # txtdataの1行目「水素1」のデータを表示
            element, Z, A, N, mass, solarMF, MF,InitialMF = line[1].split( ) # 「水素１」のdataを分割して読み込む
            
            #水素1のMFがNaNであれば計算終了
            if MF == "NaN":
                rjava.save()
                time.sleep(10)

            # NaNでないならr-processを計算する。
            else:
                # グラフを表示し、NSEの計算結果をInitialMFに設定。
                rjava.graph2()
                rjava.setInital()
                time.sleep(2)

                # r-processの計算条件を入力し、実行
                rjava.rprocess(T0,rho0,update,PolyIndex,P0,Vexp,R0)
                rjava.calculate()

                # 数秒後freezeout状態を保存
                time.sleep(10)
                txtdata_freezeout = "freezeout_" + filename + ".txt"
                rjava.Replot()
                screenshot = pyautogui.screenshot()
                path_pic_freezeout = "../進捗/0916to0924/sample/pic/freezeout_"+ filename + ".png"
                screenshot.save(path_pic_freezeout)
                rjava.Data()
                rjava.DtSv(txtdata_freezeout)

                # freezeout時のデータを表示
                path_open_freezeout = "../進捗/0916to0924/sample/data/" + txtdata_freezeout
                with open(path_open_freezeout) as f:
                    line = f.readlines()
                print(line[1])                
                element, Z, A, N, mass, solarMF, MF,InitialMF = line[1].split( )

                # NaNだったら計算終了
                if MF == "NaN":
                    rjava.save()
                    time.sleep(10)

                # NaN でなかったら計算続行
                else:   
                    time.sleep(600)

                    # ここに計算終了しているかのコードを描く
                    
                    cnt2 = 0
                    jouken = True
                    while (jouken):
                        # 0.何回目、保存名、保存場所
                        now = datetime.datetime.now()
                        print("time : %d, %d 回目" % time,cnt2)
                        txtdata_information = "InformationData_" + filename + "_cnt_" + str(cnt2) + ".txt"
                        path_information = "../進捗/0916to0924/sample/data/" + txtdata_information
                        
                        # 1.informationモジュールを開く
                        rjava.Information()
                    
                        # 2.全選択してtxtdataに保存
                        rjava.DtSv(txtdata_information)
                    
                        # 3.txtdata をpython で開き、読み込む
                        cnt_column = 0
                        with open(path_information) as g:
                            for column in g:
                                cnt_column += 1

                        with open(path_information) as f:
                            line = f.readlines()  
                        
                        # 4.Done が表示されるであろう行数を読み込み、Done があるかどうか判別する。
                        target = cnt_column - 4
                        if target < 0:
                            target = 0
                        print(line[target])

                        # 5.Done があれば計算終了
                            # 読み込みデータ数が7でなければDoneはない
                        a = line[target].split()
                        cnt10 = 0
                        for i in a:
                            cnt10 += 1
                            #読み込みデータ数が7であり、要素７が"DONE"なら終了
                        if cnt10 == 7:
                            hoge1, hoge2, hoge3, hoge4, hoge5, hoge6, hoge7 = a
                            print(hoge7)
                            if hoge7 == "DONE":
                                jouken = False
                            else:
                                cnt2 += 1
                                time.sleep(600)
                        
                        # 6.Done がなければ10分待って3.~4.以降を再度実行
                        else:
                            cnt2 += 1
                            time.sleep(600)

                    rjava.graph2()
                    rjava.Replot()
                    path_last = "../進捗/0916to0924/sample/pic/last_" + filename + ".png"
                    screenshot2 = pyautogui.screenshot()
                    screenshot2.save(path_last)
                    rjava.Data()# dataを開く
                    rjava.calstop()
                    txtdata_last = "last_" + filename + ".txt"
                    rjava.DtSv(txtdata_last)
                    rjava.save()
                    time.sleep(10)
