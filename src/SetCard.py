DIAMOND, SQUIGGLE, OVAL = 0, 1, 2
PURPLE, GREEN, RED = 0, 1, 2
HOLLOW, STRIPE, FULL = 0, 1, 2
ONE, TWO, THREE = 0, 1, 2


class SetCard:
	""" SetCard object representing a SetCard. Storing the values as integers """

	# Static Variables
	shapes = ('Diamond', 'Squiggle', 'Oval')
	colors = ('Purple', 'Green', 'Red')
	fills = ('Hollow', 'Stripe', 'Full')
	counts = ('1', '2', '3')

	def __init__(self, shape, color, fill, count):
		self.shape, self.color, self.fill, self.count = shape, color, fill, count

	def hash(self):
		""" Hashing formula of the card is just concatenating the four attributes.
		The hash function is basically: shape*10^3 + color*10^2 + fill*10 + count
		"""
		return "".join(str(x) for x in (self.shape, self.color, self.fill, self.count))

	# Operator overloading
	def __eq__(self, other):
		return (self.shape, self.color, self.fill, self.count) == (other.shape, other.color, other.fill, other.count)

	def __str__(self):
		return f"{SetCard.counts[self.count]} {SetCard.colors[self.color]} {SetCard.fills[self.fill]} {SetCard.shapes[self.shape]}"

	def __repr__(self):
		return f"SetCard({self.shape},{self.color},{self.fill},{self.count})"

	# Methods
	@classmethod
	def getMatch(cls, card1, card2):
		""" Returns card3, the matching set card """
		return cls(**({field: (3 - ((getattr(card1, field) + getattr(card2, field)) % 3)) % 3 for field in vars(card1)}))

	@staticmethod
	def isSet(card1, card2, card3):
		""" Checks if three cards are valid set """
	return SetCard.getMatch(card1, card2) == card3


if __name__ == '__main__':

	print("You are running this in debug mode :) ")

	# Debugging
	card1 = SetCard(1, 0, 0, 0)
	card2 = SetCard(1, 0, 0, 0)
	card3 = SetCard(1, 0, 0, 0)

	print(card3 == SetCard.getMatch(card1, card2))
	print(card1, card2, card3)

	test = {'2012': [0], '0102': [1], '2020': [2, 10], '0112': [3], '2210': [4], '2120': [5], '2221': [6], '2121': [7], '0201': [8], '0001': [9], '1000': [11], '0222': [12], '0120': [13], '2220': [14]}

	hashes = list(test.keys())

	stuff = []
	for ha in hashes:
		stuff.append(SetCard(*[int(s) for s in ha]))

	print(stuff)
	length = len(stuff)
	for i in range(length):
		for j in range(i + 1, length):
			for k in range(j + 1, length):
				if SetCard.isSet(stuff[i], stuff[j], stuff[k]):
					print((str(stuff[i]), str(stuff[j]), str(stuff[k])))

	from itertools import combinations

	t = combinations((card1, card2, card3), 3)
	t = list(*t)
	print(t)
	print(t, SetCard.isSet(*t))
	s = sum(SetCard.isSet(*combo) for combo in combinations(stuff, 3))
	print(s)
