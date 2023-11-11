import random
from dataclasses import dataclass
from dataclasses import field as dc_field
from itertools import cycle

from ddcb.base_controller import BaseController, ConfirmHandResponse
from ddcb.field import Deck
from ddcb.player import Player
from ddcb.turn import Turn, TurnResult


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
    print("Battle: ", Battle(player_one, player_two).battle())


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
            result = turn.do()
            if result != TurnResult.CONTINUE:
                return result


if __name__ == "__main__":
    main()
    print("battle_redux complete!")
