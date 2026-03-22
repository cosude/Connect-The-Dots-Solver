import pygame
class Button:
    def __init__(self, x, y, w, h, text, color, hover_color=None, active=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.active = active
        

    def draw(self, screen, font):
        m_pos = pygame.mouse.get_pos()
        curr_col = self.hover_color if self.rect.collidepoint(m_pos) and self.active else self.color
        if not self.active: curr_col = (50, 50, 55)
        
        pygame.draw.rect(screen, curr_col, self.rect, border_radius=12)
        txt = font.render(self.text, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return self.active and event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)