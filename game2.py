import pygame
import random
import sys
from scripts.utils import Net, Court
from scripts.entities import Player, Ball
# Colors for the ground
GREEN = (34, 180, 30)
DARK_GREEN = (0, 120, 0)
LIGHT_GREEN = (50, 205, 50)
WINDOW_SIZE  = (800, 720) # size of the outer game window
# court properties
COURT_BLUE_LIGHT = (51, 153, 255)
COURT_BLUE_DARK = (0, 51, 102)
WHITE = (255, 255, 255)
COURTWIDTH = 400
COURTHEIGHT = 720
# net properties
GRAY = (200, 200, 200)
# Net border
DARK_GRAY = (70, 70, 70)
NET_HEIGHT = 40

class GameManager:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TENNIS 2D")
        self.window_size = WINDOW_SIZE
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.window_size)
        self.create_ground()
        self.court = Court(COURTWIDTH, COURTHEIGHT, [COURT_BLUE_LIGHT, COURT_BLUE_DARK, WHITE])
        self.net = Net(height=NET_HEIGHT, surface=self.court.court_surface, colors=[GRAY, DARK_GRAY])
        self.PlayerA = Player(side="left", mode="player", width=100, height=20, x_v=0, y_v=0, surface=self.court.court)
        self.PlayerB = Player(side="right", mode="opponent", width=100, height=20, x_v=0, y_v=0, surface=self.court.court)
        self.Ball = Ball(r=10, x=10, y= 10, x_v=6, y_v=12, surface=self.court.court)
        # run game loop
        self.run()

    def create_ground(self):
        for _ in range(300000):  # Adjust the number of dots
            x = random.randint(0, 800)  # Random x position
            y = random.randint(0, 720)  # Random y position
            color = random.choice([DARK_GREEN, LIGHT_GREEN, GREEN])
            pygame.draw.circle(self.screen, color, (x, y), random.randint(1, 2))

    def run(self):
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.court.court.blit(self.court.court_surface, (0, 0))
            self.Ball.move()
            self.Ball.boundary_collision()

            # mid line of court 352.5

            if self.Ball.pos[1] > 352.5:
                self.PlayerA.move_towards_ball(self.Ball)
                self.PlayerB.move_towards_centre()
                if self.Ball.pos[1] > 640.5:
                    self.PlayerA.check_ball_collision(self.Ball)
            else: #Ball.pos[1] < 352.5:
                self.PlayerB.move_towards_ball(self.Ball)
                self.PlayerA.move_towards_centre()
                if self.Ball.pos[1] < 80.5:
                    self.PlayerB.check_ball_collision(self.Ball)
            self.PlayerA.render()
            self.PlayerB.render()

            
            
            # self.court.court_surface.blit(self.court.court, (0, 0))
            # self.court.court.blit(self.court.court_surface, (0, 0))
            self.screen.blit(self.court.court, (200, 0))
            pygame.display.flip()
            self.clock.tick(60)

    def update(self):
        pass

    def draw(self):
        pass


GameManager().run()