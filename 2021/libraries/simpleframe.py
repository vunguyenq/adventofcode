import pygame
import time

# Color constants
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
WHITE = (255, 255, 255)
MAGENTA = (255,0,255)

# This class draws dynamic frame with pixels of size tile_size x tile_size. Coordinates (left, top) = (0,0)
class SimpleFrame:
    def __init__(self, width = 1000, height = 1000, left_margin = 10, top_margin = 10, tile_size = 20, title = 'Untitled screen', background_color = WHITE, frame_rate = 0.05):
        self.screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption(title)
        pygame.font.init()
        self.background_color = background_color
        self.left_margin = left_margin
        self.top_margin = top_margin
        self.tile_size = tile_size
        self.title = title
        self.frame_rate = frame_rate

    def myfunc(self):
        print("Hello my name is " + str(self.left_margin))

    def set_title(self, title):
        self.title = title
        pygame.display.set_caption(self.title)

    def draw_tile(self, pos, color):
        x,y = pos
        x = x * self.tile_size + self.left_margin
        y = y * self.tile_size + self.top_margin
        pygame.draw.rect(self.screen, color, [x, y, self.tile_size, self.tile_size])

    def draw_lines(self, nodes, color):
        for i in range(1,len(nodes)):
            node1 = nodes[i-1]
            node2 = nodes[i]

            x1,y1 = node1
            x2,y2 = node2
            x1 = x1 * self.tile_size + int(self.tile_size/2) + self.left_margin
            y1 = y1 * self.tile_size + int(self.tile_size/2) + self.top_margin
            x2 = x2 * self.tile_size + int(self.tile_size/2) + self.left_margin
            y2 = y2 * self.tile_size + int(self.tile_size/2) + self.top_margin
            pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), 3)
    
    def set_font(self, font_type, font_size):
        self.font = pygame.font.SysFont(font_type, font_size)
    
    def display_text(self, text, left, top, color = RED):
        textsurface = self.font.render(text, False, color)
        self.screen.blit(textsurface,(left, top))
    
    def reset_background(self):
        # Fill the background
        self.screen.fill(self.background_color)
    
    def refresh(self):
        pygame.display.flip()
        time.sleep(self.frame_rate)
    
    # Exit if user clicks close
    def check_closed(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
    
    # Inherit and overide this function per use
    def draw(self):
        for i in range(100):
            self.reset_background()
            self.display_text(str(i), 200, 200)
            self.draw_tile((i,i%20), (255,0,0))
            self.refresh()
            self.check_closed()