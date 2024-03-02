from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import Optional

from cards import Suit, Rank, Card, CardStack


class Game:
    """ Игра в девятку """

    def __init__(self, players: list[Player], deck_52: bool = True) -> None:
        self._deck_52 = deck_52  # Размер колоды для игры
        self._players = players
        self._table = GameTable(deck_52=deck_52)
        self._turn_idx = 0  # Кого ход

    def _get_available_moves(self, player: Player) -> list[Card]:
        """ Возможные ходы для игрока в данный момент """
        moves = []
        for card in player.hand:
            if card.rank == Rank.NINE:
                moves.append(card)
            elif card.rank < Rank.NINE:
                if self._table.is_card_exist(Card(card.suit, card.rank + 1)):
                    moves.append(card)
            elif card.rank > Rank.NINE:
                if self._table.is_card_exist(Card(card.suit, card.rank - 1)):
                    moves.append(card)
        return moves

    def play(self) -> Player:
        """ Разыграть 1 партию. Вернуть победителя """

        # Очистить игровое поле
        self._table.clear()

        # Раздать карты игрокам
        deck = CardStack.deck_of_52() if self._deck_52 else CardStack.deck_of_36()
        deck.shuffle()
        stacks = deck.divide(len(self._players))
        random.shuffle(stacks)  # Потому что stacks меньшего размера всегда в конце
        for player, stack in zip(self._players, stacks):
            player.hand = stack

        # Выяснить кто ходит первым
        for idx, player in enumerate(self._players):
            if Card(Suit.DIAMONDS, Rank.NINE) in player.hand:
                self._turn_idx = idx

        # Собственно, игра
        while True:
            player = self._players[self._turn_idx]
            moves = self._get_available_moves(player)
            card = player.choose_move(moves, self._table)
            if card:
                player.hand.remove(card)
                self._table.put_card(card)
            if not len(player.hand):
                winner = player
                break
            self._turn_idx = (self._turn_idx + 1) % len(self._players)

        winner.win_count += 1
        return winner


class GameTable:
    """ Игровое поле """

    def __init__(self, deck_52: bool = True) -> None:
        self._deck_52 = deck_52  # Размер колоды для игры
        self._cells: list[list[Optional[Card]]] = ...  # Места под карты
        self.clear()

    def clear(self) -> None:
        """ Очистить поле """
        deck_size = 52 if self._deck_52 else 36
        row_size = int(deck_size / 4)
        self._cells = [
            [None for _ in range(row_size)],
            [None for _ in range(row_size)],
            [None for _ in range(row_size)],
            [None for _ in range(row_size)]
        ]

    def _get_card_place(self, card: Card) -> (int, int):
        """ Координаты карты на игровом поле """
        row = card.suit - 1
        column = (card.rank - 2) if self._deck_52 else (card.rank - 6)
        return row, column

    def put_card(self, card: Card) -> None:
        """ Положить карту на ее место """
        row, column = self._get_card_place(card)
        self._cells[row][column] = card

    def is_card_exist(self, card: Card) -> bool:
        """ Проверить есть ли карта на поле """
        row, column = self._get_card_place(card)
        return bool(self._cells[row][column])

    def corresponding_range(self, card: Card) -> (Card, Card):
        """ Наименьшая и наибольшая карта такой же масти на поле в данный момент """
        row, _ = self._get_card_place(card)
        cards = self._cells[row]
        left = right = None
        for card in cards:
            if card:
                left = card
                break
        for card in cards[::-1]:
            if card:
                right = card
                break
        return left, right


class Player:
    """ Игрок """

    def __init__(self, strategy: Strategy):
        self.hand: Optional[CardStack] = None
        self.win_count = 0  # Количество побед
        self.strategy = strategy

    def choose_move(self, moves: list[Card], table: GameTable) -> Optional[Card]:
        """ Выбрать какой картой походить """
        if not moves:
            return None
        return self.strategy.choose_move(moves, table, self.hand)


class Strategy(ABC):
    """ Стратегия игрока """

    @abstractmethod
    def choose_move(self, moves: list[Card], table: GameTable, hand: CardStack) -> Card:
        """ Выбрать лучший ход """
        ...


class SimpleStrategy(Strategy):
    """ Простейшая стратегия - выбрать случайный ход из возможных """

    def __str__(self) -> str:
        return "Simple strategy"

    def choose_move(self, moves: list[Card], table: GameTable, hand: CardStack) -> Card:
        """ Выбрать лучший ход """
        return random.choice(moves)


class AdvancedStrategy(Strategy):
    """ Сложная стратегия """

    def __str__(self) -> str:
        return "Advanced strategy"

    def choose_move(self, moves: list[Card], table: GameTable, hand: CardStack) -> Card:
        """ Выбрать лучший ход """

        # Вытащить самые дальние карты вперед руки
        hand.sort(key=lambda x: self._get_distance(x, table), reverse=True)

        # Выбрать возможный ход для как можно более дальней карты
        for card in hand:
            wanted_move = self._get_wanted_move(card, table)
            for move in moves:
                if move == wanted_move:
                    return move

    @staticmethod
    def _get_distance(card: Card, table: GameTable) -> int:
        """ Расстояние от этой карты до ближайшей на поле """
        left, right = table.corresponding_range(card)
        if left:
            if card.rank < left.rank:
                return left.rank - card.rank
            else:
                return card.rank - right.rank
        else:
            if card.rank < Rank.NINE:
                return Rank.NINE - card.rank + 1
            else:
                return card.rank - Rank.NINE + 1

    @staticmethod
    def _get_wanted_move(card: Card, table: GameTable) -> Card:
        """ Следующий ход в игре, который уменьшит расстояние для этой карты """
        left, right = table.corresponding_range(card)
        if not left:
            return Card(card.suit, Rank.NINE)
        else:
            if card.rank < left.rank:
                return Card(card.suit, left.rank - 1)
            else:
                return Card(card.suit, right.rank + 1)
