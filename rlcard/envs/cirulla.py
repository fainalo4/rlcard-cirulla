import numpy as np
from collections import OrderedDict

from rlcard.envs import Env
from rlcard.games.cirulla.game import CirullaGame as Game

# from rlcard.games.cirulla.utils import encode_hand
# from rlcard.games.cirulla.utils import ACTION_SPACE, ACTION_LIST
from rlcard.games.cirulla.utils import cards2list

DEFAULT_GAME_CONFIG = {
        'num_players': 2,
        'allow_step_back': True,
        'seed': 4
        }

class CirullaEnv(Env):

    def __init__(self, config = DEFAULT_GAME_CONFIG):
        self.name = 'cirulla'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = Game()
        super().__init__(config)
        self.state_shape = [[4, 4, 15] for _ in range(self.num_players)]
        self.action_shape = [[3] for _ in range(self.num_players)]

    def _extract_state(self, state): 
        pass

    def get_payoffs(self):

        return np.array(self.game.get_payoffs())

    def _decode_action(self, action_id):
        legal_ids = self._get_legal_actions()
        current_player= self.game.players[self.game.current_player_id]
        cards_in_hand= current_player.hand
        if action_id in legal_ids:
            return cards_in_hand[action_id]
        else:
            return cards_in_hand[np.random.choice(legal_ids)]

    def _get_legal_actions(self):
        legal_actions = self.game.get_legal_actions(self.game.current_player_id)
        number_of_cards_in_hand= len(legal_actions)
        legal_ids = list(range(number_of_cards_in_hand))
        return legal_ids

    def get_perfect_information(self):
        ''' Get the perfect information of the current state

        Returns:
            (dict): A dictionary of all the perfect information of the current state
        '''
        state = {}
        state['num_players'] = self.num_players
        state['hand_cards'] = [cards2list(player.hand)
                               for player in self.game.players]
        state['played_cards'] = cards2list(self.game.round.played_cards)
        state['target'] = self.game.round.target.str
        state['current_player'] = self.game.round.current_player
        state['legal_actions'] = self.game.round.get_legal_actions(
            self.game.players, state['current_player'])
        return state

# # test for action functions
# env= CirullaEnv()
# env.game.init_game()
# legal_actions= env._get_legal_actions()
# print('action ids:')
# print(legal_actions)
# which_card= 1
# print(f'action # {which_card}')
# decoded_legal_action= env._decode_action(which_card)
# print(decoded_legal_action.__str__())
# print('check')
# print(f'current player {env.game.current_player_id}')
# print(env.game.players[0].__str__())
# print(env.game.players[1].__str__())