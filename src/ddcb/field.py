import random
import typing as t

from ddcb import PKG_DATA
from ddcb.card import Card, CardList, UnitCard


def main():
    deck = Deck.from_random()
    for c in deck.cards:
        print(c.name)
    field = Field(deck)
    print(field)


class Field:
    def __init__(self, deck: "Deck"):
        self.deck: Deck = deck
        self.hand: t.List[Card] = []
        self.discard_pile: t.List[Card] = []

        self.unit: t.Optional[UnitCard] = None
        self.dp: "DPStack" = DPStack()

    def reset(self):
        self.deck.reset()
        self.hand = []
        self.discard_pile = []

        self.unit = None
        self.dp = DPStack()

    def draw(self, count=1):
        for i in range(count):
            card = self.deck.draw()
            self.hand.append(card)

    def discard(self, index=0):
        card = self.hand.pop(index)
        self.discard_pile.append(card)

    def discard_hand(self):
        for _ in range(len(self.hand)):
            self.discard()

    def play_unit(self, unit_name):
        unit_card = self.pop_unit_from_hand(unit_name)
        self.unit = unit_card

    def get_units_in_hand(self):
        return [card for card in self.hand if isinstance(card, UnitCard)]

    def has_unit(self):
        return bool(self.unit)

    def boost_dp(self, unit_name):
        unit_card = self.pop_unit_from_hand(unit_name)
        self.dp.push(unit_card)

    def pop_unit_from_hand(self, name) -> UnitCard:
        card = self.pop_card_from_hand(name)
        if isinstance(card, UnitCard):
            # noinspection PyTypeChecker
            return card
        else:
            raise Exception(f"f{card.name} is not a Unit!")

    def pop_card_from_hand(self, name):
        i = Card.find_index_by_name(self.hand, name)
        if i is None:
            raise Exception(f"Card named {name} not found!")
        return self.hand.pop(i)


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
    SIZE = 30

    def __init__(self, cards: t.List[Card]):
        self.cards = cards.copy()
        self.decklist = [c.name for c in cards]

    def reset(self):
        self.__init__(CardList().get_cards(self.decklist))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    @staticmethod
    def from_random():
        cards = random.sample(list(CardList().cards.keys()), Deck.SIZE)
        return Deck.from_names(cards)

    @staticmethod
    def from_json(path):
        import json

        with open(path, "r") as fp:
            names = json.load(fp)
        return Deck.from_names(names)

    @staticmethod
    def from_names(names: t.List[str]):
        cards = CardList().get_cards(names)
        return Deck(cards)


if __name__ == "__main__":
    main()
