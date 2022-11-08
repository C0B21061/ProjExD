import pygame as pg
import sys
from random import randint


#スクリーン
class Screen:
    def __init__(self, title, wh, bging):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(bging)
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct) 


#モグラ（今回の画像はチンアナゴを使用）
class Mogura:
    score = 0 #モグラをたたいた回数

    def __init__(self, img, zoom, center):
        sfc = pg.image.load(img)
        self.sfc = pg.transform.scale(sfc, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = center
        self.app = False #appはモグラが出ている状態を表す

    def update_on(self):
        self.app = True

    def update(self, scr:Screen):
        score(f"score:{Mogura.score}", (150, 0, 0), (100, 820), scr)
        if self.app:
            scr.sfc.blit(self.sfc, self.rct)
            
        else:
            pass
    
    #マウスカーソルが範囲内ならappをFalseにする
    def get_hit(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if self.rct.left < mouse_x < self.rct.right:
            if self.rct.top < mouse_y < self.rct.bottom:
                self.app = False
                Mogura.score += 1 #スコアの加算
            else:
                pass
        else:
            pass


#スコアのテキストを表示
def score(mes, color, vxy, scr:Screen):
    font = pg.font.SysFont(None, 75)
    text = font.render(mes, True, color)
    scr.sfc.blit(text, vxy)


#穴
def create_hole(color, vx, vy, width, height, scr:Screen):
    for i in range(5):
        for j in range(4):
            hole_sfc = pg.Surface((width,height))
            hole_sfc.set_colorkey((0, 0, 0))
            pg.draw.ellipse(hole_sfc, color, (vx, vy, width, height,))
            hole_rct = hole_sfc.get_rect()
            hole_rct.center = (205+300*i, 175+200*j)
            scr.sfc.blit(hole_sfc, hole_rct)

    
def main():
    scr = Screen("モグラたたき", (1600, 900), "fig/umi.jpg")

    mogura_data = []
    for i in range(5):
        for j in range(4):
            mogura_data.append(Mogura("fig/anago.png", (200,200), (195+300*i, 115+200*j)))

    clock = pg.time.Clock()
    while True:
        scr.blit()

        create_hole((1, 1, 1), 0, 0, 150, 50, scr)

        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                return

            if event.type == pg.MOUSEBUTTONDOWN: #マウスを押したとき
                for i in range(20):
                    mogura_data[i].get_hit(pg.mouse.get_pos())

        for i in range(20):
            a = randint(1, 1000)
            if a == 1: #1/1000の確率
                mogura_data[i].update_on() #self_appをTrueにする
            mogura_data[i].update(scr)

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()
