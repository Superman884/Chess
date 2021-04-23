import pygame
from time import sleep
from random import randrange
import keyboard
yes=['rook','bishop','pawn','king','horse','queen']
images=[]
win=pygame.display.set_mode((600,600))
clicked=None
for i in yes:
	for j in range(2):
		images.append(pygame.image.load(i+'_'+str(j+1)+'.png'))
class piece():
	def __init__(self, color=None, value=None):
		self.color=color
		self.value=value
def make_board(wid,hei):
	run=True
	for y in range(0,hei,hei//8):
		for x in range(0,wid,wid//8):
			rank=(y/75)*8+(x/75)
			if (x/75+y/75)%2==0:
				color=(255,228,156)
			else:
				color=(106,77,15)
			pygame.draw.rect(win, color, pygame.Rect(x, y, 80, 80))
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run=False
					break
			if run==False:
				break
		if run==False:
			break
class board():
	def __init__(self):
		self.pieces=[piece() for i in range(64)]
def make_pieces(fen, board):
	rank=0
	table={"r":1,"b":2,"p":3,"k":4,"h":5,"q":6}
	yye=board.pieces
	for i in fen:
		if i=='/':
			rank+=15
			continue
		if i.lower() not in table:
			rank+=int(i)
		else:
			if i.lower()==i:
				col=0
			else:
				col=1
			pie=table[i.lower()]-1
			yye[rank]=piece(col,pie)
			rank+=1
	return board
def show_pieces(board):
	x=0
	y=0
	num=0
	for i in board.pieces:
		if i.color!=None and num!=clicked:
			win.blit(images[i.value*2+i.color],(x,y))
		x+=75
		num+=1
		if x%600==0:
			x=0
			y+=75
make_board(600,600)
game=board()
boardy='pppppppprhbqkbhr'
game=make_pieces(boardy.upper()[::-1]+'//2'+boardy,game)
show_pieces(game)
pygame.display.update()
clicked=None
oth=pygame.mouse.get_pos()
c=0
while not keyboard.is_pressed('ctrl'):
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			xmark=pos[0]//75
			ymark=pos[1]//75
			if clicked==None:
				clicked=xmark+ymark*8
				if game.pieces[clicked].value==None:
					clicked=None
				else:
					pygame.draw.rect(win, (80,215,55), pygame.Rect(xmark*75, ymark*75, 75, 75))
				win.blit(images[game.pieces[clicked].value*2+game.pieces[clicked].color],(xmark*75,ymark*75))
			else:
				other=xmark+ymark*8
				if clicked==other:
					clicked=None
					other=None
					break
				game.pieces[other]=game.pieces[clicked]
				game.pieces[clicked]=piece()
				clicked=None
				make_board(600,600)
				show_pieces(game)
	pygame.display.update()
