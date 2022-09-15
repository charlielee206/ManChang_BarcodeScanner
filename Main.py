import tkinter as tk
import os
import time

import tkinter as tk

GlobalText = "HellOwO!"

class Test():
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen' , True)
        self.root.geometry("1600x900")
        #self.root.configure(background = '#202124')
        self.root.configure(background = 'black')

        self.lbl_Title = tk.Label(self.root, font=("Consolas",8), 
        text = "          _____                    _____                            _____                            _____                            _____                            _____                        _____           \n         /\    \                  /\    \                          /\    \                          /\    \                          /\    \                          /\    \                      /\    \          \n        /::\____\                /::\    \                        /::\    \                        /::\____\                        /::\    \                        /::\____\                    /::\    \         \n       /:::/    /                \:::\    \                      /::::\    \                      /::::|   |                       /::::\    \                      /::::|   |                    \:::\    \       \n      /:::/    /                  \:::\    \                    /::::::\    \                    /:::::|   |                      /::::::\    \                    /:::::|   |                     \:::\    \       \n     /:::/    /                    \:::\    \                  /:::/\:::\    \                  /::::::|   |                     /:::/\:::\    \                  /::::::|   |                      \:::\    \      \n    /:::/    /                      \:::\    \                /:::/__\:::\    \                /:::/|::|   |                    /:::/  \:::\    \                /:::/|::|   |                       \:::\    \     \n   /:::/    /                       /::::\    \              /::::\   \:::\    \              /:::/ |::|   |                   /:::/    \:::\    \              /:::/ |::|   |                       /::::\    \    \n  /:::/    /               ____    /::::::\    \            /::::::\   \:::\    \            /:::/  |::|___|______            /:::/    / \:::\    \            /:::/  |::|___|______                /::::::\    \   \n /:::/    /               /\   \  /:::/\:::\    \          /:::/\:::\   \:::\ ___\          /:::/   |::::::::\    \          /:::/    /   \:::\ ___\          /:::/   |::::::::\    \              /:::/\:::\    \  \n/:::/____/               /::\   \/:::/  \:::\____\        /:::/__\:::\   \:::|    |        /:::/    |:::::::::\____\        /:::/____/  ___\:::|    |        /:::/    |:::::::::\____\            /:::/  \:::\____\ \n\:::\    \               \:::\  /:::/    \::/    /        \:::\   \:::\  /:::|____|        \::/    / ~~~~~/:::/    /        \:::\    \ /\  /:::|____|        \::/    / ~~~~~/:::/    /           /:::/    \::/    / \n \:::\    \               \:::\/:::/    / \/____/          \:::\   \:::\/:::/    /          \/____/      /:::/    /          \:::\    /::\ \::/    /          \/____/      /:::/    /           /:::/    / \/____/  \n  \:::\    \               \::::::/    /                    \:::\   \::::::/    /                       /:::/    /            \:::\   \:::\ \/____/                       /:::/    /           /:::/    /           \n   \:::\    \               \::::/____/                      \:::\   \::::/    /                       /:::/    /              \:::\   \:::\____\                        /:::/    /           /:::/    /            \n    \:::\    \               \:::\    \                       \:::\  /:::/    /                       /:::/    /                \:::\  /:::/    /                       /:::/    /            \::/    /             \n     \:::\    \               \:::\    \                       \:::\/:::/    /                       /:::/    /                  \:::\/:::/    /                       /:::/    /              \/____/              \n      \:::\    \               \:::\    \                       \::::::/    /                       /:::/    /                    \::::::/    /                       /:::/    /                                    \n       \:::\____\               \:::\____\                       \::::/    /                       /:::/    /                      \::::/    /                       /:::/    /                                     \n        \::/    /                \::/    /                        \::/____/                        \::/    /                        \::/____/                        \::/    /                                      \n         \/____/                  \/____/                          ~~                               \/____/                                                           \/____/                                       \n                                                                                                                                                                                                                   ",
        bg = 'black', fg = 'White')

        
        self.StatusText = tk.StringVar()
        self.StatusText.set("[System] Please Select a Function...")
        self.lbl_console = tk.Label(self.root, textvariable = self.StatusText, bg = 'black', fg = 'white', font = ("Consolas",15))

        
        self.ButtonFrame = tk.Frame(self.root, borderwidth = 2, background = 'black', padx = 5, pady = 10, )

        self.btn_Quit = tk.Button(self.ButtonFrame, text = "[Quit]", relief = "flat", font = ('Consolas',7),
                                 command = self.root.destroy, borderwidth = 0,bg = 'black', fg = 'white')
        #self.btn_Quit = tk.Button(self.ButtonFrame, text = "[Quit]", relief = "flat", font = ('Consolas',8),
         #                         command = self.QuitPassword, borderwidth = 0,bg = 'black', fg = 'white')

        self.btn_Borrow = tk.Button(self.ButtonFrame, text = "[Borrow]", relief = "flat", command = self.OpenBorrow,
                                    borderwidth = 0,bg = 'black',fg = 'white', font = ('Consolas',20))
        self.btn_Return = tk.Button(self.ButtonFrame, text = "[Return]", relief = "flat", command = self.OpenReturn,
                                    borderwidth = 0,bg = 'black',fg = 'white', font = ('Consolas',20))

        
        #self.btn_Borrow.grid(row = 0, column = 2)
        #self.btn_Quit.grid(row = 0, column = 1)
        #self.btn_Return.grid(row = 0, column = 0)
        self.btn_Borrow.pack(pady = 5)
        self.btn_Return.pack(pady = 5)
        self.btn_Quit.pack(pady = 120) # Comment this line to remove Quit button
        


        self.text = tk.StringVar()
        self.text.set("Original Text")

        #self.ButtonFrame.grid(row = 1, column = 1, padx = 400, pady = 50)
        #self.lbl_Title.grid(row = 0, column = 1)
        
        self.lbl_Title.pack(side = 'top', pady = 20)
        self.lbl_console.pack(pady = 20)
        self.ButtonFrame.pack(pady = 20)

        self.root.update()
        self.root.mainloop()     

    def OpenBorrow(self):
        #self.StatusText.set("[System] Please Wait...")
        self.StatusText.set("[System] Please Wait...")
        self.root.update()
        self.Borrow()
        self.StatusText.set("[System] Done!")
        self.root.update()
        time.sleep(1.0)
        self.StatusText.set("[System] Please Select a Function...")
        self.root.update()

    def Borrow(self):
        os.system("python3 IDScanner_GUI.py")

    def OpenReturn(self):
        self.StatusText.set("[System] Please Wait...")
        self.root.update()
        os.system("python3 ReturnScanner_GUI.py")
        self.StatusText.set("[System] Return Done!")
        self.root.update()
        time.sleep(2.0)
        self.StatusText.set("[System] Please Select a Function...")
        self.root.update()

    def QuitPassword(self):
        self.LogInPage = tk.Tk()
        self.LogInPage.title("Admin Password")
        self.LogInPage.mainloop()


app=Test()


