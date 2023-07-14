import pygame, sys
import sounds
from bullet import Bullet
from alien import Alien
from star import Star
from random import randint
from time import sleep

def check_keydown_events(event, ai_settings, screen, stats, sb,
	play_button, ship, aliens, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		save_global_score(stats)
	elif event.key == pygame.K_p:
		ship.text = True
	elif event.key == pygame.K_z:
		ship.text = False
	elif event.key == pygame.K_RETURN:
		start_game(ai_settings, screen, stats, sb, play_button,
			ship, aliens, bullets)

def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False

def start_game(ai_settings, screen, stats, sb, play_button,
	ship, aliens, bullets, mouse_x=None, mouse_y=None):
	if not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		# Сброс игровой статистики
		stats.reset_stats()
		stats.game_active = True
		# Сброс изображений счетов и уровня
		sb.prep_images()
		# Очистка списков пришельцев и пуль
		aliens.empty()
		bullets.empty()

		# Создание нового флота пришельцев и размещение корабля в центре.
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def save_global_score(stats):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
	filename = "score.txt"
	with open(filename, 'w') as file_object:
		file_object.write(str(stats.high_score))
		sleep(0.5)
		sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
	""" Cоздание новой пули и включение ее в группу bullets """
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
		sounds.shot_sound()

def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
	aliens, bullets, mouse_x, mouse_y):
	""" Запускает новую игру при нажатии кнопки Плей """
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		start_game(ai_settings, screen, stats, sb, play_button,
			ship, aliens, bullets, mouse_x, mouse_y)


def check_events(ai_settings, screen, stats, sb, play_button, ship,
	aliens, bullets):
	""" Отслеживание событий клавы и мыши """
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			save_global_score(stats)

		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, stats, sb,
				play_button, ship, aliens, bullets)

		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)

		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button,
				ship, aliens, bullets, mouse_x, mouse_y)



def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
	play_button, stars): # , stars
	""" При каждом проходе цикла перерисовывается экран """
	screen.fill(ai_settings.bg_color)
	stars.draw(screen)
	""" Все пули выводятся позади корабля и пришельцев """
	for bullet in bullets.sprites():
		bullet.draw_bullet()


	ship.blitme()
	ship.easter_egg(ai_settings) # Пасхалка на клавишу p
	aliens.draw(screen)

	# Вывод счета
	sb.show_score()
	# Кнопка Play отображается в том случае, если игра неактивна.
	if not stats.game_active:
		play_button.draw_button()

	""" Отображение последнего прорисованного экрана """
	pygame.display.flip()

def check_bullet_alien_collisions(ai_settings,
	screen, stats, sb, ship, aliens, bullets):
	""" Обработка коллизий пуль с пришельцами. """
	# Проверка попаданий в пришельцев
	# При обнаружении попадания удалить пулю и пришельца
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		sounds.random_allien_sound()
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
		sb.prep_score()
		check_high_score(stats, sb)
	start_new_level(bullets, screen, ai_settings, stats, sb, ship, aliens)


def start_new_level(bullets, screen, ai_settings, stats, sb, ship, aliens):
	if len(aliens) == 0:
		# Уничтожение существующих пуль и создание нового флота (новый уровень)
		bullets.empty()
		ai_settings.increase_speed()
		# Увеличение уровня
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	""" Функция обновляет позиции пуль и удаляет старые пули """
	bullets.update()
	# Удаление пуль вышедших за пределы экрана
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings,
	screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
	""" Проверяет появился ли новый рекорд """
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
	#	filename = "score.txt"
	#	with open(filename, 'w') as file_object:
	#		file_object.write(str(stats.high_score))

#-------------------------Создание-пришельцев--------------------------#

def get_number_aliens_x(ai_settings, alien_width):
	""" Вычисляет колво приш. в ряду """
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	""" Определяет колво рядов, помещающихся на экране """
	available_space_y = (ai_settings.screen_height -
	(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	""" Создание пришельца и размещение его в ряду """
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	""" Создает флот пришельцев """
	# Создание пришельца и вычисление колва приш. в ряду
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
	alien.rect.height)

	# Создание флота пришельцев
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			# Создание пришельца и размещение его в ряду
			create_alien(ai_settings, screen, aliens, alien_number,
			row_number)

#--------------Регулирование-движения-флота-пришельцев-----------------#

def check_fleet_edges(ai_settings, aliens):
	""" Реагирует на достижение пришельцами края экрана,
	после чего вызывает функцию 'change_fleet_direction', которая
	опускает каждого пришельца на ряд ниже. """
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	""" Опускает флот на ряд ниже и меняет направление флота. """
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
	""" Обрабатывает столкновения корабля с пришельцем. """
	if stats.ships_left > 0:
		# Уменьшает ships_left
		stats.ships_left -= 1
		sb.prep_ships()

		# Очистка списков пришельцев и пуль.
		aliens.empty()
		bullets.empty()

		# Создание нового флота и размещение корабля в центре.
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		print('Get damage!')
		# Pause
		sleep(0.5)

	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		print("Game over!!!")
		#font = pygame.font.SysFont('couriernew', 60)
		#text = font.render(('Game over, bitch!'), True, (255, 0, 0))
		#screen.blit(text, (100, 220))
		#sleep(1)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens,
	bullets):
		""" Проверяет, добрались ли пришельцы до края экрана """
		screen_rect = screen.get_rect()
		for alien in aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Происходит тоже что и при столкновении с кораблем
				ship_hit(ai_settings, stats, screen, sb, ship, aliens,
					bullets)
				break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens,
	bullets):
	"""
	Проверяет, достиг ли флот края экрана,
	после чего обновляет позиции всех пришельцев во флоте.
	"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	# Проверка коллизий "пришелец-корабль".
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, sb, ship, aliens,
		bullets)
	# Проверка пришельцев, добравшихся до нижнего края экрана.
	check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens,
	bullets)

#-------------------------Создание-звезд-------------------------------#
#                  Та-же-хуйня-как-для-пришельцев

def get_number_stars_x(ai_settings, star_width):
	""" Вычисляет колво звезд в ряду """
	available_space_x = ai_settings.screen_width - 2 * star_width
	number_stars_x = int(available_space_x / (2 * star_width))
	return number_stars_x

def get_number_rows_for_stars(ai_settings, star_height):
	""" Определяет колво рядов, помещающихся на экране """
	available_space_y = (ai_settings.screen_height - star_height)
	number_rows = int(available_space_y / (star_height))
	return number_rows

def create_star(ai_settings, screen, stars, star_number, row_number):
	star = Star(ai_settings, screen)
	star_width = star.rect.width
	random_x = randint(-15,15)
	random_y = randint(-12,12)
	star.x = star_width + 3 * star_width * star_number
	star.rect.x = star.x + random_x
	star.rect.y = (star.rect.height + random_y) + 2 * star.rect.height * row_number
	stars.add(star)

def create_star_sky(ai_settings, screen, stars):
	star = Star(ai_settings, screen)
	number_stars_x = get_number_stars_x(ai_settings, star.rect.width)
	number_rows = get_number_rows_for_stars(ai_settings, star.rect.height)
	for row_number in range(number_rows):
		for star_number in range(number_stars_x):
			create_star(ai_settings, screen, stars, star_number,
			row_number)



