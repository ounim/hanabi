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
    assert(game.nb_blue_stone == 9)
    game.discard_card(0,0)
    assert(len(game.draw) == 29)
    assert(len(game.discard) == 1)
    #nb of blue stone cannot exceed 9
    assert(game.nb_blue_stone == 9)
    game.reveal()
    assert(len(game.draw) == 29)
    assert(game.nb_blue_stone == 8)
    for i in range(8):
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
