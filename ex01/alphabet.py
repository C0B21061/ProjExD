import random 
import datetime

taisyou = 10
kesson = 2
abc = []
ans = []
txt1 = ""
txt2 = ""
roop = False

def shutudai():
    global txt1,txt2
    while len(abc)<taisyou:
        a = chr(random.randint(65,90))
        if a not in abc:
            abc.append(a)
    
    for i in range(taisyou):
        txt1 += f"{abc[i]} "

    print(txt1)

    for i in range(kesson):
        num = random.randint(len(abc))
        ans.append(abc.pop(num))
    
    random.shuffle(abc)
    for i in range(taisyou-kesson):
        txt2 += f"{abc[i]} "

    print(txt2)

def kaito():
    global roop
    roop = True
    while roop:
        kesson_ans = input("欠損文字はいくつあるでしょうか？")
        if int(kesson_ans) == kesson:
            print("正解です。それでは欠損文字を1つずつ入力してください")
            roop = False

    while len(ans)>1:
        answer = input("１つ目の文字を入力してください")
        if answer in ans:
            ans.pop(ans.index(answer))
            print("正解")
        else:
            print("不正解")
    
    while len(ans)>0:
        answer = input("２つ目の文字を入力してください")
        if answer in ans:
            ans.pop(ans.index(answer))
            print("正解")
        else:
            print("不正解")

shutudai()
kaito()