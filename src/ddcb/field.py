import random
import typing as t

from ddcb.card import Card, CardList, UnitCard

MAX_HAND_SIZE = 4

type CardOrName = Card | str
type UnitOrName = UnitCard | str


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
        deck_count = len(self.deck)
        draw_count = min(count, deck_count)

        if draw_count < count:
            print(f"Unable to draw {count} cards, since deck has {deck_count} cards.")
            print(f"Drawing {draw_count} cards instead.")

        for _ in range(draw_count):
            card = self.deck.draw()
            self.hand.append(card)

    def draw_til_full(self):
        self.draw(MAX_HAND_SIZE - len(self.hand))

    def discard(self, index=0):
        card = self.hand.pop(index)
        self.discard_pile.append(card)

    def discard_hand(self):
        for _ in range(len(self.hand)):
            self.discard()

    def play_unit(self, unit: UnitOrName):
        unit_card = self.pop_unit_from_hand(unit)
        self.unit = unit_card

    def discard_unit(self):
        if self.unit is None:
            raise Exception("Tried to discard unit, but there isn't one.")
        self.discard_pile.append(self.unit)
        self.unit = None

    def has_unit_in_hand(self):
        return any((isinstance(card, UnitCard) for card in self.hand))

    def get_units_in_hand(self):
        return [card for card in self.hand if isinstance(card, UnitCard)]

    def has_unit(self):
        return bool(self.unit)

    def boost_dp(self, unit: UnitOrName):
        unit_card = self.pop_unit_from_hand(unit)
        self.dp.push(unit_card)

    def get_evolution_targets(self):
        if not self.unit:
            raise Exception("No unit active when checking evolution targets.")

        units_in_hand = self.get_units_in_hand()
        target_levels = self.unit.level.evolution_targets()
        return [unit for unit in units_in_hand if unit.level in target_levels]

    def evolve_unit(self, unit: UnitOrName):
        unit_card = self.pop_unit_from_hand(unit)

        if self.unit is None:
            raise Exception("Can't evolve without a unit!")

        prev_unit_health = self.unit.hp
        self.discard_unit()
        self.unit = unit_card
        self.unit.hp = max(self.unit.hp, prev_unit_health)

    def pop_unit_from_hand(self, unit: UnitOrName) -> UnitCard:
        card = self.pop_card_from_hand(unit)
        if isinstance(card, UnitCard):
            return card
        else:
            raise Exception(f"f{card.name} is not a Unit!")

    def pop_card_from_hand(self, card: CardOrName):
        i = Card.find_index(self.hand, card)
        if i is None:
            raise Exception(
                f"Card named {card if isinstance(card, str) else card.name} not found!"
            )
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

    def is_empty(self):
        return len(self.cards) < 1

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

    def __len__(self):
        return len(self.cards)


if __name__ == "__main__":
    main()
