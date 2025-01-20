
from rlcard.games.cirulla.card import CirullaCard as Card
# from rlcard.games.cirulla.dealer import CirullaDealer as Dealer
# from rlcard.games.cirulla.player import CirullaPlayer as Player
# from rlcard.games.cirulla.game import CirullaGame as Game

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
        cards (list): list of UnoCards objects

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


def encode_hand(plane, hand):
    ''' Encode hand and represerve it into plane

    Args:
        plane (array): 3*4*15 numpy array
        hand (list): list of string of hand's card

    Returns:
        (array): 3*4*15 numpy array
    '''
    # plane = np.zeros((3, 4, 15), dtype=int)
    plane[0] = np.ones((4, 15), dtype=int)
    hand = hand2dict(hand)
    for card, count in hand.items():
        card_info = card.split('-')
        color = COLOR_MAP[card_info[0]]
        trait = TRAIT_MAP[card_info[1]]
        if trait >= 13:
            if plane[1][0][trait] == 0:
                for index in range(4):
                    plane[0][index][trait] = 0
                    plane[1][index][trait] = 1
        else:
            plane[0][color][trait] = 0
            plane[count][color][trait] = 1
    return plane

def encode_target(plane, target):
    ''' Encode target and represerve it into plane

    Args:
        plane (array): 1*4*15 numpy array
        target(str): string of target card

    Returns:
        (array): 1*4*15 numpy array
    '''
    target_info = target.split('-')
    color = COLOR_MAP[target_info[0]]
    trait = TRAIT_MAP[target_info[1]]
    plane[color][trait] = 1
    return plane
