from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
import self as self
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pip
import pandas as pd
import xlwt
from xlwt import Workbook
from pprint import pprint

#ablak deklaralas
root = Tk()
root.geometry('400x150')
root.title('Markov lancok ')

global Matrix
szabad_tagok = np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0])
r = np.zeros(9)

#input mezok
korok=Entry(root)
korok.place(x=20,y=10)



Matrix=np.zeros((3,3))
my_frame = Frame(root)
my_frame.pack(pady=20)


my_tree=ttk.Treeview(my_frame)



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
    print("megoldas: ", C)

    Label(root,text="Varhato visszateresi ido: \n").place(x=20,y=150)
    label = Label(root, text=str(C), font=("Arial", 15)).place(x=20, y=180)
    kiment2(C)

def atdob():
    root.destroy()
    import page2


#atmeneti valoszinuseg
def szamol(szamok):
    n=int(korok.get())
    P=np.dot(szamok,szamok)
    for i in range(n):
        P=np.dot(P,szamok)
        rajzol(P)
        np.set_printoptions(precision=3)
        #print(P)


    Label(root,text="atmeneti valoszinusegek: \n").place(x=20,y=40)
    label = Label(root, text=str(P),font=("Arial", 15)).place(x=20, y=60)
    kiment1(P)

#itt rajzoljuk ki az atmeneti matrixok alakulasat
def rajzol(adat):
    fig,a = plt.subplots()
    df2 = DataFrame(adat)
    figure2 = plt.Figure(figsize=(1, 1), dpi=50)
    ax2 = figure2.add_subplot(111)
    line2 = FigureCanvasTkAgg(figure2, root)
    line2.get_tk_widget().pack(side=LEFT, fill=BOTH)
    df2.plot(kind='line', legend=False, ax=ax2, fontsize=10)
    plt.close(fig)
    ax2.set_title('Markov')

#kimentes Excel-be
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

#Excel file olvasas
def file_open():
    global Vegeleges
    filename=filedialog.askopenfilename(
        initialdir="Desktop",
        title = "Open a file",
        filetype=(("xlsx files","*.xlsx"),("All files","*.*"))
        )
    if filename:
        try:
            filename = r"{}".format(filename)
            df = pd.read_excel(filename,'Sheet1')
            df2=pd.read_excel(filename,'Sheet2')
            print(df)
            print(df2)

        except ValueError:
            my_label.config(text="Nem tudtuk megnytini a filet")

        except FileNotFoundError:
            my_label.config(text="Nem talaltunk ilyent")

    clear_tree()

    my_tree["column"]= list(df.columns)
    my_tree["show"]="headings"

    for column in my_tree["column"]:
        my_tree.heading(column, text=column)

    global df_rows
    df_rows = df.to_numpy()
    for row in df_rows:
        my_tree.insert("", "end", values=row)

    #ellenorzes
    sor = [sum(i) for i in df_rows]
    oszlopok=len(sor)
    print(sor)
    print(oszlopok)
    n = int(korok.get())
    if sum(sor) <= oszlopok:

        szamol(df_rows)
        matrix_letrehoz(df_rows)
    else:
        print("nem jo mert a sorok osszege>1")
        messagebox.showerror('hiba','Legalabb az egyik sor osszege nagyobb mint !')
    my_tree.pack()


def clear_tree():
    my_tree.delete(*my_tree.get_children())

#menu hozzaadas
my_menu=Menu(root)
root.config(menu=my_menu)

file_menu=Menu(my_menu,tearoff=FALSE)
my_menu.add_cascade(label="spreadsheets",menu=file_menu)
file_menu.add_command(label="open",command=file_open)

#itt megyunk at a manualis bevitlre
oldalvaltas = Button(root,text='manualis bevitel',command=atdob).pack(fill=X,expand=FALSE,side=BOTTOM)

my_label=Label(root,text="")
my_label.pack(pady=20)
root.mainloop()

