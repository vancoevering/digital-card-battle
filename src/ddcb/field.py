import random
import typing as t

from . import PKG_ROOT
from .card import Card, UnitCard, CardList, CardFactory


def main():
    cards = CardFactory.from_json(PKG_ROOT / 'card-list.json')
    CardList.load(cards)

    deck = Deck.from_json(PKG_ROOT / "tutorial-deck.json")
    for c in deck.cards:
        print(c)
    field = Field(deck)
    print(field)


class Field:

    def __init__(self, deck: "Deck"):
        self.deck: Deck = deck
        self.hand: t.List[Card] = []
        self.discard: t.List[Card] = []

        self.unit: t.Optional[UnitCard] = None
        self.dp: "DPStack" = DPStack()


class DPStack:
    def __init__(self):
        self.stack: t.List[UnitCard] = []

    def get_value(self) -> int:
        value = 0
        for unit in self.stack:
            value = value + unit.pp
        return value

    def push(self, unit: UnitCard):
        self.stack.append(unit)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]


class Deck:
    def __init__(self, cards: t.List[Card]):
        self.cards = cards.copy()

    def shuffle(self):
        random.shuffle(self.cards)

    @classmethod
    def from_json(cls, path):
        import json
        with open(path, "r") as fp:
            names = json.load(fp)
        return cls.from_names(names)

    @staticmethod
    def from_names(names: t.List[str]):
        cards = [CardList.get(name) for name in names]
        return Deck(cards)


if __name__ == '__main__':
    main()
