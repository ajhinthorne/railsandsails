#%%
###import packages
import pandas as pd # type: ignore

### local files
import game_module.game_classes as g

#%%

my_new_game = g.game(g.deck(),g.game_board())
my_new_game.initialize_game(2,game_type="washington")

###New changes

# %%
