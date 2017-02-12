# -*- coding: utf-8 -*-
import random

MAX_BLUE_STONE = 9
COLOR = "RGYBW"
CARD_VALUE = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
CARD_IN_HANDS = 5
MAX_BLUE_STONE = 9
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
        self.draw =  [x + str(y) for x in COLOR for y in CARD_VALUE]
        random.shuffle(self.draw)
        self.discard =  []
        self.hands = [[] for i in range(num_players)]
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

    def play_card(self, player_index, card_index):
        card = self.hands[player_index][card_index]
        color_index = COLOR.index(card[0])
        if len(self.firework[color_index]) == int(card[1]) - 1:
            #the color and the number match, add the card
            self.firework[color_index].append(card)
        else:
            #error, the card cannot be played, remove a red_stone
            if self.nb_red_stone ==  0:
                raise GameOverError("The card " + card + " cannot be played and there is no red stone anymore")
            game["nb_red_stone"] = game["nb_red_stone"] - 1
        self.hands[player_index][card_index] = self.draw_card()
def merge(know, information):
    result = []
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


def reveal_on_player(listening_player, playing_player, information):
    know = listening_player["know"][playing_player["index"]]
    know = merge(know, information)


def draw_on_player(listening_player, playing_player, card_index):
    listening_player["know"][playing_player["index"]][card_index] = "??"


def play_card_on_player(listening_player, playing_player, card_index):
    listening_player["know"][playing_player["index"]][card_index] = "??"


def strategy_random(player, game):
    pass


def init_players(index, num_players):
    """ at start everybody knows nothing"""
    return {"index": index, "know": [["??"] * CARD_IN_HANDS] * num_players}


def play_hanabi(num_players, strategy=None):
    game = init_hanabi(num_players)
    print(game)
    players = [init_players(i, num_players) for i in range(num_players)]
    turn = 0
    while game["draw"]:
        player = players[turn]
        action_on_game, action_on_players = strategy(player, game)
        action_on_game(game)
        for player in players:
            action_on_players(player)
        if is_game_finished(game):
            break
        turn = (turn + 1) % num_players
    return game_status(game)
