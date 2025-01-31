import numpy as np
from collections import OrderedDict

from rlcard.envs import Env
from rlcard.games.cirulla.game import CirullaGame as Game
from rlcard.games.cirulla.card import CirullaCard as Card

from rlcard.games.cirulla.utils import encode_cards, get_card_id, card_from_card_id

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


    def get_payoffs(self) -> np.array:
        return np.array(self.game.get_payoffs())


    def _decode_action(self, action_id: int) -> Card:
        legal_ids = self._get_legal_actions()
        if action_id in legal_ids.keys():
            return card_from_card_id(action_id)
        else:
            return card_from_card_id(np.random.choice(list(legal_ids.keys())))


    def _get_legal_actions(self) -> dict:
        legal_actions = self.game.get_legal_actions(self.game.current_player_id)
        legal_ids = {get_card_id(card): card for card in legal_actions}
        return OrderedDict(legal_ids)


    def _extract_state(self, state) -> dict:
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
# for a in legal_actions.keys():
#     print(a , f' : {legal_actions[a].__str__()}')
# which_card= 0
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

# # test step() in Env class
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