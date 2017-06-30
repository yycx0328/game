# encoding=utf-8
import sys
import pygame
import time
import random
import configparser


class ConfigHelper:
    ''' 配置文件帮助类 '''
    def __init__(self, var_cfg_file):
        self.config = configparser.ConfigParser()
        with open(var_cfg_file, 'r') as cfg:
            self.config.readfp(cfg)

    # 根据KEY获取配置值
    def get_config(self, var_key):
        return self.config.get('info', var_key)


class Enemy:
    ''' 敌军飞机类，包含飞机构建、移动、发射子弹、越界、爆炸功能 '''

    def __init__(self, var_x, var_y, var_image):
        self.config = ConfigHelper('game.cfg')
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
        self.y += int(self.config.get_config('enemy_y_move_step'))
        if self.direct == 'left':
            # 游戏向左移动超出右边界，开始向右移动
            if self.x >= 0:
                self.x -= int(self.config.get_config('enemy_x_move_step'))
            else:
                self.direct = 'right'
        elif self.direct == 'right':
            # 游戏向右移动超出右边界，开始向左移动
            if self.x <= int(self.config.get_config('screen_width')) - int(self.config.get_config('enemy_width')):
                self.x += int(self.config.get_config('enemy_x_move_step'))
            else:
                self.direct = 'left'

    # 是否超出屏幕下方
    def is_out_screen(self):
        # 当敌机头部移动超出屏幕下方，则返回True
        if self.y >= int(self.config.get_config('screen_height')) - int(self.config.get_config('enemy_height')):
            return True
        else:
            return False

    # 敌军飞机开火
    def fire(self):
        self.bullets.append(EnemyBullet(self.x + int(self.config.get_config('enemy_width'))/2, self.y + int(self.config.get_config('enemy_height')) - 10, './images/enemy-bullet.png'))

    # 飞机爆炸效果
    def bomb(self, var_screen, var_index):
        var_screen.blit(pygame.image.load('./images/enemy-bomb'+str(var_index)+'.png'), (self.x, self.y))


class Hero:
    ''' 我军飞机类 '''
    def __init__(self, var_x, var_y, var_image):
        self.config = ConfigHelper('game.cfg')
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
                self.x -= int(self.config.get_config('hero_x_move_step'))
        # 飞机向右移动，且越界判断
        elif var_direction == 'right':
            if self.x < int(self.config.get_config('screen_width')) - int(self.config.get_config('hero_width')):
                self.x += int(self.config.get_config('hero_x_move_step'))
        elif var_direction == 'up':
            if self.y > int(self.config.get_config('screen_height')) / 2:
                self.y -= int(self.config.get_config('hero_y_move_step'))
        elif var_direction == 'down':
            if self.y < int(self.config.get_config('screen_height')) - int(self.config.get_config('hero_height')):
                self.y += int(self.config.get_config('hero_y_move_step'))

    # 我军飞机开火
    def fire(self):
        self.bullets.append(HeroBullet(self.x + int(self.config.get_config('hero_width')) / 2, self.y - 10, './images/hero-bullet.png'))


class HeroBullet:
    ''' 我军飞机发射的子弹类 '''

    def __init__(self, var_x, var_y, var_image):
        self.config = ConfigHelper('game.cfg')
        self.x = var_x
        self.y = var_y
        self.image = var_image

    # 在屏幕上构建我军飞机发射的子弹
    def draw(self, var_screen):
        var_screen.blit(pygame.image.load(self.image), (self.x, self.y))

    # 子弹向上移动
    def move(self):
        self.y -= int(self.config.get_config('hero_bullet_move_step'))

    # 子弹是否越界
    def is_out_screen(self):
        if self.y <= 0:
            return True
        else:
            return False

    def is_hit_enemy(self, var_enemy):
        if self.x >= var_enemy.x + 10 and self.x <= var_enemy.x + int(self.config.get_config('enemy_width')) - 10 and self.y >= enemy.y+10 and self.y <= var_enemy.y + int(self.config.get_config('enemy_height')) - 10:
            return True
        return False


class EnemyBullet:
    ''' 敌军飞机发射的子弹类 '''
    def __init__(self, var_x, var_y, var_image):
        self.config = ConfigHelper('game.cfg')
        self.x = var_x
        self.y = var_y
        self.image = var_image

    # 在屏幕上构建我军飞机发射的子弹
    def draw(self, var_screen):
        var_screen.blit(pygame.image.load(self.image), (self.x, self.y))

    # 子弹向上移动
    def move(self):
        self.y += int(self.config.get_config('enemy_bullet_move_step'))

    # 判断子弹是否越界
    def is_out_screen(self):
        if self.y >= int(self.config.get_config('screen_width')):
            return True
        else:
            return False

    def is_hit_hero(self, var_hero):
        if self.x >= var_hero.x+10 and self.x <= var_hero.x + int(self.config.get_config('hero_width')) - 10 and self.y >= var_hero.y+10 and self.y <= var_hero.y + int(self.config.get_config('hero_height')) - 10:
            return True
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

# 我军飞机大小：102*126
# 敌军飞机大小：69*99

pygame.init()
config = ConfigHelper('game.cfg')
# 游戏主屏幕宽高
width = int(config.get_config('screen_width'))
height = int(config.get_config('screen_height'))

# 初始化我军飞机的x，y位置
hero_x_pos = (width - int(config.get_config('hero_width'))) / 2
hero_y_pos = height - int(config.get_config('hero_height'))

# 构建屏幕
screen = pygame.display.set_mode((width, height))
# 游戏屏幕背景图
screen_bg = pygame.image.load("./images/bg.png")
# 构建我军飞机
hero = Hero(hero_x_pos, hero_y_pos, './images/hero.png')
# 构建敌军飞机
enemy_image = './images/enemy.png'
enemy = Enemy(random.randint(10, width), 0, enemy_image)

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
        enemy = Enemy(random.randint(10, width), 0, enemy_image)

    rdm_enemy_fire = random.randint(1, 30)
    if rdm_enemy_fire == 16:
        enemy.fire()
    # 子弹移动
    for bullet in hero.bullets:
        bullet.move()
        if bullet.is_hit_enemy(enemy):
            print('我军飞机已击中敌军')


    # 子弹移动
    for bullet in enemy.bullets:
        bullet.move()
        if bullet.is_hit_hero(hero):
            print('敌机已击中我军飞机')

    pygame.display.update()
    time.sleep(0.001)

if __name__ == '__main__':
    main()