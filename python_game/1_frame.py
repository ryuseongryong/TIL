import pygame

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")

clock = pygame.time.Clock()

running = True
while running:
  clock.tick(30) #fps value setting : 30
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

pygame.quit()