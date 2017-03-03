# -*- coding: utf-8 -*-
import random

MAX_BLUE_STONE = 9
COLOR = "RGYBW"
CARD_VALUE = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
CARD_IN_HANDS = 5
MAX_BLUE_STONE = 8
MAX_RED_STONE = 3
NO_CARD = "NC"

class InvalidActionError(Exception):
    def __init__(self, message):
        self.message = message

class GameOverError(Exception):
    def __init__(self, message):
        self.message = message

class Game(object):
    def __init__(self, num_players):
        """play a game of hanabi"""
        self.num_players = num_players
        self.firework =  [[], [], [], [], []]
        self.nb_blue_stone =  MAX_BLUE_STONE
        self.nb_red_stone =  MAX_RED_STONE
        self.fill_draw()
        random.shuffle(self.draw)
        self.discard =  []
        self.draw_initial_hands();

    def fill_draw(self):
        self.draw =  [x + str(y) for x in COLOR for y in CARD_VALUE]

    def draw_initial_hands(self):
        self.hands = [[] for i in range(self.num_players)]
        for i in range(self.num_players):
            for j in range(CARD_IN_HANDS):
                self.hands[i].append(self.draw_card())

    def draw_card(self):
        """ At the end of the game, the hand of a player can have less than
        CARD_IN_HANDS cards. In order, not to mess up the indexes of
        the cards in the players minds, a special NO_CARD is drawn and
        put in the hands of the player. """
        if self.draw:
            return self.draw.pop()
        else:
            return NO_CARD

    def reveal(self):
        """ give information to a player only remove a blue stone on the game """
        if self.nb_blue_stone == 0:
            raise InvalidActionError("Cannot reveal, no blue stone left")
        self.nb_blue_stone = self.nb_blue_stone - 1
        
    def discard_card(self, player_index, card_index):
        """ discard the card in player_index hand at card_index position """
        self.discard.append(self.hands[player_index][card_index])
        self.nb_blue_stone = min(self.nb_blue_stone + 1, MAX_BLUE_STONE)
        self.hands[player_index][card_index] = self.draw_card()
        return self.hands[player_index][card_index]

    def play_card(self, player_index, card_index):
        card = self.hands[player_index][card_index]
        color_index = COLOR.index(card[0])
        if self.is_card_playable(card):
            #the color and the number match, add the card
            self.firework[color_index].append(card)
            #if we complete the firework for a color, we get an extra blue stone
            if len(self.firework[color_index]) == 5:
                self.nb_blue_stone = min(self.nb_blue_stone + 1, MAX_BLUE_STONE)
        else:
            #error, the card cannot be played, remove a red_stone
            if self.nb_red_stone ==  0:
                raise GameOverError("The card " + card + " cannot be played and there is no red stone anymore")
            self.nb_red_stone = self.nb_red_stone - 1
        self.hands[player_index][card_index] = self.draw_card()
        return self.hands[player_index][card_index]

    def is_card_playable(self, card):
        color_index = COLOR.index(card[0])
        return len(self.firework[color_index]) == int(card[1]) - 1

    def is_card_in_other_hands(self, own_hand_index, card):
        for i,hand in enumerate(self.hands):
            if i == own_hand_index:
                continue
            if card in hand:
                return True
        return False
   
    def score(self):
        return sum(len(i) for i in self.firework)
   
def merge(know, information):
    result = []
    return know
    for i in range(len(know)):
        a = know[i]
        b = information[i]
        r = []
        for j in range(2):
            if a[j] != '?':
                r.append(a[j])
            elif b[j] != '?':
                r.append(b[j])
            else:
                r.append('?')
        result.append(''.join(r))
    return result

class Player(object):
    def __init__(self, game, index, strategy):
        self.know = ["??"] * CARD_IN_HANDS
        self.game = game
        self.players = []
        self.index = index
        self.strategy = strategy

    def add_player(self, player):
        self.players.append(player)

    def play(self):
        self.strategy(self)
    
    def inform(self, information):
        self.know = merge(self.know, information)
        
    def reveal(self, listening_player, information):
        self.game.reveal()
        listening_player.inform(information)

    def play_card(self, card_index):
        if self.game.play_card(self.index, card_index) == NO_CARD:
            self.know[card_index] = NO_CARD
        else:
            self.know[card_index] = "??"

    def discard_card(self, card_index):
        if self.game.discard_card(self.index, card_index) == NO_CARD:
            self.know[card_index] = NO_CARD
        else:
            self.know[card_index] = "??"

class Strategy(object):
    def __call__(self, player):
        game = player.game
        hand = game.hands[player.index]
        for i, card in enumerate(hand):
            if game.is_card_playable(card):
                print "play " + card
                player.play_card(i)
                return
        for i, card in enumerate(hand):
            if card in game.draw or game.is_card_in_other_hands(player.index, card):
                print "discard " + card
                player.discard_card(i)
                return
        print "reveal "
        player.reveal(player.players[0],"R1")
      
      
def play_hanabi(num_players, strategy=None):
    game = Game(num_players)
    print(game)
    players = [Player(game, i, strategy) for i in range(num_players)]
    for player1 in players:
        for player2 in players:
            if player1.index == player2.index:
                continue
            player1.add_player(player2)
    turn = 0
    while game.draw:
        player = players[turn]
        player.play()
        turn = (turn + 1) % num_players
    #last turn
    for i in range(num_players):
        player = players[turn]
        player.play()
        turn = (turn + 1) % num_players
      
    print game.firework
    print game.hands
    print game.score()

if __name__ == "__main__":
    play_hanabi(4, Strategy())
