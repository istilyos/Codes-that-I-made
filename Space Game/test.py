# Screen dimensions
import pygame

screen_width = 1200
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tank Game")

# Load background image
background_img = pygame.image.load("grass_background.jpg")