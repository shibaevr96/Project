# -*- coding: utf-8 -*-
import sys
import pygame
from random import randrange as rnd
from pygame.locals import *
pygame.init()

w = pygame.display.set_mode((900, 600))
w.fill((10,150,150)) 

class helocopter(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.r=10
		self.vx = 0.005 
		self.vy = -0.003
		self.ax = 0.8 #ускорение для движения по горизонтали
		self.ay = 1.2 #ускорение по вертикали
		self.gy = 0.8 #ускорение свободного падения
		self.fly = 1 # в полете = 1, не в полете = 0
		self.fuelmax = 100 #емкость бака
		self.fuel = self.fuelmax - 80 # количество топлива вначале
		
		self.hel = pygame.image.load('hel.png').convert_alpha() #изображение
		self.hel_org = self.hel
		self.hel_rect = self.hel.get_rect()
		
		self.image = self.hel
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.x = 150
		self.rect.y = 150
		self.x = self.rect.x
		self.y = self.rect.y
		self.angle = 0 # угол поворота

	def left(self):
		self.vx -= self.ax 
		
	def right(self):
		self.vx += self.ax
		
	def up(self):
		self.vy -= self.ay
		self.fly = 1 # если нажали вверх, то мы в полете
	
	def down(self):
		if self.fly:
			self.vy += self.ay
		
		
	def update(self):
		if self.fly:
			self.fuel -= 0.01 # в полете тратим топливо
			#print self.fuel
		self.angle = -45*(self.vx/15) #рассчитать угол наклона в зависимости от скорости
		self.x += self.vx # изменяем координаты
		self.y += self.vy
		
		self.rect.x = self.x # перемещаем спрайт в координаты
		self.rect.y = self.y

		if self.vy < 0.8: # притяжение к земле не может быть бесконечным
			self.vy += self.gy
		self.rotate()
			
	def rotate(self):
		self.image = pygame.transform.rotate(self.hel_org, self.angle) # повернуть спрайт

		
textFont = pygame.font.Font(None, 14) # не используется

h1 = helocopter() # создать экземпляр класса вертолет
h2 = helocopter()
hels = pygame.sprite.Group() # группа для обновления (вертолеты)
hels.add(h1)
hels.add(h2)
			
clock = pygame.time.Clock() # нужно для указания количества кадров в секунду

while 1:
	textimage = textFont.render(str(h1.angle)+' '+str(h1.vy),1,(250,250,50)) # не испол.
	for event in pygame.event.get(): # перебираем все события (нам нужны нажатия клавиш)
		if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
			sys.exit(0)		# выйти по нажатию ESC или по кнопке закрытия окна
				
	keys = pygame.key.get_pressed() # определяем нажатые клавиши и управляем вертолетами
	if keys[K_LEFT]:
		h1.left()
	if keys[K_RIGHT]:
		h1.right()
	if keys[K_UP]:
		h1.up()
	if keys[K_DOWN]:
		h1.down()

	if keys[K_a]:
		h2.left() 
	if keys[K_d]:
		h2.right()
	if keys[K_w]:
		h2.up()
	if keys[K_s]:
		h2.down()
		
	w.fill((10,150,150)) # очищаем экран

	hels.update() # рассчиываем вертолеты
	hels.draw(w) # отрисовывем спрайты
	
	pygame.display.flip() # ! буфер - на экран
	clock.tick(25) # 25 кадров в секунду, не более
