"""
Created on Wed Feb 24 21:16:43 2021

@author: Sule
@name: customs.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3

import pygame

class Button():
    """
    DOCSTRING:

    """
    def __init__(self, surface, text, pos, size, bg_color, text_size=20, text_font=None, text_color=(0,0,0), border=0, border_color=(0,0,0)):
        self.surface = surface
        self.text = text
        self.pos = pos
        self.size = size
        self.bg_color = bg_color
        self.text_size = text_size
        self.text_font = text_font
        self.text_color = text_color
        self.border = border
        self.border_color = border_color
        
        self.rect = pygame.Rect(pos[0]+self.border, pos[1]+self.border, size[0]-self.border*2, size[1]-self.border*2)

    def draw(self):
        x, y = self.pos
        width, height = self.size

        if self.border > 0:
            bg = pygame.Rect(x, y, width, height)
            pygame.draw.rect(self.surface, self.border_color, bg)

        self.rect = pygame.Rect(x+self.border, y+self.border, width-self.border*2, height-self.border*2)
        pygame.draw.rect(self.surface, self.bg_color, self.rect)
        Text(self.surface, self.text, (x + width/2, y + height/2), self.text_color, self.text_size, self.text_font, True)

class Text():
    """
    DOCSTRING:

    """
    def __init__(self, surface, text, pos, color, text_size=22, text_font=None, center=False, right=False):
        self.surface = surface
        self.text = text
        self.pos = pos
        self.color = color

        self.text_size = text_size
        self.text_font = text_font
        self.center = center
        self.right = right
        
        self.draw()

    def draw(self):
        x, y = self.pos
        font = pygame.font.SysFont(self.text_font, self.text_size)
        txt = font.render(self.text, True, self.color)
        if self.center:
            text_rect = txt.get_rect(center=(x, y))
        elif self.right:
            text_rect = txt.get_rect(midright=(x, y))
        else:
            text_rect = txt.get_rect(midleft=(x, y))
        self.surface.blit(txt, text_rect)

class ImageButton():
    """
    DOCSTRING:

    """
    def __init__(self, surface, image, size, pos, alt_text, rotation=0):
        self.surface = surface
        self.image = image
        self.size = size
        self.pos = pos
        self.alt_text = alt_text
        self.rotation = rotation

    def draw(self):
        bg = pygame.image.load(self.image)
        bg = pygame.transform.scale(bg, self.size)

        if self.rotation != 0:
            bg = pygame.transform.rotate(bg, self.rotation)

        self.surface.blit(bg, self.pos)
        return bg

    def click(self, click_pos):
        x1, y1 = click_pos
        x, y = self.pos
        width, height = self.size
        if x <= x1 <= x + width and y <= y1 <= y + height:
            return True
        return False

class InputBox():
    def __init__(self, screen, pos, size, text='', color_active=(0, 255, 0), color_inactive=(255, 0,0 )):
        font = pygame.font.Font(None, 24)
        self.screen = screen
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.color_active = color_active 
        self.color_inactive = color_inactive 
        self.color = color_inactive
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def clear(self):
        self.text = ''
        font = pygame.font.Font(None, 24)
        self.txt_surface = font.render(self.text, True, self.color)
        self.draw()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                
                font = pygame.font.Font(None, 24)
                self.txt_surface = font.render(self.text, True, self.color)


    def update(self):
        width = max(self.rect.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        self.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(self.screen, self.color, self.rect, 2)

def main():
    width = 500
    height = 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Client")
    pygame.font.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (74, 145, 35)
    YELLOW = (242, 209, 17)
    ORANGE = (242, 118, 9)

    clock = pygame.time.Clock()
    click = False
    while True:
        clock.tick(60)
        win.fill((128, 128, 128))   
        btn_1 = ImageButton(win, 'images/red/red_0.jpg', (75, 150), (20, 40), '')
        btn_2 = ImageButton(win, 'images/green/green_0.jpg', (75, 150), (60, 40), '')
        btn_3 = ImageButton(win, 'images/wild_4.jpg', (75, 150), (100, 40), '')
        btn_4 = ImageButton(win, 'images/wild_color.jpg', (75, 150), (140, 40), '')
        btn_1.draw()
        btn_2.draw()
        btn_3.draw()
        btn_4.draw()
        mx, my = pygame.mouse.get_pos()

        if click:
            if btn_4.click((mx, my)):
                print('BTN4')
            elif btn_3.click((mx, my)):
                print('BTN3')
            elif btn_2.click((mx, my)):
                print('BTN2')
            elif btn_1.click((mx, my)):
                print('BTN1')

        click = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()