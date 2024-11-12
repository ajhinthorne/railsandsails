#%%
###import packages
import pandas as pd # type: ignore

### local files
import game_module.game_classes as g

#%%

my_new_game = g.game(g.deck(),g.game_board())
my_new_game.initialize_game(2,game_type="washington")


### on average how many turns does it take a route to become playable?
### steps:
### initialize game


n = 100