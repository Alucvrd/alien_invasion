import sys
import pygame
from settings import Setings
from ship import Ship
import game_functions as gf #Указываем псевдоним функции
from pygame.sprite import Group
from alien import Alien


def run_game():
    #Инициализирует игру и создаёт объект экрана
    pygame.init()
    ai_settings = Setings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #Экземпляр корабля
    ship = Ship(ai_settings, screen)

    #Создание группы для хранения пуль.
    bullets = Group()
    #Создание группы для хранения пришельцев
    aliens = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)


    #Запуск основного цикла игры
    while True:
        #Отслеживание событий клавиаутыр и мыши.
        gf.check_ivents(ai_settings, screen, ship, bullets)

        #Обновление корабля
        ship.update()
        
        #Обновление пули
        gf.update_bullets(bullets)
        # Тест количества пуль на экране
        #print(len(bullets))


        #Обновление пришельцев
        gf.update_aliens(ai_settings, aliens)


        #Обновляет экран
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)

        #Отображение последнего прорисованного экрана
        pygame.display.flip()

run_game()