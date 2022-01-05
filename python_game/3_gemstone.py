import os
import pygame

# 보석 class


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")

clock = pygame.time.Clock()

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__)  # 현재 위치 반환
background = pygame.image.load(os.path.join(current_path, "background.png"))

# 보석 이미지 불러오기(금, 큰 금, 돌, 다이아몬드)
gemstone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.png")),  # 금
    pygame.image.load(os.path.join(current_path, "big_gold.png")),  # 큰 금
    pygame.image.load(os.path.join(current_path, "stone.png")),  # 돌
    pygame.image.load(os.path.join(current_path, "diamond.png")),  # 다이아몬드
]

character = pygame.image.load()
character_size = character.get_rect().size
character_width = character_size[0]
character_width = character_size[1]

running = True
while running:
    clock.tick(30)  # fps value setting : 30

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    pygame.display.update()

pygame.quit()
