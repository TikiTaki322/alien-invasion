import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	def __init__(self, ai_settings, screen):
		""" Инициализирует корабль и задает его начальную позицию """
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		self.image = pygame.image.load('images/version.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		""" Каждый новый корабль появляется у нижнего края экрана """
		self.rect.center = self.screen_rect.center #((x, y))
		self.rect.bottom = self.screen_rect.bottom


		self.center = float(self.rect.centerx)
		self.bottom = float(self.rect.bottom)

		self.text = False
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False


	def update(self):
		""" Обновляет поз. корабля с учетом флагов """
		# Обновляется атрибут center, не rect !
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor

		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor

		if self.moving_up and self.rect.top > 0:
			self.bottom -= self.ai_settings.ship_speed_factor

		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.bottom += self.ai_settings.ship_speed_factor

		""" Обновляется атрибут rect на основании self.center """
		self.rect.centerx = self.center
		self.rect.bottom  = self.bottom

	def blitme(self):
		""" Рисует корабль в тек. позиции """
		self.screen.blit(self.image, self.rect) # Что рисовать и где(селф рект)

	def easter_egg(self, ai_settings):
		""" Вывод текста """
		if self.text != False:
			self.font = pygame.font.SysFont('couriernew', 60)
			self.text = self.font.render(
			str(self.ai_settings.text_for_egg), True,
			(self.ai_settings.egg_text_color))
			self.screen.blit(self.text, (100, 220))

	def center_ship(self):
		""" Размещает корабль по центру нижней стороны """
		self.center = self.screen_rect.centerx
		self.bottom = self.screen_rect.bottom

class Persona(Ship):
	def __init__(self, ai_settings, screen):
		super().__init__(ai_settings, screen)
		self.image = pygame.image.load('images/doom.png')

		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

