import typing as t
from dataclasses import dataclass as dc

from ddcb import PKG_DATA

DEF_CARD_LIST_FILE = PKG_DATA / "card-list.json"


def main():
    # CardList.load_from_json(PKG_DATA / "card-list.json")
    # for c in CardList.cards:
    #     print(c)
    # print(CardList.get_card("gabumon"))

    singleton = CardList()
    # for c in singleton.cards:
    #     print(c)
    print(singleton.get_card("gabumon"))

    singleton2 = CardList()
    # for c in singleton2.cards:
    #     print(c)
    print(singleton2.get_card("agumon"))


# class CardList:
#     cards: t.Dict[str, "Card"] = {}

#     @classmethod
#     def load_from_json(cls, path):
#         cls.load(CardFactory.from_json(path))

#     @classmethod
#     def load(cls, cards: t.Iterable["Card"]):
#         cls.cards = {card.name.lower(): card for card in cards}

#     @classmethod
#     def get_card(cls, name: str):
#         return cls.cards[name.lower()]

#     @classmethod
#     def get_cards(cls, names: t.Iterable[str]):
#         return [cls.get_card(c) for c in names]


class CardList:
    _instance = None

    def __new__(cls, path=DEF_CARD_LIST_FILE):
        if not cls._instance:
            print("Creating new instance...")
            cls._instance = super().__new__(cls)
            cls._instance.load_from_json(path)
        return cls._instance

    def load_from_json(self, path):
        self.load(CardFactory.from_json(path))

    def load(self, cards: t.Iterable["Card"]):
        self.cards = {card.name.lower(): card for card in cards}

    def get_card(self, name: str):
        return self.cards[name.lower()]

    def get_cards(self, names: t.Iterable[str]):
        return [self.get_card(c) for c in names]


class CardFactory:
    @classmethod
    def from_json(cls, path):
        import json

        with open(path, "r") as fp:
            cards = json.load(fp)
        yield from cls.from_dicts(cards)

    @classmethod
    def from_dicts(cls, dicts: t.Iterable[dict]):
        for d in dicts:
            yield cls.from_dict(d)

    @classmethod
    def from_dict(cls, d):
        if cls._is_unitcard(d):
            return UnitCard.from_dict(d)
        else:
            return Card.from_dict(d)

    @staticmethod
    def _is_unitcard(d):
        return "level" in d


@dc
class Card:
    id: int
    name: str
    support: str

    @staticmethod
    def from_dict(d: dict):
        return Card(**d)

    @staticmethod
    def find_index(cards: t.Iterable["Card"], card: t.Union["Card", str]):
        if isinstance(card, str):
            return Card.find_index_by_name(cards, card)
        for i, _card in enumerate(cards):
            if _card is card:
                return i

    @staticmethod
    def find_index_by_name(cards: t.Iterable["Card"], name: str):
        for i, card in enumerate(cards):
            if card.name == name:
                return i


@dc
class UnitCard(Card):
    level: str
    specialty: str
    hp: int
    dp: int
    pp: int
    c_attack: "Attack"
    t_attack: "Attack"
    x_attack: "EffectAttack"

    C_STR: t.ClassVar[str] = "[C]"
    T_STR: t.ClassVar[str] = "[T]"
    X_STR: t.ClassVar[str] = "[X]"

    @staticmethod
    def from_dict(d: dict):
        d = d.copy()
        for attack in ("c_attack", "t_attack", "x_attack"):
            d[attack] = AttackFactory.from_dict(d[attack])

        return UnitCard(**d)


class AttackFactory:
    @classmethod
    def from_dict(cls, d: dict):
        if cls.is_effect_attack(d):
            return EffectAttack(**d)
        else:
            return Attack(**d)

    @staticmethod
    def is_effect_attack(d: dict):
        return "effect" in d


@dc
class Attack:
    name: str
    damage: int


@dc
class EffectAttack(Attack):
    effect: t.Optional[str] = None


if __name__ == "__main__":
    main()
