from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Type
from ddcb.base_controller import ConfirmHandResponse

from ddcb.player import Player


class TurnResult(Enum):
    CONTINUE = 0
    NO_UNIT = 1


type PhaseFuncs = list[Callable[[], TurnResult]]


@dataclass
class Phase(ABC):
    player: Player
    opponent: Player

    @classmethod
    def from_phase(cls, phase: "Phase"):
        return cls(phase.player, phase.opponent)

    @abstractmethod
    def do(self) -> TurnResult:
        raise NotImplementedError

    def do_phases(self, phases: list[Type["Phase"]]):
        phase_funcs = [phase.from_phase(self).do for phase in phases]
        return self.do_phase_funcs(phase_funcs)

    def do_phase_funcs(self, phase_funcs: PhaseFuncs):
        for phase_func in phase_funcs:
            result = phase_func()
            if result != TurnResult.CONTINUE:
                return result
        return TurnResult.CONTINUE


class Turn(Phase):
    def do(self):
        phases: list[Type[Phase]] = [
            PrepPhase,
            UpgradePhase,
            BattlePhase,
        ]
        return self.do_phases(phases)


class PrepPhase(Phase):
    def do(self) -> TurnResult:
        subphases: PhaseFuncs = [self.draw_cards, self.prep_play_unit]
        return self.do_phase_funcs(subphases)

    def draw_cards(self):
        self.player.field.draw_til_full()
        return self.confirm_hand()

    def confirm_hand(self):
        if self.player.deck.is_empty():
            if not self.player.field.has_unit():
                return TurnResult.NO_UNIT
            # Auto-confirm
            return TurnResult.CONTINUE

        if not self.player.field.has_unit_in_hand():
            # Auto-mulligan
            return self.mulligan()

        choice = self.player.controller.confirm_hand()
        if choice == ConfirmHandResponse.MULLIGAN:
            return self.mulligan()

        return TurnResult.CONTINUE

    def mulligan(self):
        self.player.field.discard_hand()
        return self.draw_cards()

    def prep_play_unit(self):
        if self.player.field.has_unit():
            print(f"{self.player.name} already has a unit in play.")
        else:
            choice = self.player.controller.choose_unit(
                self.player.field.get_units_in_hand()
            )
            self.player.field.play_unit(choice)

        return TurnResult.CONTINUE


class UpgradePhase(Phase):
    def do(self):
        subphases: PhaseFuncs = [
            self.choose_dp_booster,
            # self.play_dp_option,
            self.choose_evolution,
        ]
        return self.do_phase_funcs(subphases)

    def choose_dp_booster(self):
        units_in_hand = self.player.field.get_units_in_hand()
        if units_in_hand:
            choice = self.player.controller.choose_dp_booster(units_in_hand)
            if choice is not None:
                self.player.field.boost_dp(choice)
        return TurnResult.CONTINUE

    def play_dp_option(self):
        raise NotImplementedError

    def choose_evolution(self):
        evolution_targets = self.player.field.get_evolution_targets()
        if len(evolution_targets) > 0:
            # TODO: we should make current unit a stack
            # so we can place the evo on top of the previous form
            choice = self.player.controller.choose_evolution(evolution_targets)
            if choice is not None:
                self.player.field.evolve_unit(choice)
        return TurnResult.CONTINUE


class BattlePhase(Phase):
    pass
