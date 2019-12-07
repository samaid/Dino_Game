# -*- coding: utf8 -*-
import pygame
import numpy as np
import random

X_SIZE = 800
Y_SIZE = 600
WIN_SIZE = (X_SIZE, Y_SIZE)

# Цвета игры
COLOR_WHITE = (255, 255, 255)
COLOR_DINO = (128, 0, 0)
COLOR_STONE = (100, 100, 100)

# Другие константы
MAX_JUMP_HEIGHT = 150

Y_GROUND = 500

DINO_SIZE_X = 10
DINO_SIZE_Y = 20

# Класс динозавр
class Dino:
    def __init__(self, screen, x):
        # Инициализация динозавра (экран, на котором рисуется динозавр и его начальная позиция)
        self.x = x
        self.screen = screen
        self.jump_height = 0
        self.jump_speed = 0

    def draw(self):
        # Нарисовать Дино в текущей позиции на текущем экране
        pygame.draw.rect(self.screen, COLOR_DINO,
                         ((self.x, Y_GROUND - self.jump_height - DINO_SIZE_Y), (DINO_SIZE_X, DINO_SIZE_Y)))


    def jump(self):

        # Определить, двигаемся или нет
        speed_sign = np.sign(self.jump_speed)  # Получить направление движения + вверх, - вниз, 0 - нет движения
        if speed_sign == 0:
            # Нет движения, но начинаем прыхок вверх
            speed_sign = 1

        # Обновить скорость
        self.jump_speed = speed_sign * max(1, int((MAX_JUMP_HEIGHT - self.jump_height) * 0.2))

        # Обновить высоту
        self.jump_height += self.jump_speed

        # Проверка, на максимальной ли высоте Дино
        if self.jump_height >= MAX_JUMP_HEIGHT:
            # Достигли максимальной высоты. Начинаем движение вниз
            self.jump_height = MAX_JUMP_HEIGHT
            self.jump_speed = -1

        # Проверка, на минимальной ли высоте Дино
        if self.jump_height <= 0:
            # Достигли минимальной высоты. Закончили прыжок
            self.jump_height = 0
            self.jump_speed = 0


    def on_the_ground(self):
        return self.jump_height == 0


# Класс камень
class Stone():
    def __init__(self, screen, x, size):
        self.screen = screen
        self.x = x
        self.size = size

    def draw(self):
        pygame.draw.circle(self.screen, COLOR_STONE, (self.x, Y_GROUND - self.size), self.size)

    def move(self):
        self.x -= 1

# Класс земля с камнями на ней и Дино
class GroundWithStonesAndDino():

    def __init__(self, screen):
        self.screen = screen
        self.stones = []  # Изначально нет камней на земле
        self.dino = Dino(screen, 50)

    def draw(self):
        pygame.draw.line(self.screen, COLOR_STONE, (0, Y_GROUND), (X_SIZE, Y_GROUND))
        for stone in self.stones:
            stone.draw()
        self.dino.draw()

    def move(self):
        for stone in self.stones:
            stone.move()
            if stone.x < -stone.size:
                self.stones.remove(stone)  # Камень скрылся за экраном, удаляем: он больше не нужен

        if random.randrange(500) == 0:
            # Создаем новый камень
            stone_size = random.randrange(10, 20)
            new_stone = Stone(self.screen, X_SIZE+stone_size, stone_size)
            self.stones.append(new_stone)

    # Определить, столкнулся ли Дино с одним из камней
    def dino_hit_stone(self):
        for stone in self.stones:
            if abs(self.dino.x - stone.x) <= stone.size and self.dino.jump_height <= stone.size:
                return True
        return False

def main():
    # Программа должна начинаться с инициализации pygame
    pygame.init()
    screen = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Run Dino! Run!")
    clock = pygame.time.Clock()

    # Другие инициализации, специфичные для игры
    do_pygame = True
    do_pause = False
    ground_with_stones_and_dino = GroundWithStonesAndDino(screen)

    # Главный цикл программы. Каждую итерацию опрашиваются и обрабатываются события,
    # изменяются объекты и перерисовываются на экране
    while do_pygame:

        # Обработка событий
        for event in pygame.event.get():  # Обрабатываем все события, которые случились с предыдущей итерации
            if event.type == pygame.QUIT:  # Если нажата кнопка ЗАКРЫТЬ - выход из программы
                do_pygame = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    do_pause = True
                elif not do_pause:  # Все остальные кнопки не работают, пока игра на паузе
                    if event.key == pygame.K_UP and ground_with_stones_and_dino.dino.on_the_ground():
                        # Если нажата клавиша ВВЕРХ и Дино на земле
                        ground_with_stones_and_dino.dino.jump()

        # Здесь перерисовывуются все объекты
        screen.fill(COLOR_WHITE)
        ground_with_stones_and_dino.draw()

        # Обрабатываем другие изменения объектов, не связанные с событиями
        if not ground_with_stones_and_dino.dino.on_the_ground():
            # Если Дино в воздухе, то он продолжает прыгать
            ground_with_stones_and_dino.dino.jump()

        ground_with_stones_and_dino.move()
        if ground_with_stones_and_dino.dino_hit_stone():
            # Игра окончена
            print("Игра окончена")
            do_pygame = False

        # Каждая итерация заканчивается этими двумя командами
        pygame.display.flip()  # Отображаем перерисованное на экране
        clock.tick(60)  # Каждая итерация занимает 60 миллисекунд

        # Освобождаем память по окончании игры
    pygame.quit()


if __name__ == "__main__":
    main()