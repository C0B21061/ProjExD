from cgitb import text
import tkinter as tk
import tkinter.messagebox as tkm

def num_click(event):
    btn = event.widget
    txt = btn["text"]
    entry.insert(tk.END,txt)

def eq_click(event):
    ans = eval(entry.get())
    entry.delete(0,tk.END)
    entry.insert(tk.END,ans)

root = tk.Tk()
root.title("電卓")
root.geometry("300x600")

entry = tk.Entry(root,width=10,font=("Times New Roman",40),justify="right")
entry.grid(row=0,column=0,columnspan=3)

for i in range(9,-1,-1):
    button = tk.Button(root,text=f"{i}",font=("times New Roman",30),width=4,height=2)
    button.bind("<1>",num_click)
    r = [4,3,3,3,2,2,2,1,1,1]
    c = [0,2,1,0,2,1,0,2,1,0]
    button.grid(row=r[i],column=c[i])

button = tk.Button(root,text=f"+",font=("times New Roman",30),width=4,height=2)
button.bind("<1>",num_click)
button.grid(row=4,column=1)

button = tk.Button(root,text=f"=",font=("times New Roman",30),width=4,height=2)
button.bind("<1>",eq_click)
button.grid(row=4,column=2)

root.mainloop()