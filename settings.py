import pygame

class Setings():
    """Класс для хранения всех настроек игры Alien Invasion"""

    def __init__(self):
        """Инициализирует статические настройки игры"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)
        self.bg_image = pygame.image.load('images/background.jpeg')


        #Параметры пули
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 14, 92
        self.bullets_allowed = 3

        #Настройки пришельцев
        self.fleet_drop_speed = 10
        
        #Кол-во кораблей
        self.ship_limit = 3


        #Темп ускорения игры
        self.speedup_scale = 1.1

        #Темп увеличения очков
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.sheep_speed_factor = 1.5
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 1
        
        #Кол-во очков за сбитие одного пришельца
        self.alien_points = 10

        #fleet_direction = 1 обозначает движение вправо; а -1 - влево
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличивает настройки скорости"""
        self.sheep_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

    def increase_score(self):
        """Увеличение счёта."""
        self.alien_points *= self.score_scale