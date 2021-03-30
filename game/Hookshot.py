import pygame
import math
import numpy
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

    def update(self, screen, spriteFloors):
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