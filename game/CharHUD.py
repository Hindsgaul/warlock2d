import pygame
class CharHUD():
    def __init__(self, x, name, knockinfo, lives, screen):
        self.rect = pygame.Rect(x, 20, 100, 50)
        self.rect = pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        self.namefont = pygame.font.SysFont('verdana', 10)
        self.knockfont = pygame.font.SysFont('verdana', 15)
        self.livesfont = pygame.font.SysFont('verdana', 10)
        self.nameinfo = self.namefont.render(name, 1, (0,0,0))
        self.knockinfo = self.namefont.render(str(knockinfo) + "%", 1, (0, 0, 0))
        self.livesinfo = self.namefont.render("Lives: " + str(lives), 1, (0, 0, 0))

    def update(self, knock, lives, screen):
        self.knockinfo = self.namefont.render(str(knock) + "%", 1, (0, 0, 0))
        self.livesinfo = self.namefont.render("Lives: " + str(lives), 1, (0, 0, 0))
        self.rect = pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
        screen.blit(self.nameinfo, (self.rect.x + 25, self.rect.y + 5))
        screen.blit(self.knockinfo, (self.rect.centerx - 2, self.rect.y + 18))
        screen.blit(self.livesinfo, (self.rect.centerx - 16, self.rect.y + 30))