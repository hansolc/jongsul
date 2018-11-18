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

j=0
i=100
dateList=[0 for i in range(100)]
date1=[0 for i in range(100)]
date2=[0 for i in range(100)]
btn_on=[0 for i in range(100)]
btn_off=[0 for i in range(100)]
result_data=[0 for i in range(100)]
alarmFlag=[0 for i in range(100)]

getCurrentTime.TaskCurrentTime()

root = Tk()

root.configure(background='white')

root.title("MAV")
root.geometry("400x500+200+150")
root.resizable(False, False)

list_font=tkf.Font(size=18,weight='bold')
listbox = Listbox(root,activestyle='none',relief='ridge',
                  bd=5, width=22, height=13,
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

        icon_font=tkf.Font(size=13,weight='bold')
        btn_on[j] = Button(root, text='ON',bd=1, anchor='center',
                          bg='seagreen1',fg='white', command=alarm_able(j),
                          relief='ridge',overrelief='groove',
                          width=2,font=icon_font, )
        btn_on[j].place(x=320,y=75+(j*31))
        btn_off[j] = Button(root, text='Off',bd=1, anchor='center',
                           bg='seagreen1',fg='white', command=alarm_disable(j),
                           relief='ridge',overrelief='groove',
                           width=2,font=icon_font, )
        btn_off[j].place(x=350,y=75+(j*31))
            
        result_data[j]=(str(date1[j])+ "시 " + str(date2[j])+"분 입니다."
                        + dateList[j] + "있습니다")
        os.system('py synthesizer.py --load_path logs/son --text="%s"'
                  % result_data[j])\
                  
        j=j+1
        i=i+25

        
        e2.delete(0,END)
        e1.delete(0,END)
        e3.delete(0,END)

    def onClick():
        print("Click")
        t = threading.Thread(name='thread1', target=mkdate)
        t.start();
        
    btn_save = Button(new, text='저장', command=onClick,
                      bd=1, anchor='center', bg='seagreen3',
                      fg='white', relief='ridge',overrelief='groove')    
    btn_save.place(x=250,y=150)
    new.mainloop()

def alarm_On(number):
    print("alarm_On")
     
    file_path='C:/Users/Rich/Downloads/tacotron/samples/alarm'+str(number+1)+'.manual.wav'
    file_wav=wave.open(file_path)
    frequency = file_wav.getframerate()
    pygame.mixer.init(frequency=frequency)
    pygame.mixer.music.load(file_path)

    pygame.mixer.music.play()

    messagebox.showinfo("알람",dateList(number))
    mb=messagebox.askyesno("알람","알람을 종료하시겠습니까?",icon='warning')

    if mb==True:
        alarm_Off()
    else:
        True
    
def alarm_Off():
    print("alarm_Off")
    
    pygame.mixer.music.stop()



def CheckTime():
    print("CheckTime")
    
    timer=threading.Timer(3,CheckTime)
    timer.start()

    
    realTime_Hour=getCurrentTime.hour
    realTime_Minute=getCurrentTime.minute

    
    for i in range(0,100):
        if(realTime_Hour==date1[i] and realTime_Minute==date2[i] and alarmFlag[i]==1 ):
            timer.cancel()
            for k in range(0,3):
                alarm_On(i)
                time.sleep(3)

                
def alarm_able(number):
     print("on")
     alarmFlag[number] =1
def alarm_disable(number):
     print("off")
     alarmFlag[number]=0

def main():
    print("main")

    CheckTime()

    
    now = datetime.datetime.now()
    today = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    main_label = Label(root, text="tacotron alarm",bg='white')
    main_label.place(x=20, y= 20)
    time_label = Label(root, text=today,bg='white')
    time_label.place(x=20, y= 40)
                       
    icon_font=tkf.Font(size=13,weight='bold')
    plus_button = Button(root, text='+',bd=1, anchor='center',
                            bg='seagreen1',fg='white', command = new_alarm,
                            relief='ridge',overrelief='groove',
                            width=2,font=icon_font, )
    plus_button.place(x=290,y=40)


    root.mainloop()
    


        
if __name__ == '__main__':
    main()
