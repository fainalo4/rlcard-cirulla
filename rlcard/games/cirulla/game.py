from copy import deepcopy
import numpy as np

from rlcard.games.cirulla.card import CirullaCard as Card
from rlcard.games.cirulla.dealer import CirullaDealer as Dealer
from rlcard.games.cirulla.player import CirullaPlayer as Player
from rlcard.games.cirulla.board import Board, Take
from rlcard.games.cirulla.judger import CirullaJudger as Judger
from rlcard.games.cirulla.utils import *

# from card import CirullaCard as Card
# from dealer import CirullaDealer as Dealer
# from player import CirullaPlayer as Player
# from board import Board, Take
# from judger import CirullaJudger as Judger
# from utils import *

 

class CirullaGame:

    def __init__(self, allow_step_back=False, num_players=2):
        
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()

        self.num_players = num_players
        self.players = [Player(i) for i in range(self.num_players)]
        self.current_player_id = self.np_random.randint(0,2)

        self.payoffs = [0 for _ in range(self.num_players)]
        self.dealer = Dealer(self.np_random)
        self.board = Board()

        self._is_over = False
        self.winner = None
        self.judger = Judger()

    def configure(self, game_config):
        ''' Specifiy some game specific parameters, such as number of players
        '''
        self.num_players = game_config['game_num_players']

    def init_game(self):
        ''' Initialize players and state

        Returns:
            (tuple): Tuple containing:

                (dict): The first state in one game
                (int): Current player's id
        '''
        self.__init__(allow_step_back= self.allow_step_back, 
                      num_players= self.num_players)
        
        flip_and_check_top_4_cards(self)

        # Deal 3 cards to each player to prepare for the game
        for player in self.players:
            self.dealer.deal_cards(player, 3)

        # Save the history for stepping back to the last state.
        self.history = []

        state = self.get_state(self.current_player_id)
        
        return state, self.current_player_id

    def step(self, raw_action: Card):
        ''' Get the next state

        Args:
            action (Card): card to be played

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        '''

        if self.allow_step_back:
            # First snapshot the current state
            _players= deepcopy(self.players)
            _current_player= deepcopy(self.current_player_id)
            _board= deepcopy(self.board)
            _dealer = deepcopy(self.dealer)
            _judger= deepcopy(self.judger)
            self.history.append((_players,_current_player,_board,_dealer,_judger))

        # current player plays card and update: hand, board, won_cards, scopa_sum
        self.players[self.current_player_id].play_card(raw_action, self.board)
        
        # check if game or round is over 
        self.is_game_or_round_over()

        switch_player(self)

        player_id = self.current_player_id
        state = self.get_state(player_id)

        return state, player_id

    def step_back(self):
        ''' Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        '''
        if not self.history:
            return False
        self.players, self.current_player_id, \
        self.board, self.dealer, self.judger = self.history.pop()
        return True

    def get_state(self, player_id: int) -> dict:
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''

        state = {}
        player = self.players[player_id]
        opponent_player = self.players[1 - player_id]
        
        state['num_players'] = self.num_players
        state['current_player'] = player_id
        state['my_hand'] = player.hand
        state['opponents_hand'] = opponent_player.hand
        state['board'] = self.board.cards
        state['my_won_cards'] = player.won_cards
        state['opponents_won_cards'] = opponent_player.won_cards

        legal_actions= self.get_legal_actions(player_id)
        state['legal_actions'] = legal_actions

        # TODO: check if needed this...
        state['num_cards'] = []
        for player in self.players:
            state['num_cards'].append(len(player.hand))

        # TODO: maybe add scopa_sum of all players to the state

        return state

    def get_legal_actions(self, player_id: int) -> list[Card]:
        ''' Return the legal actions for a player

        Returns:
            (list): A list of legal actions (as card object)
        '''

        # optional TODO: 
        # - add the possibility to choose if "bussare" or not
        # - check if this function needs the current player or whatever player_id is passed

        hand = self.players[player_id].hand

        return hand
    
    def get_payoffs(self):
        ''' Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
        try:
            winner = self.winner.player_id 
        except:
            pass # game is finished in draw
        else:
            if winner is not None:
                self.payoffs[winner] = 1
                self.payoffs[1 - winner] = -1
        return self.payoffs
    
    @staticmethod
    def get_num_actions():
        ''' Return the number of applicable actions

        Returns:
            (int): The number of actions. 
            There are 40 actions, 1 for each card in the deck
        '''
        return 40
    
    def get_num_players(self):
        return self.num_players

    def is_game_or_round_over(self):
        ''' Check if the game is over (deck and hands empty)
        or the round is over (hands empty)

        Returns:
            []
        '''
        are_hands_empty= self.players[0].hand==[] and self.players[1].hand==[]
        if self.dealer.is_deck_empty():
            if are_hands_empty: # game finished
                # TODO: complicate left cards: 
                # if there are cards on the board, the player who took the last cards takes them
                
                self.players[self.current_player_id].won_cards.extend(self.board.cards)
                self.board.cards= []
                self._is_over= True
                self.winner= self.judger.judge_winner(self.players)
        else:
            if are_hands_empty:  # round finished
                for p in range(self.num_players):
                    self.dealer.deal_cards(self.players[p], 3)

    def get_player_id(self):
        return self.current_player_id   
    
    def is_over(self):
        return self._is_over

# # test initialization game 
# game= CirullaGame()
# print(f"Player: {game.current_player_id}, points: {game.players[game.current_player_id].scopa_sum}")
# print(game.board.__str__())
# game.init_game()
# print(f"Player: {game.current_player_id}, points: {game.players[game.current_player_id].scopa_sum}")
# print(game.board.__str__())
# game.init_game()
# print(f"Player: {game.current_player_id}, points: {game.players[game.current_player_id].scopa_sum}")
# print(game.board.__str__())
# game.init_game()
# print(f"Player: {game.current_player_id}, points: {game.players[game.current_player_id].scopa_sum}")
# print(game.board.__str__())

# # init game with 15/30 sum of first 4 cards in deck 
# game= CirullaGame()
# game.dealer.deck[:4]= [Card("D","A"), Card("H","7"), Card("S","4"), Card("C","3")]
# print(f"initial deck: {[game.dealer.deck[i].__str__() for i in range(4)]}")
# game.init_game()
# for id in [0,1]:
#     assert cards2list(game.get_legal_actions(id)) == cards2list(game.players[id].hand)
#     print(game.players[id].__str__())
# print(f"board: {game.board.__str__()}")
# state= game.get_state(game.current_player_id)
# print('state 0')
# for keys,values in state.items():
#     print(keys + f":  {values}")
# game.is_game_or_round_over()

# possible_card= game.players[game.current_player_id].hand[0]
# next_state, current_player= game.step(possible_card)
# print('state 1')
# for keys,values in next_state.items():
#     print(keys + f":  {values}")


# # step() test = init game with 15/30 sum of first 4 cards in deck and go on 
# game= CirullaGame()
# game.dealer.deck= [Card("D","A"), Card("H","7"), Card("S","4"), Card("C","3"), 
#                    Card("C","A"), Card("D","7"), Card("C","4"),
#                    Card("H","A"), Card("C","7"), Card("H","4")]
# # print(f"initial deck: {[game.dealer.deck[i].__str__() for i in range(4)]}")
# game.init_game()
# for id in [0,1]:
#     assert cards2list(game.get_legal_actions(id)) == cards2list(game.players[id].hand)
#     print(game.players[id].__str__())
# print(f"board: {game.board.__str__()}")
# state= game.get_state(game.current_player_id)
# print('state 0')
# for keys,values in state.items():
#     print(keys + f":  {values}")
# game.is_game_or_round_over()

# possible_card= game.players[game.current_player_id].hand[0]
# next_state, current_player= game.step(possible_card)
# print('state 1')
# for keys,values in next_state.items():
#     print(keys + f":  {values}")

# # step() test = init game with 15/30 sum of first 4 cards in deck and go on 
# game= CirullaGame()
# game.dealer.deck= [Card("D","A"), Card("H","7"), Card("S","4"), Card("C","3"), 
#                    Card("C","A"), Card("D","7"), Card("C","4"),
#                    Card("H","A"), Card("C","7"), Card("H","4")]
# # print(f"initial deck: {[game.dealer.deck[i].__str__() for i in range(4)]}")
# game.init_game()
# for id in [0,1]:
#     assert cards2list(game.get_legal_actions(id)) == cards2list(game.players[id].hand)
#     print(game.players[id].__str__())
# print(f"board: {game.board.__str__()}")
# state= game.get_state(game.current_player_id)
# print('state 0')
# for keys,values in state.items():
#     print(keys + f":{values}")

# c=0
# while game.is_over==False:
#     c+=1
#     possible_card= game.players[game.current_player_id].hand[0]
#     next_state, current_player= game.step(possible_card)
#     print(f'state {c}')
#     for keys,values in next_state.items():
#         print(keys + f":  {values}")
#     game.is_game_or_round_over()

# print("winner is " + game.winner.__str__())


# # step() and is_over() test = init game of complete deck and go on 
# game= CirullaGame()
# game.init_game()
# for id in [0,1]:
#     assert cards2list(game.get_legal_actions(id)) == cards2list(game.players[id].hand)
#     print(game.players[id].__str__())
# print(f"board: {game.board.__str__()}")
# state= game.get_state(game.current_player_id)
# print('state 0')
# for keys,values in state.items():
#     if keys in ['my_hand','board']:
#         print(keys + f":{cards2list(values)}")
# print('current_player' + f": {state['current_player']}")

# c=0
# while game._is_over==False:
#     c+=1
#     possible_card= game.players[game.current_player_id].hand[0]
#     next_state, current_player= game.step(possible_card)
#     print(f'state {c}')
#     for keys,values in next_state.items():
#         if keys in ['my_hand','board']:
#             print(keys + f":  {cards2list(values)}")
#     print('current_player' + f": {state['current_player']}")
#     game.is_game_or_round_over()

# if isinstance(game.winner, list):
#     print('draw!')
# else:
#     print("winner is " + game.winner.__str__())
#     print("loser  is " + game.players[1-game.winner.player_id].__str__())
# print("payoffs")
# print(game.get_payoffs())

# # step_back() test = init game of complete deck and go until a point anc come back 
# game= CirullaGame(allow_step_back=True)
# game.init_game()
# for id in [0,1]:
#     assert cards2list(game.get_legal_actions(id)) == cards2list(game.players[id].hand)
#     print(game.players[id].__str__())
# print(f"board: {game.board.__str__()}")
# state= game.get_state(game.current_player_id)
# print('state 0')
# for keys,values in state.items():
#     if keys in ['my_hand','current_player','board']:
#         print(keys + f":{values}")

# c=0
# while c<3:
#     c+=1
#     possible_card= game.players[game.current_player_id].hand[0]
#     next_state, current_player= game.step(possible_card)
#     print(f'state {c}')
#     for keys,values in next_state.items():
#         print(keys + f":  {values}")
#     game.is_game_or_round_over()

# print(f'state {c-2}')
# game.step_back()
# game.step_back()
# state= game.get_state(game.current_player_id)
# for keys,values in state.items():
#     print(keys + f":  {values}")
