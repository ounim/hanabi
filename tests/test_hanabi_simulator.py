#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_hanabi_simulator
----------------------------------

Tests for `hanabi_simulator` module.
"""

import pytest


from hanabi_simulator import hanabi_simulator


@pytest.fixture
def init_game():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """


def test_init():
    """Sample pytest test function with the pytest fixture as an argument.
    """
    game = hanabi_simulator.init_hanabi(4)
    assert(len(game["draw"]) == 30)
    assert(game["draw"] != hanabi_simulator.START_GAME["draw"])
    assert(len(game["hands"]) == 4)
    for i in game["hands"]:
        assert(len(i) == hanabi_simulator.CARD_IN_HANDS)
    
