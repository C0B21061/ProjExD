import tkinter as tk
import tkinter.messagebox as tkm
import maze_maker

def key_down(event):
    global key
    key = event.keysym

def key_up(event):
    global key
    key = ""

def main_proc():
    global cx,cy,mx,my,ch_mx,ch_my
    if key == "Up":
        my -= 1
    elif key == "Down":
        my += 1
    elif key == "Left":
        mx -= 1
    elif key == "Right":
        mx += 1
    if maze[my][mx] == 0:
        if mx==1 and my==7:
            mx, my = 13,1
        cx, cy = mx*100+50, my*100+50
    else:
        if key == "Up":
            my += 1
        elif key == "Down":
            my -= 1
        elif key == "Left":
            mx += 1
        elif key == "Right":
            mx -= 1
    canv.coords("tori",cx,cy)
    
    #　↓↓関数にしたかったができなかった↓↓
    #　後ろを壁にするコードです
    if key == "Up":
        ch_my = my + 1
        ch_mx = mx
        canv.create_rectangle(ch_mx*100, ch_my*100, ch_mx*100+100, ch_my*100+100, 
                                    fill="gray")
        maze[ch_my][ch_mx]=1
    elif key == "Down":
        ch_my = my - 1
        ch_mx = mx
        canv.create_rectangle(ch_mx*100, ch_my*100, ch_mx*100+100, ch_my*100+100, 
                                    fill="gray")
        maze[ch_my][ch_mx]=1
    elif key == "Left":
        ch_mx = mx + 1
        ch_my = my
        canv.create_rectangle(ch_mx*100, ch_my*100, ch_mx*100+100, ch_my*100+100, 
                                    fill="gray")
        maze[ch_my][ch_mx]=1
    elif key == "Right":
        ch_mx = mx - 1
        ch_my = my
        canv.create_rectangle(ch_mx*100, ch_my*100, ch_mx*100+100, ch_my*100+100, 
                                    fill="gray")
        maze[ch_my][ch_mx]=1

    if mx==13 and my==7:
        tkm.showinfo("おめでとう！","ゴールしました！")
    else:
        root.after(100,main_proc)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")

    canv = tk.Canvas(root,width=1500,height=900,bg="#000000")
    tori = tk.PhotoImage(file="ex03/fig/9.png")

    maze=maze_maker.make_maze(15,9)
    maze_maker.show_maze(canv,maze)

    cx,cy = 300,400
    mx,my = 1,1
    ch_mx,ch_my=1,1
    canv.create_image(cx,cy,image=tori,tag="tori")
    canv.pack()

    key = ""

    root.bind("<KeyPress>",key_down)
    root.bind("<KeyRelease>",key_up)

    main_proc()

    root.mainloop()
