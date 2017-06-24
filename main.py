# encoding=utf-8
import sys
import pygame
import time
import random


class Enemy:
    '''
    敌军飞机类，包含飞机构建、移动、发射子弹、越界、爆炸功能
    '''
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
            if bullet.is_out_screen():
                self.bullets.remove(bullet)
            else:
                bullet.draw(var_screen)

    # 控制飞机左右移动
    def move(self):
        self.y += 3
        if self.direct == 'left':
            if self.x >= 0:
                self.x -= 8
            else:
                self.direct = 'right'
        elif self.direct == 'right':
            if self.x <= 725:
                self.x += 8
            else:
                self.direct = 'left'

    # 是否超出屏幕下方
    def is_out_screen(self):
        if self.y >= 510:
            return True
        else:
            return False

    # 敌军飞机开火
    def fire(self):
        pass
        self.bullets.append(EnemyBullet(self.x + 35, self.y + 95, './images/enemy-bullet.png'))

    # 飞机爆炸效果
    def bomb(self, var_screen, var_index):
        var_screen.blit(pygame.image.load('./images/enemy-bomb'+str(var_index)+'.png'), (self.x, self.y))


class Hero:
    '''
    我军飞机类
    '''
    def __init__(self, var_x, var_y, var_image):
        self.x = var_x
        self.y = var_y
        self.image = var_image
        self.bullets = []

    # 在屏幕上构建我军飞机
    def draw(self, var_screen):
        var_screen.blit(pygame.image.load(self.image), (self.x, self.y))
        for bullet in self.bullets:
            if bullet.is_out_screen():
                self.bullets.remove(bullet)
            else:
                bullet.draw(var_screen)

    # 控制我军飞机左右移动
    def move(self, var_direction):
        # 飞机向左移动，且越界判断
        if var_direction == 'left':
            if self.x > 0:
                self.x -= 5
        # 飞机向右移动，且越界判断
        elif var_direction == 'right':
            if self.x < 698:
                self.x += 5
        elif var_direction == 'up':
            if self.y > 300:
                self.y -= 5
        elif var_direction == 'down':
            if self.y < 498:
                self.y += 5

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

    # 子弹是否越界
    def is_out_screen(self):
        if self.y <= 0:
            return True
        else:
            return False


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

    # 判断子弹是否越界
    def is_out_screen(self):
        if self.y >= 800:
            return True
        else:
            return False


class HeroDirectionPriority:
    '''
    我军飞机移动方向优先级，这个类的主要功能就是保证在多个方向按键同时按下后，
    释放任何一个方向键都不会导致我军飞机停止移动，只有当四个方向按键都释放后，
    我军飞机才会停止移动。
    '''

    def __init__(self):
        self.direction_priority = {'left': 0, 'right': 0, 'up': 0, 'down': 0}

    # 获取最大优先级值
    def get_max_priority(self):
        return max(self.direction_priority.items(), key=lambda x: x[1])

    # 设置最大优先级值
    def set_max_priority(self, var_key):
        max_priority = self.get_max_priority()
        new_priority = max_priority[1] + 1
        self.direction_priority[var_key] = new_priority

    # 按键释放后优先级重置为0
    def set_default(self, var_key):
        self.direction_priority[var_key] = 0

pygame.init()
# 游戏主屏幕宽高
width = 800
height = 600

# 初始化我军飞机的x，y位置
hero_x_pos = 360
hero_y_pos = 480

# 构建屏幕
screen = pygame.display.set_mode((width, height))
# 游戏屏幕背景图
screen_bg = pygame.image.load("./images/bg.png")
# 构建我军飞机
hero = Hero(hero_x_pos, hero_y_pos, './images/hero.png')
# 构建敌军飞机
enemy_image = './images/enemy.png'
enemy = Enemy(random.randint(10, 800), 0, enemy_image)

hero_direct_priority = HeroDirectionPriority()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hero.fire()
            if event.key == pygame.K_LEFT:
                hero_direct_priority.set_max_priority('left')
            if event.key == pygame.K_RIGHT:
                hero_direct_priority.set_max_priority('right')
            if event.key == pygame.K_UP:
                hero_direct_priority.set_max_priority('up')
            if event.key == pygame.K_DOWN:
                hero_direct_priority.set_max_priority('down')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                hero_direct_priority.set_default('left')
            elif event.key == pygame.K_RIGHT:
                hero_direct_priority.set_default('right')
            elif event.key == pygame.K_UP:
                hero_direct_priority.set_default('up')
            elif event.key == pygame.K_DOWN:
                hero_direct_priority.set_default('down')

    max_prio = hero_direct_priority.get_max_priority()
    if max_prio[1] > 0:
        hero.move(max_prio[0])

    screen.blit(screen_bg, (0, 0))
    hero.draw(screen)
    enemy.draw(screen)
    enemy.move()

    if enemy.is_out_screen():
        enemy.bomb(screen, 1)
        enemy.bomb(screen, 2)
        enemy.bomb(screen, 3)
        enemy = Enemy(random.randint(10, 800), 0, enemy_image)

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