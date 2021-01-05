#-----!!!!SPACE INVADERS!!!!-----

import pygame
from pygame.locals import *

#----------------------------------------------------------------------

class Ship():

    def __init__(self, screen_rect):

        #self.image = pygame.image.load("spaceship.png")
        self.image = pygame.image.load("ball1.png")
        self.image = pygame.transform.scale(self.image, (100,50))

        self.rect = self.image.get_rect()

        # put ship bottom, center x 
        self.rect.bottom = screen_rect.bottom 
        self.rect.centerx = screen_rect.centerx

        self.move_x = 0

        self.shots = []
        self.shots_count = 0

        self.max_shots = 2

    #--------------------

    def event_handler(self, event):

        #print "debug: Ship.event_handler"

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.move_x = -5
            elif event.key == K_RIGHT:
                self.move_x = 5
            elif event.key == K_SPACE:
                if len(self.shots) < self.max_shots:
                    self.shots.append(Bullet(self.rect.centerx, self.rect.top))

        if event.type == KEYUP:
            if event.key in (K_LEFT, K_RIGHT):
                self.move_x = 0

    def update(self):

        #print "debug: Ship.update: move_x", self.move_x
        self.rect.x += self.move_x

        for s in self.shots:
            s.update()

        for i in range(len(self.shots)-1, -1, -1):
            print "debug: Ship.update: testing bullet ", i
            if not self.shots[i].is_alive:
                print "debug: Ship.update: removing bullet ", i
                del self.shots[i]

    #--------------------

    def draw(self, screen):

        #print "debug: Ship.draw"

        screen.blit(self.image, self.rect.topleft)

        for s in self.shots:
            s.draw(screen)

    def bullet_detect_collison(self, enemy_list):

        for s in self.shots:
            for e in enemy_list:
                if pygame.sprite.collide_circle(s, e):
                    s.is_alive = False
                    e.is_alive = False

#----------------------------------------------------------------------

class Bullet():

    def __init__(self, x, y):

        #self.image = pygame.image.load("SingleBullet.png")
        self.image = pygame.image.load("ball2.png")
        self.image = pygame.transform.scale(self.image, (25,25))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.is_alive = True

    #--------------------

    def update(self):

        self.rect.y -= 15

        if self.rect.y < 0:
            self.is_alive = False

    #--------------------

    def draw(self, screen):

        screen.blit(self.image, self.rect.topleft)

#----------------------------------------------------------------------

class Enemy():

    def __init__(self, x, y):

        self.image = pygame.image.load("ball3.png")

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.is_alive = True

    #--------------------

    def update(self):

        self.rect.y += 1

        #~ if self.rect.y < 0:
            #~ self.is_alive = False

    #--------------------

    def draw(self, screen):

        screen.blit(self.image, self.rect.topleft)

#----------------------------------------------------------------------

class Game():

    def __init__(self):

        pygame.init()

        w, h = 800, 800
        self.screen = pygame.display.set_mode((w,h))

        pygame.mouse.set_visible(False)

        self.ship = Ship(self.screen.get_rect())

        self.enemies = []

        for i in range(100, 800, 100):
            self.enemies.append(Enemy(i, 100))

        font = pygame.font.SysFont("", 72)
        self.text_paused = font.render("PAUSED", True, (255, 0, 0))
        self.text_paused_rect = self.text_paused.get_rect(center=self.screen.get_rect().center)

    #-----MAIN GAME LOOP-----

    def run(self):

        clock = pygame.time.Clock()

        RUNNING = True
        PAUSED = False

        while RUNNING:

            clock.tick(30)

            #--- events ---

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    RUNNING = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        RUNNING = False

                    if event.key == K_p:
                        PAUSED = not PAUSED

                if not PAUSED:
                    self.ship.event_handler(event)

            #--- changes ---
            if not PAUSED:

                self.ship.update()

                for e in self.enemies:
                    e.update()

                self.ship.bullet_detect_collison(self.enemies)

                for i in range(len(self.enemies)-1, -1, -1):
                    print "debug: Ship.update: testing bullet ", i
                    if not self.enemies[i].is_alive:
                        print "debug: Ship.update: removing bullet ", i
                        del self.enemies[i]

            #--- draws ---

            self.screen.fill((0,0,0))

            self.ship.draw(self.screen)

            for e in self.enemies:
                e.draw(self.screen)

            if PAUSED:
                self.screen.blit(self.text_paused, self.text_paused_rect)

            pygame.display.update()

        #--- quit ---

        pygame.quit()

#---------------------------------------------------------------------

Game().run()
