#%%
import pandas as pd
import os
import rand

card_data_path = str(os.getcwd()) + '\\game_module\\washingtoncardbank_data.csv'
city_data_path = str(os.getcwd()) + '\\game_module\\washingtoncity_data.csv'
route_data_path = str(os.getcwd()) + '\\game_module\\washingtonroute_data.csv'

card_data = pd.read_csv(card_data_path)
city_data = pd.read_csv(city_data_path)
route_data = pd.read_csv(route_data_path)


#%% 
my_hand = card_data.sample(5)



my_hand.groupby(['color','type','harbor','value','quantity']).count().reset_index()

# %%
