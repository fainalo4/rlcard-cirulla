
# from rlcard.games.cirulla.card import CirullaCard as Card
from card import CirullaCard as Card

# from rlcard.games.cirulla.palyer import CirullaPlayer as Player
from player import CirullaPlayer as Player

PRIMIERA_VALUES = {
    7: 21,
    6: 18,
    1: 16,
    5: 15,
    4: 14,
    3: 13,
    2: 12,
    10: 10,
    9: 10,
    8: 10,
}

class CirullaJudger:

    def judge_winner(self, players: list[Player]) -> list[Player] | Player:
        ''' Judge the winner of the game

        Args:
            players (list): The list of players who play the game

        Returns:
            (list): The player id of the winner
        '''
        count_0 = self.count_points(players[0])  
        count_1 = self.count_points(players[1])

        if count_0 == count_1:
            return players
        if count_0 < count_1:
            return players[1]
        return players[0]
    
    @staticmethod
    def calculate_best_primiera_card_of_suit(cards: list[Card], suit: str) -> Card:
        cards_of_suit = [c for c in cards if c.suit == suit]
        if len(cards_of_suit) == 0:
            raise ValueError("There are no cards with that suit in the list")
        return max(cards_of_suit, key=lambda c: PRIMIERA_VALUES[c.value])

    def count_points(self, player: Player) -> int:
        s = 0

        # "Grande" ("Big")
        if {"JD", "QD", "KD"} <= set([str(c) for c in player.won_cards]):
            s += 5

        # "Piccola" ("Small")
        if {"AD", "2D", "3D"} <= set([str(c) for c in player.won_cards]):
            s += 3
            for i in range(4, 7):
                if f"{i}D" in [str(c) for c in player.won_cards]:
                    s += 1
                else: break

        # "Settebello" (Seven of Diamonds)
        if '7D' in [str(c) for c in player.won_cards]:
            s += 1

        # "Primiera" (special scoring system in Cirulla)
        suits = ["S", "H", "D", "C"]
        best_cards = []
        for suit in suits:
            best_card: Card = self.calculate_best_primiera_card_of_suit(player.won_cards, suit)
            best_cards.append(best_card)
        # 2 sevens e 2 sixes
        if sum([PRIMIERA_VALUES[c.value] for c in best_cards]) >= 21 * 2 + 18 * 2:
            s += 1

        # "Cards" 
        if len(player.won_cards) >= 21:
            s += 1
        
        # "Diamonds"
        if len([c for c in player.won_cards if c.suit == "D"]) >= 6:
            s += 1

        return s + player.scopa_sum
    
# import numpy as np
# state= np.random.RandomState(10)
# p1= Player(1, state)
# p2= Player(2, state)

# p1.won_cards= [Card('C','7'), Card('S','7'), Card('H','2'), Card('D','4'), Card('D','7'), 
#                Card('H','6'), Card('D','K'), Card('D','A'), Card('D','2'), Card('D','3'),]
# p2.won_cards= [Card('C','A'), Card('S','Q'), Card('H','3'), Card('D','5'), Card('C','J')]

# judger= CirullaJudger()
# winner= judger.judge_winner(players=[p1, p2], np_random=state)    
# print(winner.__str__())
# print(f"Points: {judger.count_points(winner)}")