DIAMOND, SQUIGGLE, OVAL = 0, 1, 2
PURPLE, GREEN, RED = 0, 1, 2
HOLLOW, STRIPE, FULL = 0, 1, 2
ONE, TWO, THREE = 0, 1, 2


shapes = ['Diamond', 'Squiggle', 'Oval']
colors = ['Purple', 'Green', 'Red']
fills = ['Hollow', 'Stripe', 'Full']
counts = ['1','2','3']
class SetCard:
	""" Class to hold the attributes of the cards """
	
	def __init__(self, shape, color, fill, count): # Possibly replace this with a named tuple?
		
		self.shape, self.color, self.fill, self.count = shape, color, fill, count

	def hash(self):
		return "".join( str(x) for x in (self.shape,self.color,self.fill,self.count) )


	def __eq__(self,other):
		return (self.shape, self.color, self.fill, self.count) == (other.shape, other.color, other.fill, other.count)

	def __str__(self):
		return f"{counts[self.count]} {colors[self.color]} {fills[self.fill]} {shapes[self.shape]}" 
	
	def __repr__(self):
		return f"SetCard({self.shape},{self.color},{self.fill},{self.count})"

	@classmethod
	def getMatch(cls,card1,card2):
		""" Gets the third set to match """
		return cls(**({ field : (3 - ((getattr(card1,field) + getattr(card2,field)) % 3 )) % 3 for field in vars(card1) }) )
	
	@staticmethod
	def isSet(card1,card2,card3):
		return SetCard.getMatch(card1,card2) == card3

	

if __name__ == '__main__':
	print("You are running this in debug mode :) ")
	
	card1 = SetCard(1,0,0,0)
	card2 = SetCard(1,0,0,0)
	card3 = SetCard(1,0,0,0)


	print(card3 == SetCard.getMatch(card1,card2))
	print(card1, card2, card3)


	test = {'2012': [0], '0102': [1], '2020': [2, 10], '0112': [3], '2210': [4], '2120': [5], '2221': [6], '2121': [7], '0201': [8], '0001': [9], '1000': [11], '0222': [12], '0120': [13], '2220': [14]}

	hashes = list(test.keys())
	
	stuff = []
	for ha in hashes:
		stuff.append ( SetCard(*[int(s) for s in ha] ))

	print(stuff)
	length = len(stuff)
	for i in range(length):
		for j in range(i+1, length):
			for k in range(j+1, length):
				if SetCard.isSet(stuff[i],stuff[j],stuff[k]):
					print((str(stuff[i]),str(stuff[j]),str(stuff[k])))

	from itertools import combinations

	t = combinations((card1,card2,card3),3)
	t = list(*t)
	print(t)
	print( t, SetCard.isSet(*t))
	s = sum(SetCard.isSet(*combo) for combo in combinations(stuff,3))
	print(s)






