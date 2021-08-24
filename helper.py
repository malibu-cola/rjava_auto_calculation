import pyautogui
import pyperclip

class rjava:
    def desk(self):
        # Desktopに移動
        pyautogui.moveTo(45,40,1)
        pyautogui.click()

    def newfile(self):
        # 新しいファイルを作成        
        pyautogui.moveTo(100,400,2)
        pyautogui.click()

    def GraphButton(self):
        # グラフボタンを押す
        pyautogui.moveTo(400,400)
        pyautogui.click()

    def calculate(self):
        # calculateボタンを押す
        pyautogui.moveTo(60,40)
        pyautogui.click()

    def 

    def NSE(T0,rho0,Ye0):
        # codeボタンを押しNSE設定画面を開く
        pyautogui.moveTo(1800,200)
        pyautogui.click()
        pyautogui.moveTo(1800,230)
        pyautogui.click()

        # NSEの初期条件を代入
        # T0
        pyautogui.moveTo(1800,240)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy("1e11") # T0の値
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        # rho0
        pyautogui.moveTo(1800,260)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy("1e11") # rho0の値
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        # Ye0
        pyautogui.moveTo(1800,280)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy("0.2") # Ye0の値
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')


        #set initial MF
        pyautogui.moveTo(1800,326)
        pyautogui.click()
        pyautogui.moveTo(1610,635)
        pyautogui.click()

    def rprocess(self):
        # Type をr-processに変更
        pyautogui.moveTo(1800,200)
        pyautogui.click()
        pyautogui.moveTo(1800,250)
        pyautogui.click()

        # r-processの設定を変更
        # Environment を NSM に
        pyautogui.moveTo(1800,280)
        pyautogui.click()
        pyautogui.moveTo(1800,340)
        pyautogui.click()

        # T0
        pyautogui.moveTo(1800,305)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy("1e9") # T0の値
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        # rho0
        pyautogui.moveTo(1800,325)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy("1e10") # rho0の値
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        #Polytropic Index
        pyautogui.moveTo(1800,580)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy("1") # T0の値
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        #Polytropic Index
        pyautogui.moveTo(1800,580)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy("1") # PI0の値
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        # P0
        pyautogui.moveTo(1800,600)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy("1e-4") # P0の値
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        # Vexp
        pyautogui.moveTo(1800,620)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy("1e4") # Vexp0の値
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

        # R0
        pyautogui.moveTo(1800,645)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy("2") # R0の値
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')

