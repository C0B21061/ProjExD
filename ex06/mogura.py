import pygame as pg
import sys
from random import randint
import time
from threading import Thread

TIME = 10 #タイマー時間

class Screen:
    """スクリーンに関する処理"""
    def __init__(self, title, wh, img_path):
        # titlt: "pygame", wh: (1500, 800), img_path: "fig/sougenn.jpg"
        # ウィンドウ
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        # 背景
        img = pg.image.load(img_path)
        self.back_sfc = pg.transform.rotozoom(img, 0, 2.0)
        self.back_rct = self.back_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.back_sfc, self.back_rct)


class Hole:
    """穴を生成"""
    R = 120
    def __init__(self, scr:Screen, xy):
        self.sfc = pg.Surface((self.R*2, self.R*2))
        pg.draw.ellipse(self.sfc, (157, 135, 67), (self.R, self.R, self.R, self.R/3)) # (0, 0, 0)だと背景と同化して消えちゃうので注意
        self.sfc.set_colorkey((0, 0, 0))
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)


class Mogura:
    """モグラを生成、出現処理を実装"""
    LIMIT = 5
    NUMS = 0
    KILLS = 0
    def __init__(self, img_path, zoom, xy):
        # 変数初期化
        self.FLAG = False
        self.COOL_TIME = randint(100, 2500)
        self.WAIT_TIME = 0
        # 処理
        sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.sfc.set_colorkey((255, 255, 255))
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def cool_time(self):
        self.COOL_TIME = randint(800, 1000)

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen, hole:Hole):
        if Mogura.NUMS < Mogura.LIMIT or self.FLAG:
            if not self.FLAG:
                self.FLAG = True
                self.WAIT_TIME = randint(150, 500)
                Mogura.NUMS += 1
            else:
                self.WAIT_TIME -= 1
            self.rct.centerx = hole.rct.centerx + 60
            self.rct.centery = hole.rct.centery - 5
            self.blit(scr)
            # 待機時間がなくなった時
            if not self.WAIT_TIME:
                self.FLAG = False
                Mogura.NUMS -= 1
                self.cool_time()
        else:
            self.cool_time()
    
    def check(self, pos):
        return self.rct.collidepoint(pos)

    def click(self):
        self.FLAG = False
        Mogura.NUMS -= 1
        Mogura.KILLS += 1
        self.cool_time()


class Bird:
    """こうかとんによる妨害プログラム"""
    def __init__(self, img_path, zoom, xy):
        # img_path: "fig/6.png", zoom: 2.0, xy: (900, 400)
        # こうかとん生成
        self.vx = randint(2, 7)     # 加速度
        sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
    
    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen, basey, height, yn):
        # こうかとん位置更新
        x = self.check_bound(scr.rct)
        self.vx *= x
        self.rct.move_ip(self.vx, 0)
        # 端に衝突を検知したら, 1/2の確率で実行
        if x == -1 and randint(0, 1):
            n = randint(0, yn-1)
            self.rct.centery = basey + n*height 
        self.blit(scr)

    def check_bound(self, scr_rct):
        """
        scr_rct: スクリーン
        通常時: -1, 異常時:1
        """
        x = 1
        if self.rct.left < scr_rct.left or scr_rct.right < self.rct.right:
            x = -1
        return x


class Hammer:
    def __init__(self, img, zoom, center):
        sfc = pg.image.load(img)
        self.sfc = pg.transform.scale(sfc, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = center

    def update(self, mouse_xy):
        # 位置をマウスカーソルに合わせる
        self.rct.center = mouse_xy 

    def brit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)


def timeup(scr:Screen):
    """timeup処理をしています"""
    fonts = pg.font.Font(None, 100)
    txt = fonts.render(str("TIME UP!"), True, (255, 0, 0))
    scr.sfc.blit(txt, (250, 350))
    
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return 
 
def timer(secs):
    """
    timer処理、スレッドで行っている。
    """
    global TIME
    TIME += 1 # 同期ずれ修正
    for i in range(secs, -1, -1):
        TIME -= 1
        time.sleep(1)
              
def main():
    # スクリーン
    scr = Screen("pygame", (800, 800), "fig/sougenn.jpg")

    # マウスカーソルの非表示
    pg.mouse.set_visible(False)

    # 穴、モグラ作成
    basex = 40; basey = 150     # x/yの起点
    width = 200; height = 130   # x/y軸方向の幅
    xn = 4; yn = 5              # x/yのインスタンスの数
    holes = [[Hole(scr, (basex + x*width, basey + y*height)), 
                Mogura("fig/mogura2.jpg", 0.13, (basex + x*width, basey + y*height))]
                for x in range(xn) 
                for y in range(yn)]

    # こうかとん
    bird = Bird("fig/6.png", 1.8, (90, 140))

    #ハンマー
    hammer = Hammer("fig/piko.png", (100, 100), (400, 400))

    # クロック
    clock = pg.time.Clock()
    # タイマー
    t = Thread(target=timer,args=(TIME,), daemon=True) # daemon=True でメインとともに終了
    t.start()
    while True:
        # 背景作成
        scr.blit()
        events = pg.event.get()

        # ×で終了
        for event in events:            
            if event.type == pg.QUIT: return

        # 左上のパラメータ
        fonts = pg.font.Font(None, 40)
        txt = f"score:{Mogura.KILLS}  time:{TIME}"
        txt = fonts.render(str(txt), True, (0, 0, 0))
        scr.sfc.blit(txt, (10, 20))

        # hole処理
        for hole in holes:
            hole[0].blit(scr)
            if not hole[1].COOL_TIME:
                hole[1].update(scr, hole[0])
                for event in events:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if hole[1].check(event.pos):
                            hole[1].click()
            else:
                hole[1].COOL_TIME -= 1

        # bird(heightは、穴やモグラのy軸方向の幅)
        bird.update(scr, basey, height, yn)

        # マウスカーソルによる更新処理
        for event in events:
            if event.type == pg.MOUSEMOTION:
                hammer.update(pg.mouse.get_pos())

        # ハンマーを描写
        hammer.brit(scr) 

        # timeup処理
        if not TIME:
            timeup(scr)
            return

        # クロック 
        clock.tick(1000)  
        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()  