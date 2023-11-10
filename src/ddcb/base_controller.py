from enum import Enum
import typing as t

from ddcb.card import CardList, UnitCard


class ConfirmHandResponse(Enum):
    MULLIGAN = 0
    KEEP_HAND = 1


class BaseController:
    def confirm_hand(self):
        return ConfirmHandResponse.KEEP_HAND

    def choose_unit(self) -> t.Optional[UnitCard]:
        return CardList().get_card("Agumon")  # type: ignore
