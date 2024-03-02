from __future__ import annotations

import itertools
import random
from collections import UserList
from dataclasses import dataclass
from enum import IntEnum, auto

import more_itertools


class Suit(IntEnum):
    """ Масти карт """
    SPADES = auto()
    HEARTS = auto()
    CLUBS = auto()
    DIAMONDS = auto()


class Rank(IntEnum):
    """ Достоинства карт """
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


@dataclass
class Card:
    """ Игральная карта """
    suit: Suit
    rank: Rank

    def __repr__(self) -> str:
        # Это почему-то не всегда работает
        # rank_name = self.rank.name.capitalize()
        # suit_name = self.suit.name.capitalize()
        rank_name = [x for x in Rank if x.value == self.rank][0].name.capitalize()
        suit_name = [x for x in Suit if x.value == self.suit][0].name.capitalize()
        return f"{rank_name} of {suit_name}"


class CardStack(UserList):
    """ Стопка карт """

    @classmethod
    def deck_of_36(cls) -> CardStack:
        """ Колода из 36 карт """
        suits = list(Suit)
        ranks = [r for r in Rank if r >= Rank.SIX]
        cards = [Card(*params) for params in (itertools.product(suits, ranks))]
        return CardStack(cards)

    @classmethod
    def deck_of_52(cls) -> CardStack:
        """ Колода из 52 карт """
        suits = list(Suit)
        ranks = list(Rank)
        cards = [Card(*params) for params in (itertools.product(suits, ranks))]
        return CardStack(cards)

    def shuffle(self) -> None:
        """ Перетасовать """
        random.shuffle(self.data)

    def divide(self, n: int) -> list[CardStack]:
        """ Разделить на n последовательных стопок """
        return [CardStack(list(cards)) for cards in more_itertools.divide(n, self.data)]
