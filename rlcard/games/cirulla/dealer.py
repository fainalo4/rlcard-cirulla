
# from rlcard.games.cirulla.utils import init_deck
from utils import init_deck


class CirullaDealer:
    ''' Initialize a Cirulla dealer class
    '''
    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_deck()
        self.shuffle()

    def shuffle(self):
        ''' Shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_cards(self, player, num):
        ''' Deal some cards from deck to one player

        Args:
            player (object): The object of Player
            num (int): The number of cards to be dealed
        '''
        for _ in range(num):
            player.hand.append(self.deck.pop())

    def flip_top_4_cards(self):
        ''' Flip top 4 cards when a new game starts 
            and put them on the board with faces up

        Returns:
            list (object): The list of 4 Cards at the top of the deck
        '''
        top_4_cards = []
        for _ in range(4):
            top_4_cards.append(self.deck.pop(0))
        return top_4_cards
    
    def is_deck_empty(self) -> bool:
        return len(self.deck) == 0
    