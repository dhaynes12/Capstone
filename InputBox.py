import pygame
class InputBox:
    """Creates Text input object
    Uses x and y for start position (top left of button)
    Uses w and h for width and height
    Uses ic for initial color and ac for action color (RGB color tuple)"""

    def __init__(self, x, y, w, h, ic, ac, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.width = w
        self.inactiveColor = ic
        self.activeColor = ac
        self.font = pygame.font.SysFont("agencyfb",22)
        self.color = self.inactiveColor
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.keypad = [pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5,
                       pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9]
        self.numbers = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                        pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.activeColor if self.active else self.inactiveColor
        if event.type == pygame.KEYDOWN:
            if self.active:
                #if event.key == pygame.K_RETURN:
                #    print(self.text)
                #    self.text = ''
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif (event.key in self.keypad) or (event.key in self.numbers):
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.width, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
