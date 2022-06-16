import random
import typing as t
from dataclasses import dataclass as dc

from ddcb import PKG_DATA
from ddcb.card import CardList
from ddcb.field import Field, Deck


def main():
    CardList.load_from_json(PKG_DATA / "card-list.json")

    player_one = Battler(
        field=Field(Deck.from_json(PKG_DATA / "tutorial-deck.json")),
        controller=RandomController()
    )
    player_two = Battler(
        field=Field(Deck.from_json(PKG_DATA / "go-go-dinosaur-deck.json")),
        controller=RandomController()
    )
    player_one.battle(player_two)
    pass


@dc
class Battler:
    field: Field
    controller: "BaseController"

    def battle(self, opponent: "Battler", has_first_turn=True):
        is_battler_turn = has_first_turn
        winner = None

        self.shuffle()
        opponent.shuffle()
        while winner is None:
            if is_battler_turn:
                winner = self.do_turn(opponent)
                is_battler_turn = False
            else:
                winner = opponent.do_turn(self)
                is_battler_turn = True

    def do_turn(self, opponent: "Battler"):
        winner = None
        for phase in (self.do_prep_phase, self.do_upgrade_phase):
            winner = phase() or None
            if winner is not None:
                return winner

        winner = self.do_battle_phase(opponent)
        return winner

    @staticmethod
    def _not(bool_or_none):
        return (not bool_or_none) if (bool_or_none is not None) else None

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
        if not opponent._has_unit():
            return None

        # Battle Phase, if opponent has an active unit
        # - Player choose attack (o, t, x) AND opponent choose attack (o, t, x)
        battler_attack = self._choose_attack()
        opponent_attack = opponent._choose_attack()

        # - Opponent choose support (card from hand OR top deck) [opt]
        # - Player choose support (card from hand OR top deck) [opt]
        opponent_support = opponent._choose_card_or_gamble_opt()
        battler_support = self._choose_card_or_gamble_opt()

        # - Apply player support
        # - Apply opponent support
        pass

        # - Apply player damage
        # - Apply opponent damage
        print(battler_attack)
        print(opponent_attack)
        return None
        pass

    def shuffle(self):
        self.field.deck.shuffle()

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

    def _choose(self, options: t.Sequence[str]):
        return self.controller.choose(options)

    def _choose_opt(self, options: t.Sequence[str]):
        options = list(options) + ["No Selection"]
        return self._choose(options)

    def _choose_attack(self):
        options = [
            self.field.unit.C_STR,
            self.field.unit.T_STR,
            self.field.unit.X_STR
        ]
        return self._choose(options)

    def _choose_card(self):
        options = [card.name for card in self.field.hand]
        return self._choose(options)

    def _choose_card_or_gamble_opt(self):
        options = [card.name for card in self.field.hand] + ["All or nothing!"]
        return self._choose_opt(options)


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
