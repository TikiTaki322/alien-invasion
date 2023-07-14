class Settings():
	""" Класс для хранение всех настроек игры Alien Invasion """
	def __init__(self):
		""" Инициализация неизменяемых настроек игры """
		# Настройка экрана
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (51, 102, 204)
		# Настройка корабля
		self.ship_limit = 3 # Кол-во кораблей
		# Настройка пуль
		self.bullet_widht = 3
		self.bullet_height = 15
		self.bullet_color = 102, 0, 204 # 255, 153, 51
		self.bullets_allowed = 3
		# Пасхалка
		self.text_for_egg = 'Pashalka naidena(z)'
		self.egg_text_color = 255, 255, 255
		# Настройка пришельцев
		self.fleet_drop_speed = 10
		# Темп ускорения игры
		self.speedup_scale = 1.1
		# Темп роста стоимости пришельцев
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		""" Инициализирует настройки, изменяющиеся в ходе игры """
		# Вкл/Выкл звезды
		self.stars_settings = True #True # False
		self.ship_speed_factor = 5.5 # 5.5 - для режима со звездами
		self.bullet_speed_factor = 6.5 # 6.5 - для режима со звездами
		self.alien_speed_factor = 2 # 2 - для режима со звездами

		self.fleet_direction = 1 # fleet_direction = 1 означает движение вправо, а -1 - влево
		# Points
		self.alien_points = 10

	def increase_speed(self):
		""" Увеличивает настройки игры """
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)




