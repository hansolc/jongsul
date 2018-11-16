#-*- coding=utf-8 -*-
from tkinter import *
from playsound import playsound
import threading   
import wave
import pygame
#import getCurrentTime
import sys
import os
import time

#for server
import socket

#server ip, port
HOST = '220.149.236.92'
PORT = 9999


j=0
i=100
dateList=[0 for i in range(100)]
date1=[0 for i in range(100)]
date2=[0 for i in range(100)]
window=Tk()
#getCurrentTime.TaskCurrentTime()
alarmFlag=0
window.geometry("1000x1000")


window.title("My Artificial Voice")
Label(window,text="시를 입력하세요(ex: 오후 5시= 17)",bg="white",width=30).place(x=20,y=75)
e1=Entry(window,width=8)
e1.place(x=260,y=75)
Label(window,text="분을 입력하세요(ex: 38 분 = 38)",bg="white",width=30).place(x=20,y=100)
e2=Entry(window,width=8)
e2.place(x=260,y=100)
Label(window,text="일정",bg="white",width=10).place(x=20,y=125)
e3=Entry(window,width=31)
e3.place(x=100,y=125)


def mkdate():
    global j
    global i
    dateList_str=e3.get()
    date1_Hour=e1.get()
    date1_Minute=e2.get()
    dateList[j]=str(dateList_str)
    date1[j]=int(date1_Hour)
    date2[j]=int(date1_Minute)
    Label(window,text=str(date1[j])+"시  "+str(date2[j])+"분",bg="white",width=20).place(x=600,y=i)
    Label(window,text=dateList[j],bg="white",width=20).place(x=800,y=i)
   
    #os.system('sudo python3 synthesizer.py --load_path logs/son_2018-10-26_21-17-45 --text="%s"' % dateList[j]) 

	### checking server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST,PORT))
        sock.sendall(dateList[j].encode())

        data = sock.recv(1024)
        if not data:
            print("서버 오류 혹은 파일이 생성되지 않음")
            return

        with open('myexs/' + 'check.txt', 'wb') as f:
            try:
                while data:
                    f.write(data)
                    data_transferred += len(data)
                data = sock.recv(1024)
            except Exception as e:
                    print(e)

    print('전송성공 확인 ㄱㄱ')
            
    j=j+1
    i=i+25
    e2.delete(0,END)
    e1.delete(0,END)
    e3.delete(0,END)

def alarm_On(number):
    file_path='C:/Users/Rich/Downloads/tacotron/samples/alarm'+str(number+1)+'.manual.wav'
    file_wav=wave.open(file_path)
    frequency = file_wav.getframerate()
    pygame.mixer.init(frequency=frequency)
    pygame.mixer.music.load(file_path)

    pygame.mixer.music.play()

def alarm_Off():
    pygame.mixer.music.stop()
   

def CheckTime():
    global alarmFlag
    timer=threading.Timer(3,CheckTime)
    timer.start()

    realTime_Hour=getCurrentTime.hour
    realTime_Minute=getCurrentTime.minute
   
    for i in range(0,100):
        if(realTime_Hour==date1[i] and realTime_Minute==date2[i] and alarmFlag==1):
            timer.cancel()
            print(alarmFlag)
            alarm_On(i)

class MyAlarm:
    def __init__(self):
        pass
    def alarmSet(self):
        global alarmFlag
        alarmFlag =1
        CheckTime()
    def alarmReset(self):
        global alarmFlag
       
        alarmFlag=0
        CheckTime()



b1=Button(window,text="저장",command=mkdate)
b1.place(x=360,y=150)


myAlarm=MyAlarm()
btn_On = Button(window, text="알람설정", command=myAlarm.alarmSet)
btn_On.place(x=340,y=200)
btn_Off = Button(window, text="알람해제", command=myAlarm.alarmReset)
btn_Off.place(x=440,y=200)
window.mainloop()
