import sugarbeet as sb
from tkinter import *
from tkinter import ttk
import re
from matplotlib import pyplot as plt
import f1
import f2

root = Tk()
root.title("Sugarbeet")
root.geometry("1000x600+100+100")
root.iconbitmap(default= "imgs/sugar_cubes.ico")
root.update_idletasks()

notebook = ttk.Notebook()
notebook.pack(expand=True, fill=BOTH)   
# создаем пару фреймвов
frameOne = ttk.Frame(notebook)
frameTests = ttk.Frame(notebook)
 
frameOne.pack(fill=BOTH, expand=True)
frameTests.pack(fill=BOTH, expand=True)
 
# добавляем фреймы в качестве вкладок
notebook.add(frameOne, text="Единичный эксперимент", padding = 5)
notebook.add(frameTests, text="Серия тестов", padding = 5)

img = PhotoImage(file='imgs/fonnrgif.gif')
label = Label(frameOne,image = img)
label.place(x=0,y=0)

img2 = PhotoImage(file='imgs/fonnwgif.gif')
label2 = Label(frameTests,image = img2)
label2.place(x=0,y=0)




f1.firstFrame(root,frameOne)
f2.secondFrame(root,frameTests)
root.mainloop()