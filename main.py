#%%
###import packages
import pandas as pd
import numpy as np

### local files
from game_module import game_classes as g

#%%

my_new_game = g.game("my_new_game")
my_new_game.initialize_standard_game(2)











# %%
test_df = pd.DataFrame([["Test Name!",["city_a","city_b"]]], columns = ["my_name","my_list"])
test_df

# %%
test_df['my_list'].values[0][0]