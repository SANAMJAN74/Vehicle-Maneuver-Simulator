import os
import pygame
import numpy as np
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import time
import random

# Note: Python version check is commented out as it's not essential for runtime.
# import platform
# print(platform.python_version())

#################################################################################
class EGO_Car:
    """
    Class representing the Ego vehicle (user-controlled car).
    
    This class models the kinematics of a vehicle using a simplified bicycle model.
    It handles position, velocity, acceleration, and steering updates.
    
    Attributes:
        position (Vector2): Current position (x, y).
        velocity (Vector2): Current velocity (x-component is forward speed).
        angle (float): Heading angle in degrees.
        length (float): Vehicle length for turning radius calculation.
        max_acceleration (float): Maximum acceleration rate.
        max_steering (float): Maximum steering angle.
        max_velocity (float): Maximum allowed speed (13.85 m/s ~50 km/h).
        brake_deceleration (float): Deceleration rate when braking.
        free_deceleration (float): Natural deceleration when coasting.
        acceleration (float): Current acceleration.
        steering (float): Current steering angle.
    """
    def __init__(self, x, y, angle=90.0, length=4, max_steering=30, max_acceleration=5):
        self.position = Vector2(x, y)
        self.velocity = Vector2(8.31, 0.0)  # Initial speed: 8.31 m/s ~30 km/h
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 13.85  # Max: 13.85 m/s ~50 km/h
        self.brake_deceleration = 5
        self.free_deceleration = 1
        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        """
        Update the vehicle's state based on acceleration and steering.
        
        Args:
            dt (float): Time delta for the update step.
        """
        # Update velocity based on acceleration
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        # Calculate angular velocity for turning
        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        # Update position and angle
        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

#################################################################################
class O_Car:
    """
    Class representing Other vehicles (non-controlled, constant velocity).
    
    These vehicles move at a fixed velocity without user input.
    
    Attributes:
        position (Vector2): Current position (x, y).
        velocity (tuple): Fixed velocity (x, y).
    """
    def __init__(self, vel, x, y):
        self.position = Vector2(x, y)
        self.velocity = (0, vel)  # Velocity is downward (negative y in update)

    def update(self, dt):
        """
        Update the vehicle's position based on fixed velocity.
        
        Args:
            dt (float): Time delta for the update step.
        """
        self.position += np.array(self.velocity) * dt

#################################################################################


class Start:
    """
    Main simulation class handling Pygame initialization, event loop, and rendering.
    
    This class sets up the screen, loads assets, initializes vehicles, and runs the simulation loop.
    """
    def __init__(self):
        pygame.init()
        # Set up resizable display
        screen = pygame.display.set_mode((145, 700), pygame.RESIZABLE)
        width, height = 145, 700
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60  # Target FPS
        self.exit = False

    def run(self):
        """
        Run the main simulation loop.
        
        Handles user input, updates vehicle states, checks for collisions/end conditions,
        logs data, and renders the scene.
        """
        # Load image assets
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "car.png")
        path_amu = os.path.join(current_dir, "amu.png")
        path1 = os.path.join(current_dir, "car1.png")
        path2 = os.path.join(current_dir, "car2.png")
        path3 = os.path.join(current_dir, "car3.png")
        path4 = os.path.join(current_dir, "car4.png")
        path5 = os.path.join(current_dir, "car5.png")

        # Vehicle images
        ecar_image = pygame.image.load(path)
        amu_image = pygame.image.load(path_amu)
        car_image1 = pygame.image.load(path1)
        car_image2 = pygame.image.load(path2)
        car_image3 = pygame.image.load(path3)
        car_image4 = pygame.image.load(path4)
        car_image5 = pygame.image.load(path5)

        # Initialize vehicles with positions and velocities (1 km/h = 0.277 m/s)
        random_offset = 6 + 2 * random.random()  # Random initial x for ego
        ecar = EGO_Car(random_offset, 64, angle=90.0)
        amu = O_Car(8.31, 7, 70)  # Ambulance
        car3 = O_Car(8.31, 7, 57)
        car1 = O_Car(8.31, 3, 89)  # Top-Left car
        car2 = O_Car(8.31, 11.5, 20)  # Top-Right car
        car4 = O_Car(8.31, 3, 57)  # Another left car
        car5 = O_Car(8.31, 11.5, 57)  # Bottom-Right car

        ppu = 10  # Pixels per unit for rendering
        start_time = time.time()

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event handling
            for event in pygame.event.get():
                pressed = pygame.key.get_pressed()
                if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
                    self.exit = True

            # User input for ego vehicle
            if pressed[pygame.K_UP]:
                if ecar.velocity.x < 0:
                    ecar.acceleration = ecar.brake_deceleration
                else:
                    ecar.acceleration += 1 * dt
            elif pressed[pygame.K_DOWN]:
                if ecar.velocity.x > 0:
                    ecar.acceleration = -1 * ecar.brake_deceleration
                else:
                    ecar.acceleration -= 1 * dt
            else:
                if abs(ecar.velocity.x) > dt * ecar.free_deceleration:
                    ecar.acceleration = -copysign(ecar.free_deceleration, ecar.velocity.x)
                else:
                    if dt != 0:
                        ecar.acceleration = -ecar.velocity.x / dt
            ecar.acceleration = max(-ecar.max_acceleration, min(ecar.acceleration, ecar.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                ecar.steering -= 30 * dt
            elif pressed[pygame.K_LEFT]:
                ecar.steering += 30 * dt
            else:
                ecar.steering = 0
            ecar.steering = max(-ecar.max_steering, min(ecar.steering, ecar.max_steering))

            # Update all vehicles
            ecar.update(dt)
            amu.update(-dt)  # Negative dt for upward movement (assuming y increases downward)
            car1.update(-dt)
            car2.update(-dt)
            car3.update(-dt)
            car4.update(-dt)
            car5.update(-dt)

            # Store display positions as numpy arrays for convenience
            ecar.position_disp = np.array((ecar.position[0], ecar.position[1]))
            amu.position_disp = np.array((amu.position[0], amu.position[1]))
            car1.position_disp = np.array((car1.position[0], car1.position[1]))
            car2.position_disp = np.array((car2.position[0], car2.position[1]))
            car3.position_disp = np.array((car3.position[0], car3.position[1]))
            car4.position_disp = np.array((car4.position[0], car4.position[1]))
            car5.position_disp = np.array((car5.position[0], car5.position[1]))

            ########################################## Data Logging ###########################################
            # Log data if ambulance is still in the simulation area
            # Columns: long_dist_amu_ego, lat_dist_amu_ego, ego_long_vel, ego_acc
            # Commented lines are for additional vehicles if needed
            if amu.position_disp[1] > 1:
                out_file_path = open('Right.txt', 'a')  # Update this path to your desired output file
                with open('Right.txt', 'a') as outFile:
                    #outFile.write(str(amu.position_disp[1] - ecar.position_disp[1]))  # Long dist amu-ego
                    outFile.write(",")
                    outFile.write(str(amu.position_disp[0] - ecar.position_disp[0]))  # Lat dist amu-ego
                    outFile.write(",")
                    outFile.write(str(ecar.velocity.x))  # Ego long vel
                    outFile.write(",")
                    outFile.write(str(ecar.acceleration))  # Ego acc
                    outFile.write("\n")
            else:
                print("--- Simulation time: %s seconds ---" % (time.time() - start_time))

            # Check for end conditions: ambulance exit or collisions or out-of-bounds
            if (amu.position_disp[1] < 1) or \
               ((-4 < (ecar.position_disp[1] - amu.position_disp[1]) < 4) and (-2 < (ecar.position_disp[0] - amu.position_disp[0]) < 2)) or \
               ((-4 < (ecar.position_disp[1] - car3.position_disp[1]) < 4) and (-2 < (ecar.position_disp[0] - car3.position_disp[0]) < 2)) or \
               ((-4 < ecar.position_disp[1] - car2.position_disp[1] < 4) and (-2 < ecar.position_disp[0] - car2.position_disp[0] < 2)) or \
               ((-4 < ecar.position_disp[1] - car1.position_disp[1] < 4) and (-2 < ecar.position_disp[0] - car1.position_disp[0] < 2)) or \
               ((-4 < (ecar.position_disp[1] - car4.position_disp[1]) < 4) and (-2 < (ecar.position_disp[0] - car4.position_disp[0]) < 2)) or \
               ((-4 < (ecar.position_disp[1] - car5.position_disp[1]) < 4) and (-2 < (ecar.position_disp[0] - car5.position_disp[0]) < 2)) or \
               ((ecar.position_disp[0] > 14.5) or (ecar.position_disp[0] < 0)):
                if amu.position_disp[1] < 1:
                    print("End of the round")
                else:
                    print("Crash")
                break

            ########################################## Rendering ###########################################
            # Fill background (road gray)
            self.screen.fill((150, 150, 150))

            # Draw road boundaries and lanes
            pygame.draw.rect(self.screen, (255, 255, 255), [8, 0, 6, 1000])  # Left boundary
            pygame.draw.rect(self.screen, (255, 255, 255), [131, 0, 6, 1000])  # Right boundary
            lane_positions_1 = [[49, 1000 - i * 80, 6, 50] for i in range(1000)]  # Dashed lane 1
            lane_positions_2 = [[90, 1000 - i * 80, 6, 50] for i in range(1000)]  # Dashed lane 2
            for p in lane_positions_1:
                pygame.draw.rect(self.screen, (255, 255, 255), p)
            for h in lane_positions_2:
                pygame.draw.rect(self.screen, (255, 255, 255), h)

            # Rotate and blit vehicle images
            rotated = pygame.transform.rotate(ecar_image, ecar.angle)
            rotated_amu = amu_image  # No rotation for others
            rotated1 = car_image1
            rotated2 = car_image2
            rotated3 = car_image3
            rotated4 = car_image4
            rotated5 = car_image5

            rect = rotated.get_rect()
            rect_amu = rotated_amu.get_rect()
            rect1 = rotated1.get_rect()
            rect2 = rotated2.get_rect()
            rect3 = rotated3.get_rect()
            rect4 = rotated4.get_rect()
            rect5 = rotated5.get_rect()

            self.screen.blit(rotated, ecar.position_disp * ppu - (rect.width / 2, rect.height / 2))
            self.screen.blit(rotated_amu, amu.position_disp * ppu - (rect_amu.width / 2, rect_amu.height / 2))
            self.screen.blit(rotated1, car1.position_disp * ppu - (rect1.width / 2, rect1.height / 2))
            self.screen.blit(rotated2, car2.position_disp * ppu - (rect2.width / 2, rect2.height / 2))
            self.screen.blit(rotated3, car3.position_disp * ppu - (rect3.width / 2, rect3.height / 2))
            self.screen.blit(rotated4, car4.position_disp * ppu - (rect4.width / 2, rect4.height / 2))
            self.screen.blit(rotated5, car5.position_disp * ppu - (rect5.width / 2, rect5.height / 2))

            pygame.display.update()
            self.clock.tick(self.ticks)

        pygame.quit()

#################################################################################
if __name__ == '__main__':
    game = Start()
    game.run()
