class SetCard:
    """ SetCard object representing a SetCard. Storing the values as integers """

    # Static Variables
    shapes = ('Diamond', 'Squiggle', 'Oval')
    colors = ('Green', 'Red', 'Purple')
    fills = ('Full', 'Stripe', 'Hollow')
    counts = ('1', '2', '3')

    def __init__(self, shape, color, fill, count):
        self.shape, self.color, self.fill, self.count = shape, color, fill, count

    @property
    def encoding(self):
        """ Encoding formula of the card is just concatenating the four attributes.
        The encode function is basically: shape*10^3 + color*10^2 + fill*10 + count
        """
        return "".join(str(int(x)) for x in (self.shape, self.color, self.fill, self.count))

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

    print("You are running tests ")

    # Debugging
    card1 = SetCard(1, 0, 0, 0)
    card2 = SetCard(1, 0, 0, 0)
    card3 = SetCard(1, 0, 0, 0)

    print("Should be true:", card3 == SetCard.getMatch(card1, card2))

    test = {
        '2012': [0],
        '0102': [1],
        '2020': [2, 10],
        '0112': [3],
        '2210': [4],
        '2120': [5],
        '2221': [6],
        '2121': [7],
        '0201': [8],
        '0001': [9],
        '1000': [11],
        '0222': [12],
        '0120': [13],
        '2220': [14]
    }

    hashes = list(test.keys())

    converter = lambda code_string: [int(code) for code in code_string] # Converts str of ints to list of ints
    # Produce a list of set cards
    list_set_cards = [SetCard(*converter(codes)) for codes in hashes]


    length = len(list_set_cards)

    # Go through all combinations, finding possible sets and printing when one is found
    for i in range(length):
        for j in range(i + 1, length):
            for k in range(j + 1, length):
                if SetCard.isSet(list_set_cards[i], list_set_cards[j], list_set_cards[k]):
                    print("Set Found!:", (str(list_set_cards[i]), str(list_set_cards[j]), str(list_set_cards[k])))

    from itertools import combinations

    total_sets = sum(SetCard.isSet(*combo) for combo in combinations(list_set_cards, 3))
    print("Should find three sets: ", total_sets)
