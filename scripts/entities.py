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
        self.last_hit_time = 0  # Initialize the cooldown timer
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

    def move_towards(self, dx):
        # target_y = 670 if self.mode == "player" else 35

        dx = self.pos[0] + dx
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


    def check_ball_collision(self, ball, opponent):
        # Predict ball's next position based on its velocity
        current_time = pygame.time.get_ticks()
        next_ball_x = ball.pos[0] + ball.vel[0]
        next_ball_y = ball.pos[1] + ball.vel[1]
        
        # Create a line representing the ball's movement (path) linear interpolation
        ball_path = pygame.Rect(
            min(ball.pos[0], next_ball_x),  # Left edge of the path
            min(ball.pos[1], next_ball_y),  # Top edge of the path
            abs(ball.vel[0]) + 20,  # Width of the path
            abs(ball.vel[1]) + 20  # Height of the path
        )
        
        # Check if the player's rectangle intersects with the ball's path
        if self.rect.colliderect(ball_path) and current_time - ball.last_hit_time > 100:
            ball.last_hit_time = current_time  # Update the hit time (its the cooldown mechanism)
            ball.vel[1] *= -random.uniform(0.8, 1.1)  # Reverse Y-velocity
            
            # Boundary avoidance logic
            court_width = 400  # Example court width
            safe_zone_margin = 90  # Margin to avoid the boundary
            horizontal_randomness = random.uniform(1, 5)  # Randomize horizontal speed
            
            if ball.pos[0] >= court_width - safe_zone_margin:  # Near right boundary
                ball.vel[0] = -horizontal_randomness  # Redirect left
            elif ball.pos[0] <= safe_zone_margin:  # Near left boundary
                ball.vel[0] = horizontal_randomness  # Redirect right
            else:
                # Target weak area of the opponent
                if opponent.pos[0] > court_width / 2:  # Opponent on the right side
                    ball.vel[0] = -horizontal_randomness  # Aim left
                else:  # Opponent on the left side
                    ball.vel[0] = horizontal_randomness  # Aim right
            
            if abs(ball.vel[0]) < 0.1 or abs(ball.vel[1]) < 0.1:
                print("Ball velocity too low:", ball.vel)

            # Ensure ball velocity doesn't stagnate
            min_speed = 1.5  # Minimum allowed speed
            # ball.vel[0] = max(min_speed, abs(ball.vel[0])) * (1 if ball.vel[0] > 0 else -1)
            ball.vel[1] = max(min_speed, abs(ball.vel[1])) * (1 if ball.vel[1] > 0 else -1)
