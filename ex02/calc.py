import tkinter as tk

root = tk.Tk()
root.title("電卓")
root.geometry("300x500")

for i in range(9,-1,-1):
    button = tk.Button(root,text=f"{i}",font=("times New Roman",30),width="4",height="2")
    r = [3,2,2,2,1,1,1,0,0,0]
    c = [0,2,1,0,2,1,0,2,1,0]
    button.grid(row=r[i],column=c[i])


root.mainloop()