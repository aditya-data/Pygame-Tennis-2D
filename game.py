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

NET_HEIGHT = 360


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TENNIS 2D")
        self.window_size = (800, 720)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.window_size)
        
        
        # Pre-render the court
        self.court_surface = pygame.Surface((400, 720))
        self.create_court()
        self.court = pygame.Surface((400, 720), pygame.SRCALPHA)
        self.create_ground(screen=self.screen)
        
        # Initialize the net
        self.create_net()

        # Players and Ball
        self.user = Player(screen=self.court, player="user", left=380, top=660, width=20, height=40)
        self.other = Player(screen=self.court, player= "other", left=0, top=0, width=20, height=40)
        self.ball = Ball(screen=self.court, left=250, top=250, width=20, height=20, x_pos=250, y_pos=250)

    def create_ground(self, screen, *args):
        for _ in range(300000):  # Adjust the number of dots
            x = random.randint(0, 800)  # Random x position
            y = random.randint(0, 720)  # Random y position
            color = random.choice([DARK_GREEN, LIGHT_GREEN, GREEN])
            pygame.draw.circle(screen, color, (x, y), random.randint(1, 2))

    def create_court(self):
        # Render the court gradient
        for y in range(0, 720):
            color = (
                COURT_BLUE_LIGHT[0] + (COURT_BLUE_DARK[0] - COURT_BLUE_LIGHT[0]) * (y / 720),
                COURT_BLUE_LIGHT[1] + (COURT_BLUE_DARK[1] - COURT_BLUE_LIGHT[1]) * (y / 720),
                COURT_BLUE_LIGHT[2] + (COURT_BLUE_DARK[2] - COURT_BLUE_LIGHT[2]) * (y / 720)
            )
            pygame.draw.line(self.court_surface, color, (0, y), (400, y))

        # Draw court lines
        pygame.draw.rect(self.court_surface, WHITE, (20, 35, 360, 635), 5)  # Court boundary
        pygame.draw.line(self.court_surface, WHITE, (90, 35), (90, 669.5), 5)  # Singles Sideline
        pygame.draw.line(self.court_surface, WHITE, (310, 35), (310, 669.5), 5)  # Singles Sideline
        # pygame.draw.line(self.court_surface, WHITE, (20, 352.5), (380, 352.5), 5) # mid line
        pygame.draw.line(self.court_surface, WHITE, (90, 193.75), (310, 193.75), 5)  # Service line
        pygame.draw.line(self.court_surface, WHITE, (90, 511.25), (310, 511.25), 5)  # Service line
        pygame.draw.line(self.court_surface, WHITE, (200, 193.75), (200, 511.25), 5)  # Centre Service line

    def create_net(self):
        # Build the net
        for x in range(20, 380, 5):  # Vertical lines
            pygame.draw.line(self.court_surface, GRAY, (x, 330), (x, NET_HEIGHT), 1)
        for y in range(330, NET_HEIGHT, 3):  # Horizontal lines
            pygame.draw.line(self.court_surface, GRAY, (20, y), (380, y), 1)
        pygame.draw.line(self.court_surface, DARK_GRAY, (20, 330), (380, 330), 5)  # Top net border
        pygame.draw.line(self.court_surface, DARK_GRAY, (20, 330), (20, NET_HEIGHT+20), 7)  # Left net border
        pygame.draw.line(self.court_surface, DARK_GRAY, (380, 330), (380, NET_HEIGHT+20), 7)  # Right net border

    def hit_position(self, player):
        if ((player.rect.x - self.ball.rect.x) < 0) and abs((player.rect.x - self.ball.rect.x) <= 10):
            return ("Right", "Close")
        elif ((player.rect.x - self.ball.rect.x) < 0) and abs((player.rect.x - self.ball.rect.x) < 15):
            return ("Right", "Medium")
        elif ((player.rect.x - self.ball.rect.x) < 0) and abs((player.rect.x - self.ball.rect.x) >= 15):
            return ("Right", "Medium")
        elif ((player.rect.x - self.ball.rect.x) > 0) and abs((player.rect.x - self.ball.rect.x) <= 10):
            return ("Left", "Close")
        else:
            return ("Left", "Medium/Far")




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

            # # Collision detection and ball interaction
            # if self.user.rect.colliderect(self.ball.rect):
            #     self.ball.chk_collision(self.user)
            #     user_hit_pos, user_hit_dist = self.hit_position(self.user)
            #     user_shot_intensity = self.user.chk_collision(user_hit_pos, user_hit_dist)
            #     self.ball.ball_hit(user_shot_intensity, user_hit_pos)

            # if self.other.rect.colliderect(self.ball.rect):
            #     self.ball.chk_collision(self.other)
            #     other_hit_pos, other_hit_dist = self.hit_position(self.other)
            #     other_shot_intensity = self.other.chk_collision(other_hit_pos, other_hit_dist)
            #     self.ball.ball_hit(other_shot_intensity, other_hit_pos)

            # Draw court on the screen
            self.screen.blit(self.court, (200, 0))

            # Update the display
            pygame.display.flip()
            self.clock.tick(60)



# Run the game
Game().run()
