import pygame
import sys
import create_light

# 게임 화면 크기 설정
width, height = 640, 480

# 색상 정의
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)

# 팩맨 초기 위치 설정
pacman_x, pacman_y = width // 2, height // 2

# 이동 속도 설정
move_speed = 5

# 먹이 초기 위치 설정
food_x, food_y = 50, 50

# 점수
score = 0

# Pygame 초기화
pygame.init()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pacman Game")

clock = pygame.time.Clock()




def draw():
    window.fill(WHITE)

    # 팩맨 그리기
    pygame.draw.circle(window, YELLOW, (pacman_x, pacman_y), 20)

    # 먹이 그리기
    pygame.draw.circle(window, RED, (food_x, food_y), 10)

    create_light.save_image(width,height, pacman_x, pacman_y, pacman_x, pacman_y)

    # 이미지 불러오기
    image_path = "light.png"  # 이미지 파일 경로 설정
    image = pygame.image.load(image_path)

    # 이미지 크기 설정 (선택 사항)
    image_width = width
    image_height = height
    image = pygame.transform.scale(image, (image_width, image_height))
    window.blit(image, (0, 0))

    # 점수 표시
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, YELLOW)
    window.blit(text, (10, 10))

    pygame.display.flip()


def check_collision():
    global pacman_x, pacman_y, food_x, food_y, score

    if abs(pacman_x - food_x) < 20 and abs(pacman_y - food_y) < 20:
        score += 1
        food_x = 50
        food_y = 50


def game_loop():
    global pacman_x, pacman_y

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pacman_y -= move_speed
        if keys[pygame.K_DOWN]:
            pacman_y += move_speed
        if keys[pygame.K_LEFT]:
            pacman_x -= move_speed
        if keys[pygame.K_RIGHT]:
            pacman_x += move_speed

        check_collision()
        draw()
        clock.tick(60)


game_loop()
