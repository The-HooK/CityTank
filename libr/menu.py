import pygame
import os
import sys
import random
from sprites import *
from math import *
from data import *
from pygame.locals import *
from effects import *
from sys import exit


import pygame
import os
import sys
import random
from math import *
from pygame.locals import *
from data import *
from sprites import *
from effects import *
from sys import exit


class Menu:
    def __init__(self, screen):

        self.screen = screen
        self.font = pygame.font.Font(filepath("Abduction II.ttf"), 35)
        self.font2 = pygame.font.Font(filepath("Abduction III.ttf"), 35)
        self.font3 = pygame.font.Font(filepath("Abduction II.ttf"), 50)
        self.option = 1
        self.vehicle = None
        self.veh_pos = (100, 200)
        self.angle = 360
        self.tank= pygame.image.load(filepath("tank2.png")).convert_alpha()
        self.enemies = pygame.image.load(filepath("drone.png"))

    def loop(self):

        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_DOWN:
                        if self.option < 2:
                            self.option += 1
                        else:
                            pass
                    if event.key == K_UP:
                        if self.option > 1:
                            self.option -= 1
                        else:
                            pass
                    if event.key == K_RETURN:
                        if self.option == 1:
                            self.vehicle = "tank"
                            game = Game(self.screen, self.vehicle)
                            game.run()

                        if self.option == 2:
                            pygame.quit()
                            sys.exit()

            class Game(object):

                def __init__(self, screen, veh):

                    self.screen = screen
                    self.veh_type = veh
                    self.size = self.screen.get_size()
                    pygame.mouse.set_visible(False)
                    self.level = 1

                    self.bricks= pygame.sprite.Group()
                    self.bricks_des = pygame.sprite.Group()
                    self.bricks_non = pygame.sprite.Group()
                    self.bullets = pygame.sprite.Group()
                    self.booms = pygame.sprite.Group()
                    self.drones = pygame.sprite.Group()

                    self.city = City(self.bricks, self.bricks_des, self.bricks_non, self.drones, self.level, None)
                    self.enemies = self.city.get_enemies()
                    self.city_size = self.city.get_size()

                    self.clock = pygame.time.Clock()
                    self.timer = 0


                    self.veh_pos = self.city.get_vehicle()
                    self.veh_angle = 360
                    self.vehicle = Tank(self.veh_pos, self.veh_angle)
                    self.turret = Turret(self.veh_pos, self.veh_type, False)

                    self.background = pygame.Surface((self.city_size), 0, 32)
                    self.background2 = pygame.Surface((self.city_size), 0, 32)
                    self.background2.fill((87,87,87))
                    self.bricks_non.draw(self.background2)

                    self.camera = pygame.Rect((0,0), (self.size))
                    self.font4 = pygame.font.Font(filepath("7theb.ttf"), 13)
                    self.font5 = pygame.font.SysFont("Courier New", 16, bold=True)

                def camera_set(self):

                    b_x, b_y = self.vehicle.rect.center
                    self.camera.center = (b_x, b_y)
                    b_x, b_y = self.camera.topleft

                    camera_w, camera_h = (self.camera.width, self.camera.height)
                    city_w, city_h = (self.city_size)


                    if b_x < 0:
                        b_x = 0
                    if b_x > city_w-camera_w:
                        b_x = city_w-camera_w
                    if b_y < 0:
                        b_y = 0
                    if b_y > city_h-camera_h:
                        b_y = city_h-camera_h

                    if city_h < camera_h:
                        b_y = (city_h-camera_h)/2
                    if city_w < camera_w:
                        b_x = (city_w-camera_h)/2

                    self.camera.topleft = (b_x, b_y)

                def clear_sprites(self):
                    for s in self.bricks:
                        pygame.sprite.Sprite.kill(s)
                    for s in self.bricks_des:
                        pygame.sprite.Sprite.kill(s)
                    for s in self.bricks_non:
                        pygame.sprite.Sprite.kill(s)
                    for s in self.bullets:
                        pygame.sprite.Sprite.kill(s)
                    for s in self.booms:
                        pygame.sprite.Sprite.kill(s)
                    for s in self.drones:
                        pygame.sprite.Sprite.kill(s)

                def new_level(self, direction):
                    if direction is "right":
                        self.level += 1
                    if direction is "left":
                        self.level -=1
                    self.veh_ang = self.vehicle.angle
                    self.turr_follow = self.turret.follow
                    self.veh_last_pos = self.veh_pos
                    self.clear_sprites()
                    try:
                        self.city = City(self.bricks, self.bricks_des, self.bricks_non, self.drones, self.level, self.direction)
                    except:
                        raise SystemExit( "Oh SHIT you broke it!")
                    self.enemies = self.city.get_enemies()
                    self.city_size = self.city.get_size()
                    self.veh_pos = self.city.get_vehicle()
                    self.vehicle = Tank(self.veh_pos, self.veh_ang)
                    self.turret = Turret(self.veh_pos, self.veh_type, self.turr_follow)
                    self.background = pygame.Surface((self.city_size), 0, 32)
                    self.background2 = pygame.Surface((self.city_size), 0, 32)
                    self.background2.fill((87,87,87))
                    self.bricks_non.draw(self.background2)
                    self.camera = pygame.Rect((0,0), (self.size))
                    return


                def run(self):

                    while True:

                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == KEYDOWN:
                                if event.key == K_ESCAPE:
                                    return

                        self.clock.tick(24)
                        self.time_passed = self.clock.tick()
                        self.keys = pygame.key.get_pressed()
                        m_x, m_y = pygame.mouse.get_pos()
                        self.score = 0


                        if self.timer == 240:
                            self.chance = random.randint(1,2)
                            if self.chance == 2:
                                self.chance = True
                            else:
                                self.chance = None
                            self.timer = 0



                        self.background.fill((87,87,87))
                        self.background.blit(self.background2, (0,0))
                        self.bricks_des.draw(self.background)

                        for d in self.drones:
                            d.update(self.bricks, self.bullets, self.booms, self.vehicle.rect.center, self.city_size)
                            self.score += 1

                        if self.vehicle.alive == True:
                            self.vehicle.update(self.keys, self.bricks, self.bullets, self.booms)
                            self.turret.update(self.vehicle.rect.center, m_x, m_y, self.camera.topleft, self.keys, self.bullets, self.vehicle.angle)
                            self.background.blit(self.vehicle.image, self.vehicle.rect)
                            self.background.blit(self.turret.image, self.turret.rect)


                        self.bullets.update(self.background, self.bricks, self.booms)
                        self.booms.update(self.background)

                        self.drones.draw(self.background)
                        self.bullets.draw(self.background)

                        self.camera_set()
                        self.screen.blit(self.background, (0,0), self.camera)

                        self.killshow = self.font4.render('Kills '+str(self.enemies - self.score)+' of ' +str(self.enemies), False, (255,255,255))
                        self.healthshow = self.font4.render('Health ', False, (255,255,255))
                        self.reloadshow = self.font4.render('Reload ', False, (255,255,255))

                        pygame.draw.ellipse(self.screen, (255, ((self.vehicle.health*255)/25),0), (90, 20, 10, 13))
                        pygame.draw.ellipse(self.screen, (255, ((self.vehicle.health*255)/25),0), (92+(100*(float(self.vehicle.health)/float(25))), 20, 10, 13))
                        pygame.draw.ellipse(self.screen, (0, 230, 0), (296, 20, 10, 13))
                        pygame.draw.ellipse(self.screen, (0, 230, 0), (298+(100*(float(self.turret.timer)/float(40))),20, 10, 13))

                        self.screen.fill((255,((self.vehicle.health*255)/25),0),(96,20,(100*(float(self.vehicle.health)/float(25))), 13))
                        self.screen.fill((0,230,0),(302, 20, (100*(float(self.turret.timer)/float(40))), 13))

                        self.screen.blit(self.killshow, (5,5))
                        self.screen.blit(self.healthshow, (5, 20))
                        self.screen.blit(self.reloadshow, (205, 20))

                        pygame.display.flip()
                        self.timer += 1

                        if self.vehicle.rect.center[0] > self.city_size[0] or self.vehicle.rect.center[1] > self.city_size[1]:
                            self.direction = "right"
                            self.new_level(self.direction)

                        if self.vehicle.rect.center[0] < 0 or self.vehicle.rect.center[1] < 0 :
                            self.direction = "left"
                            self.new_level(self.direction)
            class City(object):
                def __init__(self, bricks, bricks_des, bricks_non, drones, level, direction):

                    self.level = level
                    self.direction = direction

                    if self.direction == "right":
                        self.spawn = (255,126,0, 255)
                    if self.direction == "left":
                        self.spawn = (255,255,0, 255)
                    if self.direction == None:
                        self.spawn = (0,0,255, 255)

                    if self.level == 1:
                        self.city =  pygame.image.load(filepath("city.png")).convert_alpha()
                    if self.level == 2:
                        self.city =  pygame.image.load(filepath("city1.png")).convert_alpha()
                    if self.level == 0:
                        self.city =  pygame.image.load(filepath("city0.png")).convert_alpha()
                    self.brick = pygame.image.load(filepath("brick.png")).convert_alpha()
                    self.plate = pygame.image.load(filepath("plate.png")).convert_alpha()
                    self.bricks = bricks
                    self.drones = drones
                    self.enemies = 0

                    self.x = self.y = 0
                    collidable = (255, 0, 0, 255)
                    self.height = self.city.get_height()
                    self.width = self.city.get_width()
                    self.vehicle_pos = (0,0)

                    while self.y < self.height:
                        color = self.city.get_at((self.x, self.y))
                        collidable =  (255, 0, 0, 255), (0,0,0,255)
                        top = False
                        bottom = False
                        right = False
                        left = False
                        destroyable = True
                        if color in collidable:
                            if self.y > 0:
                                if self.city.get_at((self.x, self.y-1)) not in collidable:
                                    top = True
                            if self.y < self.height-1:
                                if self.city.get_at((self.x, self.y+1)) not in collidable:
                                    bottom = True
                            if self.x > 0:
                                if self.city.get_at((self.x-1, self.y)) not in collidable:
                                    left = True
                            if self.x < self.width-1:
                                if self.city.get_at((self.x+1, self.y)) not in collidable:
                                    right = True
                            if self.x == 0 or self.y == 0 or self.x == self.width-1 or self.y == self.height-1:
                                destroyable = False
                            if color == collidable[0]:
                                self.bricks.add(Brick((self.x*50, self.y*50), self.brick, top, bottom, right, left, destroyable, bricks_des, bricks_non))
                            if color == collidable[1]:
                                self.bricks.add(Brick((self.x*50, self.y*50), self.plate, top, bottom, right, left, False, bricks_des, bricks_non))
                        if color == self.spawn:
                            self.vehicle_pos = (self.x*50, self.y*50)

                        if color == (0,255,0, 255):

                            self.drones.add(Drone((self.x*50, self.y*50)))
                            self.enemies += 1

                        self.x += 1
                        if self.x >= self.width:
                            self.x = 0
                            self.y += 1


                def get_size(self):
                    return [self.city.get_size()[0]*50, self.city.get_size()[1]*50]

                def get_vehicle(self):
                    return self.vehicle_pos

                def get_enemies(self):
                    return self.enemies


            class Brick(pygame.sprite.Sprite):

                def __init__(self, pos, image,top, bottom, right, left, destroyable, bricks_des, bricks_non):

                    pygame.sprite.Sprite.__init__(self)

                    self.rect = image.get_rect(topleft = pos)
                    self.rect = Rect(self.rect)
                    self.image = image
                    self.pos = pos
                    self.top = top
                    self.bottom = bottom
                    self.right = right
                    self.left = left
                    self.destroyable = destroyable
                    self.health = 30

                    if self.destroyable == True:
                        bricks_des.add(self)
                    else:
                        bricks_non.add(self)

            if __name__ == "__main__":
                pygame.init()
                screen = pygame.display.set_mode((640, 480), 0, 32)
                game = Game(screen, "tank")
                game.run()



            ren = self.font3.render("City Tank", 1, (255, 0, 0))
            self.screen.blit(ren, (400-ren.get_width()/2 , 50))
            ren = self.font.render("Start", 1, (255, 0, 0))
            self.screen.blit(ren, (400-ren.get_width()/2, 210))

            ren = self.font.render("Exit", 1, (255, 0, 0))
            self.screen.blit(ren, (400-ren.get_width()/2, 330))
            if self.option == 1:
                ren = self.font2.render("Start", 1, (0, 230, 0))
                self.screen.blit(ren, (400-ren.get_width()/2, 210))
                self.image = pygame.transform.rotozoom(self.tank, self.angle, 2.5)
                self.screen.blit(self.image, self.veh_pos)


            if self.option == 2:
                ren = self.font2.render("Exit", 1, (0, 230, 0))
                self.image = pygame.transform.rotozoom(self.tank, self.angle, 2.5)
                self.screen.blit(ren, (400-ren.get_width()/2, 330))

            pygame.display.flip()
            self.screen.fill((0,0,0))
            self.angle += 0.3
