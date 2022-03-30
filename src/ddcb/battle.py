from dataclasses import dataclass as dc

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
        # - Draw Cards:hand fills to 4
        #   > (Confirm:next / View:loop / Mulligan:new cards)
        # - Play Unit, if no unit
        #   > (choose unit from hand):if no unit, loss
        pass

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


class BaseController:
    pass


if __name__ == '__main__':
    main()
