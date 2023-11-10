import random
from itertools import cycle
from enum import Enum
from collections.abc import Callable

from dataclasses import dataclass, field as dc_field
from ddcb.field import Field, Deck
from ddcb.base_controller import BaseController, ConfirmHandResponse


def main():
    player_one = Player(
        name="Yugi Moto",
        deck=Deck.from_random(),
        controller=BaseController(),
    )
    player_two = Player(
        name="Seto Kaiba",
        deck=Deck.from_random(),
        controller=BaseController(),
    )
    Battle(player_one, player_two).battle()


@dataclass
class Player:
    name: str
    deck: Deck
    controller: BaseController

    field: Field = dc_field(init=False)

    def new_field(self):
        self.field = Field(self.deck)


class TurnResult(Enum):
    CONTINUE = 0
    NO_UNIT = 1

type Phases = list[Callable[[], TurnResult]]

@dataclass
class Turn:
    # TODO: Let's find a better name for this class
    player: Player
    opponent: Player

    def do_turn(self) -> TurnResult:
        # TODO: add each of the turn phases
        phases: Phases = [
            self.do_prep_phase,
        ]
        return self.do_phases(phases)
    
    def do_phases(self, phases: Phases):
        for phase in phases:
            result = phase()
            if result != TurnResult.CONTINUE:
                return result
        return TurnResult.CONTINUE


    def do_prep_phase(self) -> TurnResult:
        subphases: Phases = [self.do_prep_draw_cards, self.do_prep_play_unit]
        return self.do_phases(subphases)

    def do_prep_draw_cards(self):
        self.player.field.draw_til_full()
        return self.do_prep_confirm_hand()
    
    # def do_prep_confirm_hand_3(self) -> TurnResult:
    #     if not self.player.field.has_unit():
    #         if self.player.deck.is_empty():
    #             return TurnResult.NO_UNIT
    #         return self.do_prep_mulligan()
        
    #     if not self.player.deck.is_empty():
    #         choice = self.player.controller.confirm_hand()
    #         if choice == ConfirmHandResponse.MULLIGAN:
    #             return self.do_prep_mulligan()
        
    #     return TurnResult.CONTINUE
    
    def do_prep_confirm_hand(self) -> TurnResult:
        if self.player.deck.is_empty():
            if not self.player.field.has_unit():
                print("Deck empty and no unit!")
                return TurnResult.NO_UNIT
            print("Deck empty: Auto-confirm hand")
            return TurnResult.CONTINUE
        
        if not self.player.field.has_unit():
            # Auto-mulligan
            return self.do_prep_mulligan()
        
        choice = self.player.controller.confirm_hand()
        if choice == ConfirmHandResponse.MULLIGAN:
            return self.do_prep_mulligan()
        
        return TurnResult.CONTINUE


    # def do_prep_confirm_hand(self):
    #     if self.player.deck.is_empty():
    #         print(f"{self.player.name}'s deck is empty. Hand kept by default.")
    #         return

    #     choice = self.player.controller.confirm_hand()
    #     if choice == ConfirmHandResponse.MULLIGAN:
    #         self.do_prep_mulligan()

    def do_prep_mulligan(self):
        self.player.field.discard_hand()
        return self.do_prep_draw_cards()

    def do_prep_play_unit(self):
        if self.player.field.has_unit():
            print(f"{self.player.name} already has a unit in play.")
            return TurnResult.CONTINUE

        choice = self.player.controller.choose_unit()
        # TODO: Would we EVER let a player choose NO?
        # TODO: Should player always have at least one unit in hand at this step?
        if choice is None:
            return TurnResult.NO_UNIT
        self.player.field.play_unit(choice)
        return TurnResult.CONTINUE

    def do_prep_play_unit_2(self):
        if not self.player.field.has_unit():
            choice = self.player.controller.choose_unit()
            if choice is None:
                return TurnResult.NO_UNIT
            self.player.field.play_unit(choice)
        else:
            print(f"{self.player.name} already has a unit in play.")
        return TurnResult.CONTINUE


@dataclass
class Battle:
    player_one: Player
    player_two: Player

    turn: int = dc_field(init=False)

    def battle(self):
        self.create_fields()
        turn_order = self.decide_turn_order()
        return self.do_battle_loop(turn_order)

    def create_fields(self):
        self.player_one.new_field()
        self.player_two.new_field()

    def decide_turn_order(self):
        turn_order = [
            Turn(player=self.player_one, opponent=self.player_two),
            Turn(player=self.player_two, opponent=self.player_one),
        ]
        random.shuffle(turn_order)
        return cycle(turn_order)

    def do_battle_loop(self, turn_order):
        self.turn = 0
        while self.turn < 6:
            self.turn += 1
            turn: Turn = next(turn_order)
            print(turn.player.name, f"Turn {self.turn}")
            result = turn.do_turn()
            if result:
                return result


if __name__ == "__main__":
    main()
    print("battle_redux complete!")
