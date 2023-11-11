from enum import Enum
from typing import Optional

from ddcb.card import CardList, UnitCard


class ConfirmHandResponse(Enum):
    MULLIGAN = 0
    KEEP_HAND = 1


class BaseController:
    def confirm_hand(self) -> ConfirmHandResponse:
        return ConfirmHandResponse.KEEP_HAND

    def choose_unit(self, units: list[UnitCard]) -> UnitCard:
        return units[0]

    def choose_dp_booster(self, units: list[UnitCard]) -> Optional[UnitCard]:
        return self.choose_unit(units)

    def choose_evolution(self, units: list[UnitCard]) -> Optional[UnitCard]:
        return self.choose_unit(units)
