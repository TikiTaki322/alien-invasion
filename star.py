import pygame
from pygame.sprite import Sprite

class Star(Sprite):
	""" Класс представляющий одну звезду """
	def __init__(self, ai_settings, screen):
		""" Инициализирует пришельца и задает его начальную позицию """
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# Загрузка изображения монстра и назначение атрибута rect
		self.image = pygame.image.load('images/star3.png')
		self.rect = self.image.get_rect()

		# Каждый новый монстр появляется в левом верхнем углу экрана
		# self.rect.x = self.rect.width
		# self.rect.y = self.rect.height

		# Сохранение позиции пришельца
		# self.x = float(self.rect.x)

	def blitme(self):
		# Выводит пришельца в текущем положении
		self.screen.blit(self.image, self.rect)
