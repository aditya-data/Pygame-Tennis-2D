import pygame
import sys
import random
from scripts.entities import Player, Ball

# Colors for the ground
GREEN = (34, 180, 30)
DARK_GREEN = (0, 120, 0)
LIGHT_GREEN = (50, 205, 50)

YELLOW = (255, 255, 0)
# Colors for the court
COURT_BLUE_LIGHT = (51, 153, 255)
COURT_BLUE_DARK = (0, 51, 102)
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)

# Net
GRAY = (200, 200, 200)

# Net border
DARK_GRAY = (70, 70, 70)

NET_HEIGHT = 310


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TENNIS 2D")
        self.window_size = (800, 650)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.window_size)
        self.create_ground(screen=self.screen)
        
        # Pre-render the court
        self.court_surface = pygame.Surface((400, 580))
        self.create_court()
        self.court = pygame.Surface((400, 580), pygame.SRCALPHA)
        
        # Initialize the net
        self.net = pygame.Surface((800, 20), pygame.SRCALPHA)
        self.create_net()

        # Players and Ball
        self.user = Player(screen=self.court, left=350, top=530, width=50, height=50)
        self.other = Player(screen=self.court, left=0, top=0, width=50, height=50)
        self.ball = Ball(screen=self.court, left=250, top=250, width=20, height=20, x_pos=250, y_pos=250)

    def create_ground(self, screen, *args):
        if not args:
            for _ in range(300000):  # Adjust the number of dots
                x = random.randint(0, 800)  # Random x position
                y = random.randint(0, 650)  # Random y position
                color = random.choice([DARK_GREEN, LIGHT_GREEN, GREEN])
                pygame.draw.circle(screen, color, (x, y), random.randint(1, 2))
        else:
            for _ in range(10000):
                x = random.randint(args[0], args[0] + args[2])
                y = random.randint(args[1], args[1] + args[3])
                color = random.choice([DARK_GREEN, LIGHT_GREEN, GREEN])
                pygame.draw.circle(screen, color, (x, y), random.randint(1, 2))

    def create_court(self):
        # Render the court gradient
        for y in range(580):
            color = (
                COURT_BLUE_LIGHT[0] + (COURT_BLUE_DARK[0] - COURT_BLUE_LIGHT[0]) * (y / 580),
                COURT_BLUE_LIGHT[1] + (COURT_BLUE_DARK[1] - COURT_BLUE_LIGHT[1]) * (y / 580),
                COURT_BLUE_LIGHT[2] + (COURT_BLUE_DARK[2] - COURT_BLUE_LIGHT[2]) * (y / 580)
            )
            pygame.draw.line(self.court_surface, color, (0, y), (400, y))

        # Draw court lines
        pygame.draw.rect(self.court_surface, WHITE, (0, 0, 400, 580), 5)  # Court boundary
        pygame.draw.line(self.court_surface, WHITE, (70, 0), (70, 580), 5)  # Singles Sideline
        pygame.draw.line(self.court_surface, WHITE, (330, 0), (330, 580), 5)  # Singles Sideline
        pygame.draw.line(self.court_surface, WHITE, (70, 145), (330, 145), 5)  # Service line
        pygame.draw.line(self.court_surface, WHITE, (70, 435), (330, 435), 5)  # Service line
        pygame.draw.line(self.court_surface, WHITE, (200, 145), (200, 435), 5)  # Centre Service line

    def create_net(self):
        # Build the net
        for x in range(0, 400, 5):  # Vertical lines
            pygame.draw.line(self.court_surface, GRAY, (x, 270), (x, NET_HEIGHT), 1)
        for y in range(270, NET_HEIGHT, 3):  # Horizontal lines
            pygame.draw.line(self.court_surface, GRAY, (0, y), (400, y), 1)
        pygame.draw.line(self.court_surface, DARK_GRAY, (0, 270), (400, 270), 5)  # Top net border
        pygame.draw.line(self.court_surface, DARK_GRAY, (0, 270), (0, NET_HEIGHT), 7)  # Left net border
        pygame.draw.line(self.court_surface, DARK_GRAY, (400, 270), (400, NET_HEIGHT), 7)  # Right net border

    def run(self):
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Clear the court
            self.court.blit(self.court_surface, (0, 0))

            # Update ball position and draw it
            # self.ball.move()
            # self.ball.show(self.court, self.ball.rect)

            # Update player position and draw it

            # self.user.move()
            # self.user.show(self.court, self.user.rect)

            # self.other.move()
            # self.other.show(self.court, self.other.rect)



            # Draw court on the screen
            self.screen.blit(self.court, (200, 50))

            # Update the display
            pygame.display.flip()
            self.clock.tick(60)


# Run the game
Game().run()
