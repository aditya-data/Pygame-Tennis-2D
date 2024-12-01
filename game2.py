import pygame
import random
import sys
from scripts.utils import Net, Court
from scripts.entities import Player, Ball
# Colors for the ground
GREEN = (34, 180, 30)
DARK_GREEN = (0, 120, 0)
LIGHT_GREEN = (50, 205, 50)
WINDOW_SIZE  = (1200, 720) # size of the outer game window
# court properties
COURT_BLUE_LIGHT = (51, 153, 255)
COURT_BLUE_DARK = (0, 51, 102)
WHITE = (255, 255, 255)
COURTWIDTH = 600
COURTHEIGHT = 720
# net properties
GRAY = (200, 200, 200)
# Net border
DARK_GRAY = (70, 70, 70)
NET_HEIGHT = 40

YELLOW = (255, 0, 0)

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
        self.Ball = Ball(r=10, x=200, y= 350, x_v=0, y_v=0, surface=self.court.court)
        # run game loop
        self.game_state = "start" # [serve, play, point_over]
        self.server = self.PlayerA
        self.font = pygame.font.Font(None, 40)
        self.run()

    def create_ground(self):
        for _ in range(300000):  # Adjust the number of dots
            x = random.randint(0, 1200)  # Random x position
            y = random.randint(0, 720)  # Random y position
            color = random.choice([DARK_GREEN, LIGHT_GREEN, GREEN])
            pygame.draw.circle(self.screen, color, (x, y), random.randint(1, 2))
    
    def display_info(self):
        # Create the text to be displayed
            text1 = self.font.render("Press Space Bar to Serve!", True, YELLOW)
            text2 = self.font.render("Player A is Serving", True, YELLOW)
            text3 = self.font.render("Get Ready!", True, YELLOW)

            # Calculate the x-position for centering the text
            text_x = (600 - text1.get_width()) // 2  # Same for all texts if centered

            # Position each text vertically, with some space in between
            text_y1 = (700 - (text1.get_height() + text2.get_height() + text3.get_height())) // 2
            text_y2 = text_y1 + text1.get_height() + 10  # 10 pixels space between text blocks
            text_y3 = text_y2 + text2.get_height() + 10  # 10 pixels space between text blocks

            # Draw each text on the court
            self.court.court.blit(text1, (text_x, text_y1))
            self.court.court.blit(text2, (text_x, text_y2))
            self.court.court.blit(text3, (text_x, text_y3))


            pygame.display.flip()

    def run(self):
        while True:
            # print(f"PlayerA position: {self.PlayerA.pos}")
            # print(f"PlayerB position: {self.PlayerB.pos}")
            pygame.key.set_repeat(200, 60)
            self.court.court.blit(self.court.court_surface, (0, 0))
            self.PlayerA.render()
            self.PlayerB.render()
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.PlayerA.move_towards(-35)  # Start moving left
                    if event.key == pygame.K_RIGHT:
                        self.PlayerA.move_towards(35)   # Start moving right
                    if event.key == pygame.K_SPACE:
                        if self.game_state == "serve":
                            x_ini = random.randint(6, 8)
                            y_ini = random.randint(14, 18)
                            # Spacebar pressed during serve
                            if self.PlayerA.side == "left":
                                # self.Ball.reset_pos(30, 620)
                                self.Ball.vel = [x_ini + 1, -y_ini]
                            elif self.PlayerA.side == "right":
                                # self.Ball.reset_pos(350, 620)
                                self.Ball.vel = [-x_ini - 2, -y_ini ]
                            self.game_state = "play"             

                if event.type == pygame.KEYUP:
                        if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                            self.PlayerA.move_towards(0)  # Stop moving   
            if self.game_state == "start":
                self.PlayerA.default_reset()
                self.PlayerB.default_reset()
                self.game_state = "serve"
            elif self.game_state == "serve":
                if self.server == self.PlayerA:
                    self.display_info()
                    self.Ball.reset_pos(self.server.rect.x + 50, self.server.rect.y -20)                 
                else:
                    if self.PlayerB.side == "left":
                        self.Ball.vel = [-5, -15]
                    elif self.PlayerB.side == "right":
                        self.Ball.vel = [5, -15]
                    self.Ball.reset_pos(self.server.rect.x + 50, self.server.rect.y +20)
            elif self.game_state == "play":
                self.Ball.move()
                if self.Ball.boundary_collision() == "continue":
                    if self.Ball.pos[1] > 352.5:
                        if self.Ball.pos[1] > 640:
                            keys = pygame.key.get_pressed()
                            if keys[pygame.K_SPACE]:
                                self.PlayerA.check_ball_collision(self.Ball, self.PlayerB)
                            else:
                                self.PlayerA.check_ball_collision(self.Ball, self.PlayerB)
                    else:  
                        self.PlayerB.move_towards_ball(self.Ball)
                        if self.Ball.pos[1] < 40:
                            self.PlayerB.check_ball_collision(self.Ball, self.PlayerA)
                else:
                    self.PlayerA.switch_side()
                    self.PlayerB.switch_side()
                    self.PlayerA.default_reset()
                    self.PlayerB.default_reset()
                    self.server = self.PlayerA  #switch server here based on requirement
                    self.game_state = "serve"
            else:
                # declare winner and scoreboard highlight
                pass

            # print(self.Ball.rect)
            self.screen.blit(self.court.court, (300, 0))
            pygame.display.flip()
            self.clock.tick(60)

    def update(self):
        pass

    def draw(self):
        pass


GameManager().run()