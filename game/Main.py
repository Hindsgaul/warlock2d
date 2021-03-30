# import the pygame module, so you can use it

import pygame
import math
import numpy

#from game.Character import Character
from game.Math import Math
from game.Hookshot import Hookshot
from game.SmashHit import SmashHit
from game.Fireball import Fireball
from game.Wall import Wall
from game.CharHUD import CharHUD
from game.CharInput import CharInput

SCREENWIDTH = 720
SCREENHEIGHT = 450

pygame.init()
# load and set the logo
logo = pygame.image.load("logo32x32.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("minimal program")

clock = pygame.time.Clock()

spriteFloors = []
spriteChars = []
spriteSmashes = []
spriteHookshots = []

# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)
screen.fill((255, 255, 255))

keys = pygame.key.get_pressed()

ply1ctrls = list()
ply2ctrls = list()

ply1ctrls.extend((keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_j], keys[pygame.K_i],
                  keys[pygame.K_DOWN], keys[pygame.K_k], keys[pygame.K_l]))

ply2ctrls.extend((keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_f], keys[pygame.K_t],
                  keys[pygame.K_s], keys[pygame.K_g], keys[pygame.K_h]))


spriteFireballs = list()

class Char:

    def __init__(self, x, y, hudx, controls):
        self.imageright1, self.imageright2, self.imageright3, self.imageright4 = pygame.image.load("wiz1.png"), \
            pygame.image.load("wiz2.png"), pygame.image.load("wiz3.png"), pygame.image.load("wiz4.png")
        self.imageleft1, self.imageleft2, self.imageleft3, self.imageleft4 = pygame.image.load("wizl1.png"), \
            pygame.image.load("wizl2.png"), pygame.image.load("wizl3.png"), pygame.image.load("wizl4.png")
        self.dashimage = pygame.image.load("dash.png")
        self.spawnx = x - self.imageright1.get_rect().width / 2
        self.spawny = y
        self.rect = pygame.Rect(self.spawnx, self.spawny, self.imageright1.get_rect().width, self.imageright1.get_rect().height)
        print(self.rect.width)
        print(self.rect.height)
        self.movementSpeed = 6
        self.xforce, self.yforce = 0, 0
        self.isJump = False
        self.movementDirection = "none"
        self.lives = 3

        self.moveindex = 1

        #Midlertidig
        self.printcounter = 0
        #Midlertidig

        #Tests#
        self.movelockx = 0
        self.movelocky = 0
        #Tests#

        self.multipliery = 0
        self.multiplierx = 0

        # For the cooldowns
        self.fireballcooldown = 1
        self.lastfireballtimer = 0
        self.fireballtickshot = 0

        self.hookcooldown = 4
        self.lasthooktimer = 0
        self.hooktickshot = 0

        self.smashcooldown = 1
        self.lastsmashtimer = 0
        self.smashtickshot = 0

        self.jumpcooldown = 0.01
        self.lastjumptimer = 0
        self.jumptickshot = 0

        # For the receiving hits
        self.smashhitdirection = ""
        self.smashhittimer = 0
        self.smashhittick = 0
        self.smashhitduration = 0.5
        self.smashhitpower = 2

        self.fireballhittimer = 0
        self.fireballhittick = 0
        self.fireballhiteffectsec = 0.5
        self.fireballhitdirection = ""
        self.fireballhitpower = 5

        self.beingHooked = False
        self.isHit = False
        # For the roll
        # Cooldown
        self.rollcooldown = 1
        self.lastrolltimer = 0
        self.rolltickshot = 0

        # roll duration and speed
        self.rollhittimer = 0
        self.rollhittick = 0
        self.rollhitduration = 0.3
        self.rollpower = 5

        self.isRoll = False

        self.flyingToHook = False

        self.unmoveable = False

        self.vup, self.vdown = 1, 0.3
        self.knockbackbonus = 0
        self.name = "MaddyIce"
        self.controls = controls
        self.hud = CharHUD(hudx, self.name, self.knockbackbonus, self.lives, screen)
        self.input = CharInput(controls)

    def moveLeft(self):
        self.movementDirection = "left"
        move = True

        if not self.left_check() and not self.flyingToHook and not self.isRoll:
            self.xforce -= self.movementSpeed
            #self.rect.x -= self.movementSpeed

    def moveRight(self):
        self.movementDirection = "right"
        if not self.right_check() and not self.flyingToHook and not self.isRoll:
            self.xforce += self.movementSpeed
            #self.rect.x += self.movementSpeed


    def roll(self):
        if not self.isRoll and self.lastrolltimer == 0:
            if self.movementDirection == "right":
                self.rollpower = 10
            else:
                self.rollpower = -10
            self.rolltickshot = pygame.time.get_ticks()
            self.lastrolltimer = 0.1  # starter tick
            self.isRoll = True
            if self.rollhittimer == 0:
                self.rollhittick = pygame.time.get_ticks() - 0.1
                self.rollhittimer = 0.1  # starter tick

    def rolldurationupdate(self):
        if self.rollhittimer > 0:
            self.xforce += self.rollpower
            if self.isRoll and self.rollpower > 0:
                screen.blit(self.dashimage, (self.rect.x - self.rect.width, self.rect.y))
            elif self.isRoll and self.rollpower < 0:
                screen.blit(self.dashimage, (self.rect.x + self.rect.width, self.rect.y))
            self.rollhittimer = (pygame.time.get_ticks() - self.rollhittick) / 1000  # calculate how many seconds

        if self.rollhittimer > self.rollhitduration:
            self.isRoll = False
            self.rollhittimer = 0

    def jump(self):
        if not self.isJump and self.ground_check() and self.lastjumptimer == 0:
            self.isJump = True
            #self.lastjumptimer, self.jumptickshot = self.action_starter(self.lastjumptimer, self.jumptickshot)

    def shootfireball(self):
        self.lastfireballtimer, self.fireballtickshot = self.action_starter(self.lastfireballtimer, self.fireballtickshot, Fireball(self))

    def shoothook(self):
        self.lasthooktimer, self.hooktickshot = self.action_starter(self.lasthooktimer, self.hooktickshot, Hookshot(self))

    def action_starter(self, timer, tickshot, obj = ""):
        if timer == 0:
            tickshot = pygame.time.get_ticks()
            if isinstance(obj, Fireball):
                if self.input.up:
                    spriteFireballs.append(Fireball(self, "up"))
                elif self.input.down:
                    spriteFireballs.append(Fireball(self, "down"))
                else:
                    spriteFireballs.append(Fireball(self))
            elif isinstance(obj, Hookshot):
                spriteHookshots.append(Hookshot(self))

            timer = 0.1
        return timer, tickshot

    def check_for_hook(self):
        for hook in spriteHookshots:
            if hook.char == self:
                if hook.targethit:
                    self.flyingToHook = True
                    mag = magnitude(hook, self)
                    self.movelockx += (20 * math.cos(mag))
                    self.movelocky += (5 * math.sin(mag))
                if self.rect.colliderect(hook):
                    self.flyingToHook = False
                    spriteHookshots.remove(hook)
                    break
                if self.isHit and self.flyingToHook:
                    self.flyingToHook = False
                    self.movelockx = 0
                    self.movelocky = 0
                    spriteHookshots.remove(hook)

    def smash(self):
        if self.lastsmashtimer == 0:
            self.smashtickshot = pygame.time.get_ticks()
            spriteSmashes.append(SmashHit(self, spriteChars))
            self.lastsmashtimer = 0.1  # starter tick

    def check_for_hits(self):

        self.isHit = False

        # Check for fireball
        if not self.isRoll:
            for fireball in spriteFireballs:
                if fireball.rect.colliderect(self):
                    if not fireball.owner == self:
                        self.isHit = True
                        mag = (magnitude(self, fireball))
                        self.multipliery = math.sin(mag)
                        self.multiplierx = math.cos(mag)

                        self.knockbackbonus += 4
                        if self.fireballhittimer == 0:
                            self.fireballhittick = pygame.time.get_ticks() - 0.1
                            self.fireballhittimer = 0.1  # starter tick
                        spriteFireballs.remove(fireball)

        if self.fireballhittimer > 0:

            self.xforce += ((self.fireballhitpower * self.knockbackbonus/5) * self.multiplierx)
            if not self.ground_check() or self.multipliery < 0:
                self.yforce += ((self.fireballhitpower * self.knockbackbonus / 5) * self.multipliery)

            self.fireballhittimer = (pygame.time.get_ticks() - self.fireballhittick) / 1000  # calculate how many seconds
            self.fireballhitpower -= 0.3
            #print(self.fireballhitpower)

        if self.fireballhittimer > self.fireballhiteffectsec:
            self.fireballhitpower = 5
            self.fireballhittimer = 0

        # Check for smashes
        if not self.isRoll:
            for smash in spriteSmashes:
                if smash.rect.colliderect(self):
                    if smash.owner != self:
                        self.isHit = True
                        if smash.direction == "right":
                            self.smashhitdirection = "right"
                        else:
                            self.smashhitdirection = "left"
                        spriteSmashes.remove(smash)
                        self.knockbackbonus += 5
                        if self.smashhittimer == 0:
                            self.smashhittick = pygame.time.get_ticks() - 0.1
                            self.smashhittimer = 0.1  # starter tick
                        break
        if self.smashhittimer > 0:
            if self.smashhitdirection == "right":
                self.xforce += self.smashhitpower * (self.knockbackbonus * 0.3)
            else:
                self.xforce -= self.smashhitpower * (self.knockbackbonus * 0.3)
            self.smashhittimer = (pygame.time.get_ticks() - self.smashhittick) / 1000  # calculate how many seconds
            self.smashhitpower -= 0.3

        if self.smashhittimer > self.smashhitduration:
            self.smashhitpower = 5
            self.smashhittimer = 0

        for hook in spriteHookshots:
            if hook.char != self:
                if hook.rect.colliderect(self):
                    self.beingHooked = True
                    spriteHookshots.remove(hook)

        if self.beingHooked:
            for opponent in spriteChars:
                if opponent != self:
                    mag = magnitude(self, opponent)
                    self.movelockx -= (20 * math.cos(mag))
                    self.movelocky -= (5 * math.sin(mag))
                    if self.rect.colliderect(opponent):
                        self.beingHooked = False
                        # spriteHookshots.remove(hook)
                        break


        if self.isHit and self.flyingToHook:
            self.beingHooked = False
            self.movelockx = 0
            self.movelocky = 0
            #spriteHookshots.remove(hook)

        if self.isHit:
            self.vdown = 0.3

    def moveDown(self):
        if self.ground_check() and not self.isJump:
            if self.ground_check().rect.height <= 16:
                self.vdown = 0.3
                self.yforce += 26
            #self.rect.y += 26

    def keypresses(self):
        self.input.update(self.controls)

        # Move to the right
        if self.input.right:
            self.moveRight()

        # Move to the left
        elif self.input.left:
            self.moveLeft()

        if keys[pygame.K_p]:
            print(self.rect)
            self.knockbackbonus += 1

        # Jump
        if self.input.up:
            self.jump()

        # Shoot fireball
        if self.input.shoot:
            self.shootfireball()

        if self.input.hit:
            self.smash()

        if self.input.down:
            self.moveDown()

        if self.input.hook:
            self.shoothook()

        if self.input.roll:
            self.roll()

    def refresh_cooldown(self, timer, tickshot, cooldown):
        if timer > 0:
            timer = (pygame.time.get_ticks() - tickshot) / 1000  # calculate how many seconds
        if timer > cooldown:
            timer = 0

        return timer, tickshot, cooldown

    def check_for_cooldowns(self):
        self.lastfireballtimer, self.fireballtickshot, self.fireballcooldown = self.refresh_cooldown(self.lastfireballtimer, self.fireballtickshot, self.fireballcooldown)
        self.lastsmashtimer, self.smashtickshot, self.smashcooldown = self.refresh_cooldown(self.lastsmashtimer, self.smashtickshot, self.smashcooldown)
        self.lasthooktimer, self.hooktickshot, self.hookcooldown = self.refresh_cooldown(self.lasthooktimer, self.hooktickshot, self.hookcooldown)
        self.lastrolltimer, self.rolltickshot, self.rollcooldown = self.refresh_cooldown(self.lastrolltimer, self.rolltickshot, self.rollcooldown)
        self.lastjumptimer, self.jumptickshot, self.jumpcooldown = self.refresh_cooldown(self.lastjumptimer, self.jumptickshot, self.jumpcooldown)

    def gravity_and_jump(self):
        if self.isJump:
            if self.vup > 0.3:
                self.yforce -= 20 * self.vup
                #self.rect.y -= 25 * self.vup
                self.vup -= 0.11
            else:
                self.vup = 1
                self.isJump = False
        elif self.ground_check():
            self.rect.bottom = self.ground_check().rect.top
        else:
            if not self.ground_check():
                self.yforce += 20 * self.vdown

                if self.ground_check():
                    self.rect.bottom = self.ground_check().rect.top

                if self.vdown < 1:
                    self.vdown += 0.05
            else:
                self.vdown = 0.3

    def check_for_top(self):
        for wall in spriteFloors:
            if self.rect.top + self.yforce <= wall.rect.bottom and self.rect.top + self.yforce >= wall.rect.centery and \
                self.rect.right >= wall.rect.left and self.rect.left <= wall.rect.right:
                if wall.rect.height <= 16:
                    self.unmoveable = True
                else:
                    self.rect.top = wall.rect.bottom
                    self.yforce = 0
                    self.vup = 0.3


    def ground_check(self):
        onground = None
        for floor in spriteFloors:
            if floor.rect.top <= self.rect.bottom + self.yforce <= floor.rect.top + 25 \
                    and self.rect.left + self.rect.width * 0.8 + self.xforce >= floor.rect.left and \
                    self.rect.right - self.rect.width * 0.8 + self.xforce <= floor.rect.right:
                onground = floor
                break
        return onground

    def right_check(self):
        wall = None
        for floor in spriteFloors:
            if (self.rect.left + self.xforce <= floor.rect.left <= self.rect.right + self.xforce <= floor.rect.right
                    and floor.rect.top <= self.rect.centery + self.yforce <= floor.rect.bottom):
                wall = floor
                break
        return wall

    def left_check(self):
        wall = None
        for floor in spriteFloors:
            if (floor.rect.right >= self.rect.left + self.xforce >= floor.rect.left
                    and self.rect.left + self.rect.width + self.xforce >= floor.rect.left
                    and floor.rect.top <= self.rect.centery + self.yforce <= floor.rect.bottom):
                wall = floor
                break
        return wall

    def update(self):

        #check for hits
        self.rolldurationupdate()
        self.check_for_hits()

        self.check_for_cooldowns()

        self.keypresses()

        # hud update
        self.hud.update(self.knockbackbonus, self.lives, screen)

        self.check_for_hook()

        self.gravity_and_jump()

        if self.ground_check():
            if self.yforce > 0:
                self.yforce = 0
            if self.lastjumptimer == 0:
                self.jumptickshot = pygame.time.get_ticks()
                self.lastjumptimer = 0.1  # starter tick

        if self.check_for_top():
            print("")
        elif self.left_check():
            print("LEFT CHECK")
            wall = self.left_check()
            if not self.unmoveable:
                if self.rect.left < wall.rect.right:
                    print("left = right")
                    self.xforce = 0
                    #self.rect.left = wall.rect.right
        elif self.right_check():
            wall = self.right_check()
            if not self.unmoveable:
                if self.rect.right < wall.rect.left:
                    print("right 0 left")
                    self.xforce = 0
                    #self.rect.right = wall.rect.left
        self.unmoveable = False

        if not self.movelockx == 0 and not self.movelocky == 0:
            print(self.movelockx)
            print(self.movelocky)
            self.rect.x += self.movelockx
            self.rect.y += self.movelocky
        elif self.isRoll:
            self.rect.x += self.xforce
        else:
            self.rect.x += self.xforce
            self.rect.y += self.yforce

       # for floor in spriteFloors:
        #    if self.rect.right >= floor.rect.left and self.rect.left <= floor.rect.right and \
        #            self.rect.bottom > floor.rect.top and self.rect.top <= floor.rect.top:
       #         print(self.printcounter)
       #         self.printcounter += 1
       #         print("TEEEEEEST")
       #         self.rect.x -= self.xforce

        #self.rect.y -= self.yforce
        self.movelockx = 0
        self.movelockx = 0

        # Change lives and respawn
        if self.rect.y <= 0 or self.rect.x <= 0 or self.rect.x >= SCREENWIDTH or self.rect.y >= SCREENHEIGHT or self.rect.bottom >= SCREENHEIGHT:
            self.lives -= 1
            self.knockbackbonus = 0
            self.flyingToHook = False
            self.beingHooked = False
            for hook in spriteHookshots:
                if hook.char == self:
                    spriteHookshots.remove(hook)
            self.rect = pygame.Rect(self.spawnx, self.spawny, self.imageright1.get_rect().width, self.imageright1.get_rect().height)

       # self.rect.width = 32
       # self.rect.height = 64
        self.rect = pygame.draw.rect(screen, (50, 50, 50), self.rect, 1)

        self.moveindex += 1

        if self.moveindex > 4:
            self.moveindex = 1

        if self.movementDirection == "right":
            if self.moveindex == 1:
                screen.blit(self.imageright1, (self.rect.x, self.rect.y))
            elif self.moveindex == 2:
                screen.blit(self.imageright2, (self.rect.x, self.rect.y))
            elif self.moveindex == 3:
                screen.blit(self.imageright3, (self.rect.x, self.rect.y))
            elif self.moveindex == 4:
                screen.blit(self.imageright4, (self.rect.x, self.rect.y))
        else:
            if self.moveindex == 1:
                screen.blit(self.imageleft1, (self.rect.x, self.rect.y))
            elif self.moveindex == 2:
                screen.blit(self.imageleft2, (self.rect.x, self.rect.y))
            elif self.moveindex == 3:
                screen.blit(self.imageleft3, (self.rect.x, self.rect.y))
            elif self.moveindex == 4:
                screen.blit(self.imageleft4, (self.rect.x, self.rect.y))

        self.xforce = 0
        self.yforce = 0

# define a main function
def main():
    # initialize the pygame module
    global keys
    global screen

    hudpos = 30
    spriteChars.append(Char(SCREENWIDTH * 0.3, SCREENHEIGHT * 0.5, hudpos, ply1ctrls))
    hudpos += 100
    spriteChars.append(Char(SCREENWIDTH * 0.7, SCREENHEIGHT * 0.5, hudpos, ply2ctrls))

    spriteFloors.append(Wall(screen, SCREENWIDTH * 0.25, SCREENHEIGHT * 0.7, 200, 16, "brick.png", "brick.png"))
    spriteFloors.append(Wall(screen, SCREENWIDTH * 0.75, SCREENHEIGHT * 0.7, 200, 16, "brick.png", "brick.png"))
    spriteFloors.append(Wall(screen, 0, 0, 64, 126, "brick.png", "brick.png"))
    spriteFloors[2].attach(spriteFloors[1], "right")
    spriteFloors.append(Wall(screen, 0, 0, 64, 126, "brick.png", "brick.png"))
    spriteFloors[3].attach(spriteFloors[0], "left")
    spriteFloors.append(Wall(screen, SCREENWIDTH * 0.5, SCREENHEIGHT * 0.95, 64, 32))
    spriteFloors.append(Wall(screen, SCREENWIDTH * 0.25, SCREENHEIGHT * 0.95, 128, 32))
    spriteFloors.append(Wall(screen, SCREENWIDTH * 0.75, SCREENHEIGHT * 0.95, 128, 32))
    spriteFloors.append(Wall(screen, SCREENWIDTH * 0.5, SCREENHEIGHT * 0.45, 200, 16, "brick.png", "brick.png"))
    spriteFloors.append(Wall(screen, SCREENWIDTH * 0.5, SCREENHEIGHT * 0.20, 64, 16, "brick.png", "brick.png"))
    spriteFloors[7].moveleftandright(SCREENWIDTH*0.3, SCREENWIDTH*0.7, 10)

    bgimage = pygame.image.load("bg.png")

    # define a variable to control the main loop
    running = True

    # main loop
    while running:

        screen.fill((255, 255, 255))
        screen.blit(bgimage, (0, 0))
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            ply1ctrls.clear()
            ply2ctrls.clear()
            ply1ctrls.extend(
                (keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_j], keys[pygame.K_i],
                 keys[pygame.K_DOWN], keys[pygame.K_k], keys[pygame.K_l]))
            ply2ctrls.extend((keys[pygame.K_f], keys[pygame.K_h], keys[pygame.K_t], keys[pygame.K_a], keys[pygame.K_w],
                              keys[pygame.K_g], keys[pygame.K_s], keys[pygame.K_d]))

            if event.type == pygame.QUIT:
                running = False

            if keys[pygame.K_0]:
                screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)
            if keys[pygame.K_9]:
                screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.FULLSCREEN)
        # Updates here

        #spriteFloors[4].moveleftandright(SCREENWIDTH/2 - 300, SCREENWIDTH/2, 10)

        for char in spriteChars:
            char.update()

        for floor in spriteFloors:
            floor.update(screen)

        for smash in spriteSmashes:
            smash.update(spriteChars, spriteSmashes, screen)

        for hook in spriteHookshots:
            hook.update(screen, spriteFloors)

        for fire in spriteFireballs:
            fire.update(spriteFloors, spriteFireballs, SCREENHEIGHT, SCREENWIDTH, pygame, screen)

        pygame.display.update()
        clock.tick(30)
        ##delay at 20


def magnitude(obj1, obj2):
    # Try atan2
    return math.atan2((obj2.rect.centery - obj1.rect.centery),
                        (obj2.rect.centerx - obj1.rect.centerx)) + math.pi

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
