#%%
###import packages
import pandas as pd
import numpy as np

###ever present object for cards
# deck, face_up_pile, discard_pile
class card_bank:
    def __init__(self,name):
        self.name = name
        self.deck = pd.DataFrame(columns = ['color','type','harbor','value'])
        self.discard_pile = pd.DataFrame(columns = ['color','type','harbor','value'])
        self.face_up_pile = pd.DataFrame(columns = ['color','type','harbor','value'])

    def reset_deck_from_discard(self):
        self.deck = pd.concat([self.deck,self.discard_pile]).reset_index(drop = True)
        self.discard_pile = pd.DataFrame(columns = ['color','type','harbor','value'])
        
        print("Deck has been reset from discard pile")

    def draw_from_deck_to_face_up_pile(self):

        draws = 6 - np.shape(self.face_up_pile)[0]

        ### if the deck is not large enough to accomodate the number of draws, the deck must be reset from discard
        if np.shape(self.deck)[0] < draws:
            self.reset_deck_from_discard()
    
        draw_action = self.deck.sample(draws)

        self.face_up_pile = pd.concat([self.face_up_pile,draw_action])
        self.deck = self.deck.drop(list(draw_action.index)).reset_index(drop=True)
        self.face_up_pile = self.face_up_pile.reset_index(drop = True)

class player:
    def __init__(self,name):
        self.name = name
        self.hand = pd.DataFrame(columns = ['color','type','harbor','value'])
        self.pieces = pd.DataFrame(columns = ['type'])

    ### actions
    def deal_start_of_game_hand(self,card_bank):

        train_cards = card_bank.deck[card_bank.deck['type'] == 'train'].sample(3)
        ship_cards = card_bank.deck[card_bank.deck['type'] == 'ship'].sample(7)

        new_cards = pd.concat([train_cards,ship_cards])
        card_bank.deck = card_bank.deck.drop(list(new_cards.index)).reset_index(drop = True)
        new_cards = new_cards.reset_index(drop=True)

        self.hand = new_cards

        print(f'''{self.name} has been dealt a new hand''')      
    
    def draw_from_deck_to_hand(self,card_bank,draws):
    
        ### if the deck is not large enough to accomodate the number of draws, the deck must be reset from discard
        if np.shape(card_bank.deck)[0] < draws:
            card_bank.reset_deck_from_discard()

        new_cards = card_bank.deck.sample(draws)
        card_bank.deck = card_bank.deck.drop(list(new_cards.index)).reset_index(drop = True)
        new_cards = new_cards.reset_index(drop = True)
        
        self.hand = pd.concat([self.hand,new_cards]).reset_index(drop = True)

        print("Cards drawn to hand: " + str(np.shape(new_cards)[0]))

    def discard_from_hand(self,card_bank,hand_discard):
        card_bank.discard_pile = pd.concat([card_bank.discard_pile,hand_discard]).reset_index(drop = True)
        self.hand = self.hand.drop(list(hand_discard.index)).reset_index(drop = True)
        
        print(f'''Number of cards discarded: {str(np.shape(hand_discard)[0])}''')


    def draw_from_face_up_pile_to_hand(self,card_bank,face_up_index_list):
        new_cards = card_bank.face_up_pile.iloc[[face_up_index_list]]
        card_bank.face_up_pile = card_bank.face_up_pile.drop(list(new_cards.index)).reset_index(drop = True)
        card_bank.draw_from_deck_to_face_up_pile()
        self.hand = pd.concat([self.hand,new_cards]).reset_index(drop = True)

        print(f'''Number of cards drawn from the face_up_pile: {str(np.shape(new_cards)[0])}''')
        
class route:
    def __init__(self):
        self.city_list = []
        self.length = 0
        self.cost = 0
        self.points = 0
        self.status = "Incomplete"

class ticket:
    def __init__(self):
        self.route_df = pd.DataFrame(columns = ['order','route'])
        self.base_points = 0 
        self.in_order_point_bonus = 0
        self.status = "Incomplete"

# Build a Function To set up the game

### functions

#%%
class game:
     def __init__(self,name):
        self.name = name
        self.bank = card_bank("game_bank")
        self.player_list = []

    ### do we want to create a player dictionary that consists of the player's names?

     def initialize_test_game(self,number_of_players):

            if number_of_players < 2 | number_of_players > 5:
                raise ValueError(f'''Number of players has to be between 2 and 5. Current Number of Players: {number_of_players}''')

            ### create the deck from the deck initialization dataframe
            ### for now this is the version of the game we will be testing with, it is the actual specs from the game
            card_types = pd.DataFrame([['pink','train',False,1,7],
                            ['yellow','train',False,1,7],
                            ['wild','train',False,1,7]],
                                columns = ['color','type','harbor','value','quantity'])

            for type in card_types.iterrows():
                for x in range(0,type[1]['quantity']):
                    new_card = pd.DataFrame([[type[1]['color'],type[1]['type'],type[1]['harbor'],type[1]['value']]],columns = ['color','type','harbor','value'])
                    self.bank.deck = self.bank.deck.append(new_card).reset_index(drop = True)

            for x in range(1,(number_of_players + 1)):
                new_player = player(f'''player_{x}''')
                new_player.deal_start_of_game_hand(self.bank)
                self.player_list.append(new_player)
                print(f'''{new_player.name} has been added to the player list''')
            
            self.bank.draw_from_deck_to_face_up_pile()
            print(f'''New Test Game has been created''')

     def initialize_standard_game(self,number_of_players):

            if number_of_players < 2 | number_of_players > 5:
                raise ValueError(f'''Number of players has to be between 2 and 5. Current Number of Players: {number_of_players}''')

            ### STANDARD GAME SCHEMA
                ### There are 80 train cards, 11 of each color, except for 14 wilds
                ### all wilds are harbor cards, 4/11 cards are harbor cards for each color
                ### There are 60 ship cards, 24 are singles (4 of each color, except for wilds), 36 are doubles (6 of each color, except for wilds)
                ### Each single ship card is a harbor card
                #6 colors of trains x 2 harbor types
                #1 wild card train type

            
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
                    self.bank.deck = self.bank.deck.append(new_card).reset_index(drop = True)

            for x in range(1,(number_of_players + 1)):
                new_player = player(f'''player_{x}''')
                new_player.deal_start_of_game_hand(self.bank)
                self.player_list.append(new_player)
                print(f'''{new_player.name} has been added to the player list''')
            
            self.bank.draw_from_deck_to_face_up_pile()
            print(f'''New Standard Game has been created''')














# %%
