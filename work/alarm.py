#-*- coding=utf-8 -*-
from tkinter import *
import datetime
import tkinter.font as tkf
import wave
import sys
import os
import time
import pygame
import playsound

import getCurrentTime

import threading #for multi-threading

hour = ""
minute = ""

j=0
i=100
dateList=[0 for i in range(100)]
date1=[0 for i in range(100)]
date2=[0 for i in range(100)]
alarmFlag=0

getCurrentTime.TaskCurrentTime()

root = Tk()

root.configure(background='white')

root.title("MAV")
root.geometry("400x500+200+150")
root.resizable(False, False)

list_font=tkf.Font(size=18,weight='bold')
listbox = Listbox(root,activestyle='none',relief='ridge',
                  bd=5, width=26, height=13,
                  selectbackground='seagreen1',selectforeground='white',
                  font=list_font)
listbox.place(x= 20,y= 70)

def new_alarm():
    print("new_alarm")
    
    new = Tk()
    
    new.geometry("320x200+220+170")
    new.resizable(False,False)
    new.title("Alarm")
    new.configure(bg='white')
    
    l1=Label(new,text="시",bg="white")
    l1.place(x=20,y=35)
    e1=Entry(new,width=8)
    e1.place(x=100,y=35)
    
    l2=Label(new,text="분",bg="white")
    l2.place(x=20,y=60)
    e2=Entry(new,width=8)
    e2.place(x=100,y=60)
    
    l3=Label(new,text="일정",bg="white")
    l3.place(x=20,y=85)
    e3=Entry(new,width=24)
    e3.place(x=100,y=85)

    def mkdate():
        print("mkdate")
        
        global j
        global i
    
        dateList_str=e3.get()
        date1_Hour=e1.get()
        date1_Minute=e2.get()
        dateList[j]=str(dateList_str)
        date1[j]=int(date1_Hour)
        date2[j]=int(date1_Minute)
        listbox.insert(j,str(date1[j])+"시  "+str(date2[j])+"분 : "+
                       dateList[j])
    
        os.system('py synthesizer.py --load_path logs/son --text="%s"'
                  % dateList[j])\
                  
        j=j+1
        i=i+25
        e2.delete(0,END)
        e1.delete(0,END)
        e3.delete(0,END)
        
   # def onClick():
       #t = threading.Thread(name='thread1', target=mkdate)
      #  t.start();

    btn_save = Button(new, text='저장', command=mkdate,
                      bd=1, anchor='center', bg='seagreen3',
                      fg='white', relief='ridge',overrelief='groove')    
    btn_save.place(x=250,y=150)

def alarm_On(number):
    print("alarm_On")
     
    file_path='C:/Users/Rich/Downloads/tacotron/samples/alarm'+str(number+1)+'.manual.wav'
    file_wav=wave.open(file_path)
    frequency = file_wav.getframerate()
    pygame.mixer.init(frequency=frequency)
    pygame.mixer.music.load(file_path)

    pygame.mixer.music.play()
    
def alarm_Off():
    print("alarm_Off")
    
    pygame.mixer.music.stop()



def CheckTime():
    print("CheckTime")
    
    global alarmFlag
    timer=threading.Timer(3,CheckTime)
    timer.start()

    
    realTime_Hour=getCurrentTime.hour
    realTime_Minute=getCurrentTime.minute

    
    if(alarmFlag == 0):
        print("알람음 종료합니다.")
        alarm_Off()
                
    for i in range(0,100):
        if(realTime_Hour==date1[i] and realTime_Minute==date2[i] and alarmFlag==1):
            timer.cancel()
            print(alarmFlag)
            for k in range(0,3):
                alarm_On(i)
                time.sleep(3)



def main():
    print("main")
    
    myAlarm=MyAlarm()

    main_label = Label(root, text="tacotron alarm",bg='white')
    main_label.place(x=20, y= 20)
                       
    icon_font=tkf.Font(size=13,weight='bold')
    plus_button = Button(root, text='+',bd=1, anchor='center',
                            bg='seagreen1',fg='white', command = new_alarm,
                            relief='ridge',overrelief='groove',
                            width=2,font=icon_font, )
    plus_button.place(x=340,y=40)
    on_button = Button(root, text='ON',bd=1, anchor='center',
                            bg='seagreen1',fg='white', command=myAlarm.alarmSet,
                            relief='ridge',overrelief='groove',
                            width=2,font=icon_font, )
    on_button.place(x=280,y=40)
    off_button = Button(root, text='Off',bd=1, anchor='center',
                            bg='seagreen1',fg='white', command=myAlarm.alarmReset,
                            relief='ridge',overrelief='groove',
                            width=2,font=icon_font, )
    off_button.place(x=310,y=40)


    root.mainloop()

        
class MyAlarm:
    def __init__(self):
        print("Alarm__init__")
        pass
    def alarmSet(self):
        print("Alarm On")
        global alarmFlag
        alarmFlag =1
        CheckTime()
    def alarmReset(self):
        print("Alarm Off")
        global alarmFlag
        alarmFlag=0
        CheckTime()


        
if __name__ == '__main__':
    main()
