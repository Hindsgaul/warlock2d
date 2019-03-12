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

spriteWalls = []
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

ply1ctrls.extend((keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_x], keys[pygame.K_c],
                  keys[pygame.K_DOWN], keys[pygame.K_z], keys[pygame.K_v]))

ply2ctrls.extend((keys[pygame.K_j], keys[pygame.K_l], keys[pygame.K_i], keys[pygame.K_SPACE], keys[pygame.K_u],
                  keys[pygame.K_k], keys[pygame.K_o], keys[pygame.K_p]))


spriteFireballs = list()

class CharInput():
    def __init__(self, ctrls):
        self.left, self.right, self.up, self.shoot, self.hit, self.down, self.hook, self.roll = \
            ctrls[0], ctrls[1], ctrls[2], ctrls[3], ctrls[4], ctrls[5], ctrls[6], ctrls[7]

    def update(self, ctrls):
        self.left, self.right, self.up, self.shoot, self.hit, self.down, self.hook, self.roll = \
            ctrls[0], ctrls[1], ctrls[2], ctrls[3], ctrls[4], ctrls[5], ctrls[6], ctrls[7]


class CharHUD():
    def __init__(self, x, name, knockinfo):
        self.rect = pygame.Rect(x, 20, 100, 50)
        self.rect = pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        self.namefont = pygame.font.SysFont('verdana', 10)
        self.knockfont = pygame.font.SysFont('verdana', 15)
        self.nameinfo = self.namefont.render(name, 1, (0,0,0))
        self.knockinfo = self.namefont.render(str(knockinfo) + "%", 1, (0, 0, 0))

    def update(self, knock):
        self.knockinfo = self.namefont.render(str(knock) + "%", 1, (0, 0, 0))
        self.rect = pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        screen.blit(self.nameinfo, (self.rect.x + 25, self.rect.y + 5))
        screen.blit(self.knockinfo, (self.rect.centerx - 2, self.rect.y + 15))


class SmashHit:

    def __init__(self, char):
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
        self.smashduration = 0.2
        self.charindex = spriteChars.index(char)

    def update(self):
        if self.direction == "right":
            self.rect = pygame.Rect(spriteChars[self.charindex].rect.centerx, spriteChars[self.charindex].rect.y,
                                    self.image.get_rect().width, self.image.get_rect().height)
        else:
            self.rect = pygame.Rect(spriteChars[self.charindex].rect.centerx - spriteChars[self.charindex].rect.width, spriteChars[self.charindex].rect.y,
                                    self.image.get_rect().width, self.image.get_rect().height)
        self.rect = pygame.draw.rect(screen, (50, 50, 50), self.rect, 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # cooldowns
        if self.smashtimer > 0:
            self.smashtimer = (pygame.time.get_ticks() - self.smashtickshot) / 1000  # calculate how many seconds
        if self.smashtimer > self.smashduration:
            spriteSmashes.remove(self)

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
            for wall in spriteWalls:
                if self.rect.colliderect(wall):
                    self.targethit = True
                    break
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
    def __init__(self, char):
        self.image = pygame.image.load("fireball.png")
        if char.movementDirection == "right":
            self.rect = pygame.Rect(char.rect.x + char.rect.width, char.rect.y + char.rect.height * 0.3,
                                    self.image.get_rect().width, self.image.get_rect().height)
            self.direction = 30
        else:
            self.rect = pygame.Rect(char.rect.x - self.image.get_rect().width, char.rect.y + char.rect.height * 0.3,
                                    self.image.get_rect().width, self.image.get_rect().height)
            self.direction = -30
            #direction was 30 before

    def update(self):
        for floor in spriteFloors:
            if self.rect.colliderect(floor):
                spriteFireballs.remove(self)
                break
        self.rect = pygame.draw.rect(screen, (50, 50, 50), self.rect, 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.x += self.direction


class Char:

    def __init__(self, x, y, hudx, controls):
        self.image = pygame.image.load("art2.png")
        self.dashimage = pygame.image.load("dash.png")
        self.rect = pygame.Rect(x, y, self.image.get_rect().width, self.image.get_rect().height)
        self.movementSpeed = 7
        self.xforce, self.yforce = 0
        self.isJump = False
        self.movementDirection = "none"

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
        self.onground = None
        self.knockbackbonus = 0
        self.name = "MaddyIce"
        self.controls = controls
        self.hud = CharHUD(hudx, self.name, self.knockbackbonus)
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
            self.rect.x -= self.movementSpeed

    def moveRight(self):
        self.movementDirection = "right"
        move = True

        for floor in spriteFloors:
            if (self.rect.right - self.rect.width <= floor.rect.left <= self.rect.right <= floor.rect.right
                    and floor.rect.top <= self.rect.centery <= floor.rect.bottom):
                move = False
                break

        if move and not self.flyingToHook and not self.isRoll:
            self.rect.x += self.movementSpeed

    def roll(self):
        if not self.isRoll and self.lastrolltimer == 0:
            if self.movementDirection == "right":
                self.rollpower = 10
            else:
                self.rollpower = -10
            self.rolltickshot = pygame.time.get_ticks()
            self.lastrolltimer = 0.1  # starter tick
            self.isRoll = True
            print("Roll!")
            if self.rollhittimer == 0:
                self.rollhittick = pygame.time.get_ticks() - 0.1
                self.rollhittimer = 0.1  # starter tick

    def rolldurationupdate(self):
        if self.rollhittimer > 0:
            self.rect.x += self.rollpower
            if self.isRoll and self.rollpower > 0:
                screen.blit(self.dashimage, (self.rect.x - self.rect.width, self.rect.y))
            elif self.isRoll and self.rollpower < 0:
                screen.blit(self.dashimage, (self.rect.x + self.rect.width, self.rect.y))
            self.rollhittimer = (pygame.time.get_ticks() - self.rollhittick) / 1000  # calculate how many seconds

        if self.rollhittimer > self.rollhitduration:
            self.isRoll = False
            self.rollhittimer = 0

    def jump(self):
        if not self.isJump and self.onground:
            self.isJump = True

    def shootfireball(self):
        if self.lastfireballtimer == 0:
            self.fireballtickshot = pygame.time.get_ticks()
            spriteFireballs.append(Fireball(self))
            self.lastfireballtimer = 0.1  # starter tick

    def shoothook(self):
        if self.lasthooktimer == 0:
            self.hooktickshot = pygame.time.get_ticks()
            spriteHookshots.append(Hookshot(self))
            self.lasthooktimer = 0.1  # starter tick

    def check_for_hook(self):
        for hook in spriteHookshots:
            if hook.char == self:
                if hook.targethit:
                    self.flyingToHook = True
                    if hook.direction > 0:
                        self.rect.x += 20
                    else:
                        self.rect.x -= 20
                    if self.rect.centery < hook.rect.centery + 50:
                        self.rect.y += 20
                    elif self.rect.centery > hook.rect.centery - 50:
                        self.rect.y -= 20

                if self.rect.colliderect(hook):
                    self.flyingToHook = False
                    spriteHookshots.remove(hook)
                    break

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

    def checkforhits(self):

        # Check for fireball
        if not self.isRoll:
            for fireball in spriteFireballs:
                if fireball.rect.colliderect(self):

                    mag = (magnitude(self, fireball))
                    self.multipliery = math.sin(mag)
                    self.multiplierx = math.cos(mag)


                    print(self.multiplierx)
                    print(self.multipliery)

                    '''
                    if fireball.direction > 0:
                        self.fireballhitdirection = "right"
                    else:
                        self.fireballhitdirection = "left"
                    '''
                    self.knockbackbonus += 2
                    if self.fireballhittimer == 0:
                        self.fireballhittick = pygame.time.get_ticks() - 0.1
                        self.fireballhittimer = 0.1  # starter tick

                    spriteFireballs.remove(fireball)

        if self.fireballhittimer > 0:
            '''
            if self.fireballhitdirection == "right":
                self.rect.x += self.fireballhitpower * (self.knockbackbonus * 0.3)
            else:
                self.rect.x -= self.fireballhitpower * (self.knockbackbonus * 0.3)
            '''
            self.rect.x += ((self.fireballhitpower * self.knockbackbonus/5) * self.multiplierx)
            self.rect.y += ((self.fireballhitpower * self.knockbackbonus/5) * self.multipliery)

            self.fireballhittimer = (pygame.time.get_ticks() - self.fireballhittick) / 1000  # calculate how many seconds
            self.fireballhitpower -= 0.3
            print(self.fireballhitpower)

        if self.fireballhittimer > self.fireballhiteffectsec:
            self.fireballhitpower = 5
            self.fireballhittimer = 0

        # Check for smashes
        if not self.isRoll:
            for smash in spriteSmashes:
                if smash.rect.colliderect(self):
                    if smash.owner != self:
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
                self.rect.x += self.smashhitpower * (self.knockbackbonus * 0.3)
            else:
                self.rect.x -= self.smashhitpower * (self.knockbackbonus * 0.3)
            self.smashhittimer = (pygame.time.get_ticks() - self.smashhittick) / 1000  # calculate how many seconds
            self.smashhitpower -= 0.3

        if self.smashhittimer > self.smashhitduration:
            self.smashhitpower = 5
            self.smashhittimer = 0

    def moveDown(self):
        if self.ground_check() and not self.isJump:
            self.vdown = 0.3
            self.rect.y += 26

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

    def check_for_cooldowns(self):
        # fireballs
        if self.lastfireballtimer > 0:
            self.lastfireballtimer = (pygame.time.get_ticks() - self.fireballtickshot) / 1000  # calculate how many seconds
        if self.lastfireballtimer > self.fireballcooldown:
            self.lastfireballtimer = 0

        if self.lastsmashtimer > 0:
            self.lastsmashtimer = (pygame.time.get_ticks() - self.smashtickshot) / 1000  # calculate how many seconds
        if self.lastsmashtimer > self.smashcooldown:
            self.lastsmashtimer = 0

        if self.lasthooktimer > 0:
            self.lasthooktimer = (pygame.time.get_ticks() - self.hooktickshot) / 1000  # calculate how many seconds
        if self.lasthooktimer > self.hookcooldown:
            self.lasthooktimer = 0

        if self.lastrolltimer > 0:
            self.lastrolltimer = (pygame.time.get_ticks() - self.rolltickshot) / 1000  # calculate how many seconds
        if self.lastrolltimer > self.rollcooldown:
            self.lastrolltimer = 0

    def gravity_and_jump(self):

        if self.isJump:
            if self.vup > 0.3:
                self.rect.y -= 25 * self.vup
                self.vup -= 0.1
            else:
                self.vup = 1
                self.isJump = False
        elif self.ground_check():
            self.rect.bottom = self.ground_check().rect.top
        else:
            if not self.onground and not self.flyingToHook:
                self.rect.y += 25 * self.vdown

                if self.ground_check():
                    self.rect.bottom = self.ground_check().rect.top

                if self.vdown < 1:
                    self.vdown += 0.1
            else:
                self.vdown = 0.3

    def update(self):

        #check if on ground
        self.onground = self.ground_check()

        #check for hits
        self.rolldurationupdate()
        self.checkforhits()

        self.gravity_and_jump()

        self.rect = pygame.draw.rect(screen, (50, 50, 50), self.rect, 1)
        screen.blit(self.image, (self.rect.x, self.rect.y))

        self.check_for_cooldowns()

        self.keypresses()

        # hud update
        self.hud.update(self.knockbackbonus)

        self.check_for_hook()


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


    spriteFloors.append(Wall(SCREENWIDTH - 30, 0, 30, SCREENHEIGHT))
    spriteFloors.append(Wall(0, 0, 30, SCREENHEIGHT))

    spriteFloors.append(Wall(0, SCREENHEIGHT-50, SCREENWIDTH, 25))
    spriteFloors.append(Wall(SCREENWIDTH / 2, SCREENHEIGHT - 150, SCREENWIDTH / 2, 25))
    spriteFloors.append(Wall(SCREENWIDTH / 2, SCREENHEIGHT - 250, SCREENWIDTH / 2, 25))
    spriteFloors.append(Wall(SCREENWIDTH * 0.2, SCREENHEIGHT - 400, SCREENWIDTH / 2, 25))
    spriteFloors.append(Wall(SCREENWIDTH * 0.7, SCREENHEIGHT - 510, SCREENWIDTH * 0.2, 25))
    spriteFloors.append(Wall(SCREENWIDTH * 0.1, SCREENHEIGHT - 300, SCREENWIDTH * 0.2, 200))
    spriteFloors.append(Wall(SCREENWIDTH * 0.1, SCREENHEIGHT - 300, 50, 300))
    spriteFloors.append(Wall(10, SCREENHEIGHT - 300, SCREENWIDTH * 0.2, 25))
    spriteFloors.append(Wall(10, SCREENHEIGHT - 200, SCREENWIDTH * 0.2, 25))
    spriteFloors.append(Wall(10, SCREENHEIGHT - 375, SCREENWIDTH * 0.2, 25))

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
                (keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_x], keys[pygame.K_c],
                 keys[pygame.K_DOWN], keys[pygame.K_z], keys[pygame.K_v]))
            ply2ctrls.extend(
                (keys[pygame.K_j], keys[pygame.K_l], keys[pygame.K_i], keys[pygame.K_SPACE], keys[pygame.K_u],
                 keys[pygame.K_k], keys[pygame.K_o], keys[pygame.K_p]))

            if event.type == pygame.QUIT:
                running = False

        # Updates here

        screen.fill((255, 255, 255))

        spriteFloors[4].moveleftandright(SCREENWIDTH/2 - 300, SCREENWIDTH/2, 10)

        for char in spriteChars:
            char.update()

        for wall in spriteWalls:
            wall.update()

        for floor in spriteFloors:
            floor.update()

        for smash in spriteSmashes:
            smash.update()

        for fire in spriteFireballs:
            fire.update()

        for hook in spriteHookshots:
            hook.update()

        pygame.display.update()
        clock.tick(30)
        pygame.time.delay(20)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
