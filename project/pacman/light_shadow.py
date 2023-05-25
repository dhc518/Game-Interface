import pygame
import math

# 화면 초기화
pygame.init()
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# 배경 설정
background_color = (255, 255, 255)  # 흰색
screen.fill(background_color)

# 사각형 설정
rect_color = (0, 0, 255)  # 파란색
rect_width, rect_height = 200, 200
rect_x, rect_y = 100, 100
pygame.draw.rect(screen, rect_color, (rect_x, rect_y, rect_width, rect_height))

# 원형 영역의 픽셀 투명 처리
center_x, center_y = 150, 150  # 원의 중심 좌표
radius = 10  # 원의 반지름

# 마스크 표면 생성
mask_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
mask_surface.fill((0, 0, 0, 0))

for x in range(rect_width):
    for y in range(rect_height):
        distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        if distance <= radius:
            alpha = int(255 * (1 - (distance / radius)))  # 투명도 계산
            mask_surface.set_at((x, y), (0, 0, 0, alpha))

# 마스크 표면을 기존 화면에 합성
screen.blit(mask_surface, (rect_x, rect_y), special_flags=pygame.BLEND_RGBA_MIN)

# 화면 업데이트
pygame.display.flip()

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

# 파이게임 종료
pygame.quit()
