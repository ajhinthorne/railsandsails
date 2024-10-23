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

###ever present object for cards
# deck, face_up_pile, discard_pile
class card_bank:
    def __init__(self,deck,discard_pile,face_up_pile):
        self.deck = deck
        self.discard_pile = discard_pile
        self.face_up_pile = face_up_pile


    deck = pd.DataFrame(columns = ['color','type','harbor','value'])
    discard_pile = pd.DataFrame(columns = ['color','type','harbor','value'])
    face_up_pile = pd.DataFrame(columns = ['color','type','harbor','value'])

    def reset_bank(self):
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

        ### draw six cards from the deck to create the face up pile
        face_up_pile = pd.DataFrame(columns = ['color','type','harbor','value'])

        face_up_pile = deck.sample(6)
        deck = deck.drop(list(face_up_pile.index)).reset_index(drop=True)
        face_up_pile = face_up_pile.reset_index(drop = True)

        ### create empty discard pile
        discard_pile = pd.DataFrame(columns = ['color','type','harbor','value'])

        self.deck = deck
        self.face_up_pile = face_up_pile
        self.discard_pile = discard_pile

        print("Bank has been reset")
        return self

    def reset_deck_from_discard(deck,discard_pile):
        deck = pd.concat([deck,discard_pile]).reset_index(drop = True)
        discard_pile = pd.DataFrame(columns = ['color','type','harbor','value'])
        
        print("Deck has been reset from discard pile")
        return deck,discard_pile
    
    def draw_from_deck_to_face_up_pile(deck,face_up_pile,discard_pile):

        draws = 6 - np.shape(face_up_pile)[0]

        ### if the deck is not large enough to accomodate the number of draws, the deck must be reset from discard
        if np.shape(deck)[0] < draws:
            deck = self.reset_deck_from_discard()
    
        draw_action = deck.sample(draws)

        face_up_pile = pd.concat([face_up_pile,draw_action.new_cards]).reset_index(drop=True)
        deck = draw_action.deck

        return face_up_pile, deck
    
class player:
    def __init__(self,name,hand):
        self.name = name
        self.hand = hand

    def deal_start_of_game_hand(self,card_bank):

        self.hand = pd.DataFrame(columns = ['color','type','harbor','value'])

        train_cards = card_bank.deck[card_bank.deck['type'] == 'train'].sample(3)
        ship_cards = card_bank.deck[card_bank.deck['type'] == 'train'].sample(7)

        new_cards = pd.concat([train_cards,ship_cards])
        card_bank.deck = card_bank.deck.drop(list(new_cards.index)).reset_index(drop = True)
        new_cards = new_cards.reset_index(drop=True)

        self.hand = new_cards

        print(f'''{self.name} has been dealt a new hand''')
        return self      

    def draw_from_deck_to_hand(self,card_bank,draws):
    
        ### if the deck is not large enough to accomodate the number of draws, the deck must be reset from discard
        if np.shape(card_bank.deck)[0] < draws:
            card_bank.deck = card_bank.reset_deck_from_discard()

        new_cards = card_bank.deck.sample(draws)
        card_bank.deck = card_bank.deck.drop(list(new_cards.index)).reset_index(drop = True)
        new_cards = new_cards.reset_index(drop = True)
        
        self.hand = pd.concat([self.hand,new_cards]).reset_index(drop = True)

        print("Cards drawn to hand: " + str(np.shape(new_cards)[0]))

    def draw_from_face_up_pile_to_hand(self,card_bank,face_up_index_list):

        new_cards = card_bank.face_up_pile.iloc[[face_up_index_list]]

    def discard_from_hand(card_bank,hand_discard):
        card_bank.discard_pile = pd.concat([card_bank.discard_pile,hand_discard]).reset_index(drop = True)
        print("Number of cards discarded: " + str(np.shape(hand_discard)[0]))

class route:
    def __init__(self,city_list,length,points):
        self.city_list = city_list
        self.length = length
        self.points = points

# Build a Function To set up the game

def initialize_game(number_of_players):
        
        game_bank = card_bank

        if number_of_players < 2 | number_of_players > 5:
            raise ValueError(f'''Number of players has to be between 2 and 5. Current Number of Players: {number_of_players}''')

        ### create the deck
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
                game_bank.deck = game_bank.deck.append(new_card).reset_index(drop = True)

        player_list = []
        for x in range(1,(number_of_players + 1)):
            new_player = player(name = f'''player_{x}''')
            new_player = new_player.deal_start_of_game_hand(new_player,game_bank)

            player_list.append(new_player)
            print(f'''{new_player.name} has been added to the player list''')

        return [game_bank, player_list]










# %%
