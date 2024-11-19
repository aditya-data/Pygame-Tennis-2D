import pygame
# from game import Game

class Player:

    def __init__(self,  screen, player, side="left", state="idle", left=500, top=460, width=50, height=50):
        self.preview_list = []
        self.rect = pygame.Rect(left, top, width, height) #rectangle object
        self.position = [left, top]
        self.velocity = [0, 0] # X and Y velocity
        self.state = state # idle, moving, swinging racket
        self.side = side # side is the side of the court (left/right) where userP will stand at first
        self.show(screen=screen, player_rect=self.rect)
        self.player = player

    def show(self, screen, player_rect, color=(255, 0, 0)):
        # draw the animated character on the screen
        pygame.draw.rect(screen, (255, 0, 0), player_rect)
    
    def move_to_centre(self):
        # Move the ball towards the center (x = 400)
        if (self.position[0] < 200):
            self.velocity[0] = 5  # Speed of movement towards the center
        elif self.position[0] > 0:
            self.velocity[0] = -5

        # Update position with velocity
        self.position[0] += self.velocity[0]
        self.rect.x = self.position[0]

    def run_towards_ball(self, ball):
        # Call move_to_centre for x-axis and implement any y-axis movement logic
        self.move_to_centre()
        ball_x_pos = ball.rect.x
        player_x_pos = self.rect.x
        distance = (ball_x_pos - player_x_pos)
        if abs(distance) > 0:
            self.velocity[0] = max(min(distance // abs(distance), 5), -5)*5  # Move towards the ball
        else:
            self.velocity[0] = 0  # Stop if close enough

        # Update position using the velocity
        self.position[0] += self.velocity[0]
        self.rect.x = self.position[0]

    def reset(self):
        #the function will run when player misses the ball
        if self.player == "user":
            self.position[0] = 0
        else:
            self.position[0] = 380
        
        self.rect.x = self.position[0]
    

    def chk_collision(self, pos, x_dist):
        # a feature should be here for the hit strength
        # only thing that the user controls
        intensity = ['High', 'Medium', 'Low']
        intensity_map = {
            "Right" + "Close" : "High",
            "Right" + "Medium": "Medium",
            "Right" + "Far": "Low",
            "Left" + "Close": "Medium",
            "Left" + "Medium/Far": "Low",
            "Left" + "Far": "Low"
        }

        shot = intensity_map[pos + x_dist]

        if shot == "High":
            return (3, 20) #velocity at x and y
        elif shot == "Medium":
            return (2, 14) #velocity at x and y
        else: #shot == "Low"
            return (1, 10) #velocity at x and y


    def update(self):
        # update to true state either left side or right side of the court 
        pass


    def serve(self, ball):
        pass


class Ball:

    def __init__(self, screen, x_pos, y_pos, state="idle", left=400, top=460, width=50, height=50):
        self.preview_list = []
        self.rect = pygame.Rect(left, top, width, height)  # rectangle object
        self.position = [x_pos, y_pos]
        self.velocity = [0, -10]  # X and Y velocity
        self.state = state  # idle, moving, swinging racket
        self.show(screen=screen, ball_rect=self.rect)
        # self.move()

    def show(self, screen, ball_rect, color=(125, 255, 0)):
        # draw the animated ball on the screen
        # self.create_ground(self.screen, ball_rect.x, ball_rect.y, ball_rect.width, ball_rect.height)
        pygame.draw.rect(screen, color, ball_rect)

    # def move_bounce(self):
    # # Reverse direction when hitting the top or bottom boundaries
    #     if (self.position[1] <= 0)  or (self.position[1] >= 680):  # Top boundary # Bottom boundary
    #         self.velocity[1] *= -1  # Move downwards # Move upwards 

    #     # Update position with velocity
    #     self.position[1] += self.velocity[1]
    #     # Update rect position for rendering
    #     self.rect.y = self.position[1]
    
    def ball_hit(self, vel, direction):
        # Set velocity based on hit intensity and direction
        x_v, y_v = vel
        if direction == "Right":
            self.velocity = [x_v, -y_v]  # Ball moves to the right and upward/downward
        else:  # direction == "Left"
            self.velocity = [-x_v, -y_v]  # Ball moves to the left and upward/downward
        
        # Update ball's position with new velocity
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
    

    def update(self):
        # Update ball's position and state
        pass
