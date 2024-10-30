#%%
###import packages
import pandas as pd
import numpy as np

### local files
from game_module import game_classes as g

#%%

my_new_game = g.game(g.deck(),g.game_board())
my_new_game.game_board.initialize_board_from_data()
my_new_game.deck.initialize_deck_from_data()






# %%
test_df['my_list'].values[0][0]