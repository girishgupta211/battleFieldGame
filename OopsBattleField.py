import string
from pprint import pprint 

def validateBattleShip(func):
	def inner_func(self,location, dimention, type,maxX,maxY ):		
		x =ord(location[0]) - 64
		y = location[1]		

		if ( x+dimention[0]-1 > maxX or  y+dimention[1]-1 > ord(maxY) - 64):
			raise Exception("battleShip should be within battle field dimention of " + str(maxX) + " by " + str(maxY))
	
		return func(self,location,dimention,type,maxX,maxY)
	return inner_func


def validateRange(func):
	def inner_func(self,X, Y):
		if X > 9:
			raise Exception("M needs to be less than 9")		
		if( Y not in list(string.ascii_uppercase)):
			raise Exception( "N should be between 'A' and 'Z' (Capital letter Only)" )		
		
		return func(self,X,Y)
	return inner_func


class BattleArea():
	@validateRange
	def __init__(self,maxX,maxY):		
		self.maxX = maxX
		self.maxY = ord(maxY) - 64

	def createBattleArea(self):
		self.battleArea = [ [0 for i in xrange(self.maxX)] for i in xrange(self.maxY) ]


class BattleShip():
	@validateBattleShip
	def __init__(self, location, dimention,type,maxX,maxY):				
		self.location = location
		self.dimention = dimention
		self.type = type		

class BattleField(BattleArea):
	totalPower = 0
	def __init__(self, m,n,battleShipArry):
		BattleArea.__init__(self,m,n)
		self.createBattleArea()		
		self.populateBattleField(battleShipArry)
	
	def populateBattleField(self,battleShipArry):		
		for tank in battleShipArry:
			x = tank.location[1]
			y =ord(tank.location[0]) - 64			
			xRange = [ x + i  for i in range(tank.dimention[0]) ]
			yRange = [ y + i  for i in range(tank.dimention[1]) ]			
			power = { 'P':1 , 'Q':2 }			
			for i in xRange:
				for j in yRange:
					self.battleArea[i-1][j-1] = power[tank.type]
					self.totalPower += power[tank.type]
		# pprint.pprint (self.battleArea)


class Player():
	"""docstring for Player"""
	def __init__(self, battleField,targetMissiles):
		self.battleField = battleField
		self.targetMissiles = targetMissiles
		
def convertToCartesian(targetLocations,m,n):
	return [ (ord(location[0]) - 64 , location[1]) for location in targetLocations]

def run():
	m = 9
	n = 'H'
	location = ('A',1)
	dimention = (1,2)
	type = 'P'
	
	battleShipsArea1 = []
	battleShipsArea1.append(BattleShip(location,dimention,type,m,n))
	# battleShipsArea1.append(BattleShip( ('H', 7) ,(2,2),'Q',m,n))	
	battleField1 = BattleField(m,n,battleShipsArea1)

	battleShipsArea2 = []
	battleShipsArea2.append(BattleShip(location,dimention,type,m,n))
	# battleShipsArea2.append(BattleShip( ('D', 3) ,(2,2),'Q',m,n))	
	battleField2 = BattleField(m,n,battleShipsArea2)
	targetsPlayer1 = [('A',1) , ('A',3),  ('A',2) ]
	targetsPlayer2 = [('A',1) , ('B',2), ('B',2), ('B',3) ]	
	targetsPlayer1 = convertToCartesian(targetsPlayer1,m,n)
	targetsPlayer2 = convertToCartesian(targetsPlayer2,m,n)
	player1 = Player(battleField1,targetsPlayer1)
	player2 = Player(battleField2,targetsPlayer2)
	
	play(player1, player2)	


def hitMissile(battleField,target):	
	# check if target shell is an active shell( having power (1 or 2))	
	if(battleField.battleArea[target[0]-1][target[1]-1] > 0):
		battleField.battleArea[target[0]-1][target[1]-1] -= 1
		battleField.totalPower -= 1
		return True
	else:
		return False

def play(player1,player2):	
# def play(battleField1,battleField2,targetsPlayer1,targetsPlayer2):	
	currPlayer = 1 
	status = False
	while(True):
		if(player1.battleField.totalPower == 0):
			print ("Player-2 won the battle")
			break
		if(player2.battleField.totalPower == 0):
			print ("Player-1 won the battle")
			break

		if(len(player1.targetMissiles) == 0 and len(player2.targetMissiles) == 0):
			print ("Player-1 and Player-2 have no more missiles left. players declare peace.")
			break

		if(len(player1.targetMissiles) == 0):
			print ("Player-1 no more missiles left")
			currPlayer = 2			

		if(len(player2.targetMissiles) == 0):
			print ("Player-2 no more missiles left")
			currPlayer = 1			

		# print targetsPlayer1
		if(currPlayer == 1):
			target = player1.targetMissiles.pop(0)			
			status = hitMissile(player2.battleField, target)
			if(status):
				print ("Player-1 fires a missile with target " +  str(target) + " which hit")
				currPlayer = 1				
			else:
				print ("Player-1 fires a missile with target " +  str(target) + " which missed")
				currPlayer = 2
			
		else:	
			target = player2.targetMissiles.pop(0)			
			status = hitMissile(player1.battleField, target)
			if(status):
				print ("Player-2 fires a missile with target " +  str(target) + " which hit")
				currPlayer = 2			
			else:
				print ("Player-2 fires a missile with target " +  str(target) + " which missed")
				currPlayer = 1
	
if __name__ == '__main__':
	run()
