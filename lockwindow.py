#!/usr/bin/python
# -*- coding: UTF-8 -*-

import _thread
import time

import os,time,random
# 导入用户界面所需额外模块
try:
    import PySimpleGUI as sg
except:
    os.system('pip install pysimplegui')
    import PySimpleGUI as sg

import ctypes

# 导入屏幕快照所需额外模块
try:
    from PIL import ImageGrab
except:
    os.system('pip install pillow')
    from PIL import ImageGrab   

# 导入摄像头监测所需模块
try:
    import cv2
    import numpy as np
except:
    os.system('pip install opencv-python numpy')
    import cv2
    import numpy as np

# 制作动图所需模块
try:
    import imageio
except:
    os.system('pip install imageio')
    import imageio

import mitmproxy.http
from mitmproxy import flowfilter

from mitmproxy import ctx

def lockscreen_ui(log_height=6,input_height=1,force_mode=0,input_prompt='',**kw):
    '''
    定义用户界面
    '''
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    #screensize = (1920,1080)
    bk_color = "#222222"
    font_style = 'Helvetica'
    font_size = 120
    log_font = ("Calibri",14)
    log_width = 60
    
    
    timer = sg.Text("",
                            font=('Helvetica', font_size),
                            key='_OUTPUT_',
                            background_color=bk_color,
                            size=(10,1),
                            text_color="#fafafa")
    
    up_padding = sg.Text("",font=(font_style,60),justification="center",background_color=bk_color)
    
    #left_padding = sg.Text("",size=(16,45),font=log_font,justification="center",background_color="#1111ff")
    left_padding = sg.Text("",size=(16,45),font=log_font,justification="center",background_color=bk_color)
    # right_padding = sg.Text("",size=(20,1),font=log_font,justification="center",background_color="#fafafa")
    # left_padding = sg.Image('left-padding.png',background_color="#ffffff",size=(screensize[0]*0.1,screensize[1]))
    # right_padding = sg.Image('left-padding.png',background_color="#ffffff",size=(screensize[0]*0.1,screensize[1]))
    
    btn_quit = sg.Quit(button_color=('black', 'orange'),disabled=(force_mode>0))

    column = [[timer]]

    layout = [[left_padding,sg.Column(column,background_color=bk_color)]]
    window = sg.Window('Stand Up And Drink Water',
                        layout, 
                        no_titlebar=True, 
                        keep_on_top=True, 
                        disable_close=True, 
                        disable_minimize=True,
                        grab_anywhere=False,
                        background_color=bk_color,
                        alpha_channel=1,
                        transparent_color="#1111ff",
                        size=screensize
                        )
    return window    

def fmt(sc):
    sc += 0.5
    t = str(sc)
    i = t.find('.')
    if i==-1:
        return t
    else:
        return t[0:i]

def startup():
    os.system("displayswitch /internal")
    time_tag = time.strftime("%Y-%m-%d", time.localtime())
    window = lockscreen_ui(force_mode=1,input_prompt='请输入今天的计划')
    title = "专注 "
    stime = time.time()
    gap = 0
    while gap<=180:
        gap = time.time()-stime
        event, values = window.Read(timeout=100)
        window['_OUTPUT_'].update(title+fmt((180-gap))+" 秒\n\n")
    window.Close()
    os.system("displayswitch /extend")

startup()
