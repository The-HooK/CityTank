"""
Dans ce module sont contenues les classes de tous les véhicules
"""

import pygame
from pygame.locals import *
import os
import sys
import random
import math

from libr.data import *
from libr.effects import *


class Tank(pygame.sprite.Sprite): #définiton de la classe "Tank"

    def __init__(self, pos, angle):# Constructeur de la classe
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filepath("tank.png")).convert_alpha()
        self._image = self.image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)
        self.health = 25
        self.alive = True
        self.speed = 5
        self.angle = angle
        self.timer = 3
        self.timerstart = 0
        self.x, self.y = self.rect.center
        self.bullet_s = pygame.mixer.Sound(filepath("bullet.wav"))
        self.bullet_s.set_volume(.05)

    def rotate(self): #Definition de la fonction rotate qui permet de faire tourner le tank
        center = self.rect.center
        self.image = pygame.transform.rotozoom(self._image, self.angle, 1.0)
        self.rect = self.image.get_rect(center = center)

    def update(self, keys, bricks, bullets, booms): # Gestion du vehicule (position, angle, vie)
        self._rect = Rect(self.rect)
        self._rect.center = self.x, self.y
        self.rotate()
        turn_speed = 3

        if keys[K_UP] or keys[K_w]:
            self.x += math.sin(math.radians(self.angle))*-self.speed
            self.y += math.cos(math.radians(self.angle))*-self.speed
        if keys[K_DOWN] or keys[K_s]:
            self.x += math.sin(math.radians(self.angle))*self.speed
            self.y += math.cos(math.radians(self.angle))*self.speed
        if keys[K_LEFT] or keys[K_a]:
            self.angle += turn_speed
        if keys[K_RIGHT] or keys[K_d]:
            self.angle -= turn_speed
        if keys[K_SPACE]:
            if self.timer >= 3:
                self.timer = self.timerstart
                self.b_size = "small"
                bullets.add(Bullet(self.rect.center, self.angle, self.b_size, "vehicle"))
                self.bullet_s.play()
        if self.timer < 3:
            self.timer += 1

        if self.angle > 360:
            self.angle = self.angle-360
        if self.angle <0:
            self.angle = self.angle+360

        self.rect.center = self.x, self.y

        x = self.rect.centerx
        y = self.rect.centery
        _x = self._rect.centerx
        _y = self._rect.centery
        for b in bricks:
            if self.rect.colliderect(b.rect):
                if _x+21 <= b.rect.left and x+21 > b.rect.left:
                    if b.left == True:
                        self.x = b.rect.left-21
                if _x-21 >= b.rect.right and x-21 < b.rect.right:
                    if b.right == True:
                        self.x = b.rect.right+21
                if _y+21 <= b.rect.top and y+21 > b.rect.top:
                    if b.top == True:
                        self.y = b.rect.top-21
                if _y-21 >= b.rect.bottom and y-21 < b.rect.bottom:
                    if b.bottom == True:
                        self.y = b.rect.bottom+21

        for b in bullets:
            if self.rect.colliderect(b.rect) and b.who != "vehicle":
                b_size = b.get_size()
                pygame.sprite.Sprite.kill(b)
                if b_size == "small":
                    booms.add(Boom(b.rect.center, "small"))
                    self.health -= 1
                if b_size == "big":
                    booms.add(Boom(b.rect.center, "big"))
                    self.health -=5

        if self.health <= 0:
            booms.add(Boom(self.rect.center, "huge"))
            self.alive = False
            self.health = 0

class Turret(pygame.sprite.Sprite):

    def __init__(self, pos, veh, follow):# Constructeur de la classe
        pygame.sprite.Sprite.__init__(self)
        self.veh_type = veh
        self.image = pygame.image.load(filepath("turret.png")).convert_alpha()
        self.timer = 40
        self.timer_start = self.timer
        self.size = "big"
        self.bang_s = pygame.mixer.Sound(filepath("bang.wav"))
        self.speed = 3
        self.bang_s.set_volume(1.0)
        self._image = self.image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)
        self.angle = 360
        self.timer = 40
        self.wait_timer = 5
        self.timer_restart = 0
        self.x, self.y = self.rect.center
        self.follow = follow

    def rotate(self):
        center = self._rect.center
        self.image = pygame.transform.rotozoom(self._image, self.angle, 1.0)
        self.rect = self.image.get_rect(center = center)

    def update(self, pos, mx, my, camera, keys, bullets, tank_angle):
        self._rect = Rect(self.rect)
        self._rect.center = pos
        self.tank_angle = tank_angle
        c_x, c_y = camera
        t_x, t_y = self.rect.center
        _t_x = t_x-c_x
        _t_y = t_y-c_y
        m_x = mx+13
        m_y = my+13
        xd = m_x - _t_x
        yd = m_y - _t_y
        if keys[K_m]:
            if self.wait_timer >= 5:
                self.follow = not self.follow
                self.wait_timer = self.timer_restart
        if self.angle != self.tank_angle:
            if self.angle < self.tank_angle:
                if math.fabs(self.angle - self.tank_angle) < 180:
                    self.angle +=self.speed
                else:
                    self.angle -=self.speed
            else:
                if math.fabs(self.angle - self.tank_angle) < 180:
                    self.angle -=self.speed
                else:
                    self.angle +=self.speed
            if math.fabs(self.angle - self.tank_angle) < self.speed+.5:
                self.angle = self.tank_angle
        else:
            self.angle = self.tank_angle

        self.rotate()
        if self.angle > 360:
            self.angle = self.angle-360
        if self.angle <0:
            self.angle = self.angle+360
        if self.wait_timer < 5:
            self.wait_timer += 1


        if pygame.mouse.get_pressed()[0] is 1:
            if self.timer >= self.timer_start:
                self.timer = self.timer_restart
                self.b_size = self.size
                bullets.add(Bullet(self.rect.center, self.angle, self.b_size, "vehicle"))
                self.bang_s.play()
        if self.timer < 40:
            self.timer += 1


class Drone(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filepath("drone.png")).convert_alpha()
        self._image = self.image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)
        self.x, self.y = self.rect.center

        self.speed = 3
        self.angle = random.randint(1,360)
        self.target_angle = self.angle
        self.timer = 3
        self.timer_reset = 3
        self.health = 5
        self.track = False
        self.b_timer = 10
        self.b_timer_reset = 0
        self.bullet_s = pygame.mixer.Sound(filepath("bullet.wav"))
        self.bullet_s.set_volume(.25)
    def rotate(self):
        center = self._rect.center
        self.image = pygame.transform.rotozoom(self._image, self.angle, 1.0)
        self.rect = self.image.get_rect(center = center)

    def get_distance(self):
        x, y = self.rect.center
        v_x, v_y = self.veh_pos
        self.veh_dis = (x-v_x)**2 + (y-v_y)**2
        self.veh_dis = math.sqrt(self.veh_dis)

    def update(self, bricks, bullets, booms, veh_pos, city_size):
        self._rect = Rect(self.rect)
        self._rect.center = self.x, self.y
        self.veh_pos = veh_pos
        self.rotate()
        self.get_distance()
        v_x, v_y = self.veh_pos
        d_x, d_y = self.x, self.y
        xd= v_x - d_x
        yd = v_y - d_y
        if self.veh_dis <= 800:
            self.target_angle = math.atan2(xd, yd)*(180/math.pi) +180
            self.track = True

        if self.track == True:
            if self.veh_dis >= 200:
                self.y += math.cos(math.radians(self.angle))*-self.speed
                self.x += math.sin(math.radians(self.angle))*-self.speed
            if self.angle != self.target_angle:
                if self.angle < self.target_angle:
                    if math.fabs(self.angle - self.target_angle) < 180:
                        self.angle +=self.speed
                    else:
                        self.angle -=self.speed
                else:
                    if math.fabs(self.angle - self.target_angle) < 180:
                        self.angle -=self.speed
                    else:
                        self.angle +=self.speed
                if math.fabs(self.angle - self.target_angle) < self.speed+1:
                    self.angle = self.target_angle
            else:
                self.angle = self.target_angle

            if self.angle == self.target_angle and self.veh_dis <= 300:
                if self.b_timer >= 20:
                    self.b_timer = self.b_timer_reset
                    bullets.add(Bullet(self.rect.center, self.angle, "small", "drone"))
                    self.bullet_s.play()
            if self.b_timer < 20:
                self.b_timer += 1

            self.rect.center = self.x, self.y
            x = self.rect.centerx
            y = self.rect.centery
            _x = self._rect.centerx
            _y = self._rect.centery

            for b in bricks:
                if self.rect.colliderect(b.rect):
                    if self.rect.colliderect(b.rect):
                        if _x+12 <= b.rect.left and x+12 > b.rect.left:
                            if b.left == True:
                                self.x = b.rect.left-12
                        if _x-12 >= b.rect.right and x-12 < b.rect.right:
                            if b.right == True:
                                self.x = b.rect.right+12
                        if _y+12 <= b.rect.top and y+12 > b.rect.top:
                            if b.top == True:
                                self.y = b.rect.top-12
                        if _y-12 >= b.rect.bottom and y-12 < b.rect.bottom:
                            if b.bottom == True:
                                self.y = b.rect.bottom+12
        for b in bullets:
            if self.rect.colliderect(b.rect) and b.who != "drone":
                b_size = b.get_size()
                pygame.sprite.Sprite.kill(b)
                if b_size == "small":
                    booms.add(Boom(b.rect.center, "small"))
                    self.health -= 1
                if b_size == "big":
                    booms.add(Boom(b.rect.center, "big"))
                    self.health -=5

        if self.health <= 0:
            pygame.sprite.Sprite.kill(self)
            booms.add(Boom(self.rect.center, "large"))

        if self.angle > 360:
            self.angle = self.angle-360
        if self.angle <0:
            self.angle = self.angle+360
