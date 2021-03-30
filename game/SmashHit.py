import pygame

class SmashHit:

    def __init__(self, char, spriteChars):
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

    def update(self, spriteChars, spriteSmashes, screen):
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