
from rlcard.games.base import Card

''' Note: 2 dicts are used to convert between rank and value, and vice versa.
'''
UTIL_DICT = {
        1: "A",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "J",
        9: "Q",
        10: "K"
}
REVERSE_UTIL_DICT = {v: k for k, v in UTIL_DICT.items()}


class CirullaCard(Card):
    '''
    Card stores the suit and rank of a single card
    In Cirulla there are 40 cards, 4 suits and 10 ranks
    '''
    suit = None
    rank = None
    value = None
    valid_suit = ['S', 'H', 'D', 'C']
    valid_rank = ['A', '2', '3', '4', '5', '6', '7', 'J', 'Q', 'K']

    def __init__(self, suit, rank):
        ''' Initialize the suit and rank of a card

        Args:
            suit: string, suit of the card, should be one of valid_suit
            rank: string, rank of the card, should be one of valid_rank
            value: int, value of the card depending on the rank
        '''
        self.suit = suit
        self.rank = rank
        self.value = REVERSE_UTIL_DICT.get(rank)

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        else:
            # don't attempt to compare against unrelated types
            return NotImplemented

    def __hash__(self):
        suit_index = Card.valid_suit.index(self.suit)
        rank_index = Card.valid_rank.index(self.rank)
        return rank_index + 100 * suit_index

    def __str__(self):
        ''' Get string representation of a card.

        Returns:
            string: the combination of rank and suit of a card. Eg: AS, 5H, JD, 3C, ...
        '''
        return self.rank + self.suit

    def get_index(self):
        ''' Get index of a card.

        Returns:
            string: the combination of suit and rank of a card. Eg: 1S, 2H, AD, BJ, RJ...
        '''
        return self.suit+self.rank
