import pygame

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
