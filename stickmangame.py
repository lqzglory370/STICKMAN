from tkinter import *
import random
import time


#Game类
class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Mr.Stick Man Races For the Exit")
        self.tk.resizable(0, 0)                          #让窗口大小固定       
        self.tk.wm_attributes("-topmost", 1)        #把窗口移到所有其他窗口之前
        self.canvas = Canvas(self.tk, width=500, height=500, \
                             highlightthickness=0)
        # \ 可用于把一行很长的代码拆开，分两行写
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500

        #创建变量bg，装载PhotoImage对象
        self.bg1 = PhotoImage(file="background.gif")
        self.bg2 = PhotoImage(file="background2.gif")
        self.flag = True
        #把图形高宽保存到w, h中。
        w = self.bg1.width()
        h = self.bg1.height()
        #平铺背景，create_image()用于把图形画在坐标上。
        for x in range(0, 5):
            for y in range(0, 5):
                if self.flag == True:
                    self.canvas.create_image(x * w, y * h, \
                                         image=self.bg1, anchor='nw')
                    self.flag = False
                    continue
                if self.flag == False:
                    self.canvas.create_image(x * w, y * h, \
                                         image=self.bg2, anchor='nw')
                    self.flag = True
                    continue
        self.sprites = []
        self.running = True

    #Game类中的mainloop函数用于游戏的动画。
    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            #重绘制屏幕并休息0.01s
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


#Coords类——坐标类
class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


#在水平方向判断是否冲突
def within_x(co1, co2):
    if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
        or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
        or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
        or (co2.x2 > co1.x1 and co2.x2 < co1.x2):
        return True
    else:
        return False

#在垂直方向判断是否冲突
def within_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
        or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
        or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
        or (co2.y2 > co1.y1 and co2.y2 < co1.y2):
        return True
    else:
        return False
        
#判断左侧相撞
def collided_left(co1, co2):
    if within_y(co1, co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
            return True
    return False

 #判断右侧相撞
def collided_right(co1, co2):
    if within_y(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False

#判断顶部相撞
def collided_top(co1, co2):
    if within_x(co1, co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False

#判断底部相撞
def collided_bottom(co1, co2):
    if within_x(co1, co2):
        y_calc = co1.y2 + y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
    return False


#Sprite类——精灵类
class Sprite:
    def __init__(self, game):
        #让创建的每个精灵都能访问游戏中的其他精灵的列表。
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates


#PlatformSprite——平台类(精灵类的子类)
class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, \
                            image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)


#StickFigureSprite——火柴人类
class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [
            PhotoImage(file="figure_L1.gif"),
            PhotoImage(file="figure_L2.gif"),
            PhotoImage(file="figure_L3.gif")
        ]
        self.images_right = [
            PhotoImage(file="figure_R1.gif"),
            PhotoImage(file="figure_R2.gif"),
            PhotoImage(file="figure_R3.gif")
        ]
        self.image = game.canvas.create_image(200, 470, \
                            image=self.images_left[0], anchor='nw')
        self.x = -2
        self.y = 0
        self.current_image = 0                  #保存显示在屏幕上图形的索引位置
        self.current_image_add = 1            #包含数字，加上索引位置得到下一个索引位置
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        #键盘按键绑定
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    #让火柴人左转
    def turn_left(self. evt):
        if self.y == 0:
            self.x = -2
        
    #让火柴人右转
    def turn_right(self, evt):
        if self.y == 0:
            self.x = 2

    #让火柴人跳跃
    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0

    #判断移动方式并相应改变图形
    def animate(self):
        #计算函数自上次调用以来的时间，用于判断是否需要画序列中下一个图形。
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, \
                                            image=self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image, \
                                            image=self.images_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, \
                                            image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, \
                                            image=self.images_right[self.current_image])

    #判断火柴人在屏幕的位置
    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates

    #控制火柴人移动
    def move(self):
        self.animate()
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 4
        if self.y > 0:
            self.jump_count -= 1

        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True





#加入平台对象
g = Game()
platform1 = PlatformSprite(g, PhotoImage(file="platform3.gif"), \
                           0, 480, 100, 10)
platform2 = PlatformSprite(g, PhotoImage(file="platform3.gif"), \
                           150, 440, 100, 10)
platform3 = PlatformSprite(g, PhotoImage(file="platform3.gif"), \
                           300, 400, 100, 10)
platform4 = PlatformSprite(g, PhotoImage(file="platform3.gif"), \
                           300, 160, 100, 10)
platform5 = PlatformSprite(g, PhotoImage(file="platform2.gif"), \
                           175, 350, 66, 10)
platform6 = PlatformSprite(g, PhotoImage(file="platform2.gif"), \
                           50, 300, 66, 10)
platform7 = PlatformSprite(g, PhotoImage(file="platform2.gif"), \
                           170, 120, 66, 10)
platform8 = PlatformSprite(g, PhotoImage(file="platform2.gif"), \
                           45, 60, 66, 10)
platform9 = PlatformSprite(g, PhotoImage(file="platform1.gif"), \
                           170, 250, 32, 10)
platform10 = PlatformSprite(g, PhotoImage(file="platform1.gif"), \
                           230, 200, 32, 10)
g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)
g.mainloop()










