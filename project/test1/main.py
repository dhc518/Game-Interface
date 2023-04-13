from queue import Queue
from threading import Thread

import apply_coordinate
import pygame
import test







if __name__ == '__main__':
    pygame.init()
    q1 = Queue()
    q2 = Queue()

    p1 = Thread(target=test.main, args=(q1, q2))
    p2 = Thread(target=apply_coordinate.check_face, args=(q1, q2))


    p1.start()
    p2.start()

    p1.join() #test 프로그램 종료 대기
    p2.join() #mediapipe 프로그램 종료 대기