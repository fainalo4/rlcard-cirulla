import numpy as np
from collections import OrderedDict

from rlcard.envs import Env
from rlcard.games.cirulla.game import CirullaGame as Game

from rlcard.games.cirulla.utils import cards2list, encode_cards

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
        self.state_shape = [[5,40] for _ in range(self.num_players)]
        self.action_shape = [[3] for _ in range(self.num_players)]

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

    def _extract_state(self, state):
        ''' Encode state

        Args:
            state (dict): dict of original state

        Returns:
            numpy array: 5 * 40 array
                         5 :board state         (1 if card in board else 0) 
                            my hand             (1 if card in hand else 0)
                            oppents hand        (1 if card in hand else 0)
                            my won cards        (1 if card in won cards else 0)
                            opponents won cards (1 if card in won cards else 0)
        TODO: add also points for each player as integers
        '''
   
        board_rep= encode_cards(state['board'])
        my_hand_rep= encode_cards(state['my_hand'])
        opponents_hand_rep= encode_cards(state['opponents_hand'])
        my_won_cards_rep= encode_cards(state['my_won_cards'])
        opponents_won_cards_rep= encode_cards(state['opponents_won_cards'])

        extracted_state= {}
        extracted_state['obs']= np.array([board_rep,
                                          my_hand_rep, 
                                          opponents_hand_rep, 
                                          my_won_cards_rep, 
                                          opponents_won_cards_rep])
        extracted_state['raw_obs']= state
        extracted_state['legal_actions']= self._get_legal_actions() 
        extracted_state['raw_legal_actions']= state['legal_actions']

        return extracted_state


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


# # test for _extract_state function
# env= CirullaEnv()
# env.game.init_game()
# player= env.game.current_player_id
# extr_state= env._extract_state(env.game.get_state(player))
# print('extracted state:')
# for keys,values in extr_state.items():
#     print(keys + f":  {values}")
# env.step(0)
# player= env.game.current_player_id
# extr_state= env._extract_state(env.game.get_state(player))
# print('extracted state:')
# for keys,values in extr_state.items():
#     print(keys + f":  {values}")
# env.step(0)
# player= env.game.current_player_id
# extr_state= env._extract_state(env.game.get_state(player))
# print('extracted state:')
# for keys,values in extr_state.items():
#     print(keys + f":  {values}")

# # # test run() in Env class
# env= CirullaEnv()
# env.run()