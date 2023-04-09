import sugarbeet as sb
from tkinter import *
from tkinter import ttk
import re
from matplotlib import pyplot as plt
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


sv=StringVar()
tp=StringVar(value="Матрица")
N = 0
matr = [[]]
a = []
b = []
c = []
matrLab = Label(frameOne,text = "Матрица коэфициэнтов сахаристости:",bg = '#edf5f3',font = "Times 13")
parLab = Label(frameOne,text = "Параметры распределения коэфициентов:",bg = '#edf5f3',font = "Times 13")
parLabA = Label(frameOne,text = "Интервал разброса значений сахаристости:",bg = '#edf5f3',font = "Times 13")
parLabB = Label(frameOne,text = "Интервал разброса коэфициентов дозаривания:",bg = '#edf5f3',font = "Times 13")
parLabC = Label(frameOne,text = "Интервал разброса коэфициентов деградации:",bg = '#edf5f3',font = "Times 13")
def ttt(*args):
    global matr
    global N
    global a
    global b
    global c
    for i in matr:
        for j in i:
            j.place_forget()
    matrLab.place_forget()
    if entN.get().isnumeric() == False :
        return
    matr = [[]]
    N = entN.getint(entN.get())
    if tp.get()=="Матрица":
        matrLab.place(x = 50, y = 260)
        if N > 12:
            entN.delete(0, END)
            entN.insert(0,"12")
            N = 12
        for i in range(N):
            for j in range(N):
                ent = Entry(frameOne, width = 3,bg = '#edf5f3')
                ent.place(x=62+j*19,y=290+i*19)
                matr[i].append(ent)
            matr.append([])

def watchh(*args):
    global matr
    global N
    global a
    global b
    global c
    for i in matr:
        for j in i:
            j.place_forget()
    matrLab.place_forget()
    parLab.place_forget()
    parLabA.place_forget()
    parLabB.place_forget()
    parLabC.place_forget()
    for j in a:
        j.place_forget()
    for j in b:
        j.place_forget()
    for j in c:
        j.place_forget()
    if tp.get()=="Матрица":
        if len(matr) != N+1:
            ttt()
        matrLab.place(x = 50, y = 260)
        i=0
        for x in matr:
            j = 0
            for ent in x:
                ent.place(x=62+j*19,y=290+i*19)
                j+=1
            i+=1
    else:
        parLab.place(x = 50, y = 260)   
        parLabA.place(x = 50, y = 290)
        for ent,i in zip(a,range(2)):
            ent.place(x=80+i*40,y=330)
        parLabB.place(x = 50, y = 380)
        for ent,i in zip(b,range(2)):
            ent.place(x=80+i*40,y=420)
        parLabC.place(x = 50, y = 460)
        for ent,i in zip(c,range(2)):
            ent.place(x=80+i*40,y=500)

for i in range(2):
    ent = Entry(frameOne, width = 4,bg = '#edf5f3',font = "Times 13")
    # ent.place(x=80+i*40,y=330)
    a.append(ent)
for i in range(2):
    ent = Entry(frameOne, width = 4,bg = '#edf5f3',font = "Times 13")
    # ent.place(x=80+i*40,y=420)
    b.append(ent)
for i in range(2):
    ent = Entry(frameOne, width = 4,bg = '#edf5f3',font = "Times 13")
    # ent.place(x=80+i*40,y=500)
    c.append(ent)

sv.trace("w",callback=ttt)
tp.trace("w",callback=watchh)
laNum = Label(frameOne,text="Количество партий сырья:",font = "Times 13",bg = '#edf5f3')
laNum.place(x=50,y=105)
entN = Entry(frameOne,width=5,textvariable=sv,font = "Times 14",bg = '#edf5f3')
entN.place(x=53,y=135)

laB = Label(frameOne,text="Способ ввода системы:",font = "Times 13",bg = '#edf5f3')
laB.place(x=50,y=170)
box = ttk.Combobox(frameOne,background='#edf5f3', values=['Матрица','Набор параметров'], textvariable = tp,font = "Times 13")
box.place(x=53,y=215)
# for i in range(5):
#     for j in range(6):
#         ent = Entry(frameOne, width = 3)
#         ent.place(x=12+i*19,y=100+j*19)

def calcOne():
    global matr
    global N
    global a
    global b
    global c
    tmatr = []
    if tp.get()=="Матрица":
        for x in matr:
            tt = []
            for y in x:
                tt.append(y.getdouble(y.get()))
            tmatr.append(tt)
        tmatr.pop()
    else:
        aa1 , aa2 = a[0].getdouble(a[0].get()),a[1].getdouble(a[1].get())  
        bb1 , bb2 = b[0].getdouble(b[0].get()),b[1].getdouble(b[1].get())  
        cc1 , cc2 = c[0].getdouble(c[0].get()),c[1].getdouble(c[1].get())  
        tmatr = sb.gen_p_matrix(N,3,aa1,aa2,bb1,bb2,cc1,cc2)
    res1, indices1 = sb.hungarian_max(tmatr)
    res2, indices2 = sb.hungarian_min(tmatr)
    res3, indices3 = sb.greedy(tmatr)
    res4, indices4 = sb.saving(tmatr)
    resMas1 = [0]
    down = [x  for x in range(N+1)]
    s = 0 
    for i in range(N):
        s += tmatr[indices1[i]][i]
        resMas1.append(s)
    resMas2 = [0]
    s = 0 
    for i in range(N):
        s += tmatr[indices2[i]][i]
        resMas2.append(s)
    resMas3 = [0]
    s = 0 
    for i in range(N):
        s += tmatr[indices3[i]][i]
        resMas3.append(s)
    resMas4 = [0]
    s = 0 
    for i in range(N):
        s += tmatr[indices4[i]][i]
        resMas4.append(s)
    plt.rcParams ['figure.figsize'] = [9, 6]
    plt.plot(down,resMas1,'r-.',label = 'Венгерский алгоритм(максимум)')
    plt.plot(down,resMas2,'g',label = 'Венгерский алгоритм(минимум)')
    plt.plot(down,resMas3,'b:',label = 'Жадный алгоритм')
    plt.plot(down,resMas4,'c--',label = 'Бережливый алгоритм')
    plt.legend(loc=2)
    plt.xlabel("Время")
    plt.ylabel("S")
    plt.title("Единичный эксперимент")
    plt.show()
    
btn = Button(frameOne,text="Провести расчеты",font = "Times 13",bg = '#00ffff',command=calcOne)
btn.place( x = 50,y = 50)

f2.secondFrame(root,frameTests)
root.mainloop()