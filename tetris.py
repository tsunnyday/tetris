import pygame, sys, random
from pygame.locals import *


STEP_TIME = 600
STAGE_WIDTH = 10
STAGE_HEIGHT = 20

# name: number of rotations, width/height (everything is stored in a square), each rotation
pieces = {"i":[2, 4, [0,1,0,0,
					  0,1,0,0,
					  0,1,0,0,
					  0,1,0,0],
					 [0,0,0,0,
					  0,0,0,0,
					  1,1,1,1,
					  0,0,0,0]],
					  
		  "o":[1, 2, [1,1,
					  1,1]],
          
		  "j":[4, 3, [0,1,0,
					  0,1,0,
					  1,1,0],
					 [0,0,0,
					  1,1,1,
					  0,0,1],
					 [0,1,1,
					  0,1,0,
					  0,1,0],
					 [1,0,0,
					  1,1,1,
					  0,0,0]],
		
          "l":[4, 3, [0,1,0,
					  0,1,0,
					  0,1,1],
					 [0,0,1,
					  1,1,1,
					  0,0,0],
					 [1,1,0,
					  0,1,0,
					  0,1,0],
					 [0,0,0,
					  1,1,1,
					  1,0,0]],
					  
		  
		  "s":[2, 3, [1,1,0,
					  0,1,1,
					  0,0,0],
					 [0,0,1,
					  0,1,1,
					  0,1,0]],
					  
		  "z":[2, 3, [0,1,1,
				      1,1,0,
					  0,0,0],
					 [1,0,0,
					  1,1,0,
					  0,1,0]]}
					
			   
class Piece:
	def __init__(self, kind, x, y):
		self.index = 0
		self.kind = kind
		self.x, self.y = x, y
		
	
	def rot_left(self):
		if self.index == 0:
			self.index = pieces[self.kind][0] - 1
		else:
			self.index -= 1
		self.adjust()
	
	def rot_right(self):
		if self.index == pieces[self.kind][0] - 1:
			self.index = 0
		else:
			self.index += 1
		self.adjust()
	
	def advance(self):
		self.y += 32
		
	def move_x(self, x_off):
		self.x += x_off
		self.adjust()
		
	def adjust(self):
		for i in range(self.get_size()):
			if any(self.get_column(i)):
				if self.x + 32*i < 0:
					self.x = 0 - 32*i
				break
		for i in reversed(range(self.get_size())):
			if any(self.get_column(i)):
				if self.x + 32*(i+1) > 32*10:
					self.x = 32*10 - 32*(i+1)
				break
			
	
			
	def get_column(self, x):
		return [self.get_matrix()[i*self.get_size()+x] for i in range(self.get_size())]
	
	def get_row(self, y):
		return [self.get_matrix()[y*self.get_size() + i] for i in range(self.get_size())]
	
	
	def get_pos(self):
		return (self.x, self.y)
	
	def get_size(self):
		return pieces[self.kind][1]
	
	def get_matrix(self):
		return pieces[self.kind][2 + self.index]

def draw_piece(surface, sprite, pos, dim, matrix):
	for i in range(dim):
		for j in range(dim):
			if matrix[dim * i + j]:
				surface.blit(sprite, (pos[0] + j*32, pos[1] + i*32))
	

pygame.init()
pygame.key.set_repeat(100, 75)
screen = pygame.display.set_mode((10*32, 640))
pygame.display.set_caption("TETRIS")

block_sprite = pygame.image.load("block.png").convert()



screen.fill((255,255,255))
pygame.display.update()

test_piece = Piece(random.choice(pieces.keys()), 160, 0)
step = 0
stage = [0] * (10*20)

while 1:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_LEFT:
				test_piece.move_x(-32)
			if event.key == K_RIGHT:
				test_piece.move_x(32)
			if event.key == K_UP:
				test_piece.rot_left()
			if event.key == K_z:
				test_piece.rot_left()
			if event.key == K_x:
				test_piece.rot_right()
			if event.key == K_DOWN:
				step += 400
			if event.key == K_RCTRL:
				test_piece = Piece(random.choice(pieces.keys()), 160, 0)
			if event.key == K_0:
				test_piece.get_row(0)
	
	step += 1
	if step >= STEP_TIME:
		step = 0
		test_piece.advance()
		
	
	screen.fill((255,255,255))
	draw_piece(screen, block_sprite, test_piece.get_pos(), test_piece.get_size(), test_piece.get_matrix())
	pygame.display.update()
