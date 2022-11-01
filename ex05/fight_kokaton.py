import pygame as pg
import sys
from random import randint

class Screen:
    def __init__(self, title, wh, bging):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(bging)
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct) # 練習2


class Bird:
    key_delta = {
        pg.K_UP:    -1,
        pg.K_DOWN:  +1
    }

    def __init__(self, img, zoom, center):
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = center

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_states[key]:
                self.rct.centery += delta
                if check(self.rct, scr.rct) != 1 :
                    self.rct.centery-= delta
        self.blit(scr) 


class Enemy:
    def __init__(self, img, zoom, center, vy):
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = center
        self.vy = vy 

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(0, self.vy)
        tate = check(self.rct, scr.rct)
        self.vy *= tate
        self.blit(scr)


class Attack:
    def __init__(self, color, radius, vxy, center, scr:Screen):
        self.sfc = pg.Surface((radius*2,radius*2)) 
        self.sfc.set_colorkey((0, 0, 0)) 
        pg.draw.circle(self.sfc, color, (radius, radius), radius) 
        self.rct = self.sfc.get_rect()
        self.rct.center = center
        self.vx, self.vy = vxy
        self.update(scr)
    
    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        tate = check(self.rct, scr.rct)
        self.vy *= tate
        self.blit(scr)


def check(obj_rct, scr_rct):
    tate = +1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return tate


def main():
    #敵のライフ
    en_life = 10 

    #スクリーン
    scr = Screen("負けるな！こうかとん", (1600, 900), "fig/pg_bg.jpg")

    #こうかとん
    tori = Bird("fig/9.png", 2.0, (1350, 450))

    #敵
    enemy = Enemy("fig/enemy.png", 0.75, (250,450), +1)

    #本来は書かないが攻撃処理ができなかったためテストで作成している(弾)
    attack = Attack((255, 0, 0), 10, (-1, 0), tori.rct.center, scr)

    clock = pg.time.Clock() 
    while True:

        zandan = []
        for i in range(20):
            zandan.append(Attack((255, 0, 0), 10, (-1, 0), tori.rct.center, scr))
        
        scr.blit() 
        
        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                return
  
        tori.update(scr)
        
        enemy.update(scr)

        attack.update(scr) #本来は書かない
        
        """
        key_states = pg.key.get_pressed()
        if key_states[pg.K_SPACE]:
            attack = True
        if attack == True:
           attack.update(scr)
           if attack.
        """

        #ここでスペースを押したらAttackのインスタンスを作成して攻撃したかった

        # 弾があたったら敵のライフを削る
        if enemy.rct.colliderect(attack.rct): 
            en_life -= 1

        # ０になったら終了 
        if en_life < 0:
            return  


        pg.display.update() 
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()