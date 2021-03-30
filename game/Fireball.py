import pygame
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

    def update(self, spriteFloors, spriteFireballs, SCREENHEIGHT, SCREENWIDTH, pygame, screen):
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
