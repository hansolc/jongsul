import sys
import os
from tkinter import *

#import tkMessageBox

root = Tk()

def helloCallBack():
	os.system('sudo python3 ../multi-speaker-tacotron-tensorflow/synthesizer.py --text="%s"' % e1.get())

Label(root, text="Insert text").grid(row=0)

e1 = Entry(root)

e1.grid(row=0, column=1)

Button(root, text="hello", command=helloCallBack).grid(row=0, column=2, sticky=W, pady=4)

root.mainloop()
