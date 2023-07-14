import pygame
import sounds
import game_functions as gf
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from bullet import Bullet
from ship import Ship, Persona
from button import Button

def run_game():
	""" Инициализация pygame, settings и объекта экрана """
	pygame.init()
	""" Music """
	sounds.ost_sound()
	""" Тут задействуется импортируемый модуль с настройками """
	ai_settings = Settings()
	screen = pygame.display.set_mode(
	(ai_settings.screen_width, ai_settings.screen_height))

	pygame.display.set_caption('Alien invasion') #Название игры
	# Создание кнопки Play
	play_button = Button(ai_settings, screen, "Play")
	# Создание экземпляров GameStats и Scoreboard
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)

	ship = Ship(ai_settings, screen)
	# Создание группы пуль
	bullets = Group()
	# Создание группы звезд
	stars = Group()
	# Создание группы пришельцев
	aliens = Group()
	# Создание флота пришельцев
	gf.create_fleet(ai_settings, screen, ship, aliens)
	# Создание звезд
	if ai_settings.stars_settings: # Если в настройках флаг Тру
		gf.create_star_sky(ai_settings, screen, stars)

	persona = Persona(ai_settings, screen)

	while True:
		#pygame.time.delay(-100)
		""" Для отслеживания экрана вызывается функция из модуля Гф """
		gf.check_events(ai_settings, screen, stats, sb, play_button,
			ship, aliens, bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb,
				ship, aliens, bullets)
			gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens,
				bullets)
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
			bullets, play_button, stars) # ,stars

run_game()
