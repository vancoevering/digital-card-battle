import random
from enum import Enum
import typing as t

from ddcb import PKG_DATA
from ddcb.card import CardList, Attack
from ddcb.field import Field, Deck

T = t.TypeVar("T")


def main():
    CardList.load_from_json(PKG_DATA / "card-list.json")

    player_one = Battler(
        field=Field(Deck.from_random()),
        controller=BaseController(),
    )
    player_two = Battler(
        field=Field(deck=Deck.from_random()),
        controller=BaseController(),
    )
    result = player_one.battle(player_two)
    print(f"Result: player one {result.name}")


class Battler:
    def __init__(self, field: Field, controller: "BaseController"):
        self.field = field
        self.controller = controller

    def battle(self, opponent: "Battler", has_first_turn=True) -> "BattleResult":
        self._setup_field()
        opponent._setup_field()

        return self._battle_loop(opponent, has_first_turn)

    def _setup_field(self):
        self.field.reset()
        self.field.deck.shuffle()

    def _battle_loop(self, opponent: "Battler", is_own_turn: bool) -> "BattleResult":
        while True:
            if is_own_turn:
                result = self.do_turn(opponent)
                if result is not None:
                    return result
            else:
                result = opponent.do_turn(self)
                if result is not None:
                    return result.flip()

            is_own_turn = not is_own_turn

    def do_turn(self, opponent: "Battler") -> t.Optional["BattleResult"]:
        for phase in (self.do_prep_phase, self.do_upgrade_phase):
            result = phase() or None
            if result is not None:
                return result

        result = self.do_battle_phase(opponent)
        return result

    def do_prep_phase(self):
        # Prep Phase
        while True:
            # - Draw Cards:hand fills to 4
            # likely need to catch a deck empty exception here
            self._draw_til_full()

            #   > (Confirm: next / Mulligan:new cards)
            # if self._confirm_draw():
            if self.controller.prep_confirm_draw():
                break
            else:
                self._discard_hand()

        # - Play Unit, if no unit
        #   > (choose unit from hand):if no unit, loss
        if not self._has_unit():
            self._play_unit()

    def do_upgrade_phase(self):
        # Upgrade Phase

        self._boost_dp()
        # - Play Upgrade [opt]
        #   > (choose upgrade card from hand to play)
        pass

    def do_battle_phase(self, opponent: "Battler") -> t.Optional["BattleResult"]:
        print("---")
        if not opponent._has_unit():
            return None

        # Battle Phase, if opponent has an active unit
        # - Player choose attack (o, t, x) AND opponent choose attack (o, t, x)
        battler_attack = self._choose_attack()
        opponent_attack = opponent._choose_attack()

        # - Opponent choose support (card from hand OR top deck) [opt]
        # - Player choose support (card from hand OR top deck) [opt]
        # opponent_support = opponent._choose_card_or_gamble_opt()
        # battler_support = self._choose_card_or_gamble_opt()
        opponent_support = opponent.controller.battle_choose_support_or_gamble()
        battler_support = self.controller.battle_choose_support_or_gamble()

        # - Apply player support
        # - Apply opponent support
        pass

        print(f"own hp: {self.get_hp()}")
        print(f"opp hp: {opponent.get_hp()}")
        # - Apply player damage
        print(f"own attack: {battler_attack}")
        self._do_attack(battler_attack, opponent)
        print(f"opp hp: {opponent.get_hp()}")

        # - Apply opp damage
        if not opponent.unit_is_defeated():
            print(f"opponent attack: {opponent_attack}")
            opponent._do_attack(opponent_attack, self)
            print(f"own hp: {self.get_hp()}")

        if self.unit_is_defeated() and opponent.unit_is_defeated():
            print(
                f"Tie - own hp: {self.get_hp()} - is defeated: {self.unit_is_defeated()}"
            )
            print(
                f"Tie - opp hp: {opponent.get_hp()} - is defeated: {opponent.unit_is_defeated()}"
            )
            return BattleResult.Tie
        elif self.unit_is_defeated():
            return BattleResult.Loss
        elif opponent.unit_is_defeated():
            return BattleResult.Win
        else:
            return None

    @staticmethod
    def _do_attack(attack: Attack, opponent: "Battler"):
        opponent.set_hp(opponent.get_hp() - attack.damage)

    def _draw_til_full(self):
        self.field.draw(4 - len(self.field.hand))

    def _confirm_draw(self):
        choice = self._choose(["keep hand", "mulligan"])
        return choice == "keep hand"

    def _discard_hand(self):
        self.field.discard_hand()

    def _has_unit(self):
        return self.field.has_unit()

    def _play_unit(self):
        units = self.field.get_units_in_hand()
        if units:
            unit_name = self._choose(units).name
            self.field.play_unit(unit_name)
        else:
            raise Exception("Battler can't play a UNIT!")

    def _boost_dp(self):
        # - Boost DP [opt]
        #   > (choose unit from hand to add to DPStack)
        units = self.field.get_units_in_hand()
        if units:
            choice = self._choose_opt(units)
            if isinstance(choice, str) or choice is None:
                unit_name = choice
            else:
                unit_name = choice.name
            # unit_name = self._choose_opt(units)
            if unit_name:
                self.field.boost_dp(unit_name)

    def _choose(self, options: t.Sequence[T]) -> T:
        return self.controller.choose(options)

    def _choose_opt(self, options: t.Sequence[T]) -> T:
        options = list(options)
        options.append(None)
        return self._choose(options)

    def _choose_attack(self):
        options: t.List[Attack] = [
            self.field.unit.c_attack,
            self.field.unit.t_attack,
            self.field.unit.x_attack,
        ]
        return self._choose(options)

    def get_hp(self):
        return self.field.unit.hp

    def set_hp(self, value: int):
        self.field.unit.hp = value

    def unit_is_defeated(self):
        return self.get_hp() <= 0


class BattleResult(Enum):
    Win = 1
    Loss = 2
    Tie = 3

    def flip(self):
        if self.value == BattleResult.Win:
            return BattleResult.Loss
        if self.value == BattleResult.Loss:
            return BattleResult.Win
        if self.value == BattleResult.Tie:
            return BattleResult.Tie
        return self


class BaseController:
    @staticmethod
    def prep_confirm_draw() -> bool:
        return True

    @staticmethod
    def battle_choose_support_or_gamble() -> dict:
        return {"gamble": True}

    @staticmethod
    def choose(options: t.Sequence[T]) -> T:
        return options[0]


class RandomController(BaseController):
    @staticmethod
    def choose(options: t.Sequence[str]):
        return random.choice(options)


if __name__ == "__main__":
    main()
