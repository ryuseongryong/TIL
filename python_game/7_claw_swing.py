# 집게를 좌우로 이동시키기
import os
import pygame
from pygame.draw import rect

# 집게 class


class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.original_image = image
        self.rect = image.get_rect(center=position)
        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position

        self.direction = LEFT  # 집게의 이동 방향
        self.angle_speed = 2.5  # 집게의 각도 변경 폭(좌우 이동 속도 - 프레임 당)
        self.angle = 10  # 최초 각도 정의 (오른쪽 끝, 시작점)

    def update(self):
        if self.direction == LEFT:  # 왼쪽으로 이동중이라면
            self.angle += self.angle_speed  # 이동속도만큼 각도 증가
        elif self.direction == RIGHT:  # 오른쪽으로 이동중이라면
            self.angle -= self.angle_speed  # 이동속도만큼 각도 감소

        # 허용 각도 범위를 벗어나는 경우
        if self.angle > 170:
            self.angle = 170
            self.direction = RIGHT
        elif self.angle < 10:
            self.angle = 10
            self.direction = LEFT

        self.rotate()  # 회전처리

        # print(self.angle, self.direction)
        # rect_center = self.position + self.offset
        # self.rect = self.image.get_rect(center=rect_center)

    def rotate(self):
        # 새로운 이미지를 만들어 주는 효과, pygame.transform.rotate()함수도 있지만 화면상 매끄럽지 못한 부분이 있음
        # -를 붙이는 이유는 + 가 반시계 방향, -가 시계방향으로 각도 변경되기 때문
        self.image = pygame.transform.rotozoom(
            self.original_image, -self.angle, 1)  # 회전대상이미지, 각도, 크기

# vector2에서 자동으로 rotate 정보를 계산해줌
        offset_rotated = self.offset.rotate(self.angle)
        # print(offset_rotated)

        # rect를 조정해줘야 원하는 의도대로 움직일 수 있음
        self.rect = self.image.get_rect(center=self.position + offset_rotated)
        # print(self.rect)
        pygame.draw.rect(screen, RED, self.rect, 1)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3)  # 중심점 표시
        # 최초 중심위치(self.position)에서 self.rect.center(집게 현재 위치)까지 선을 긋는다.
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5)


# 보석 class
class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)


def setup_gemstone():
    # 금
    # 0번 째 이미지를 (200, 380) 위치에 설정
    small_gold = Gemstone(gemstone_images[0], (200, 380))
    gemstone_group.add(small_gold)  # 그룹에 추가
    # 큰 금
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500)))
    # 돌
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380)))
    # 다이아몬드
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 420)))


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")
clock = pygame.time.Clock()

#! 게임 관련 변수
default_offset_x_claw = 40  # 중심점에서 집게까지의 기본 x간격
LEFT = -1  # 왼쪽 방향
RIGHT = 1  # 오른쪽 방향

#! 색 변수
RED = (255, 0, 0)  # RGB 기준 값
BLACK = (0, 0, 0)

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

# 보석 그룹
gemstone_group = pygame.sprite.Group()
setup_gemstone()  # 게임에 원하는 만큼의 보석을 정의

# 집게
claw_image = pygame.image.load(os.path.join(current_path, "claw.png"))
# 가로 위치 : 화면 가운데, 세로 위치 : 위에서 110px
claw = Claw(claw_image, (screen_width // 2, 110))

running = True
while running:
    clock.tick(30)  # fps value setting : 30

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen)  # group내 모든 sprite를 screen에 그려라
    claw.update()
    claw.draw(screen)

    pygame.display.update()

pygame.quit()
