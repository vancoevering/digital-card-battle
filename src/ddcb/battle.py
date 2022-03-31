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
        # - Boost DP [opt]
        #   > (choose unit from hand to add to DPStack)
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
        choice = self.controller.choose(["keep hand", "mulligan"])
        return choice == "keep hand"

    def _discard_hand(self):
        self.field.discard_hand()

    def _has_unit(self):
        return bool(self.field.unit)

    def _play_unit(self):
        units = [card for card in self.field.hand if isinstance(card, UnitCard)]
        if units:
            unit = self._choose_unit(units)
            self.field.unit = unit
        else:
            raise Exception("Battler can't play a UNIT!")

    def _choose_unit(self, units: list):
        return self.controller.choose(units)


class BaseController:
    @staticmethod
    def choose(options: list):
        return options[0]


if __name__ == '__main__':
    main()
