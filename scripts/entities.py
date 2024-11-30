import pygame
import random
# from game import Game
# ball color
YELLOW = (255, 255, 0)


class Ball:

    def __init__(self, r, x, y, x_v, y_v, surface):
        self.radius = r
        self.pos = [x, y] #initializing
        self.vel = [x_v, y_v] #initial velocity
        self.bounce_count = 0 #initialize it with 0
        self.surface = surface # default surface court
        self.rect = pygame.Rect(self.pos[0]-self.radius, self.pos[1]- self.radius, self.radius*2, self.radius*2)
        self.render() #visualising on the surface

    def render(self):
        pygame.draw.circle(surface=self.surface, center=self.rect.center, radius=self.radius, color=YELLOW)
    
    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.rect.center = self.pos  # Sync rect with the updated position
        self.render()

    def boundary_collision(self):
        court_rect = pygame.Rect(5, 5, 390, 710)  # Court boundary
        if self.rect.left < court_rect.left or self.rect.right > court_rect.right:
            self.vel[0] *= -1  # Reverse horizontal velocity
            return "leave"

            # return "left" if self.rect.left < court_rect.left else "right"
        if self.rect.top < court_rect.top or self.rect.bottom > court_rect.bottom:
            self.vel[1] *= -1  # Reverse vertical velocity
            return "leave"
            # return "top" if sel f.rect.top < court_rect.top else "bottom"
        return "continue"

    def check_net(self):
        pass

    def reset_pos(self, new_x, new_y):
        self.pos = [new_x, new_y]  # Update position
        self.rect.center = self.pos  # Sync rect with the new position
        self.render()

class Player:

    def __init__(self, side, width, height, mode, x_v, y_v, surface):
        self.side = side
        self.mode = mode #player and opponent
        self.pos = [0, 0]
        self.surface = surface
        self.width = width
        self.height = height
        self.velocity = [x_v, y_v]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.default_reset()
        self.render()

    def move_towards_ball(self, ball):
        ball_x = ball.rect.x
        dx = ball_x - self.pos[0]

        # Dynamically cap player speed based on ball velocity
        self.velocity[0] = dx / 8  # Clamp speed

        self.move()

    
    def switch_side(self):
        if self.side == "left":
            self.side = "right"
        else:
            self.side = "left"

    def move_towards_centre(self):
        target_x = 200
        # target_y = 670 if self.mode == "player" else 35

        dx = target_x - self.pos[0]
        # dy = target_y - self.pos[1]

        self.velocity = [dx/20, 0]
        self.move()

    def move(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.center = self.pos  # Sync rect with the updated position
        self.render()


    def default_reset(self):
        if self.mode == "player":
            if self.side == "left":
                self.pos[0] = 10
                self.pos[1] = 670
            else: #self.side == right
                self.pos[0] = 310
                self.pos[1] = 670
        elif self.mode == "opponent":
            if self.side == "left":
                self.pos[0] = 310
                self.pos[1] = 35
            else: #self.side == right
                self.pos[0] = 10
                self.pos[1] = 35
        self.render()
    
    def render(self):
        pygame.draw.ellipse(surface=self.surface, color=YELLOW, rect=self.rect)


    def check_ball_collision(self, ball):
        if self.rect.colliderect(ball):
            # Reverse the vertical direction (bounce back)
            ball.vel[1] *= -1

            # Randomize horizontal velocity
            horizontal_randomness = random.uniform(2.5, 3.5)  # Adjust speed variation range

            # Avoid hitting out of bounds
            if ball.pos[0] >= 310:  # Ball near right boundary
                ball.vel[0] = -horizontal_randomness  # Push left
            elif ball.pos[0] <= 90:  # Ball near left boundary
                ball.vel[0] = horizontal_randomness  # Push right
            else:
                # Randomize direction when near the center
                ball.vel[0] = horizontal_randomness * random.choice([-1, 1])

            # Optional: Add slight randomness to vertical velocity
            ball.vel[1] *= random.uniform(0.9, 1.2)


    def return_to_neutral(self):
        pass