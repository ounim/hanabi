# -*- coding: utf-8 -*-
import random

MAX_BLUE_STONE = 9
COLOR = "RGYBW"
CARD_VALUE = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
CARD_IN_HANDS = 5
MAX_BLUE_STONE = 9
MAX_RED_STONE = 3
START_GAME = {"firework": [[], [], [], [], []],
              "nb_blue_stone": MAX_BLUE_STONE,
              "nb_red_stone": MAX_RED_STONE,
              "draw": [x + str(y) for x in COLOR for y in CARD_VALUE],
              "discard": []
}

class InvalidActionError(Exception):
    def __init__(self, message):
        self.message = message

def reveal_on_game(game):
    if game["nb_blue_stone"] == 0:
        raise InvalidActionError("Cannot reveal, no blue stone left")
    game["nb_blue_stone"] = game["nb_blue_stone"] - 1


def discard_on_game(game, player, card_index):
    game["discard"].append(game["hands"][player][card_index])
    game["nb_blue_stone"] = min(game["nb_blue_stone"] + 1, MAX_BLUE_STONE)
    game["hands"][player][card_index] = game["draw"].pop()


def play_card_on_game(game, player, card_index):
    i = COLOR.index(card[0])
    if len(game["firework"][i]) == int(card[1]) - 1:
        game["firework"][i].append(card)
    else:
        game["nb_red_stone"] = game["nb_red_stone"] - 1
        if game["nb_red_stone"] < 0:
            raise "Game over, too many errors"
    game["hands"][player][card_index] = game["draw"].pop()


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

def draw(game, player, num_card = 1):
    for i in range(num_card):
        game["hands"][player].append(game["draw"].pop())

def init_hanabi(num_players):
    """play a game of hanabi"""
    import copy
    game = copy.deepcopy(START_GAME)
    random.shuffle(game["draw"])
    game["hands"] = [[] for i in range(num_players)]
    for i in range(num_players):
        draw(game, i, num_card = CARD_IN_HANDS)
    return game


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
