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
    game = hs.init_hanabi(4)
    assert(len(game["draw"]) == 30)
    assert(game["draw"] != hs.START_GAME["draw"])
    assert(len(game["hands"]) == 4)
    for i in game["hands"]:
        assert(len(i) == hs.CARD_IN_HANDS)
    
def test_action_on_game():
    """Test the different possible action on the game"""
    game = hs.init_hanabi(4)
    assert(game["nb_blue_stone"] == 9)
    hs.discard_on_game(game,0,0)
    #nb of blue stone cannot exceed 9
    assert(game["nb_blue_stone"] == 9)
    hs.reveal_on_game(game)
    assert(game["nb_blue_stone"] == 8)
