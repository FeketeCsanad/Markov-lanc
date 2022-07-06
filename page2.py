from tkinter import *
from tkinter import messagebox

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandas import DataFrame
from decimal import *

root = Tk()
root.geometry('800x500')
root.title('PythonExamples.org - Tkinter Example')

global e1
global numm
global my_entry
szabad_tagok = np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0])
r = np.zeros(9)

my_entry= Entry(root)
e1=Entry(root)
e1.place(x=100,y=180)
korok=Entry(root)
korok.place(x=100,y=210)
entries=[]
entries2=[]
new_array=[]

def gauss_jordan_eliminacio(a,b):
    n=9

    #a foatlon nullatol eltero elem legyen
    for k in range(n):
        if a[k,k]==0:
            for i in range (k+1,n):
                if np.fabs(a[i,k])>np.fabs(a[k,k]):
                    for j in range(k,n):
                        a[k,j],a[i,j]=a[i,j],a[k,j]
                    b[k],b[i]=b[i],b[k]
                    break

        #sor felosztasa
        pivot=a[k,k]
        if (pivot==0):
            pivot=10^(-16)
        for j in range(k,n):
            a[k,j]/=pivot
        b[k]/=pivot

        #Eliminalas
        for i in range(n):
            if i == k or a[i,k]==0:continue
            factor=a[i,k]
            for j in range(k,n):
                a[i,j]-=factor * a[k,j]

            b[i]-=factor*b[k]

    return  a,b


def matrix_letrehoz(a):
    A = np.array([[-1, 0, 0,a[0,1], 0, 0, a[0,2], 0, 0],
                  [0, -1+a[0,0], 0, 0, 0, 0, 0, a[0,2], 0],
                  [0, 0, -1+a[0,0], 0, 0, a[0,1], 0, 0, 0],
                  [0, 0, 0, -1+a[1,1], 0, 0, a[1,2], 0, 0],
                  [0, a[1,0], 0, 0, -1, 0, 0, a[1,2], 0],
                  [0, 0,a[1,0], 0, 0,-1+a[1,1], 0, 0, 0],
                  [0, 0, 0,a[2,1], 0, 0,-1+a[2,2], 0, 0],
                  [0,a[2,0], 0, 0, 0, 0, 0,-1+a[2,2], 0],
                  [0, 0,a[2,0], 0, 0,a[2,1], 0, 0, -1]
                  ])
    print(A)

    D, C = gauss_jordan_eliminacio(A, szabad_tagok)

    np.set_printoptions(precision=3)
    print("Solution: ", C)

    Label(root,text="Varhato visszateresi ido: \n").place(x=20,y=600)
    label = Label(root, text=str(C), font=("Arial", 15)).place(x=20, y=620)
    kiment2(C)

def kiment1(adat):
    df = pd.DataFrame(adat)
    datatoexcel = pd.ExcelWriter("eredmeny1.xlsx", engine='xlsxwriter')
    df.to_excel(datatoexcel, sheet_name='Sheet 1')
    workbook = datatoexcel.book
    worksheet = datatoexcel.sheets['Sheet 1']
    format1 = workbook.add_format({'num_format': '0.000'})
    worksheet.set_column('B1:H10', None, format1)
    datatoexcel.save()

def kiment2(adat):
    df = pd.DataFrame(adat)
    datatoexcel = pd.ExcelWriter("eredmeny2.xlsx", engine='xlsxwriter')
    df.to_excel(datatoexcel, sheet_name='Sheet 1')
    workbook = datatoexcel.book
    worksheet = datatoexcel.sheets['Sheet 1']
    format1 = workbook.add_format({'num_format': '0.000'})
    worksheet.set_column('B1:H10', None, format1)
    datatoexcel.save()

def szamol(szamok):
    n=int(korok.get())
    P=np.dot(szamok,szamok)
    fig, a = plt.subplots(1, n) #n sor letrehozasa az elso ploton az elso fig-en
    for i in range(n):
        P=np.dot(P,szamok)
        rajzol(P, fig,a[i]) # melyik sor mutassa a P-t
        np.set_printoptions(precision=3)
        print(P)

    Label(root, text="atmeneti-valoszinusegek: \n").place(x=20, y=240)
    label = Label(root, text=str(P),font=("Arial", 15)).place(x=20, y=270)
    kiment1(P)

def rajzol(adat,figure,ax):
    df2 = DataFrame(adat)
    line3 = FigureCanvasTkAgg(figure, root)
    line3.get_tk_widget().place(x=300,y=100)
    df2.plot(kind='line', legend=False, ax=ax, fontsize=10) # megjelenites az x tengelyen
    plt.close(figure)
def letrehoz():
    numm = int(e1.get())
    global my_entry
    for x in range(numm):
        row = []
        for i in range(numm):
            my_entry = Entry(root)
            my_entry.grid(row=x, column=i)
            row.append(my_entry)
        entries.append(row)


def mentes():
    my_array = [[float(el.get()) for el in row] for row in entries]
    new_array = np.asarray(my_array)

    print(new_array)

    #ellenorzes
    sor = [sum(i) for i in new_array]
    oszlopok = len(sor)
    if sum(sor) <= oszlopok:

        szamol(new_array)
        matrix_letrehoz(new_array)

    else:
        print("nem jo mert a sorok osszege>1")
        messagebox.showerror('hiba','Legalabb az egyik sor osszege nagyobb mint 1 !')

letrehoz = Button(root,text='Elfogad',command=letrehoz).place(x=40,y=180)
mentes = Button(root,text='Szamol',command=mentes).place(x=40,y=210)

my_label=Label(root,text='')
root.mainloop()