import sys
import pygame
from settings import Setings
from ship import Ship
import game_functions as gf #Указываем псевдоним функции
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

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



    #Создание экземпляря для хранение статистики игры и счёта.
    stats = GameStats(ai_settings)
    scoreboard = Scoreboard(ai_settings, screen, stats)

    #Создание кнопки Play.
    play_button = Button(ai_settings, screen, "Play")
    
    gf.create_fleet(ai_settings, screen, ship, aliens)

    gf.update_screen(ai_settings, screen, stats, scoreboard, ship, aliens, bullets, play_button)
    #Запуск основного цикла игры
    while True:
        #Отслеживание событий клавиаутыр и мыши.
        gf.check_ivents(ai_settings, screen, stats, play_button, ship, aliens, bullets, scoreboard)

        if stats.game_active: 
            #Обновление корабля
            ship.update()
        
            #Обновление пули
            gf.update_bullets(ai_settings, screen, ship, stats, scoreboard, aliens, bullets)
            # Тест количества пуль на экране
            #print(len(bullets))


            #Обновление пришельцев
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)

            gf.update_screen(ai_settings, screen, stats, scoreboard, ship, aliens, bullets, 
            play_button)

run_game()