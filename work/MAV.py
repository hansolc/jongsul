#-*- coding=utf-8 -*-
from tkinter import *
from tkinter import messagebox

import tkinter.ttk as ttk
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

import socket

HOST = '192.168.219.101'
PORT = 9999
alarm_num = 1

count=0
dateList=[0 for i in range(100)]
date1=[0 for i in range(100)]
date2=[0 for i in range(100)]
btn_on=[0 for i in range(100)]
btn_off=[0 for i in range(100)]
result_data=[0 for i in range(100)]
alarmFlag=[0 for i in range(100)]
num = 0

getCurrentTime.TaskCurrentTime()

root = Tk()

root.configure(background='cadetblue')
root.title("MAV")
root.geometry("400x500+200+150")
root.resizable(False, False)

list_font=tkf.Font(size=18,weight='bold')
listbox = Listbox(root,activestyle='none',relief='ridge',
                  bd=5, width=22, height=13,bg='cadetblue',fg='white',
                  selectbackground='cadetblue',selectforeground='white',
                  font=list_font)
listbox.place(x= 20,y= 70)


def new_alarm():
    print("new_alarm")
    
    new = Tk()
    
    new.geometry("320x200+220+170")
    new.resizable(False,False)
    new.title("Alarm")
    new.configure(bg='cadetblue')

    hour_val=[str(i) for i in range(0,24)]
    min_val=[str(i) for i in range(0,60)]
    
    l1=Label(new,text="시",bg="cadetblue",fg="white")
    l1.place(x=20,y=35)
    e1=ttk.Combobox(new,width=8,height=8, values=hour_val)
    e1.place(x=100,y=35)
    
    l2=Label(new,text="분",bg="cadetblue",fg="white")
    l2.place(x=20,y=60)
    e2=ttk.Combobox(new,width=8,height=8, values=min_val)
    e2.place(x=100,y=60)
    
    l3=Label(new,text="일정",bg="cadetblue",fg="white")
    l3.place(x=20,y=85)
    e3=Entry(new,width=24)
    e3.place(x=100,y=85)

    def mkdate():
        print("mkdate")
        
        global count
        global num
        global alarm_num
        
        num = count
        
        dateList_str=e3.get()
        date1_Hour=e1.get()
        date1_Minute=e2.get()
        dateList[num]=str(dateList_str)
        date1[num]=int(date1_Hour)
        date2[num]=int(date1_Minute)
        listbox.insert(num,str(date1[num])+"시  "+str(date2[num])+"분 : "+
                       dateList[num])
        
        icon_font=tkf.Font(size=13,weight='bold')
        
        for i in range(0,99):
            if i==num:
                x= i
                btn_on[x] = Button(root, text='ON',bd=1, anchor='center',
                                  bg='cadetblue',fg='white', command=lambda:alarm_able(x),
                                  relief='ridge',overrelief='groove',
                                  width=2,font=icon_font )
                btn_on[x].place(x=320,y=75+(x*31))
                btn_off[x] = Button(root, text='Off',bd=1, anchor='center',
                                   bg='cadetblue',fg='white', command=lambda:alarm_disable(x),
                                   relief='ridge',overrelief='groove',
                                   width=2,font=icon_font)
                btn_off[x].place(x=350,y=75+(x*31))
                
        result_data[num]=(str(date1[num])+ "시 " + str(date2[num])+"분 입니다."
                        + dateList[num] + "있습니다")


        count= num+1
        
        e2.delete(0,END)
        e1.delete(0,END)
        e3.delete(0,END)
        
        
        
        #os.system('py synthesizer.py --load_path logs/son --text="%s"'
        #          % result_data[num])

        #client server
        
        data_transferred = 0
        filename = result_data[num]
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST,PORT))
            sock.sendall(filename.encode())

            data = sock.recv(1024)
            if not data:
                print('파일[%s]: 서버에 존재하지 않거나 전송중 오류 발생' % filename)
                return

            with open('C:/Users/Rich/Downloads/tacotron/samples/alarm'+str(alarm_num)+'.manual.wav', 'wb') as f:
                try:
                    while data:
                        f.write(data)
                        data_transferred += len(data)
                        data = sock.recv(1024)
                except Exception as e:
                    print(e)
        print('파일[%s] 전송종료. 전송량 [%d]' %(filename, data_transferred))
        alarm_num = alarm_num + 1
        


    def onClick():
        print("Click")
        t = threading.Thread(name='thread1', target=mkdate)
        t.start();
        
    btn_save = Button(new, text='저장', command=onClick,
                      bd=1, anchor='center', bg='cadetblue',
                      fg='white', relief='ridge',overrelief='groove')    
    btn_save.place(x=250,y=150)
    new.mainloop()

def alarm_On(number):
    print("alarm_On")


    for k in range(0,3):
        print("show!")
        file_path='C:/Users/Rich/Downloads/tacotron/samples/alarm'+str(number+1)+'.manual.wav'
        file_wav=wave.open(file_path)
        frequency = file_wav.getframerate()
        pygame.mixer.init(frequency=frequency)
        pygame.mixer.music.load(file_path)
        print("play!")
        pygame.mixer.music.play()
        mb=messagebox.askyesno("알람",str(date1[number])+ "시 "
                               + str(date2[number])+"분 입니다. 일정 : "
                               + dateList[number])
        if mb==True:
            alarm_Off()
            break
        time.sleep(5)
        if k==2:
            alarm_Off()


def alarm_Off():
    print("alarm_Off")
    
    pygame.mixer.music.stop()

    time.sleep(50)
    
    CheckTime()



def CheckTime():
    print("CheckTime")
    
    timer=threading.Timer(3,CheckTime)
    timer.start()

    
    realTime_Hour=getCurrentTime.hour
    realTime_Minute=getCurrentTime.minute

    
    for n in range(0,100):
        if(realTime_Hour==date1[n] and realTime_Minute==date2[n] and alarmFlag[n]==1 ):
            timer.cancel()
            alarm_On(n)
                

                
def alarm_able(number):
     print("on"+str(number))
     alarmFlag[number] =1
def alarm_disable(number):
     print("off"+str(number))
     alarmFlag[number] =0

def main():
    print("main")

    CheckTime()

    
    now = datetime.datetime.now()
    photo = PhotoImage(file="alarm.png")
    icon_label = Label(root, image=photo, bg='cadetblue')
    icon_label.photo = photo
    icon_label.place(x=20, y= 10)
    
    today = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    time_label = Label(root, text=today,bg='cadetblue',fg='white')
    time_label.place(x=300, y= 475)
                       
    icon_font=tkf.Font(size=13,weight='bold')
    plus_button = Button(root, text='+',bd=1, anchor='center',
                            bg='cadetblue',fg='white', command = new_alarm,
                            relief='ridge',overrelief='groove',
                            width=3,height=1,font=icon_font, )
    plus_button.place(x=280,y=35)


    root.mainloop()
    


        
if __name__ == '__main__':
    main()
