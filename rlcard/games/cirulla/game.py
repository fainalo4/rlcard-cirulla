from copy import deepcopy
import numpy as np

# from rlcard.games.cirulla.card import CirullaCard as Card
# from rlcard.games.cirulla.dealer import CirullaDealer as Dealer
# from rlcard.games.cirulla.player import CirullaPlayer as Player
# from rlcard.games.cirulla.board import Board, Take
# from rlcard.games.cirulla.judger import CirullaJudger as Judger
# from rlcard.games.cirulla.utils import flip_top_4_cards 

from card import CirullaCard as Card
from dealer import CirullaDealer as Dealer
from player import CirullaPlayer as Player
from board import Board, Take
from judger import CirullaJudger as Judger
from utils import flip_and_check_top_4_cards, switch_player

 

class CirullaGame:

    def __init__(self, allow_step_back=False, num_players=2):
        
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()

        self.num_players = num_players
        # Initialize 2 players to play the game
        self.players = [Player(i, self.np_random) for i in range(self.num_players)]

        self.current_player_id = self.np_random.randint(0,2)

        self.payoffs = [0 for _ in range(self.num_players)]
        self.dealer = Dealer(self.np_random)
        self.board = Board()

        self.is_over = False
        self.winner = None

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
        flip_and_check_top_4_cards(self)

        # Deal 3 cards to each player to prepare for the game
        for player in self.players:
            self.dealer.deal_cards(player, 3)

        # Save the history for stepping back to the last state.
        self.history = []

        state = self.get_state(self.current_player_id)
        
        return state, self.current_player_id

    def step(self, action):
        ''' Get the next state

        Args:
            action (str): A specific action

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        '''

        if self.allow_step_back:
            # First snapshot the current state
            his_dealer = deepcopy(self.dealer)
            his_round = deepcopy(self.round)
            his_players = deepcopy(self.players)
            self.history.append((his_dealer, his_players, his_round))

        self.round.proceed_round(self.players, action)
        player_id = self.round.current_player
        state = self.get_state(player_id)
        return state, player_id

    def step_back(self):
        ''' Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        '''
        if not self.history:
            return False
        self.dealer, self.players, self.round = self.history.pop()
        return True

    def get_state(self, player_id):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        pass

    def get_legal_actions(self):
        ''' Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        '''

        return self.round.get_legal_actions(self.players, self.round.current_player)

    def get_num_players(self):
        ''' Return the number of players in Limit Texas Hold'em

        Returns:
            (int): The number of players in the game
        '''
        return self.num_players

    def get_payoffs(self):
        ''' Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
        winner = self.winner
        if winner is not None and len(winner) == 1:
            self.payoffs[winner[0]] = 1
            self.payoffs[1 - winner[0]] = -1
        return self.payoffs
    
    @staticmethod
    def get_num_actions():
        ''' Return the number of applicable actions

        Returns:
            (int): The number of actions. 
            There are 40 actions, 1 for each card in the deck
        '''
        return 40

    def get_player_id(self):
        ''' Return the current player's id

        Returns:
            (int): current player's id
        '''
        return self.current_player_id

    def is_over(self):
        ''' Check if the game is over

        Returns:
            (boolean): True if the game is over
        '''
        return self.is_over


# game= CirullaGame()
# print(f"Player: {game.current_player_id}, points: {game.players[game.current_player_id].scopa_sum}")
# print(game.board.__str__())
# game.init_game()
# print(f"Player: {game.current_player_id}, points: {game.players[game.current_player_id].scopa_sum}")
# print(game.board.__str__())

# init game with 15/30 sum of first 4 cards in deck 
# game= CirullaGame()
# print(f"Player: {game.current_player_id}, points: {game.players[game.current_player_id].scopa_sum}")
# print(game.board.__str__())
# game.dealer.deck[:4]= [Card("D","A"), Card("H","7"), Card("S","4"), Card("C","3")]
# print([game.dealer.deck[i].__str__() for i in range(4)])
# flip_and_check_top_4_cards(game)
# print(f"Player: {game.current_player_id}, points: {game.players[game.current_player_id].scopa_sum}")
# print(game.board.__str__())
# switch_player(game)
# print(f"Player: {game.current_player_id}, points: {game.players[game.current_player_id].scopa_sum}")