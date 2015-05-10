import pygame, sys, random
from pygame.locals import *


STARTING_STEP_TIME = 200
MIN_STEP_TIME = 100
STAGE_WIDTH = 10
STAGE_HEIGHT = 20

pygame.init()
pygame.key.set_repeat(100, 75)
screen = pygame.display.set_mode((16*32, 640))
pygame.display.set_caption("TETRIS")

block_sprite = pygame.image.load("block.png").convert()
frozen_block_sprite = pygame.image.load("frozen_block.png").convert()
font = pygame.font.Font(None, 35)

board = pygame.Surface((320, 640))
board.fill((255,255,255))
sidebar = pygame.Surface((6*32, 640))
sidebar.fill((0, 0, 255))
gameover_txt = font.render("GAME OVER: SPACE TO PLAY AGAIN", False, (0,0,0))

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
	def __init__(self, kind, x=-1):
		self.index = 0
		self.kind = kind
		if x != -1:
			self.x = x
			self.adjust()
		else:
			self.x = 32*((STAGE_WIDTH / 2) - (self.get_size() / 2))
		self.y = - 32*self.get_size()
		
	
	def rot_left(self, world):
		old_index = self.index
		if self.index == 0:
			self.index = pieces[self.kind][0] - 1
		else:
			self.index -= 1
		self.adjust()
		if not self.check_safe(world):
			self.index = old_index
	
	def rot_right(self, world):
		old_index = self.index
		if self.index == pieces[self.kind][0] - 1:
			self.index = 0
		else:
			self.index += 1
		self.adjust()
		if not self.check_safe(world):
			self.index = old_index
	
	def advance(self):
		self.y += 32
		
	def move_x(self, x_off):
		self.x += x_off
		self.adjust()
		
	def move_left(self, world):
		if not any(self.check_left(world)):
			self.x -= 32
	
	def move_right(self, world):
		if not any(self.check_right(world)):
			self.x += 32
		
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
	
	def check_safe(self, world):
		x, y = self.get_pos()
		for loc, block in enumerate(self.get_matrix()):
			if block:
				x_o = loc % self.get_size()
				y_o = loc / self.get_size()
				if world[(y/32 + y_o) * STAGE_WIDTH + x/32 + x_o]:
					return False
		return True
			
	def check_below(self, world):
		below = [0] * self.get_size()
		for column in range(self.get_size()):
			for row in reversed(range(self.get_size())):
				if self.get_matrix()[row*self.get_size()+column]:
					if self.y/32 + row  >= STAGE_HEIGHT:
						below[column] = 1
						break
					if self.y/32 + row < 0:
						below[column] = 0
						break
					below[column] = world[(self.y/32 + row ) * STAGE_WIDTH + self.x/32 + column]
					break
		return below
	
	def check_left(self, world):
		left = [0] * self.get_size()
		for row in range(self.get_size()):
			for column in range(self.get_size()):
				if self.get_matrix()[row*self.get_size()+column]:
					if self.x/32 + column - 1 < 0:
						left[row] = 1
						break
					if self.y/32 + row < 0:
						left[row] = 0
						break	
					left[row] = world[(self.y/32 + row) * STAGE_WIDTH + self.x/32 + column - 1]
					break
		return left
	
	def check_right(self, world):
		right = [0] * self.get_size()
		for row in range(self.get_size()):
			for column in reversed(range(self.get_size())):
				if self.get_matrix()[row*self.get_size()+column]:
					if self.x/32 + column + 1 >= STAGE_WIDTH:
						right[row] = 1
						break
					if self.y/32 + row < 0:
						right[row] = 0
						break
					right[row] = world[(self.y/32 + row) * STAGE_WIDTH + self.x/32 + column + 1]
					break
		return right
			
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
		
	def get_kind(self):
		return self.kind

def draw_piece(surface, sprite, pos, dim, matrix):
	for i in range(dim):
		for j in range(dim):
			if matrix[dim * i + j]:
				surface.blit(sprite, (pos[0] + j*32, pos[1] + i*32))

def check_lines(world):
	i = 0
	r = STAGE_HEIGHT - 1
	while r >= 0:
		line = world[r*STAGE_WIDTH:r*STAGE_WIDTH + STAGE_WIDTH]
		if all(line):
			i += 1

			
			for row in reversed(range(0,r)):
				world[(row+1)*STAGE_WIDTH:(row+1)*STAGE_WIDTH + STAGE_WIDTH] = world[(row)*STAGE_WIDTH:(row)*STAGE_WIDTH + STAGE_WIDTH] 
		else:
			r -= 1
	return i
		

score_txt = font.render("Score:0", False, (0,0,0))
score = 0
test_piece = Piece(random.choice(pieces.keys()))
next_piece = random.choice(pieces.keys())
step = 0
switched = False
cur_step_time = STARTING_STEP_TIME
stage = [0] * (10*20)







while 1:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if test_piece:
				if event.key == K_LEFT:
					test_piece.move_left(stage)
				if event.key == K_RIGHT:
					test_piece.move_right(stage)
				if event.key == K_UP:
					test_piece.rot_left(stage)
				if event.key == K_z:
					test_piece.rot_left(stage)
				if event.key == K_x:
					test_piece.rot_right(stage)
				if event.key == K_DOWN:
					step += .6 * cur_step_time
				if event.key == K_RCTRL:
					if not switched:
						switched = True
						tmp = test_piece.get_kind()
						x = test_piece.get_pos()[0]
						test_piece = Piece(next_piece, x)
						next_piece = tmp
			elif event.key == K_SPACE:
				score_txt = font.render("Score:0", False, (0,0,0))
				score = 0
				test_piece = Piece(random.choice(pieces.keys()))
				next_piece = random.choice(pieces.keys())
				step = 0
				switched = False
				cur_step_time = STARTING_STEP_TIME
				stage = [0] * (10*20)
	
	if test_piece:
		step += 1
	if step >= cur_step_time:
		step = 0
		test_piece.advance()
	if test_piece:
		if any(test_piece.check_below(stage)):
			x, y = test_piece.get_pos()
			if y < 0:
				test_piece = None
				print "GAME OVER"
			else:
				for loc, block in enumerate(test_piece.get_matrix()):
					if block:
						y_off = loc / test_piece.get_size()
						x_off = loc % test_piece.get_size()
						
						
						stage[((y/32 + y_off - 1) * STAGE_WIDTH) + x/32 + x_off] = 1
				
				switched = False
				
				test_piece = Piece(next_piece, x)
				next_piece = random.choice(pieces.keys())
				num_of_lines = check_lines(stage)
				score += num_of_lines
				score_txt = font.render("Score:"+str(score), False, (0,0,0))
				if cur_step_time > MIN_STEP_TIME:
					cur_step_time -= 5 * num_of_lines

	
	screen.blit(board, (0,0))
	screen.blit(sidebar, (320,0))
	screen.blit(score_txt, (330,20))
	draw_piece(screen, block_sprite, (352, 300), pieces[next_piece][1], pieces[next_piece][2])
	for loc, block in enumerate(stage):
		if block:
			screen.blit(frozen_block_sprite, (32*(loc % STAGE_WIDTH), 32*(loc / STAGE_WIDTH)))
	
	if test_piece:
		draw_piece(screen, block_sprite, test_piece.get_pos(), test_piece.get_size(), test_piece.get_matrix())
	else:
		screen.blit(gameover_txt, (20,80))
	
	pygame.display.update()
