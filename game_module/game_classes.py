#%%
import pandas as pd
import random as rand

### pandas and numpy required

###pandas and numpy required
### card banks contain dataframes representing the deck, discard, and face up piles

class city:
    def __init__(self):
        self.name = ""
        self.harbor = False
        self.owner = ""
        self.connections = []

class route:
    def __init__(self,route_code):
        self.route_code = route_code
        self.city_list = []
        self.color = ""
        self.type = ""
        self.cost = 0
        self.length = 0
        self.points = 0
        self.owner = ""       

class game_board:
    def __init__(self):
        self.name = ""
        self.routes = []
        self.cities = []

    def initialize_board_from_data(self,city_csv,route_csv):
        city_info = pd.read_csv(city_csv)
        route_info = pd.read_csv(route_csv)

        for city in city_info:
            new_city = city()
            new_city.name = city[1]["name"]
            new_city.harbor = city[1]["harbor"]

            self.cities.append(new_city)
        
        for route in route_info:
            new_route = route(route[1]['route_code'])
            new_route.city_list = [route[1]['city_a'],route[1]['city_b']]
            new_route.color = route[1]['color']
            new_route.type = route[1]['type']
            new_route.cost = route[1]['cost']
            new_route.length = route[1]['length']
            new_route.points = route[1]['points']

            ###appending city connections to each of the cities
            [city for city in self.cities if city.name == route[1]['city_a']][0].connections.append(route[1]['city_b'])
            [city for city in self.cities if city.name == route[1]['city_b']][0].connections.append(route[1]['city_a'])

            self.routes.append(new_route)

class card:
    def __init__(self):
        self.color = ""
        self.type = ""
        self.harbor = False
        self.value = 0

class deck:
    def __init__(self,name):
        self.name = name
        self.train_draw_pile = []
        self.ship_draw_pile = []
        self.faceup_pile = []
        self.discard_pile = []

    def reset_discard_pile(self):
        self.discard_pile = []

    def initialize_deck_from_data(self,card_csv):
        card_info = pd.read_csv(card_csv)

        for card_types in card_info.iterrows():
            for card_num in range(0,card_types[1]['quantity']):
                    new_card = card()
                    new_card.color = card_types[1]['color']
                    new_card.type = card_types[1]['type']
                    new_card.harbor = card_types[1]['harbor']
                    new_card.value = card_types[1]['value']

                    if new_card.type == 'train':
                        self.train_draw_pile.append(new_card)
                    elif new_card.type == 'ship':
                        self.ship_draw_pile.append(new_card)

    def initialize_faceup_pile(self):
        for train_card in range(0,3):
            self.transfer_one_card_from_draw_to_faceup_pile('train')

        for ship_card in range(0,3):
            self.transfer_one_card_from_draw_to_faceup_pile('ship') 

    def deal_start_of_game_hand_to_player(self,player):
        
        ### deal 3 train cards to a player
        train_cards = rand.sample(self.train_draw_pile,3)
        player.hand.cards = player.hand.cards + train_cards
        self.train_draw_pile = list(set(self.train_draw_pile) - set(train_cards))

        ### deal 7 ship cards to a player
        ship_cards = rand.sample(self.ship_draw_pile,7)
        player.hand.cards = player.hand.cards + ship_cards
        self.ship_draw_pile = list(set(self.ship_draw_pile) - set(ship_cards))

        print(f'''{player.name} has been dealt a new hand''') 

    def output_deck_as_dataframe(self):
        output_df = pd.DataFrame(columns = ['color','type','harbor','value'])

        for card in self.train_draw_pile:
            new_card_df = pd.DataFrame([[card[1]['color'],card[1]['type'],card[1]['harbor'],card[1]['value']]],columns = ['color','type','harbor','value'])

            output_df = pd.concat([output_df,new_card_df])

        for card in self.ship_draw_pile:
            new_card_df = pd.DataFrame([[card[1]['color'],card[1]['type'],card[1]['harbor'],card[1]['value']]],columns = ['color','type','harbor','value'])

            output_df = pd.concat([output_df,new_card_df])           

        return output_df
    
    def reset_draw_piles_from_discard(self):
        self.train_draw_pile = self.train_draw_pile + [train_card for train_card in self.discard_pile if train_card.type == 'train']
        self.ship_draw_pile = self.ship_draw_pile + [ship_card for ship_card in self.discard_pile if ship_card.type == 'ship']
        self.reset_discard_pile()

    def transfer_one_card_from_draw_to_faceup_pile(self,type):

        if (len(self.train_draw_pile) == 0) | (len(self.ship_draw_pile) == 0):
                self.reset_draw_piles_from_discard()

        if type == 'train':
            new_card = rand.sample(self.train_draw_pile,1)
            self.faceup_pile = self.faceup_pile + new_card
            self.train_draw_pile = list(set(self.train_draw_pile) - set(new_card))

        elif type == 'ship':
            new_card = rand.sample(self.ship_draw_pile,1)
            self.faceup_pile = self.faceup_pile + new_card
            self.ship_draw_pile = list(set(self.ship_draw_pile) - set(new_card))

class hand():
    def __init__(self):
        self.cards = []

    def draw_cards_from_draw_deck(self,deck,draw_size):
        if len(deck.draw_pile) < draw_size:
            deck.reset_deck_from_discard() 
        
        new_cards = rand.sample(deck.draw_pile,draw_size)

        self.cards = self.cards + new_cards
        deck.draw_pile = list(set(deck.draw_pile) - set(new_cards))

    def choose_one_card_from_face_up_pile(self,deck,card,type):
        self.cards = self.cards + card
        deck.faceup_pile = list(set(deck.faceup_pile)-set(card))
        deck.transfer_one_card_from_draw_to_faceup_pile(type)

    def discard_from_hand(self,deck,hand_discard):
        deck.discard_pile = deck.discard_pile + hand_discard
        self.cards = list(set(self.cards) - set(hand_discard))
        
        print(f'''Number of cards discarded: {str(len(hand_discard))}''')

class ticket:
    def __init__(self):
        self.cities = []
        self.points = 0
        self.status = "Incomplete"

class piece:
    def __init__(self):
        owner = ""
        type = ""

class player(hand):
    def __init__(self,name,hand):
        self.name = name
        self.hand = hand
        self.pieces = []
        self.routes = []

    ### 20 trains and 40 ships is the recommended distribution
    def choose_piece_distribution(self,trains = 20, ships = 40):
        if trains <= 0 | ships <= 0:
            raise ValueError(f'''Cannot have negative train ({trains}) or ship ({ships}) pieces. Reselect piece distribution.''')
        
        elif trains >= 60 | ships >= 60:
            raise ValueError(f'''Too many train ({trains}) or ship ({ships}) pieces. Reselect piece distribution.''')
        
        elif trains + ships != 60:
            raise ValueError(f'''Train ({trains}) and ship ({ships}) pieces must total to 60 pieces. Current: {trains + ships} pieces. Reselect piece distribution.''')

        for train in range(0,trains):
            new_piece = piece()
            new_piece.owner = self.name
            new_piece.type = "train"

            self.pieces.append(new_piece)

        for ship in range(0,ships):
            new_piece = piece()
            new_piece.owner = self.name
            new_piece.type = "ship"

            self.pieces.append(new_piece)

        for harbor in range(0,3):
            new_piece = piece()
            new_piece.owner = self.name
            new_piece.type = "harbor"
     
class game(deck,game_board):
     def __init__(self):
        self.deck = deck
        self.game_board = game_board
        self.player_list = []

    ### do we want to create a player dictionary that consists of the player's names?

     def initialize_test_game(self,number_of_players):

            if number_of_players < 2 | number_of_players > 5:
                raise ValueError(f'''Number of players has to be between 2 and 5. Current Number of Players: {number_of_players}''')

            ### create the deck from the deck initialization dataframe
            ### for now this is the version of the game we will be testing with, it is the actual specs from the game
            card_types = pd.DataFrame([['pink','train',False,1,40],
                            ['yellow','train',False,1,40],
                            ['wild','train',False,1,40],
                            ['pink','ship',False,1,40],
                            ['yellow','ship',False,1,40]],
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

            for x in range(1,(number_of_players + 1)):
                new_player = player(f'''player_{x}''')
                new_player.deal_start_of_game_hand(self.bank)
                self.player_list.append(new_player)
                print(f'''{new_player.name} has been added to the player list''')
            
            self.bank.draw_from_deck_to_face_up_pile()
            print(f'''New Standard Game has been created''')
# %%
