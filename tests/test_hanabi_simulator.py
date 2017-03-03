#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_hanabi_simulator
----------------------------------

Tests for `hanabi_simulator` module.
"""

import pytest


import hanabi_simulator as hs


@pytest.fixture
def init_game():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """


def test_init():
    """Test that the initialisation of the game is good
    """
    game = hs.Game(4)
    assert(len(game.draw) == 30)
    assert(len(game.hands) == 4)
    assert(len(game.discard) == 0)
    for i in game.hands:
        assert(len(i) == hs.CARD_IN_HANDS)
    
def test_action_on_game():
    """Test the different possible action on the game"""
    game = hs.Game(4)
    assert(game.nb_blue_stone == hs.MAX_BLUE_STONE)
    game.discard_card(0,0)
    assert(len(game.draw) == 29)
    assert(len(game.discard) == 1)
    #nb of blue stone cannot exceed 9
    assert(game.nb_blue_stone == hs.MAX_BLUE_STONE)
    game.reveal()
    assert(len(game.draw) == 29)
    assert(game.nb_blue_stone == hs.MAX_BLUE_STONE - 1)
    for i in range(hs.MAX_BLUE_STONE -1):
        game.reveal()
    try:
       game.reveal()
       assert(False)
    except hs.InvalidActionError:
        pass

    #draw all the card
    for i in range(29):
        game.discard_card(0,0)
    
    game.discard_card(0,0)
    assert(game.hands[0][0] == hs.NO_CARD)

def test_firework_on_game():
    """test firework fill when the right card is played"""
    game = hs.Game(4)
    game.draw = [x + str(y) for x in hs.COLOR for y in hs.CARD_VALUE]
    game.draw.reverse()
    game.draw_initial_hands()

    assert(game.hands[0][0] == "R1")
    game.play_card(0,0)
    assert(game.hands[0][0] == "Y1")
    assert(game.firework[0] == ["R1"])
    assert(game.hands[2][0] == "G1")
    game.play_card(2,0)
    assert(game.hands[2][0] == "Y1")
    assert(game.firework[0] == ["R1"])
    assert(game.firework[1] == ["G1"])

    assert(game.hands[0][3] == "R2")
    game.play_card(0,3)
    assert(game.hands[0][3] == "Y1")
    assert(game.firework[0] == ["R1","R2"])

def test_error_on_game():
    """test error when the wrong card is played"""
    game = hs.Game(4)
    game.draw = [x + str(y) for x in hs.COLOR for y in hs.CARD_VALUE]
    game.draw.reverse()
    game.draw_initial_hands()
    assert(game.hands[0][4] == "R2")
    game.play_card(0,4)
    assert(game.nb_red_stone == 2)
    game.play_card(1,2)
    game.play_card(1,3)
    try:
        game.play_card(1,4)
        assert(False)
    except hs.GameOverError:
        pass

def test_extra_blue_stone_on_game():
    """test extra blue stone when a firework finish"""
    game = hs.Game(4)
    game.draw = [x + str(y) for x in hs.COLOR for y in hs.CARD_VALUE]
    game.draw.reverse()
    game.draw_initial_hands()
    game.reveal()
    assert(game.nb_blue_stone == hs.MAX_BLUE_STONE - 1)
    game.play_card(0,0)
    game.play_card(0,3)
    game.play_card(1,0)
    game.play_card(1,2)
    game.play_card(1,4)
    assert(game.nb_blue_stone == hs.MAX_BLUE_STONE)

def test_score_on_game():
    game = hs.Game(4)
    game.draw = [x + str(y) for x in hs.COLOR for y in hs.CARD_VALUE]
    game.draw.reverse()
    game.draw_initial_hands()
    assert(game.score() == 0)
    assert(game.hands[0][0] == "R1")
    game.play_card(0,0)
    assert(game.hands[0][0] == "Y1")
    assert(game.score() == 1)
    game.play_card(0,0)
    assert(game.score() == 2)
