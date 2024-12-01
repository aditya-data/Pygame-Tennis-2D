import pygame


class Court:
    
    def __init__(self, width, height, colors=[]):
        self.court = pygame.Surface((width, height))
        self.court_surface = pygame.Surface((width, height))
        self.colors = colors
        self.draw()


    def draw(self):
        for y in range(0, 720):
            color = (
                self.colors[0][0] + (self.colors[1][0] - self.colors[0][0]) * (y / 720),
                self.colors[0][1] + (self.colors[1][1] - self.colors[0][1]) * (y / 720),
                self.colors[0][2] + (self.colors[1][2] - self.colors[0][2]) * (y / 720)
            )
            pygame.draw.line(self.court_surface, color, (0, y), (600, y))

        # Draw court lines
        pygame.draw.rect(self.court_surface, self.colors[2], (120, 35, 360, 635), 5)  # Court boundary
        pygame.draw.line(self.court_surface, self.colors[2], (190, 35), (190, 669.5), 5)  # Singles Sideline
        pygame.draw.line(self.court_surface, self.colors[2], (410, 35), (410, 669.5), 5)  # Singles Sideline
        # pygame.draw.line(self.court_surface, self.colors[2], (20, 352.5), (380, 352.5), 5) # mid line
        pygame.draw.line(self.court_surface, self.colors[2], (190, 193.75), (410, 193.75), 5)  # Service line
        pygame.draw.line(self.court_surface, self.colors[2], (190, 511.25), (410, 511.25), 5)  # Service line
        pygame.draw.line(self.court_surface, self.colors[2], (300, 193.75), (300, 511.25), 5)  # Centre Service line




class Net:

    def __init__(self, height, surface, colors):
        self.height = height # example = 50
        self.colors = colors
        self.draw(surface)

    def draw(self, Surface):
        # Build the net
        for x in range(120, 480, 5):  # Vertical lines
            pygame.draw.line(Surface, self.colors[0], (x, 330), (x, 330 + self.height), 1)
        for y in range(330, 330 + self.height, 3):  # Horizontal lines
            pygame.draw.line(Surface, self.colors[0], (120, y), (480, y), 1)
        pygame.draw.line(Surface, self.colors[1], (120, 330), (480, 330), 5)  # Top net border
        pygame.draw.line(Surface, self.colors[1], (120, 330), (120, 330 + self.height+20), 7)  # Left net border
        pygame.draw.line(Surface, self.colors[1], (480, 330), (480, 330 + self.height+20), 7)  # Right net border

    def check_collison(self):
        pass
