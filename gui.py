import pygame
from big_grid import *
from threading import Thread

width=600
height=700
pygame.init()
win=pygame.display.set_mode((width, height))
pygame.display.set_caption("Ultimate Tic Tac Toe")
pygame.font.init()

white=(255,255,255)

def draw_board(win):
	win.fill((51,171,249))
	pygame.draw.line(win, white, (200,100),(200,700), 6)
	pygame.draw.line(win, white, (400,100),(400,700), 6)
	pygame.draw.line(win, white, (0,300),(600,300), 6)
	pygame.draw.line(win, white, (0,500),(600,500), 6)
	for i in range(3):
		for j in range(3):
			pygame.draw.line(win, white, (200*i+70,200*j+110),(200*i+70,200*j+290), 3)
			pygame.draw.line(win, white, (200*i+130,200*j+110),(200*i+130,200*j+290), 3)
			pygame.draw.line(win, white, (200*i+10,200*j+170),(200*i+190,200*j+170), 3)
			pygame.draw.line(win, white, (200*i+10,200*j+230),(200*i+190,200*j+230), 3)
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
	pos_y-=100
	if pos_x%200<=10 or pos_x%200>=190 or pos_y%200<=10 or pos_y%200>=190 or pos_y<=0:
		return (-1,-1,-1,-1)
	pos_x-=10
	pos_y-=10
	if (pos_x%200)%60 <=5 or (pos_y%200)%60 <=5 or (pos_x%200)%60 >=55 or (pos_y%200)%60 >=55:
		return (-1,-1,-1,-1)
	grid_x=pos_x//200
	grid_y=pos_y//200
	x=(pos_x%200)//60
	y=(pos_y%200)//60
	return (grid_x, grid_y, x, y)

def show_move(win, move, bg, flag):
	grid_x=move[0]
	grid_y=move[1]
	x=move[2]
	y=move[3]
	if flag:
		pygame.draw.line(win, white, (200*grid_x+20+60*x,200*grid_y+120+60*y),(200*grid_x+60+60*x,200*grid_y+160+60*y), 4)
		pygame.draw.line(win, white, (200*grid_x+20+60*x,200*grid_y+160+60*y),(200*grid_x+60+60*x,200*grid_y+120+60*y), 4)
	else:
		pygame.draw.circle(win, white, (200*grid_x+40+60*x,200*grid_y+140+60*y), 22, 2)
	if not bg.localWinners[move[0], move[1]]==0:
		grid_x=move[0]
		grid_y=move[1]
		if bg.localWinners[grid_x, grid_y]==1:
			pygame.draw.line(win, white, (200*grid_x+30,200*grid_y+130),(200*grid_x+170,200*grid_y+270), 8)
			pygame.draw.line(win, white, (200*grid_x+170,200*grid_y+130),(200*grid_x+30,200*grid_y+270), 8)
		else:
			pygame.draw.circle(win, white, (200*grid_x+100,200*grid_y+200), 75, 5)
	pygame.display.update()

timex=600
timeo=600

def timer(flag):
	global stop_flag_o, timex, timeo, win, start_ticks
	if not flag:
		while not stop_flag_o:
			secs=(pygame.time.get_ticks()-start_ticks)//1000
			if secs>0:
				timeo-=1
				start_ticks=pygame.time.get_ticks()
				show_timer(win, timex, timeo)

def show_timer(win, tx, to):
	if tx<0:
		display_winner(win, -1)
		return
	if to<0:
		display_winner((win, 1))
		return
	font=pygame.font.SysFont("comicsans",50)
	textx=font.render(str(tx),1,(255,255,255),True)
	texto=font.render(str(to),1,(255,255,255),True)
	blankSurface=pygame.Surface((600, 90))
	blankSurface.fill((51,171,249))
	win.blit(blankSurface, (0,5))
	win.blit(textx,(50,20))
	win.blit(texto,(520, 20))
	pygame.display.update()

bg=BigGrid()

flag=True
move=(0,1,None, None)
run=True
i=0
draw_board(win)

while run:
	if flag:
		start_time = time.time()
		val, move =bMinimax(bg, maximizing=flag, depth=optimalDepth(i), lastMoveX=move[-2], lastMoveY=move[-1])
		timex-=round(time.time()-start_time, 3)
		show_timer(win, timex, timeo)
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
		if len(bg.get_playable_positions())==0:
			run=False
			display_winner(win, bg.winner)
			pygame.time.delay(5000)
			pygame.quit()
			break
		if bg.winner==0:
			lmx=move[2]
			lmy=move[3]
			start_ticks=pygame.time.get_ticks()
			stop_flag_o=False
			Thread(target = timer, args =(False, )).start()
			while not is_valid(bg, move, lmx, lmy):
				for event in pygame.event.get():
				    if event.type==pygame.QUIT:
				        pygame.quit()
				        run=False
				    if event.type==pygame.MOUSEBUTTONUP:
				    	pos = pygame.mouse.get_pos()
				    	move=get_move(pos)
			stop_flag_o=True
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