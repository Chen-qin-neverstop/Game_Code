from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import pygame
from pygame.examples.cursors import image
from pygame.locals import *
from awthemes import AwthemesStyle
from PIL import Image,ImageTk

'''
Pygame 和 tkinter创建窗口的机制不同，会有窗口所有权冲突
所以单独用tkinter做独立窗口，用于提示信息
'''

def quit():
    d1 = messagebox.askokcancel("退出","确定关闭吗")
    if d1:
        pygame.quit()
    else: pass


def create_windows(img_path):
    global root
    root = tk.Tk()
    a2 = root.maxsize()
    k, g = a2
    l = int(k * 0.3)
    h = int(g * 0.3)
    root.geometry(f'{l}x{h}+{int(l*1.25)}+{int(h*1.25)}')
    root.title('恭喜！')
    root.resizable(False, False)
    root.iconbitmap('tkinter_renderer/DORO.ico')

    style = AwthemesStyle(root)
    style.theme_use("awclearlooks")

    # Load and resize the image
    photo1 = Image.open(img_path)
    photo1_new = photo1.resize((int(l * 0.85), int(h * 0.85)))
    photo1_use = ImageTk.PhotoImage(photo1_new)

    # Store the image reference properly
    label1 = tk.Label(root, image=photo1_use)
    label1.image = photo1_use  # 保持引用
    label1.pack()

    Button1 = ttk.Button(root, text='返回', command=new_start, width=10)
    Button1.place(x=l * 0.22, y=h * 0.89)
    Button2 = ttk.Button(root, text='退出', command=quit, width=10)
    Button2.place(x=l * 0.55, y=h * 0.89)

    root.mainloop()

def new_start():
    global root
    root.destroy()
    from main import MainMenu  # 仅在函数内部需要时导入
    menu = MainMenu()  # 重新回到主页面
    menu.run()
    root = tk.Tk()
def quit():
    root.destroy()
    pygame.quit()




