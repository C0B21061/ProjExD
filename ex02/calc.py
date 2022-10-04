import tkinter as tk
import tkinter.messagebox as tkm
from math import log10

enzan_list=["**","+","-","*","/"]

def color1(event):
    event.widget["bg"]="#000000"
    event.widget["fg"]="#ffffff"

def color2(event):
    event.widget["bg"]="SystemButtonFace"
    event.widget["fg"]="#000000"

def num_click(event):
    btn = event.widget
    txt = btn["text"]
    entry.insert(tk.END,txt)

def eq_click(event):
    ans = eval(entry.get())
    entry.delete(0,tk.END)
    entry.insert(tk.END,ans)

def AC_click(event):
    entry.delete(0,tk.END)

def C_click(event):
    entry.delete(len(entry.get())-1,tk.END)

def log_click(event):
    txt = entry.get()
    entry.delete(0,tk.END)
    entry.insert(tk.END,f"log10({txt})")
    
def bin_click(event):
    txt = entry.get()
    ans = eval(f"format({txt},'b')")
    entry.delete(0,tk.END)
    entry.insert(tk.END,ans)

root = tk.Tk()
root.title("電卓")
root.geometry("400x700")

entry = tk.Entry(root,width=10,font=("Times New Roman",40),justify="right")
entry.grid(row=0,column=0,columnspan=3)

for i in range(9,-1,-1):
    button = tk.Button(root,text=f"{i}",font=("times New Roman",30),width=4,height=2)
    button.bind("<1>",num_click)
    button.bind("<Enter>",color1)
    button.bind("<Leave>",color2)
    r = [5,4,4,4,3,3,3,2,2,2] #それぞれのボタンのrowの位置を格納したリスト
    c = [1,2,1,0,2,1,0,2,1,0] #それぞれのボタンのcolumnの位置を格納したリスト
    button.grid(row=r[i],column=c[i])

button = tk.Button(root,text="AC",font=("times New Roman",30),width=4,height=2)
button.bind("<1>",AC_click)
button.bind("<Enter>",color1)
button.bind("<Leave>",color2)
button.grid(row=1,column=0)

button = tk.Button(root,text="C",font=("times New Roman",30),width=4,height=2)
button.bind("<1>",C_click)
button.bind("<Enter>",color1)
button.bind("<Leave>",color2)
button.grid(row=1,column=1)

button = tk.Button(root,text="=",font=("times New Roman",30),width=4,height=2)
button.bind("<1>",eq_click)
button.bind("<Enter>",color1)
button.bind("<Leave>",color2)
button.grid(row=5,column=2)

for i,enzan in enumerate(enzan_list,1):
    button = tk.Button(root,text=f"{enzan}",font=("times New Roman",30),width=4,height=2)
    button.bind("<1>",num_click)
    button.bind("<Enter>",color1)
    button.bind("<Leave>",color2)
    button.grid(row=i,column=4)

button = tk.Button(root,text="log10",font=("times New Roman",30),width=4,height=2)
button.bind("<1>",log_click)
button.bind("<Enter>",color1)
button.bind("<Leave>",color2)
button.grid(row=1,column=2)

button = tk.Button(root,text="bin",font=("times New Roman",30),width=4,height=2)
button.bind("<1>",bin_click)
button.bind("<Enter>",color1)
button.bind("<Leave>",color2)
button.grid(row=5,column=0)

root.mainloop()