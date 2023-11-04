import random

from dataclasses import dataclass, field as dc_field
from field import Field, Deck
from base_controller import BaseController


def main():
    player_one = Player(
        name="Yugi", deck=Deck.from_random(), controller=BaseController()
    )
    player_two = Player(
        name="Kaiba",
        deck=Deck.from_random(),
        controller=BaseController(),
    )
    Battle(player_one, player_two)


@dataclass
class Player:
    name: str
    deck: Deck
    controller: BaseController

    field: Field = dc_field(init=False)

    def new_field(self):
        self.field = Field(self.deck)


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
        turn_order = [self.player_one, self.player_two]
        random.shuffle(turn_order)
        return turn_order

    def do_battle_loop(self, turn_order: list[Player]):
        self.turn = 1
        while self.turn < 1000:
            player = turn_order[self.turn % 2]
            opponent = turn_order[(self.turn + 1) % 2]
            print(player.name)
            result = self.do_turn(player, opponent)
            if result:
                return result

    def do_turn(self, player, opponent):
        raise NotImplementedError


if __name__ == "__main__":
    main()
    print("battle_redux complete!")
