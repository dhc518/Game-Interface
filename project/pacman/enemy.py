import time
import random
import pygame

# 10x10 배열 생성
array = [['empty' for _ in range(10)] for _ in range(10)]

# 35개의 block을 랜덤하게 넣기
for _ in range(35):
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        if array[x][y] == 'empty':
            array[x][y] = 'block'
            break

# 결과 출력
for row in array:
    print(row)

class Pixel:
    def __init__(self, array_x, array_y, window_x, window_y, velocity):
        self.array_x = array_x
        self.array_y = array_y
        self.window_x = window_x
        self.window_y = window_y
        #self.velocity = velocity 1초에 배열 1칸
        self.alive = True

    def draw(self, window):

        pygame.draw.circle(window, (255, 0, 0), (self.array_x * self.window_x / 10, self.array_y * self.window_y / 10), 20)

    def check_collision(self):


    def update(self):
        direct_list = [0, 1, 2, 3]
        random.shuffle(direct_list)

        while True:
            direction = direct_list.pop()

            if direction == 0:
            elif direction == 1:
            elif direction == 1:




