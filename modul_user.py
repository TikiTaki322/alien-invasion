class User():
	""" Супер-класс для объявления пользователя, и при надобности
	дополнительной информации """
	def __init__(self, first_name, last_name, **user_info):
		self.first_name = first_name
		self.last_name = last_name
		self.user_info = user_info
		self.full_name = self.first_name + ' ' + self.last_name
		self.login_attempts = 0

	def describe_user(self):
		""" Метод выводит инфу о пользователе. Если нет доп инфы,выводит
		только имя фамилию """
		print('\nFull name: %s.' % (self.full_name.title()))
		if self.user_info:
			person = {}
			person['first_name'] = self.first_name
			person['last_name'] = self.last_name
			for key, value in self.user_info.items():
				person[key] = value
			for i,v in person.items():
				print(i,'->',v)
		print('Hello, %s.' % (self.first_name.title()))

	def incremet_login_attempts(self):
		""" Метод для подсчета количества попыток авторизации """
		if self.login_attempts < 8:
			self.login_attempts += 1
		else:
			print('Kol-vo tryev zakonchilos`!')

	def reset_login_attempts(self):
		""" Метод для обнуления попыток """
		self.login_attempts = 0


""" Функция для авторизации юзера """
def autorization(user_name, user_pass):
	""" Для вызова, в нее передаются входные данные юзера, которые
	используются при его объявлении """
	while True :
		parol = input('\nEnter password for %s: '
		%(user_name.full_name.title()))
		if parol.lower() != user_pass:
			print('\t-Wrong password!')
			user_name.incremet_login_attempts()
			if user_name.login_attempts >= 8:
				print('Kol-vo tryev zakonchilos`!')
				break
		else:
			print('%s, autorization good =)' % (user_name.full_name.title()))
			print('Summa traev --> %d.' % (user_name.login_attempts + 1))
			break

class Privileges():
	""" Вспомогательный класс, служит атрибутом в классе Admin. Осуществляет
	перебор списка в котором хранятся возможности(привелегии), которыми
	обладает администратор """
	def __init__(self, privileges=''):
		self.privileges = privileges
	def show_privileges(self):
		""" Простейший метод для перебора списка """
		for privilege in self.privileges:
			print(privilege)

class Admin(User):
	""" Наследующий класс от класса User, создан для вычленения подгруппы
	'администраторов' среди общей массы юзеров, позволяет передавать
	список с привелегиями, которые будут перебраны и отображены с помощью
	класса Privileges """
	def __init__(self, first_name, last_name, peremen='', **user_info):
		super().__init__(first_name, last_name, **user_info)
		self.priv = Privileges(peremen)
