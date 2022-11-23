import sys
import pygame
from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Реагирует на нажатие клавиш"""
        #Вправо
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
        #Влево
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)



def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш"""
        #Вправо
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
        #Влево
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        #Переместить корабль вправо и влево



def check_ivents(ai_settings, screen, ship, bullets):
    """Обрабатывает нажатия клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #Нажал клавишу
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        #Отпустил клавишу
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)



def update_screen(ai_settings, screen, ship, bullets):
    """Обновляет изображение на экране и отображает новый экран."""
    #Все пули выводятся позади изображений корабля и пришельцев.

    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()



def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум ещё не достигнут."""
    if len(bullets) < ai_settings.bullets_allowed:
        #Создание новой пули и включение её в группу bullets.
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)



def update_bullets(bullets):
    """Обновляет позиции пуль и уничтожает старые пули."""
    #Обновление позиций пуль
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)