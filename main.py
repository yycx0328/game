import sys
import pygame
import time
import random


class Enemy:
    ''' 敌军飞机类 '''
    def __init__(self, var_x, var_y, var_image):
        self.x = var_x
        self.y = var_y
        self.direct = 'right'
        self.image = var_image
        self.bullets = []

    # 在屏幕上构建敌军飞机
    def draw(self, var_screen):
        var_screen.blit(pygame.image.load(self.image), (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(var_screen)

    # 控制飞机左右移动
    def move(self):
        if self.direct == 'left':
            if self.x >= 0:
                self.x -= 2
            else:
                self.direct = 'right'
        elif self.direct == 'right':
            if self.x <= 725:
                self.x += 2
            else:
                self.direct = 'left'

    # 敌军飞机开火
    def fire(self):
        pass
        self.bullets.append(EnemyBullet(self.x + 35, self.y + 95, './images/enemy-bullet.png'))


class Hero:
    ''' 我军飞机类 '''
    def __init__(self, var_x, var_y, var_image):
        self.x = var_x
        self.y = var_y
        self.image = var_image
        self.bullets = []

    # 在屏幕上构建我军飞机
    def draw(self, var_screen):
        var_screen.blit(pygame.image.load(self.image), (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(var_screen)

    # 控制我军飞机左右移动
    def move(self, var_direction):
        # 飞机向左移动，且越界判断
        if var_direction == 'left':
            if self.x > 0:
                self.x -= 5
        # 飞机向右移动，且越界判断
        else:
            if self.x < 698:
                self.x += 5

    # 我军飞机开火
    def fire(self):
        self.bullets.append(HeroBullet(self.x + 51, self.y - 10, './images/hero-bullet.png'))


class HeroBullet:
    ''' 我军飞机发射的子弹类 '''
    def __init__(self, var_x, var_y, var_image):
        self.x = var_x
        self.y = var_y
        self.image = var_image

    # 在屏幕上构建我军飞机发射的子弹
    def draw(self, var_screen):
        var_screen.blit(pygame.image.load(self.image), (self.x, self.y))

    # 子弹向上移动
    def move(self):
        self.y -= 10
        if self.y <= 0:
            del self


class EnemyBullet:
    ''' 敌军飞机发射的子弹类 '''
    def __init__(self, var_x, var_y, var_image):
        self.x = var_x
        self.y = var_y
        self.image = var_image

    # 在屏幕上构建我军飞机发射的子弹
    def draw(self, var_screen):
        var_screen.blit(pygame.image.load(self.image), (self.x, self.y))

    # 子弹向上移动
    def move(self):
        self.y += 10
        if self.y >= 800:
            del self

pygame.init()
# 游戏主屏幕宽高
size = width, height = 800, 600
# 构建屏幕
screen = pygame.display.set_mode(size)
# 游戏屏幕背景图
screen_bg = pygame.image.load("./images/bg.png")
# 构建我军飞机
hero = Hero(360, 480, './images/hero.png')
# 构建敌军飞机
enemy = Enemy(10, 0, './images/enemy.png')

# 标记是否按下向左键，保证长按向左键，我机一直往左移动
key_left_flag = False
# 标记是否按下向右键，保证长按向右键，我机一直往右移动
key_right_flag = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hero.fire()
            if event.key == pygame.K_LEFT:
                key_left_flag = True
                key_right_flag = False
            if event.key == pygame.K_RIGHT:
                key_left_flag = False
                key_right_flag = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                key_left_flag = False
            if event.key == pygame.K_RIGHT:
                key_right_flag = False

    # 向左键按下，我机往左移动
    if key_left_flag:
        hero.move('left')
    # 向右键按下，我机往右移动
    if key_right_flag:
        hero.move('right')

    screen.blit(screen_bg, (0, 0))
    hero.draw(screen)
    enemy.draw(screen)
    enemy.move()
    rdm_enemy_fire = random.randint(1, 30)
    if rdm_enemy_fire == 16:
        enemy.fire()
    # 子弹移动
    for bullet in hero.bullets:
        bullet.move()

    # 子弹移动
    for bullet in enemy.bullets:
        bullet.move()

    pygame.display.update()
    time.sleep(0.001)

if __name__ == '__main__':
    main()