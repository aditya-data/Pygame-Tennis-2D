import pygame
# from game import Game

class Player:

    def __init__(self,  screen, side="left", state="idle", left=500, top=460, width=50, height=50):
        self.preview_list = []
        self.rect = pygame.Rect(left, top, width, height) #rectangle object
        self.position = [left, top]
        self.velocity = [0, 0] # X and Y velocity
        self.state = state # idle, moving, swinging racket
        self.power = 0 #hit strength
        self.side = side # side is the side of the court (left/right) where userP will stand at first
        self.show(screen=screen, player_rect=self.rect)

    def show(self, screen, player_rect, color=(255, 0, 0)):
        # draw the animated character on the screen
        pygame.draw.rect(screen, (255, 0, 0), player_rect)
    
    def move_to_centre(self):
        # Move the ball towards the center (x = 400)
        if self.position[0] < 175:
            self.velocity[0] = 1  # Speed of movement towards the center
        elif self.position[0] > 175:
            self.velocity[0] = -1
        else:
            self.velocity[0] = 0  # Stop if at center

        # Update position with velocity
        self.position[0] += self.velocity[0]
        self.rect.x = self.position[0]

    def move(self):
        # Call move_to_centre for x-axis and implement any y-axis movement logic
        self.move_to_centre()

    def chk_collision(self, pos, x_dist):
        # a feature should be here for the hit strength
        # only thing that the user controls
        intensity = ['High', 'Medium', 'Low']
        intensity_map = {
            "Right" + "Close" : "High",
            "Right" + "Medium": "Medium",
            "Right" + "Far": "Low",
            "Left" + "Close": "Medium",
            "Left" + "Medium": "Low",
            "Left" + "Far": "Low"
        }

        shot = intensity_map[pos + x_dist]

        if shot == "High":
            return (5, 10) #velocity at x and y
        elif shot == "Medium":
            return (3, 7) #velocity at x and y
        else: #shot == "Low"
            return (2, 4) #velocity at x and y



    def update(self):
        # update to true state either left side or right side of the court 
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

    def move_bounce(self):
    # Reverse direction when hitting the top or bottom boundaries
        if (self.position[1] <= 0)  or (self.position[1] >= 560):  # Top boundary # Bottom boundary
            self.velocity[1] *= -1  # Move downwards # Move upwards 

        # Update position with velocity
        self.position[1] += self.velocity[1]
        # Update rect position for rendering
        self.rect.y = self.position[1]
    
    def move_back(self, x_vel, y_vel):
        pass


    def move(self):
        # Call move_to_centre for x-axis and implement any y-axis movement logic
        self.move_bounce()

        # Implement other movement behavior here (e.g., if the ball needs to move vertically)
        # if self.state == "moving":
        #     self.position[1] += self.velocity[1]  # Adjust this to your needs
        #     self.rect.y = self.position[1]

    def swing(self):
        pass

    def chk_collision(self):
        # Add logic for collision detection here
        pass

    def update(self):
        # Update ball's position and state
        pass
