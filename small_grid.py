import numpy as np
import copy

class SmallGrid():
	def __init__(self):
		self.contents=np.zeros((3,3))
		self.won=0	#1 for x wins, -1 for o wins

	def play(self, num, pos_x, pos_y):
		#num is 1 for x, -1 for o; pos_x, pos_y are less than 3
		self.contents[pos_x,pos_y]=num
		if self.evaluate()==25:
			self.won=1
		elif self.evaluate()==-25:
			self.won=-1
		else:
			self.won=0

	def playable_positions(self):
		#yields pos_x, pos_y of playable position
		if self.contents[1, 1]==0:
			yield 1,1
		if self.contents[0, 0]==0:
			yield 0,0
		if self.contents[0, 2]==0:
			yield 0,2
		if self.contents[2, 2]==0:
			yield 2,2
		if self.contents[2, 0]==0:
			yield 2,0
		if self.contents[1, 0]==0:
			yield 1,0
		if self.contents[1, 2]==0:
			yield 1,2
		if self.contents[0, 1]==0:
			yield 0,1
		if self.contents[2, 1]==0:
			yield 2,1

	def evaluate(self):
		magicsquare=get_magic_square()
		prod=magicsquare*self.contents
		a=np.sum(prod, axis=0).tolist()
		b=np.sum(prod, axis=1).tolist()
		c=np.trace(prod)
		d=np.trace(np.flip(prod, 1))
		if 15 in a or 15 in b or c==15 or d==15:
			return 25
		if -15 in a or -15 in b or c==-15 or d==-15:
			return -25
		return nonWinEval(self.contents)

def nonWinEval(grid):
	grid=grid.tolist()
	row0=grid[0]
	row1=grid[1]
	row2=grid[2]
	col0=[grid[0][0],grid[1][0],grid[2][0]]
	col1=[grid[0][1],grid[1][1],grid[2][1]]
	col2=[grid[0][2],grid[1][2],grid[2][2]]
	diag0=[grid[0][0],grid[1][1],grid[2][2]]
	diag1=[grid[0][2],grid[1][1],grid[2][0]]
	temp=[row0,row1,row2,col0, col1, col2, diag0, diag1]
	score=0
	for series in temp:
		score+=rowEval(series)
	return score

def rowEval(row):
	if (1 in row) and (-1 in row):
		return 0
	cnt=0
	for lmnt in row:
		if lmnt==1:
			cnt+=1
		elif lmnt==-1:
			cnt-=1
	helplist=[0,1,4,-4,-1]
	return helplist[cnt]

def get_magic_square(n=3):
	p = np.arange(1, n+1)
	return n*np.mod(p[:, None] + p - (n+3)//2, n) + np.mod(p[:, None] + 2*p-2, n) + 1

def minimax(smallgrid, alpha=-10000, beta=+10000, maximizing=True, depth=9):
	if not smallgrid.won==0:
		return smallgrid.won*25, None
	moves_list=[]
	for x,y in smallgrid.playable_positions():
		moves_list.append((x,y))
	if len(moves_list)==0 or depth==0:
		return smallgrid.evaluate(), None
	best_move=(0,0)
	if maximizing:
		bestval=-10000
		for x,y in smallgrid.playable_positions():
			smallgrid.play(1,x,y)
			currentval,current_move=minimax(smallgrid, alpha, beta, False, depth-1)
			smallgrid.play(0,x,y)
			if currentval>bestval:
				bestval=currentval
				best_move=(x,y)
			alpha=max(alpha, currentval)
			if beta<=alpha:
				break
		return bestval, best_move	#+ depth - 9 to val, for faster wins
	else:
		bestval=10000
		for x,y in smallgrid.playable_positions():
			smallgrid.play(-1,x,y)
			currentval, current_move=minimax(smallgrid, alpha, beta, True, depth-1)
			smallgrid.play(0,x,y)
			if currentval<bestval:
				bestval=currentval
				best_move=(x,y)
			beta=min(beta, currentval)
			if beta<=alpha:
				break
		return bestval, best_move	#- depth + 9 to val, for faster wins

# sg=SmallGrid()
# sg.play(1,1,1)
# sg.play(-1,0,0)
# sg.play(1,0,2)
# print(sg.contents)
# val, move=minimax(sg, maximizing=False,depth=9)
# print(val, move)