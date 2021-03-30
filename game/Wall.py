import pygame
class Wall:

    def __init__(self, screen, x, y, width, height, topimage ="grass.png", bottomimage = "dirt.png"):
        self.rect = pygame.Rect(x - width / 2, y - height / 2, width, height)
        while self.rect.width % 16 != 0:
            self.rect.width += 1
        while self.rect.height % 16 != 0:
            self.rect.height += 1
        self.rect = pygame.draw.rect(screen, (255, 0, 0), self.rect, 0)
        self.topimage = pygame.image.load(topimage)
        self.bottomimage = pygame.image.load(bottomimage)
        self.movement = -10

    def attach(self, wall, side):
        if side == "left":
            self.rect.bottomleft = wall.rect.topleft
            self.rect.y = self.rect.y - wall.rect.height * 2 + 1
        else:
            self.rect.bottomright = wall.rect.topright
            self.rect.y = self.rect.y - wall.rect.height * 2 + 1

    def update(self, screen):
        dirtx = 0
        dirty = 0
        while dirtx + self.rect.x < self.rect.right:
            while dirty + self.rect.y < self.rect.bottom:
                dirty += 16
                screen.blit(self.bottomimage, (self.rect.x + dirtx, self.rect.y + dirty))
            dirty = 0
            screen.blit(self.topimage, (self.rect.x + dirtx, self.rect.y))
            dirtx += 16
        #self.rect = pygame.draw.rect(screen, (0, 0, 0), self.rect, 0)

    def moveleftandright(self, leftside, rightside, speed):
        if self.rect.x <= leftside:
            self.rect.x += speed
        if self.rect.x >= rightside:
            self.rect.x -= -speed
        self.rect.x += self.movement

