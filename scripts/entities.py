import pygame
import random
import math
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
        court_rect = pygame.Rect(5, 5, 590, 710)  # Court boundary
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
        self.width = width
        self.height = height
        self.surface = surface
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.default_reset()
        self.velocity = [x_v, y_v]
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

        # dx = self.pos[0] + dx
        # dy = target_y - self.pos[1]

        self.velocity = [dx, 0]
        self.move()

    def move(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.pos[0] = max(0, min(self.pos[0], 600))  # Replace SCREEN_WIDTH with your court width
        self.rect.center = self.pos  # Sync rect with the updated position
        self.render()


    def default_reset(self):
        if self.mode == "player":
            if self.side == "left":
                self.pos[0] = 130
                self.pos[1] = 690
            else: #self.side == right
                self.pos[0] = 500
                self.pos[1] = 690
        elif self.mode == "opponent":
            if self.side == "left":
                self.pos[0] = 500
                self.pos[1] = 15
            else: #self.side == right
                self.pos[0] = 130
                self.pos[1] = 15

        self.rect.center = self.pos
        # self.render()
    
    def render(self):
        pygame.draw.ellipse(surface=self.surface, color=YELLOW, rect=self.rect)


    def calculate_velocity(self, ball, target_x, target_y, max_speed):
        # Calculate the difference in position
        dx = target_x - ball.pos[0]
        dy = target_y - ball.pos[1]

        # Calculate the required speed
        distance = math.sqrt(dx**2 + dy**2)
        time = max(1, distance / max_speed)  # Avoid division by zero, minimum time is 1 frame

        # Calculate velocity components
        vel_x = dx / time
        vel_y = dy / time

        # Scale velocities to maintain max_speed
        current_speed = math.sqrt(vel_x**2 + vel_y**2)
        if current_speed > max_speed:
            vel_x = vel_x * (max_speed / current_speed)
            vel_y = vel_y * (max_speed / current_speed)

        return vel_x, vel_y



    def check_ball_collision(self, ball, opponent):
        # Intensity is on a scale of 1-5 [5 is Max]
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
            ball.last_hit_time = current_time  # Update the hit time (cooldown mechanism)

            # Court boundaries and net position
            court_bounds = (120, 35, 360, 635)  # Left, Top, Width, Height
            net_position = (120, 352.5, 480, 352.5)  # Start and end of the net

            left, top, width, height = court_bounds
            right = left + width
            bottom = top + height
            net_mid_x = (net_position[0] + net_position[2]) / 2
            net_y = net_position[1]

            # Determine target zone based on opponent position
            if opponent.rect.centerx > (left + right) // 2:  # Opponent on the right
                target_x = random.randint(left, (left + right) // 2)
            else:  # Opponent on the left
                target_x = random.randint((left + right) // 2, right)

            # Target y-coordinate should be inside the opponent's half
            if self.rect.centery < net_y:  # Player on top
                target_y = random.randint(int(net_y) + 10, int(bottom) - 10)
            else:  # Player on bottom
                target_y = random.randint(int(top) + 10, int(net_y) - 10)

            # Adjust target to pass over the net
            if self.rect.centery > net_y:  # Coming from the bottom
                intermediate_target = (net_mid_x, net_y - 10)
            else:  # Coming from the top
                intermediate_target = (net_mid_x, net_y + 10)

            # Calculate velocity to pass above the net
            ball.vel[0], ball.vel[1] = self.calculate_velocity(ball, *intermediate_target, max_speed=5)

            # Add some randomness to the shot
            ball.vel[1] *= random.uniform(0.9, 1.1)

            # Calculate velocity towards the final target after crossing the net
            final_vel_x, final_vel_y = self.calculate_velocity(ball, target_x, target_y, max_speed=10)

            # Blend the final velocity after crossing the net
            ball.vel[0] += (final_vel_x - ball.vel[0])
            ball.vel[1] += (final_vel_y - ball.vel[1]) * random.uniform(1.8, 2.2)

            # Ensure the ball stays in bounds if the player is beyond the court edges
            if self.rect.centerx < left:  # Player beyond left boundary
                ball.vel[0] = abs(ball.vel[0]) + random.uniform(1.5, 2.5)  # Increase x_vel to the right
            elif self.rect.centerx > right:  # Player beyond right boundary
                ball.vel[0] = -abs(ball.vel[0]) - random.uniform(1.5, 2.5)  # Increase x_vel to the left
