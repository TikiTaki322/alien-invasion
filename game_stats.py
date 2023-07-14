
class GameStats():
	""" Отслеживание статы для игры """
	def __init__(self, ai_settings):
		self.ai_settings = ai_settings
		self.reset_stats()
		# Игра запускается в неактивном состоянии
		self.game_active = False
		# Рекорд
		self.high_score = 0
		self.file_check()

	def reset_stats(self):
		""" Инициализирует стату, изменяющуюся в ходe игры. """
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1

	def file_check(self):
		""" Проверяет есть ли файл с записанным рекордом. """
		try:
			with open("score.txt", 'r') as f:
				j = int(f.read())
				self.high_score = j
		except FileNotFoundError:
			pass
