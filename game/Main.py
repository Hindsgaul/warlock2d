# import the pygame module, so you can use it

import pygame
import math

SCREENWIDTH = 1280
SCREENHEIGHT = 720

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
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
screen.fill((255, 255, 255))

keys = pygame.key.get_pressed()

ply1ctrls = list()
ply2ctrls = list()

ply1ctrls.extend((keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_j], keys[pygame.K_i],
                  keys[pygame.K_DOWN], keys[pygame.K_k], keys[pygame.K_l]))

ply2ctrls.extend((keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_f], keys[pygame.K_t],
                  keys[pygame.K_s], keys[pygame.K_g], keys[pygame.K_h]))


spriteFireballs = list()

class CharInput():
    def __init__(self, ctrls):
        self.left, self.right, self.up, self.shoot, self.hit, self.down, self.hook, self.roll = \
            ctrls[0], ctrls[1], ctrls[2], ctrls[3], ctrls[4], ctrls[5], ctrls[6], ctrls[7]

    def update(self, ctrls):
        self.left, self.right, self.up, self.shoot, self.hit, self.down, self.hook, self.roll = \
            ctrls[0], ctrls[1], ctrls[2], ctrls[3], ctrls[4], ctrls[5], ctrls[6], ctrls[7]


class CharHUD():
    def __init__(self, x, name, knockinfo, lives):
        self.rect = pygame.Rect(x, 20, 100, 50)
        self.rect = pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        self.namefont = pygame.font.SysFont('verdana', 10)
        self.knockfont = pygame.font.SysFont('verdana', 15)
        self.livesfont = pygame.font.SysFont('verdana', 10)
        self.nameinfo = self.namefont.render(name, 1, (0,0,0))
        self.knockinfo = self.namefont.render(str(knockinfo) + "%", 1, (0, 0, 0))
        self.livesinfo = self.namefont.render("Lives: " + str(lives), 1, (0, 0, 0))

    def update(self, knock, lives):
        self.knockinfo = self.namefont.render(str(knock) + "%", 1, (0, 0, 0))
        self.livesinfo = self.namefont.render("Lives: " + str(lives), 1, (0, 0, 0))
        self.rect = pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        screen.blit(self.nameinfo, (self.rect.x + 25, self.rect.y + 5))
        screen.blit(self.knockinfo, (self.rect.centerx - 2, self.rect.y + 18))
        screen.blit(self.livesinfo, (self.rect.centerx - 16, self.rect.y + 30))


class SmashHit:

    def __init__(self, char):
        self.movex = 0
        self.movey = 0
        self.image = pygame.image.load("smash.png")
        self.owner = char
        if char.movementDirection == "right":
            self.direction = "right"
            self.rect = pygame.Rect(char.rect.centerx, char.rect.y,
                                    self.image.get_rect().width, self.image.get_rect().height)
        else:
            self.direction = "left"
            self.rect = pygame.Rect(char.rect.centerx - char.rect.width, char.rect.y,
                                    self.image.get_rect().width, self.image.get_rect().height)
        self.smashtimer = 0.1
        self.smashtickshot = pygame.time.get_ticks() - 0.1
        self.smashduration = 0.3
        self.charindex = spriteChars.index(char)

    def update(self):
        if self.direction == "right":
            self.rect = pygame.Rect(spriteChars[self.charindex].rect.centerx + self.movex, spriteChars[self.charindex].rect.y + self.movey,
                                    self.image.get_rect().width, self.image.get_rect().height)
        else:
            self.rect = pygame.Rect(spriteChars[self.charindex].rect.centerx + self.movex - spriteChars[self.charindex].rect.width, spriteChars[self.charindex].rect.y + self.movey,
                                    self.image.get_rect().width, self.image.get_rect().height)
        # cooldowns
        if self.smashtimer > 0:
            self.smashtimer = (pygame.time.get_ticks() - self.smashtickshot) / 1000  # calculate how many seconds
            if self.direction == "right":
                if self.smashtimer < self.smashduration / 2:
                     self.movex += 3.5
            else:
                if self.smashtimer < self.smashduration / 2:
                    self.movex -= 3.5
            self.movey += 3.3
        if self.smashtimer > self.smashduration:
            spriteSmashes.remove(self)
        self.rect = pygame.draw.rect(screen, (50, 50, 50), self.rect, 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Hookshot:
    def __init__(self, char):
        if char.movementDirection == "right":
            self.image = pygame.image.load("hookright.png")
            self.direction = 25
            self.rect = pygame.Rect(char.rect.x + char.rect.width, char.rect.y + char.rect.height * 0.3,
                                    self.image.get_rect().width, self.image.get_rect().height)
            self.rect.left = char.rect.right
            #self.imagerect = self.rect
        else:
            self.image = pygame.image.load("hookleft.png")
            self.direction = -25
            self.rect = pygame.Rect(char.rect.x - char.rect.width, char.rect.y + char.rect.height * 0.3,
                                    self.image.get_rect().width, self.image.get_rect().height)
            self.rect.right = char.rect.left
           # self.imagerect = self.rect
        self.targethit = False
        self.char = char

    def update(self):
        if not self.targethit:
            for floor in spriteFloors:
                if self.rect.colliderect(floor):
                    self.targethit = True
                    break

        if not self.targethit:
            if self.direction:
                self.rect.x += self.direction
                #self.imagerect.right += self.direction
            else:
                self.rect.x += self.direction
                #self.rect.width += self.direction
                #self.imagerect.x += self.direction

        self.rect = pygame.draw.rect(screen, (50, 50, 50), self.rect, 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Fireball:
    def __init__(self, char, direction = ""):
        self.image = pygame.image.load("fireball.png")
        self.ydirection = 0
        self.xdirection = 0
        self.owner = char
        self.active = True
        self.rect = pygame.Rect(0,0,1,1)
        if direction == "up":
            self.ydirection = -2
            if char.movementDirection == "right":
                self.rect = pygame.Rect(char.rect.x + char.rect.width, char.rect.top - self.image.get_rect().height - 1,
                                        self.image.get_rect().width, self.image.get_rect().height)
                self.xdirection = 20
            else:
                self.xdirection = -20
                self.rect = pygame.Rect(char.rect.x - self.image.get_rect().width, char.rect.top - self.image.get_rect().height - 1,
                                        self.image.get_rect().width, self.image.get_rect().height)
        elif direction == "down":
            self.ydirection = 2
            if char.movementDirection == "right":
                self.rect = pygame.Rect(char.rect.x + char.rect.width, char.rect.top - self.image.get_rect().height - 1,
                                        self.image.get_rect().width, self.image.get_rect().height)
                self.xdirection = 20
            else:
                self.xdirection = -20
                self.rect = pygame.Rect(char.rect.x - self.image.get_rect().width, char.rect.top - self.image.get_rect().height - 1,
                                        self.image.get_rect().width, self.image.get_rect().height)
        elif char.movementDirection == "right":
            self.rect = pygame.Rect(char.rect.x + char.rect.width, char.rect.y + char.rect.height * 0.3,
                                    self.image.get_rect().width, self.image.get_rect().height)
            self.xdirection = 20
        elif char.movementDirection == "left":
            self.rect = pygame.Rect(char.rect.x - self.image.get_rect().width, char.rect.y + char.rect.height * 0.3,
                                    self.image.get_rect().width, self.image.get_rect().height)
            self.xdirection = -20

    def update(self):
        self.ydirection *= 1.3
        for floor in spriteFloors:
            if self.rect.colliderect(floor):
                if self.ydirection == 0:
                    spriteFireballs.remove(self)
                    self.active = False
                break

        if self.rect.top <= 0 or self.rect.bottom >= SCREENHEIGHT or self.rect.right >= SCREENWIDTH or self.rect.left <= 0:
            if self.active:
                spriteFireballs.remove(self)

        self.rect = pygame.draw.rect(screen, (50, 50, 50), self.rect, 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.x += self.xdirection
        if self:
            self.rect.y += self.ydirection


class Char:

    def __init__(self, x, y, hudx, controls):
        self.image = pygame.image.load("art2.png")
        self.dashimage = pygame.image.load("dash.png")
        self.spawnx = x
        self.spawny = y
        self.rect = pygame.Rect(self.spawnx, self.spawny, self.image.get_rect().width, self.image.get_rect().height)
        print(self.rect.width)
        print(self.rect.height)
        self.movementSpeed = 7
        self.xforce, self.yforce = 0, 0
        self.isJump = False
        self.movementDirection = "none"
        self.lives = 3

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
        self.hit = False
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

        self.vup, self.vdown = 1, 0.3
        self.knockbackbonus = 0
        self.name = "MaddyIce"
        self.controls = controls
        self.hud = CharHUD(hudx, self.name, self.knockbackbonus, self.lives)
        self.input = CharInput(controls)

    def moveLeft(self):
        self.movementDirection = "left"
        move = True

        for floor in spriteFloors:
            if (floor.rect.right >= self.rect.left >= floor.rect.left
                    and self.rect.left + self.rect.width >= floor.rect.left
                    and floor.rect.top <= self.rect.centery <= floor.rect.bottom):
                move = False
                break

        if move and not self.flyingToHook and not self.isRoll:
            self.xforce -= self.movementSpeed
            #self.rect.x -= self.movementSpeed

    def moveRight(self):
        self.movementDirection = "right"
        move = True

        for floor in spriteFloors:
            if (self.rect.right - self.rect.width <= floor.rect.left <= self.rect.right <= floor.rect.right
                    and floor.rect.top <= self.rect.centery <= floor.rect.bottom):
                move = False
                break

        if move and not self.flyingToHook and not self.isRoll:
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
        if not self.isJump and self.ground_check():
            self.isJump = True

    def shootfireball(self):
        self.lastfireballtimer, self.fireballtickshot = self.action_starter(self.lastfireballtimer, self.fireballtickshot, Fireball(self))

    def shoothook(self):
        self.lasthooktimer, self.hooktickshot = self.action_starter(self.lasthooktimer, self.hooktickshot, Hookshot(self))

    def action_starter(self, timer, tickshot, obj):
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
            else:
                print("NOT A CLASS OBJECT!")
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
                if self.hit and self.flyingToHook:
                    self.flyingToHook = False
                    self.movelockx = 0
                    self.movelocky = 0
                    spriteHookshots.remove(hook)

    def smash(self):
        if self.lastsmashtimer == 0:
            self.smashtickshot = pygame.time.get_ticks()
            spriteSmashes.append(SmashHit(self))
            self.lastsmashtimer = 0.1  # starter tick

    def ground_check(self):
        onground = None
        for floor in spriteFloors:
            if floor.rect.top <= self.rect.bottom <= floor.rect.top + 25 \
                    and self.rect.left + self.rect.width * 0.8 >= floor.rect.left and \
                    self.rect.right - self.rect.width * 0.8 <= floor.rect.right:
                onground = floor
                break
        return onground

    def check_for_hits(self):

        self.hit = False

        # Check for fireball
        if not self.isRoll:
            for fireball in spriteFireballs:
                if fireball.rect.colliderect(self):
                    if not fireball.owner == self:
                        self.hit = True
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
                        self.hit = True
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


        if self.hit and self.flyingToHook:
            self.beingHooked = False
            self.movelockx = 0
            self.movelocky = 0
            #spriteHookshots.remove(hook)

        if self.hit:
            self.vdown = 0.3

    def moveDown(self):
        if self.ground_check() and not self.isJump:
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

    def gravity_and_jump(self):
        if self.isJump:
            if self.vup > 0.3:
                self.yforce -= 25 * self.vup
                #self.rect.y -= 25 * self.vup
                self.vup -= 0.1
            else:
                self.vup = 1
                self.isJump = False
        elif self.ground_check():
            self.rect.bottom = self.ground_check().rect.top
        else:
            if not self.ground_check():
                self.yforce += 25 * self.vdown

                if self.ground_check():
                    self.rect.bottom = self.ground_check().rect.top

                if self.vdown < 1:
                    self.vdown += 0.05
            else:
                self.vdown = 0.3

    def update(self):

        #check for hits
        self.rolldurationupdate()
        self.check_for_hits()

        self.check_for_cooldowns()

        self.keypresses()

        # hud update
        self.hud.update(self.knockbackbonus, self.lives)

        self.check_for_hook()

        self.gravity_and_jump()

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

        if self.rect.y <= 0 or self.rect.x <= 0 or self.rect.x >= SCREENWIDTH or self.rect.y >= SCREENHEIGHT or self.rect.bottom >= SCREENHEIGHT:
            self.lives -= 1
            self.knockbackbonus = 0
            self.flyingToHook = False
            self.beingHooked = False
            for hook in spriteHookshots:
                if hook.char == self:
                    spriteHookshots.remove(hook)
            self.rect = pygame.Rect(self.spawnx, self.spawny, self.image.get_rect().width, self.image.get_rect().height)

       # self.rect.width = 32
       # self.rect.height = 64
        self.rect = pygame.draw.rect(screen, (50, 50, 50), self.rect, 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))

        self.xforce = 0
        self.yforce = 0


class Wall:

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.rect = pygame.draw.rect(screen, (255, 0, 0), self.rect, 0)
        self.movement = -10

    def update(self):
        self.rect = pygame.draw.rect(screen, (255, 0, 0), self.rect, 0)

    def moveleftandright(self, leftside, rightside, speed):
        if self.rect.x <= leftside:
            self.movement = speed
        if self.rect.x >= rightside:
            self.movement = -speed
        self.rect.x += self.movement


def magnitude(obj1, obj2):
    #Try atan2
    return math.atan2((obj2.rect.centery - obj1.rect.centery), (obj2.rect.centerx - obj1.rect.centerx)) + math.pi


# define a main function
def main():
    # initialize the pygame module
    global keys

    hudpos = 30
    spriteChars.append(Char(SCREENWIDTH * 0.3, 280, hudpos, ply1ctrls))
    hudpos += 100
    spriteChars.append(Char(SCREENWIDTH * 0.6, 280, hudpos, ply2ctrls))


    # Bottom, right and top
    spriteFloors.append(Wall(SCREENWIDTH - 16, 0, 16, SCREENHEIGHT))
    spriteFloors.append(Wall(0, 0, 16, SCREENHEIGHT))
    spriteFloors.append(Wall(0, 0, SCREENWIDTH, 16))

    # Top center
    spriteFloors.append(Wall(SCREENWIDTH * 0.5 - SCREENWIDTH * 0.1, SCREENHEIGHT - 610, SCREENWIDTH * 0.2, 16))
    spriteFloors[3].rect.centerx = SCREENWIDTH/2

    spriteFloors.append(Wall(SCREENWIDTH * 0.5 - SCREENWIDTH * 0.1, SCREENHEIGHT - 500, SCREENWIDTH * 0.2, 16))
    spriteFloors[4].rect.centerx = SCREENWIDTH/2 - 200

    spriteFloors.append(Wall(SCREENWIDTH * 0.5 - SCREENWIDTH * 0.1, SCREENHEIGHT - 500, SCREENWIDTH * 0.2, 16))
    spriteFloors[5].rect.centerx = SCREENWIDTH/2 + 200

    #spriteFloors.append(Wall(SCREENWIDTH / 2, SCREENHEIGHT - 150, SCREENWIDTH / 2, 16))
    #spriteFloors.append(Wall(SCREENWIDTH / 2, SCREENHEIGHT - 250, SCREENWIDTH / 2, 16))
    spriteFloors.append(Wall(SCREENWIDTH * 0.2, SCREENHEIGHT - 400, SCREENWIDTH / 2, 16))
    spriteFloors[6].rect.centerx = SCREENWIDTH / 2

    spriteFloors.append(Wall(SCREENWIDTH - 50, 200, 16, 256 * 2.1))
    spriteFloors.append(Wall(SCREENWIDTH - 250, 200, 16, 256 * 2.1))

    spriteFloors.append(Wall(0,256,200,16))
    spriteFloors[9].rect.left = spriteFloors[8].rect.right

    spriteFloors.append(Wall(0,406,200,16))
    spriteFloors[10].rect.left = spriteFloors[8].rect.right

    spriteFloors.append(Wall(0,556,400,16))
    spriteFloors[11].rect.centerx = spriteFloors[8].rect.centerx

    spriteFloors.append(Wall(0,606,128,16))
    spriteFloors[12].rect.x = SCREENWIDTH/2 + 50

    spriteFloors.append(Wall(0,656,128,16))
    spriteFloors[13].rect.x = SCREENWIDTH/2 - 100

    spriteFloors.append(Wall(0,456,202,16))
    spriteFloors[14].rect.x = SCREENWIDTH/2 - 130

    spriteFloors.append(Wall(0,606,128,16))
    spriteFloors[15].rect.x = SCREENWIDTH/2 - 240

    spriteFloors.append(Wall(10, SCREENHEIGHT - 100, SCREENWIDTH * 0.2, 32))
    spriteFloors.append(Wall(10, SCREENHEIGHT - 250, SCREENWIDTH * 0.2, 32))
    spriteFloors.append(Wall(10, SCREENHEIGHT - 500, SCREENWIDTH * 0.2, 32))

    spriteFloors.append(Wall(16, SCREENHEIGHT * 0.33, 16, SCREENHEIGHT * 0.73))

    # define a variable to control the main loop
    running = True

    # main loop
    while running:

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

        # Updates here

        screen.fill((255, 255, 255))

        spriteFloors[4].moveleftandright(SCREENWIDTH/2 - 300, SCREENWIDTH/2, 10)

        for char in spriteChars:
            char.update()

        for floor in spriteFloors:
            floor.update()

        for smash in spriteSmashes:
            smash.update()

        for hook in spriteHookshots:
            hook.update()

        for fire in spriteFireballs:
            fire.update()

        pygame.display.update()
        clock.tick(30)
        ##delay at 20
        pygame.time.delay(0)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
