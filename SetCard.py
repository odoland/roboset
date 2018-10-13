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
		
	def __eq__(self,other):
		return (self.shape, self.color, self.fill, self.count) == (other.shape, other.color, other.fill, other.count)

	def __str__(self):
		return f"{counts[self.count]} {colors[self.color]} and {fills[self.fill]} {shapes[self.shape]}" 
	
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
	
	card1 = SetCard(0,1,1,2)
	card2 = SetCard(0,2,0,1)
	card3 = SetCard(0,0,2,0)

	print(card3 == SetCard.getMatch(card1,card2))
	print(card1, card2, card3)









