import pygame
import random
import math
import copy



pygame.init()
screen = pygame.display.set_mode((1920, 1080))

colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255),
    (128, 0, 128), (0, 128, 128)
]

q = [0,1,2,3,4,5,6]
random.shuffle(q)

def create_points():
    global q



    center_color = random.choice(colors)
    other_colors = copy.deepcopy(colors)
    other_colors.remove(center_color)
    target_colors = other_colors
    random.shuffle(target_colors)
    target_colors.insert(q.pop(0),center_color)

    return center_color, target_colors

def draw_points(center_color, target_colors):
    pygame.draw.circle(screen, center_color, (960, 540), 50)

    positions = [
        (25, 25), (960, 25),(1895, 25),
        (25, 540), (1895, 540),
        (25, 1055), (960, 1055), (1895, 1055)
    ]

    for i, position in enumerate(positions):
        pygame.draw.circle(screen, target_colors[i], position, 25)

def check_clicked_color(mouse_pos, center_color, target_colors):
    positions = [
        (25, 25), (960, 25),(1895, 25),
        (25, 540), (1895, 540),
        (25, 1055), (960, 1055), (1895, 1055)
    ]

    for i, position in enumerate(positions):
        dx, dy = mouse_pos[0] - position[0], mouse_pos[1] - position[1]
        distance = math.sqrt(dx * dx + dy * dy)

        if distance <= 25:
            return target_colors[i] == center_color #, i

    return False

def draw_timer(time_elapsed):
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"{time_elapsed:.1f}s", True, (0, 0, 0))
    screen.blit(timer_text, (935, 400))

def draw_timer(time_elapsed):
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"{time_elapsed:.1f}s", True, (0, 0, 0))
    screen.blit(timer_text, (935, 400))

def draw_complite():
    font = pygame.font.Font(None, 36)
    complite_text = font.render("Complite & Ready", True, (0, 0, 0))
    screen.blit(complite_text, (885, 400))


def main():
    global q

    running = True
    game_started = False
    center_color, target_colors = create_points()

    clock = pygame.time.Clock()
    start_ticks = 0

    while running:
        if len(q) == 0:
            q = [0, 1, 2, 3, 4, 5, 6]
            random.shuffle(q)
            game_started = False


        screen.fill((255, 255, 255))
        time_elapsed = (pygame.time.get_ticks() - start_ticks) / 1000

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()




            if keys[pygame.K_q]:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    game_started = True
                    start_ticks = pygame.time.get_ticks()

                elif check_clicked_color(pygame.mouse.get_pos(), center_color, target_colors):
                    correct_click_position = pygame.mouse.get_pos()
                    print("좌표:", correct_click_position)
                    center_color, target_colors = create_points()
                    start_ticks = pygame.time.get_ticks()

        draw_points(center_color, target_colors)

        if game_started:
            draw_timer(time_elapsed)
        else:
            draw_complite()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()


