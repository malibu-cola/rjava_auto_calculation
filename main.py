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


# 初期化の仕方
# r-javaをデフォルトの状態、デフォルトのディレクトリで開いておく
# またテキストファイルも同様にデフォルトで開いてい置く
# DataモジュールのdisplayをGeneralDataだけにしておく

#----------------------------------------------------
#計算条件
update = "500"
PolyIndex = "1"
P0 = "1e-4"
Vexp = "1e4"
R0 = "2"
# --------------------------------------------------
# 初期条件
vYe0_0 = ["23","26","29", "30", "01","03","06","16"]# 12こ
        #["09","10", "13", "19","20",] 終了したYe

vT0_9 = ["7e11", "4e9", "7e9",\
    "7e10", "1e11", "4e11",  "1e12",\
     "1e10", "4e10"] # 10こ

vrho0_10 = ["1e12", "4e12", "7e12",\
    "1e11", "4e11", "7e11",\
            "4e13","1e10","4e10", "7e10",\
            "1e13"] # 11こ

# ----------------------------------------------------
# データを保存するディレクトリ
today_Path = "../progress/1025to1101/run1"
data_Path = today_Path + "/data"
pic_Path = today_Path + "/pic"

# ----------------------------------------------------
# 計算何回目か
cnt = 0

# ---------------------------------------------------
# 計算開始
for Ye0 in vYe0_0:
    for T0 in vT0_9:
        for rho0 in vrho0_10:
            #---------------------------------------------------
            # 現在の時刻を表示
            now = datetime.datetime.now()
            print(now)
            
            # --------------------------------------------------
            # 何回目、初期条件を表示
            print(cnt, "回目, Ye0:", Ye0,"  T0:", T0,"rho0",rho0)
            cnt+=1 #何回目か

            # -------------------------------------------------
            # 飛ばす項目
            if Ye0 == "19" and T0 == "7e11" and rho0 == "4e13":
                print("計算不能なので飛ばすよ。")
                continue
            if Ye0 == "19" and T0 == "7e11" and rho0 == "7e11":
                print("計算不能なので飛ばすよ。")
                continue
            if Ye0 == "20" and T0 == "4e9" and rho0 == "4e12":
                print("計算不能なので飛ばすよ。")
                continue
            
            # --------------------------------------------------
            # 保存するファイルの名前
            filename = "Ye_0" + Ye0 + "_T0_" + T0 + "_rho0_" + rho0

            # --------------------------------------------------
            # rjavaの動作
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

            # ------------------------------------------------
            # screenshotを撮り、保存
            screenshot = pyautogui.screenshot()
            path_pic_NSE = pic_Path + "/NSE_"+ filename + ".png"
            screenshot.save(path_pic_NSE)
            
            # ------------------------------------------------
            # rjavaの動作
            # Dataモジュールを開き、NSEでの分布をtxtdataとして保存
            rjava.Data()
            txtdata_NSE = "NSE_" + filename + ".txt"
            rjava.DtSv(txtdata_NSE)

            # -----------------------------------------------------------------
            # テキストデータをこのpythonで開き,水素1がNaNであれば次の計算条件に移行
            # Pathを指定し開く。
            path_open_NSE = data_Path + "/" + txtdata_NSE
            with open(path_open_NSE) as f:
                line = f.readlines()
            print(line[1]) # txtdataの1行目「水素1」のデータを表示
            element, Z, A, N, mass, solarMF, MF,InitialMF = line[1].split( ) # 「水素１」のdataを分割して読み込む
            
            #水素1のMFがNaNであれば計算終了
            if MF == "NaN":
                rjava.save()
                time.sleep(10)

            # -------------------------------------------------------------------
            # NaNでないならr-processを計算する
            else:
                # ---------------------------------------------------------------
                # rjavaの動作
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
                path_pic_freezeout = pic_Path + "/freezeout_"+ filename + ".png"
                screenshot.save(path_pic_freezeout)
                rjava.Data()
                rjava.DtSv(txtdata_freezeout)

                # ----------------------------------------------------------------
                # freezeout時のデータを表示
                path_open_freezeout = data_Path + "/" + txtdata_freezeout
                with open(path_open_freezeout) as f:
                    line = f.readlines()
                print(line[1])                
                element, Z, A, N, mass, solarMF, MF,InitialMF = line[1].split( )

                # NaNだったら計算終了
                if MF == "NaN":
                    rjava.save()
                    time.sleep(10)

                # ----------------------------------------------------------------
                # NaN でなかったら計算続行
                else:   
                    # ------------------------------------------------------------
                    # rjavaの動作
                    # 計算終了するまで待つ。
                    time.sleep(600)

                    cnt2 = 0 # rjavaシミュレーションが終わるまでの待つ時間 = 600sec + cnt2
                    jouken = True 
                    # jouken = falseになる or cnt2 == 100 (17時間程度)経ったら、計算終了
                    while (jouken and cnt2 <= 100):
                        # -------------------------------------------------------------------
                        # 0.何回目、保存名、保存場所
                        now = datetime.datetime.now()
                        print(now)
                        print("%d 回目" % cnt2)
                        txtdata_information = "InformationData_" + filename + "_cnt_" + str(cnt2) + ".txt"
                        path_information = data_Path + "/" + txtdata_information
                        
                        # ------------------------------------------------------------------
                        # rjavaの動作。
                        # 1.informationモジュールを開く
                        rjava.Information()
                    
                        # 2.全選択してtxtdataに保存
                        rjava.DtSv(txtdata_information)
                    
                        # --------------------------------------------------------------------
                        # 3.txtdata を python で開き、読み込む
                        cnt_column = 0 # 読み込む行数
                        with open(path_information) as g:
                            for column in g:
                                cnt_column += 1

                        with open(path_information) as f:
                            line = f.readlines()  
                        
                        # 4.Done が表示されるであろう行数を読み込み、Done があるかどうか判別する。
                        target1 = cnt_column - 1
                        target2 = cnt_column - 2
                        target3 = cnt_column - 3
                        target4 = cnt_column - 4
                        
                        if target1 < 0:
                            target1 = 0
                        print(line[target1])
                        if target2 < 0:
                            target2 = 0
                        print(line[target2])
                        if target3 < 0:
                            target3 = 0
                        print(line[target3])
                        if target4 < 0:
                            target4 = 0
                        print(line[target4])
                        
                        # -----------------------------------------------------------------------
                        # 5.Done があれば計算終了
                        # 読み込みデータ数が7でなければDoneはない
                        a1 = line[target1]
                        a2 = line[target2]
                        a3 = line[target3]
                        a4 = line[target4]
                        
                        result1 = 'DONE' in a1
                        result2 = 'DONE' in a2
                        result3 = 'DONE' in a3
                        result4 = 'DONE' in a4

                        if result1 or result2 or result3 or result4:
                            jouken = False
                        # -------------------------------------------------------------------------    
                        # 6.Done がなければ10分待って3.~4.以降を再度実行
                        else:
                            cnt2 += 1
                            time.sleep(600)
                    
                    # --------------------------------------------------------------------------------
                    # rjavaの動作
                    # 計算終了したらグラフを開き、スクリーンショットを撮る。 
                    rjava.graph2()
                    rjava.Replot()
                    path_last = pic_Path + "/last_" + filename + ".png"
                    screenshot2 = pyautogui.screenshot()
                    screenshot2.save(path_last)

                    # (計算終了していなくても計算ストップし)最終的なデータを保存する。
                    rjava.Data()# dataを開く
                    rjava.calstop()
                    txtdata_last = "last_" + filename + ".txt"
                    rjava.DtSv(txtdata_last)
                    rjava.save()
                    time.sleep(10)
                    # ----------------------------------------------------------------------------------
                    # 次の計算に移行。
