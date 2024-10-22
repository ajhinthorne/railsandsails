#%%
###import packages
import pandas as pd
import numpy as np

###decks interact with player hands and the discard pile


#%%
class card:
    def __init__(self,color,type,harbor,value):
        self.color = color
        self.type = type
        self.harbor = harbor
        self.value = value

#%%    
card_colors = ['pink','yellow','green','red','white','black','wild']
card_types = ['train','ship']
harbor_bool = [True,False]
card_value = [1,2]

### There are 80 train cards, 11 of each color, except for 14 wilds
### all wilds are harbor cards, 4/11 cards are harbor cards for each color
### There are 60 ship cards, 24 are singles (4 of each color, except for wilds), 36 are doubles (6 of each color, except for wilds)
### Each single ship card is a harbor card
#6 colors of trains x 2 harbor types
#1 wild card train type

#6 colors of ships x 2 card quantities
# no wilds
#%% 
face_up_pile = pd.DataFrame(columns = ['color','type','harbor','value'])

### functions for game play
#%%

def reset_deck():
    deck = pd.DataFrame(columns = ['color','type','harbor','value'])

    card_types = pd.DataFrame([['pink','train',False,1,7],
                     ['pink','train',True,1,4],
                     ['yellow','train',False,1,7],
                     ['yellow','train',True,1,4],
                     ['green','train',False,1,7],
                     ['green','train',True,1,4],
                     ['red','train',False,1,7],
                     ['red','train',True,1,4],
                     ['white','train',False,1,7],
                     ['white','train',True,1,4],
                     ['black','train',False,1,7],
                     ['black','train',True,1,4],
                     ['wild','train',False,1,14],
                     ['pink','ship',True,1,4],
                     ['pink','ship',False,2,6],
                     ['yellow','ship',True,1,4],
                     ['yellow','ship',False,2,6],
                     ['green','ship',True,1,4],
                     ['green','ship',False,2,6],
                     ['red','ship',True,1,4],
                     ['red','ship',False,2,6],
                     ['white','ship',True,1,4],
                     ['white','ship',False,2,6],
                     ['black','ship',True,1,4],
                     ['black','ship',False,2,6]],
                        columns = ['color','type','harbor','value','quantity'])

    for type in card_types.iterrows():
        for x in range(0,type[1]['quantity']):
            new_card = pd.DataFrame([[type[1]['color'],type[1]['type'],type[1]['harbor'],type[1]['value']]],columns = ['color','type','harbor','value'])
            deck = deck.append(new_card).reset_index(drop = True)

    print("Deck has been reset")
    return deck

def reset_discard():
    discard_pile = pd.DataFrame(columns = ['color','type','harbor','value'])

    print("Discard Pile has been reset")
    return discard_pile

def reset_deck_from_discard(deck,discard_pile):
    deck = pd.concat([deck,discard_pile]).reset_index(drop = True)
    reset_discard()

    print("Deck has been reset from discard pile")
    return deck



#%%

def draw_from_deck(deck, draws = 1,discard_pile):
 
    ### check if deck needs to be replenished from discard pile
    if np.shape(deck)[0] < draws:
        deck = reset_deck_from_discard(deck,discard_pile)

    new_cards = deck.sample(draws)
    deck = deck.drop(list(new_cards.index)).reset_index(drop = True)
    new_cards = new_cards.reset_index(drop = True)

    return new_cards, deck
    
def draw_from_face_up_pile(face_up_pile,face_up_index,deck):
    
    
    
    
    while np.shape(face_up_pile)[0] < 6:
        
