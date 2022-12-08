import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets, scoreboard):
    """Реагирует на нажатие клавиш"""
        #Вправо
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
        #Влево
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    #Запускает новую игру при нажатии P на клавиатуре
    elif event.key == pygame.K_p:
        ai_settings.initialize_dynamic_settings()
        start_game(ai_settings, screen, stats, ship, aliens, bullets, scoreboard)


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш"""
        #Вправо
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
        #Влево
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        #Переместить корабль вправо и влево



def check_ivents(ai_settings, screen, stats, play_button, ship, aliens, bullets, scoreboard):
    """Обрабатывает нажатия клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #Нажал клавишу
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets, scoreboard)
        #Отпустил клавишу
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        #Клик мыши по кнопке
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, scoreboard)


def start_game(ai_settings, screen, stats, ship, aliens, bullets, scoreboard):
    """Запускает новую игру."""
    #Указатель мыши скрывается
    pygame.mouse.set_visible(False)


    #Сброс игровой статистики
    stats.reset_stats()
    stats.game_active = True
    #Сброс изображение счетов и уровня
    scoreboard.prep_score()
    scoreboard.prep_hight_score()
    scoreboard.prep_level()
    scoreboard.prep_ships()

    #Очистка списков пришельцев и пуль
    bullets.empty()
    aliens.empty()

    #Создание нового флота и размещение корабля в центре
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, scoreboard):
    """Запускает новую игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, ship, aliens, bullets, scoreboard)
        ai_settings.initialize_dynamic_settings()


def update_screen(ai_settings, screen, stats, scoreboard, ship, aliens, bullets, play_button):
    """Обновляет изображение на экране и отображает новый экран."""
    #Все пули выводятся позади изображений корабля и пришельцев.

    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    scoreboard.show_score()
    ship.blitme()
    aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()
    
    pygame.display.flip()



def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум ещё не достигнут."""
    if len(bullets) < ai_settings.bullets_allowed:
        #Создание новой пули и включение её в группу bullets.
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)



def update_bullets(ai_settings, screen, ship, stats, scoreboard, aliens, bullets):
    """Обновляет позиции пуль и уничтожает старые пули."""
    #Обновление позиций пуль
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, stats, scoreboard, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещающихся на экране."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создаёт пришельца и размещает его в ряду."""   
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width

    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Создаёт флот пришельцев"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #Создание пришельца и размешение его в ряду.
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_bullet_alien_collisions(ai_settings, screen, ship, stats, scoreboard, aliens, bullets):
    """Обработка коллизий пуль с пришельцами."""
    #Проверка попаданий в пришельцев
    #При обнаружении попадания удалить пулю и пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.alien_points * len(alien)
        scoreboard.prep_score()
        check_hight_score(stats, scoreboard)
    if len(aliens) == 0:
        #Уничтожение существующих пуль и создание нового флота
        bullets.empty()
        ai_settings.increase_speed()
        ai_settings.increase_score()
        stats.level += 1
        scoreboard.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, scoreboard):
    """Обрабатывает столкновение корабля с пришельцем."""
    if stats.ships_left > 0:
        #Уменьшение ships_left
        stats.ships_left -= 1
        scoreboard.prep_ships()
        #Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()

        #Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #Пауза
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, scoreboard):
    """Проверяет, достиг ли флот края экрана, после чего обновляет позиции всех пришельцев в ряду"""
    check_fleet_edges(ai_settings, aliens)

    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)
    
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, scoreboard):
    """Проверяет, добрались ли пришельцы до нижнего края экрана."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Происходит то же, что при столкновении с кораблём.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)
            break

def check_hight_score(stats, scoreboard):
    """Проверяет, появился ли новый рекорд."""
    if stats.score > stats.hight_score:
        stats.hight_score = stats.score
        scoreboard.prep_hight_score()
