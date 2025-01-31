
from rlcard.games.cirulla.card import CirullaCard as Card
import numpy as np

def init_deck():
    ''' Initialize a Cirulla deck of 40 cards

    Returns:
        (list): A list of Card object
    '''
    suit_list = ['S', 'H', 'D', 'C']
    rank_list = ['A', '2', '3', '4', '5', '6', '7', 'J', 'Q', 'K']
    res = [Card(suit, rank) for suit in suit_list for rank in rank_list]
    return res


def cards2list(cards):
    ''' Get the corresponding string representation of cards

    Args:
        cards (list): list of CirullaCard objects

    Returns:
        (string): string representation of cards
    '''
    cards_list = []
    for card in cards:
        cards_list.append(card.__str__())
    return cards_list


def hand2dict(hand):
    ''' Get the corresponding dict representation of hand

    Args:
        hand (list): list of string of hand's card

    Returns:
        (dict): dict of hand
    '''
    hand_dict = {}
    for card in hand:
        if card not in hand_dict:
            hand_dict[card] = 1
        else:
            hand_dict[card] += 1
    return hand_dict


def flip_and_check_top_4_cards(game):
    ''' Flip the top 4 cards of the card pile, then put them on the board.
    Check sum of first 4 cards:
    - if it is 15 or 30 then the player who flipped the cards gets the cards 
        and scores 1 or 2 points respectively.
    - else leaves the cards on the board and the game continues.

    Returns:
        (object of UnoCard): the top card in game

    '''

    # TODO: Implement logic for checking if in the 4 cards:
    # - there are at least 2 aces
    # - there are at least 3 cards with the same rank
    # - there are at least 4 cards with the same rank (victory)
    # while loop until the condition is met
    
    top = game.dealer.flip_top_4_cards()

    top_sum = sum([c.value for c in top])
    if top_sum in [15, 30]:     
        points = 1 if top_sum == 15 else 2
        game.players[game.current_player_id].scopa_sum += points
        game.players[game.current_player_id].won_cards.extend(top)
        game.board.cards = []
    else:
        game.board.cards = top
    switch_player(game)


def switch_player(game):
    ''' Switch to the next player

    Args:
        game (Game): The current game
    '''
    if game.current_player_id == 1:
        game.current_player_id = 0
    else:
        game.current_player_id = 1


# functions below are copied from gin_rummy implementation (a big thanks to the authors)
def encode_cards(cards: list[Card]) -> np.ndarray:
    plane = np.zeros(40, dtype=int)
    for card in cards:
        card_id = get_card_id(card)
        plane[card_id] = 1
    return plane

def get_card_id(card: Card) -> int:
    rank_id = get_rank_id(card)
    suit_id = get_suit_id(card)
    return rank_id + 10 * suit_id


def get_rank_id(card: Card) -> int:
    return Card.valid_rank.index(card.rank)


def get_suit_id(card: Card) -> int:
    return Card.valid_suit.index(card.suit)

def card_from_card_id(card_id: int) -> Card:
    ''' Make card from its card_id

    Args:
        card_id: int in range(0, 52)
     '''
    if not (0 <= card_id < 40):
        raise Exception("card_id is {}: should be 0 <= card_id < 40.".format(card_id))
    rank_id = card_id % 10
    suit_id = card_id // 10
    rank = Card.valid_rank[rank_id]
    suit = Card.valid_suit[suit_id]
    return Card(rank=rank, suit=suit)

# # test card encoding into a plane of 40
# cards= [Card('S', 'A'), Card('H', '2'), Card('D', '3'), Card('C', 'K')]
# plane= encode_cards(cards)
# print(plane)