
# from rlcard.games.cirulla.card import CirullaCard as Card
from card import CirullaCard as Card
from more_itertools import powerset

class Take:

    def __init__(self, cards: list[Card] | set[Card] | Card) -> None:
        if isinstance(cards, Card):
            self.cards = {cards}
        elif isinstance(cards, set):
            self.cards = cards
        else: 
            self.cards = set(cards)
        self.value = sum([c.value for c in self.cards])

    def add(self, card: Card):
        self.cards.add(card)
        self.value += card.value

    def remove(self, card: Card):
        self.cards.remove(card)
        self.value -= card.value

    def __eq__(self, __value: object) -> bool:
        return self.cards == __value.cards
    
    def __hash__(self) -> int:
        return hash((tuple(self.cards), self.value))

class Board:
    def __init__(self):
        self.cards: list[Card] = []

    def find_normal_takes(self) -> list[Take]:
        '''
        Calculate takes by using player's card equal to sum of cards on the board 
        '''
        takes = []
        for sublist in powerset(self.cards):
            take = Take(sublist)
            if take.value <= 10:                   # 10 is the maximum value of a card
                takes.append(take)
        return takes
    
    def find_all_takes(self) -> list[Take]:
        '''
        Calculate all possible takes by using player's card equal to sum of cards on the board
        and extending to the takes with player's card plus sum of cards on the board equal 15.
        '''
        takes = self.find_normal_takes()
        new_takes = []
        for t in takes:
            if t.value <= 15:
                cards = t.cards
                new_take = Take(cards)
                new_take.value = 15 - t.value
                if new_take.value <= 10:           # 10 is the maximum value of a card
                    new_takes.append(new_take)
        takes.extend(new_takes)

        is_ace_one_board= any([c.value==1 for c in self.cards])
        if not is_ace_one_board:
            take_with_ace = Take(self.cards)
            take_with_ace.value = 1
            takes.append(take_with_ace)

        return takes
    
    def is_empty(self) -> bool:
        return len(self.cards) == 0
    
    def __str__(self) -> str:
        s = "["
        for card in self.cards:
            s += str(card) + ", "
        return s[0:-2] + "]"
    