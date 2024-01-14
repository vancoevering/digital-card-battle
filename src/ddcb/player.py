from dataclasses import dataclass, field as dc_field
from ddcb.base_controller import BaseController

from ddcb.field import Deck, Field


@dataclass
class Player:
    name: str
    deck: Deck
    controller: BaseController

    field: Field = dc_field(init=False)

    def new_field(self):
        self.field = Field(self.deck)
