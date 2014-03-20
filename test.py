import sys
import pygame
from random import randrange as rnd
from pygame.locals import *
pygame.init()

#br1_test

w = pygame.display.set_mode((900, 600))
w.fill((10,150,150)) 

class helocopter(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.r=10
		self.vx = 0.005
		self.vy = -0.003
		self.ax = 0.8
		self.ay = 1.2
		self.gy = 0.8
		self.jump = 0
		self.fly = 1
		self.fuelmax = 100
		self.fuel = self.fuelmax - 80
		
		self.hel = pygame.image.load('hel.jpg').convert_alpha()
		self.hel_org = self.hel
		self.hel_rect = self.hel.get_rect()
		self.hel.set_colorkey((255,255,255))
		
		self.image = self.hel
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.x = 150
		self.rect.y = 150
		self.x = self.rect.x
		self.y = self.rect.y
		self.angle = 0

	def left(self):
		self.vx -= self.ax
		
	def right(self):
		self.vx += self.ax
		
	def up(self):
		self.vy -= self.ay
		self.fly = 1
	
	def down(self):
		if self.fly:
			self.vy += self.ay
		
		
	def update(self):
		if self.fly:
			self.fuel -= 0.01
			print self.fuel
		self.angle = -45*(self.vx/15)
		self.x += self.vx
		self.y += self.vy
		
		self.rect.x = self.x
		self.rect.y = self.y

		if self.vy < 0.8:
			self.vy += self.gy
		self.rotate()
			
	def rotate(self):
		self.image = pygame.transform.rotate(self.hel_org, self.angle)

		
textFont = pygame.font.Font(None, 14)

h1 = helocopter()
h2 = helocopter()
hels = pygame.sprite.Group()
hels.add(h1)
hels.add(h2)
			
clock = pygame.time.Clock()

while 1:
	textimage = textFont.render(str(h1.angle)+' '+str(h1.vy),1,(250,250,50))
	for event in pygame.event.get():
		if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
			sys.exit(0)		
				
	keys = pygame.key.get_pressed()
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
		
	w.fill((10,150,150))	

	hels.update()
	hels.draw(w)
	
	pygame.display.flip()
	clock.tick(25)
