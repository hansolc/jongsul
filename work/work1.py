import sys
import os
import tkinter as tk
#import tkMessageBox

root = tk.Tk()

def helloCallBack():
	os.system('python3 multi-speaker-tacotron-tensorflow/synthesizer.py')

b1=tk.Button(root, text="hello",bg="white", command=helloCallBack)
b1.pack()

root.mainloop()
