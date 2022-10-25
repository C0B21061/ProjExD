import random as rd
import pygame as pg
import sys

def check_bound(obj_rct,scr_rct):
    yoko, tate= 1, 1
    if obj_rct.left < scr_rct.left or obj_rct.right > scr_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or obj_rct.bottom > scr_rct.bottom:
        tate = -1
    return yoko, tate

def check_bound_bomb(obj_rct,scr_rct):
    global bound #爆弾がバウンドしたときにTrueにし、処理を行う
    yoko, tate= 1, 1
    if obj_rct.left < scr_rct.left or obj_rct.right > scr_rct.right:
        yoko = -1
        bound = True
    if obj_rct.top < scr_rct.top or obj_rct.bottom > scr_rct.bottom:
        tate = -1
        bound = True
    return yoko, tate

def main():
    global bound
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600, 900))
    scrn_rct = scrn_sfc.get_rect()
    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()

    tori_sfc = pg.image.load("fig/5.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400

    bomb_sfc = pg.Surface((20,20))
    bomb_sfc.set_colorkey((0,0,0))
    pg.draw.circle(bomb_sfc,(255,0,0),(10,10),10)
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx = rd.randint(20,100)
    bomb_rct.centery = rd.randint(20,880)

    warp_sfc = pg.Surface((120,120)) #ワープホールの描写
    warp_sfc.set_colorkey((0,0,0))
    pg.draw.circle(warp_sfc,(25,25,25),(60,60),60)
    warp_rct = warp_sfc.get_rect()
    warp_rct.centerx = rd.randint(1500,1540)
    warp_rct.centery = rd.randint(40,840)

    vx, vy = 1, 1
    vx2, vy2 = -1, -1

    clock = pg.time.Clock() 
    while True:
        scrn_sfc.blit(bg_sfc, bg_rct) 
        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                return

        key_states = pg.key.get_pressed()
        if key_states[pg.K_SPACE]: #スペースを押している間加速
            walk = 3
        else: 
            walk = 1

        if key_states[pg.K_UP]:
            tori_rct.centery -= walk
        if key_states[pg.K_DOWN]:
            tori_rct.centery += walk
        if key_states[pg.K_LEFT]:
            tori_rct.centerx -= walk
        if key_states[pg.K_RIGHT]:
            tori_rct.centerx += walk

        yoko, tate = check_bound(tori_rct, scrn_rct)
        if yoko == -1:
            if key_states[pg.K_LEFT]:
                tori_rct.centerx += walk
            if key_states[pg.K_RIGHT]:
                tori_rct.centerx -= walk
        if tate == -1:
            if key_states[pg.K_UP]:
                tori_rct.centery += walk
            if key_states[pg.K_DOWN]:
                tori_rct.centery -= walk
        scrn_sfc.blit(tori_sfc, tori_rct) 

        yoko, tate = check_bound(warp_rct,scrn_rct)
        yoko_bomb,tate_bomb = check_bound_bomb(bomb_rct,scrn_rct)

        if bound == True: #爆弾が壁にぶつかったとき
            kasoku = 0.2
            if vx < 0:
                vx -= kasoku
                if vy < 0:
                    vy -= kasoku
                elif vy > 0:
                    vy += kasoku
            elif vx > 0:
                vx += kasoku
                if vy < 0:
                    vy -= kasoku
                elif vy > 0:
                    vy += kasoku
            bound = False

        vx *= yoko_bomb
        vy *= tate_bomb
        vx2 *= yoko
        vy2 *= tate
        bomb_rct.move_ip(vx,vy)
        warp_rct.move_ip(vx2,vy2)
        scrn_sfc.blit(bomb_sfc,bomb_rct)
        scrn_sfc.blit(warp_sfc,warp_rct)

        if tori_rct.colliderect(warp_rct): #ワープホールにあたった時の処理
            tori_rct.centery = rd.randint(100,800)
            tori_rct.centerx = rd.randint(100,1500)
            scrn_sfc.blit(tori_sfc, tori_rct)

        if tori_rct.colliderect(bomb_rct):
            return

        pg.display.update() 
        clock.tick(1000)

if __name__ == "__main__":
    pg.init() 
    bound = False
    main() 
    pg.quit() 
    sys.exit()