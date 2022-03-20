import typing as t
from dataclasses import dataclass as dc


def main():
    cards = CardFactory.from_json('card-list.json')
    for c in cards:
        print(c)


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
        if cls.is_unitcard(d):
            return UnitCard.from_dict(d)
        else:
            return Card.from_dict(d)

    @staticmethod
    def is_unitcard(d):
        return "level" in d


@dc
class Card:
    id: int
    name: str
    support: str

    @staticmethod
    def from_dict(d: dict):
        return Card(**d)


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
        for attack in ('c_attack', 't_attack', 'x_attack'):
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
        return 'effect' in d


@dc
class Attack:
    name: str
    damage: int


@dc
class EffectAttack(Attack):
    effect: str = None


if __name__ == '__main__':
    main()
