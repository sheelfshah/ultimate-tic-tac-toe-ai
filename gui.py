import pygame
from big_grid import *

width=600
height=600
win=pygame.display.set_mode((width, height))
pygame.display.set_caption("Ultimate Tic Tac Toe")
pygame.font.init()

white=(255,255,255)

def draw_board(win):
	win.fill((51,171,249))
	pygame.draw.line(win, white, (200,0),(200,600), 6)
	pygame.draw.line(win, white, (400,0),(400,600), 6)
	pygame.draw.line(win, white, (0,200),(600,200), 6)
	pygame.draw.line(win, white, (0,400),(600,400), 6)
	for i in range(3):
		for j in range(3):
			pygame.draw.line(win, white, (200*i+70,200*j+10),(200*i+70,200*j+190), 3)
			pygame.draw.line(win, white, (200*i+130,200*j+10),(200*i+130,200*j+190), 3)
			pygame.draw.line(win, white, (200*i+10,200*j+70),(200*i+190,200*j+70), 3)
			pygame.draw.line(win, white, (200*i+10,200*j+130),(200*i+190,200*j+130), 3)
	pygame.display.flip()
def display_winner(win, winner):
	win.fill((51,171,249))
	font=pygame.font.SysFont("comicsans",80)
	if not winner==0:
		if winner==1:
			string="X"
		else:
			string="O"
		text=font.render(string + " Wins",1,(255,255,255),True)
	else:
		text=font.render("Draw",1,(255,255,255),True)
	win.blit(text,(width/2-text.get_width()/2,height/2-text.get_height()/2))
	pygame.display.flip()

def is_valid(bg, move, lastMoveX, lastMoveY):
	if -1 in move:
		return False
	if not bg.localWinners[move[0], move[1]]==0:
		return False
	if bg.localWinners[lastMoveX, lastMoveY]==0:
		if move[0]==lastMoveX and move[1]==lastMoveY:
			if bg.smallGrids[lastMoveX][lastMoveY].contents[move[2], move[3]]==0:
				return True
		return False
	else:
		if bg.smallGrids[move[0]][move[1]].contents[move[2], move[3]]==0:
			return True
		return False

def get_move(pos):
	pos_x=pos[0]
	pos_y=pos[1]
	if pos_x%200<=10 or pos_x%200>=190 or pos_y%200<=10 or pos_y%200>=190:
		return (-1,-1,-1,-1)
	pos_x-=10
	pos_y-=20
	if (pos_x%200)%60 <=5 or (pos_y%200)%60 <=5 or (pos_x%200)%60 >=55 or (pos_y%200)%60 >=55:
		return (-1,-1,-1,-1)
	grid_x=pos_x//200
	grid_y=pos_y//200
	x=(pos_x%200)//60
	y=(pos_y%200)//60
	return (grid_x, grid_y, x, y)

def show_move(win, move, bg, flag):
	if bg.localWinners[move[0], move[1]]==0:
		grid_x=move[0]
		grid_y=move[1]
		x=move[2]
		y=move[3]
		if flag:
			pygame.draw.line(win, white, (200*grid_x+20+60*x,200*grid_y+20+60*y),(200*grid_x+60+60*x,200*grid_y+60+60*y), 4)
			pygame.draw.line(win, white, (200*grid_x+20+60*x,200*grid_y+60+60*y),(200*grid_x+60+60*x,200*grid_y+20+60*y), 4)
		else:
			pygame.draw.circle(win, white, (200*grid_x+40+60*x,200*grid_y+40+60*y), 26, 4)
	else:
		grid_x=move[0]
		grid_y=move[1]
		if bg.localWinners[grid_x, grid_y]==1:
			pygame.draw.line(win, white, (200*grid_x+30,200*grid_y+30),(200*grid_x+170,200*grid_y+170), 8)
			pygame.draw.line(win, white, (200*grid_x+170,200*grid_y+30),(200*grid_x+30,200*grid_y+170), 8)
		else:
			pygame.draw.circle(win, white, (200*grid_x+100,200*grid_y+100), 80, 8)
	pygame.display.update()

bg=BigGrid()
flag=True
move=(0,1,None, None)
run=True
i=0
draw_board(win)
while run:
	if flag:
		val, move =bMinimax(bg, maximizing=flag, depth=optimalDepth(i), lastMoveX=move[-2], lastMoveY=move[-1])
		if move==None:
			run=False
			display_winner(win, bg.winner)
			pygame.time.delay(5000)
			pygame.quit()
			break
		bg.play(1,move[0], move[1], move[2], move[3])
		show_move(win, move, bg, flag)
		i+=1
	else:
		if bg.winner==0:
			lmx=move[2]
			lmy=move[3]
			while not is_valid(bg, move, lmx, lmy):
				for event in pygame.event.get():
				    if event.type==pygame.QUIT:
				        pygame.quit()
				        run=False
				    if event.type==pygame.MOUSEBUTTONUP:
				    	pos = pygame.mouse.get_pos()
				    	move=get_move(pos)
			bg.play(-1,move[0], move[1], move[2], move[3])
			show_move(win, move, bg, flag)
			i+=1
		else:
			display_winner(win, bg.winner)
			run=False
			pygame.time.delay(5000)
			pygame.quit()
			break
		for event in pygame.event.get():
		    if event.type==pygame.QUIT:
		        pygame.quit()
		        run=False
	flag= not flag
	for event in pygame.event.get():
	    if event.type==pygame.QUIT:
	        pygame.quit()
	        run=False