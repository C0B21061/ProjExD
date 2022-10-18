import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    canv = tk.Canvas(root,width=1500,height=900,bg="#000000")
    tori = tk.PhotoImage(file="ex03/fig/9.png")
    cx,cy = 300,400
    canv.create_image(cx,cy,image=tori,tag="tori")
    canv.pack()

    root.mainloop()
