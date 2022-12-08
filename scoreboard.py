import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """Класс для вывода игровой информации."""
    def __init__(self, ai_settings, screen, stats):
        """Инициализирует атрибуты подсчёта очков"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats


        #Настройки шрифты для вывода счёта.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        #Подготовка исходного изображения.
        self.prep_score()
        self.prep_hight_score()
        self.prep_level()
        self.prep_ships()
    

    def prep_score(self):
        """Преобразует текущий счёт в графическое изображение."""
        rounded_score = int(round(self.stats.score, -1))
        #Директива форматирования
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
        self.ai_settings.bg_color)

        #Вывод счёта в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def show_score(self):
        """Выводит счёт на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.hight_score_image, self.hight_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #Вывод кораблей.
        self.ships.draw(self.screen)


    def prep_hight_score(self):
        """Преобразует рекордный счёт в графическое изображение."""
        hight_score = int(round(self.stats.hight_score, -1))
        #Директива форматирования
        hight_score_str = "{:,}".format(hight_score)
        self.hight_score_image = self.font.render(hight_score_str, True, self.text_color, 
        self.ai_settings.bg_color)

        #Вывод счёта в центре верхней стороне
        self.hight_score_rect = self.score_image.get_rect()
        self.hight_score_rect.centerx = self.screen_rect.centerx
        self.hight_score_rect.top = self.score_rect.top
    

    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        self.level_image = self.font.render(str(self.stats.level), True,
        self.text_color, self.ai_settings.bg_color)

        #Уровень выводится под текущим счётом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    

    def prep_ships(self):
        """Сообщает количество оставшихся кораблей."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)