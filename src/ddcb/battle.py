import random
import typing as t
from dataclasses import dataclass as dc

from .card import UnitCard
from .field import Field


def main():
    pass


@dc
class Battler:
    field: Field
    controller: "BaseController"

    def do_turn(self, opponent: "Battler"):
        self.do_prep_phase()
        self.do_upgrade_phase()
        self.do_battle_phase(opponent)

    def do_prep_phase(self):
        # Prep Phase
        while True:
            # - Draw Cards:hand fills to 4
            # likely need to catch a deck empty exception here
            self._draw_til_full()

            #   > (Confirm: next / Mulligan:new cards)
            if self._confirm_draw():
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

    def do_battle_phase(self, opponent: "Battler"):
        # Battle Phase, if opponent has an active unit
        # - Player choose attack (o, t, x) AND opponent choose attack (o, t, x)
        # - Opponent choose support (card from hand OR top deck) [opt]
        # - Player choose support (card from hand OR top deck) [opt]
        # - Apply player support
        # - Apply opponent support
        # - Apply player damage
        # - Apply opponent damage
        pass

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
            unit_name = self._choose(units)
            self.field.play_unit(unit_name)
        else:
            raise Exception("Battler can't play a UNIT!")

    def _boost_dp(self):
        # - Boost DP [opt]
        #   > (choose unit from hand to add to DPStack)
        units = self.field.get_units_in_hand()
        if units:
            unit_name = self._choose_opt(units)
            if unit_name:
                self.field.boost_dp(unit_name)

    def _choose(self, options: t.Sequence[str]):
        return self.controller.choose(options)

    def _choose_opt(self, options: t.Sequence[str]):
        options = list(options) + ["No Selection"]
        return self._choose(options)


class BaseController:
    @staticmethod
    def choose(options: t.Sequence[str]):
        return options[0]


class RandomController(BaseController):
    @staticmethod
    def choose(options: t.Sequence[str]):
        return random.choice(options)


if __name__ == '__main__':
    main()
