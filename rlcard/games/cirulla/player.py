
from rlcard.games.cirulla.card import CirullaCard as Card
from rlcard.games.cirulla.board import Take, Board

class CirullaPlayer:

    def __init__(self, player_id):
        ''' Initilize a player.

        Args:
            player_id (int): The id of the player
        '''
        self.player_id = player_id
        self.hand = []
        self.won_cards = []
        self.scopa_sum = 0

    def get_player_id(self):
        ''' Return the id of the player
        '''
        return self.player_id

    def is_buona_three(self) -> bool:
        if len(self.hand) == 3:
            if "7C" not in [str(c) for c in self.hand]:
                return sum([c.value for c in self.hand]) < 10
            else:
                return sum([c.value for c in self.hand if str(c) != "7C"]) < 9
        return False
    
    def is_buona_ten(self) -> bool:
        if len(self.hand) == 3:
            cards = [c for c in self.hand if str(c) != "7C"]
            val = cards[0].value
            return all([c.value == val for c in cards])
        return False

    def play_card(self, card: Card, board: Board) -> Take:
        """
        Plays a card on the board and updates the player's score.

        Args:
            card (Card): The card to be played.
            board (Board): The current state of the game board.

        Returns:
            take (Take): The take that the card will be used for.
        """

        # Check for "buona" 
        if self.is_buona_ten():
            self.scopa_sum += 10
        if self.is_buona_three():
            self.scopa_sum += 3
        
        best_take= Take([])

        # aces take everything on the board (if no ace is already present)
        if card.value == 1 and 1 not in [c.value for c in board.cards] and not board.is_empty():
            self.scopa_sum += 1
            self.won_cards.extend(board.cards)
            self.won_cards.append(card)
            board.cards = []
            best_take= Take(self.won_cards)
        
        else:
            possible_takes= set(board.find_all_takes())
            for take in possible_takes:
                if card.value == take.value:
                    if set(take.cards) == set(board.cards): # scopa is made
                        best_take= take
                        break
                    else:
                        if len(best_take.cards) < len(take.cards): # more cards taken the better
                            best_take= take
        
            if best_take != Take([]):
                best_take.cards.add(card)
                self.won_cards.extend(best_take.cards)
                board.cards = list(set(board.cards) - set(best_take.cards))
                # check if "scopa" is made (no cards left on the board)
                if len(board.cards) == 0:
                    self.scopa_sum += 1
            else:
                board.cards.append(card)
        
        self.hand.remove(card)
        
        return best_take
    

    def __str__(self):
        return f"Player: {self.player_id} " +\
               f"Hand: {[str(c) for c in self.hand]}  " +\
               f"Won cards: {[str(c) for c in self.won_cards]}  " +\
               f"Scope: {self.scopa_sum}"
    
# # OLD check buona
# import numpy as np
# player= CirullaPlayer(1, np.random.RandomState(10))
# player.hand= [Card('C','2'), Card('S','2'), Card('H','2')]
# print(player.__str__())
# board= Board()
# board.cards= [Card('D','7')]
# card= player.play_card(Card('C','2'), None, board)
# print(player.__str__())

# # OLD check take with ace
# import numpy as np
# player= CirullaPlayer(1, np.random.RandomState(10))
# player.hand= [Card('C','A'), Card('S','Q'), Card('H','2')]
# print(player.__str__())
# board= Board()
# board.cards= [Card('D','7')]
# print(f"Board: {board.__str__()}")
# card= player.play_card(Card('C','A'), Take(board.cards), board)
# print(player.__str__())
# print(f"Board: {board.__str__()}")

# import numpy as np
# from utils import cards2list
# player= CirullaPlayer(1, np.random.RandomState(10))
# player.hand= [Card('H','A'), Card('S','Q'), Card('H','A')]
# print(player.__str__())
# board= Board()
# board.cards= [Card('D','2'), Card('D','A'), Card('C','A')]
# print(f"Board: {board.__str__()}")
# take= player.play_card(player.hand[0], board)
# print(f"Take: {cards2list(take.cards)}")
# print(f"Board: {board.__str__()}")