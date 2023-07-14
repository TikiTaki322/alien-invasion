import pygame, random

def ost_sound():
	""" Music """
	pygame.mixer.music.load('sounds/мистичная тема.wav')
	pygame.mixer.music.set_volume(0.6)
	pygame.mixer.music.play(loops=-1)

def shot_sound():
	shoot_sound = pygame.mixer.Sound('sounds/shot1.wav')
	shoot_sound.play()

def random_allien_sound():
	random_allien_death = list()
	for item in ['sounds/пришелец1.wav', 'sounds/пришелец2.wav',
				'sounds/1.wav', 'sounds/2.wav', 'sounds/3.wav',
				'sounds/4.wav', 'sounds/5.wav']:
		random_allien_death.append(pygame.mixer.Sound(item))
	random.choice(random_allien_death).play()
