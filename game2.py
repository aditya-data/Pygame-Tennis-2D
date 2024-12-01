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
        self.PlayerA = Player(side="right", mode="player", width=100, height=20, x_v=0, y_v=0, surface=self.court.court)
        self.PlayerB = Player(side="right", mode="opponent", width=100, height=20, x_v=0, y_v=0, surface=self.court.court)
        self.Ball = Ball(r=10, x=10, y= 10, x_v=6, y_v=12, surface=self.court.court)
        # run game loop
        self.game_state = "start" # [serve, play, point_over]
        self.server = self.PlayerA
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
            keys = pygame.key.get_pressed() #capturing key presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                    
            self.court.court.blit(self.court.court_surface, (0, 0))
            self.PlayerA.render()
            self.PlayerB.render()

            if self.game_state == "start":
                self.PlayerA.default_reset()
                self.PlayerB.default_reset()
                self.game_state = "serve"
            elif self.game_state == "serve":
                if self.server == self.PlayerA:
                    if self.PlayerA.side == "left":
                        self.Ball.reset_pos(30, 620)
                        self.Ball.vel = [3, 15]
                    elif self.PlayerA.side == "right":
                        self.Ball.reset_pos(350, 620)
                        self.Ball.vel = [-3, 15]
                else:
                    if self.PlayerB.side == "left":
                        self.Ball.reset_pos(360, 50)
                        self.Ball.vel = [-5, -15]
                    elif self.PlayerB.side == "right":
                        self.Ball.reset_pos(25, 50)
                        self.Ball.vel = [5, -15]
                self.Ball.move()
                self.game_state = "play"
            elif self.game_state == "play":
                #### game play logic
                self.Ball.move()
                
                if self.Ball.boundary_collision() == "continue":
                    if self.Ball.pos[1] > 352.5:
                        # self.PlayerA.move_towards_ball(self.Ball)
                        # self.PlayerB.move_towards_centre()
                        self.PlayerA.move_towards_ball(self.Ball)
                        if self.Ball.pos[1] > 640:
                            self.PlayerA.check_ball_collision(self.Ball, self.PlayerB)

                    else: #Ball.pos[1] < 352.5:  
                        self.PlayerB.move_towards_ball(self.Ball)
                        if self.Ball.pos[1] < 40:
                            self.PlayerB.check_ball_collision(self.Ball, self.PlayerA)
                else:
                    # print("Yeh ")
                    self.PlayerA.switch_side()
                    self.PlayerB.switch_side()
                    self.PlayerA.default_reset()
                    self.PlayerB.default_reset()
                    self.server = self.PlayerA
                    self.Ball.reset_pos(self.server.pos[0], self.server.pos[0]+ 40)
                    self.Ball.vel = [0, 0]
                    self.game_state = "serve"
            else:
                # declare winner and scoreboard highlight
                pass

            # print(self.Ball.rect)
            self.screen.blit(self.court.court, (200, 0))
            pygame.display.flip()
            self.clock.tick(60)

    def update(self):
        pass

    def draw(self):
        pass


GameManager().run()