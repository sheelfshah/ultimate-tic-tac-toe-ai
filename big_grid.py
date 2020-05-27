from small_grid import *
import numpy as np

class BigGrid():
	def __init__ (self):
		self.smallGrids=[[SmallGrid(),SmallGrid(), SmallGrid()],
			[SmallGrid(),SmallGrid(), SmallGrid()],
			[SmallGrid(),SmallGrid(), SmallGrid()]]
		self.winner=0
		self.localWinners=np.zeros((3,3))
		self.localEvaluations=np.zeros((3,3))

	def play(self,num, grid_x, grid_y, pos_x, pos_y):
		self.smallGrids[grid_x][grid_y].play(num,pos_x,pos_y)
		self.refresh()

	def refresh(self):
		for i in range(3):
			for j in range(3):
				self.localWinners[i, j]=self.smallGrids[i][j].won
				self.localEvaluations[i, j]=self.smallGrids[i][j].evaluate()
		magicsquare=get_magic_square()
		prod=magicsquare*self.localWinners
		a=np.sum(prod, axis=0).tolist()
		b=np.sum(prod, axis=1).tolist()
		c=np.trace(prod)
		d=np.trace(np.flip(prod, 1))
		if 15 in a or 15 in b or c==15 or d==15:
			self.winner=1
			return
		if -15 in a or -15 in b or c==-15 or d==-15:
			self.winner=-1
			return
		self.winner=0
		return

	def get_playable_positions(self,lastMoveX=None, lastMoveY=None):
		return_list=[]
		if lastMoveX==None:
			for grid_x in range(3):
				for grid_y in range(3):
					for x in range(3):
						for y in range(3):
							return_list.append((grid_x, grid_y, x, y))
			return return_list
		if self.localWinners[lastMoveX, lastMoveY]==0:
			for x,y in self.smallGrids[lastMoveX][lastMoveY].playable_positions():
				return_list.append((lastMoveX, lastMoveY, x, y))
			return return_list
		for (grid_x, grid_y) in [(1,1),(0,0),(0,2),(2,2),(2,0),(1,0),(0,1),(2,1),(1,2)] :
			if self.localWinners[grid_x, grid_y]==0:
				for x,y in self.smallGrids[grid_x][grid_y].playable_positions():
					return_list.append((grid_x, grid_y, x, y))
		return return_list

	def fullEvaluate(self):
		if not self.winner==0:
			return self.winner*625
		grid=self.localEvaluations.tolist()
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
			score+=bigRowEval(series)
		return score

def bigRowEval(row):
	if (25 in row) and (-25 in row):
		return 0
	else:
		tot=row[0]+row[1]+row[2]
		if 25 in row or -25 in row:
			cnt=0
			for i in range(3):
				if row[i]==25:
					cnt+=1
				elif row[i]==-25:
					cnt+=1
		else:
			cnt=1
		return cnt*tot 

def bMinimax(biggrid, alpha=-10000, beta=+10000, maximizing=True, depth=3, lastMoveX=None, lastMoveY=None):
	if not biggrid.winner==0:
		return biggrid.winner*625, None
	moves_list=biggrid.get_playable_positions(lastMoveX, lastMoveY)
	if len(moves_list)==0 or depth==0:
		return biggrid.fullEvaluate(), None
	best_move=(0,0,0,0)
	if maximizing:
		bestval=-10000
		for tup in moves_list:
			(grid_x, grid_y, x, y)=tup
			print(tup)
			biggrid.play(1,grid_x,grid_y,x,y)
			currentval,current_move=bMinimax(biggrid, alpha, beta, False, depth-1, x, y)
			biggrid.play(0,grid_x,grid_y,x,y)
			if currentval>bestval:
				bestval=currentval
				best_move=(grid_x, grid_y, x, y)
			alpha=max(alpha, currentval)
			if beta<=alpha:
				break
		return bestval, best_move	#+ depth - 9 to val, for faster wins
	else:
		bestval=10000
		for tup in moves_list:
			(grid_x, grid_y, x, y)=tup
			print(tup)
			biggrid.play(-1,grid_x,grid_y,x,y)
			currentval, current_move=bMinimax(biggrid, alpha, beta, True, depth-1, x, y)
			biggrid.play(0,grid_x,grid_y,x,y)
			if currentval<bestval:
				bestval=currentval
				best_move=(grid_x, grid_y, x, y)
			beta=min(beta, currentval)
			if beta<=alpha:
				break
		return bestval, best_move	#- depth + 9 to val, for faster wins

bg=BigGrid()
flag=True
move=(0,1,None, None)
# for i in range(81):
# 	val, move =bMinimax(bg, maximizing=flag, depth=4+(i//10), lastMoveX=move[-2], lastMoveY=move[-1])
# 	if move==None:
# 		print("winner: ", bg.winner)
# 		break
# 	print(i, val, move, flag)
# 	if flag:
# 		bg.play(1,move[0], move[1], move[2], move[3])
# 	else:
# 		move = [int(x) for x in input("Enter move: ").split()]
# 		bg.play(-1,move[0], move[1], move[2], move[3])
# 	flag= not flag