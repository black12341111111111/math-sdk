"""Game override with custom mechanics for Crypto Stacks Metavault."""

from game_executables import GameExecutables
from src.calculations.statistics import get_random_outcome


class GameStateOverride(GameExecutables):
    """
    Implements:
    1. Multiplying wilds (x2 or x3) during free spins
    2. CHIP collection mechanic during free spins
    3. Symbol upgrade logic (M1->M2->M3->M4->DIAMOND)
    """

    def reset_book(self):
        """Reset global values used across multiple projects."""
        super().reset_book()
        # Free spins specific state - reset for each base game spin
        if not hasattr(self, 'in_freespins') or not self.in_freespins:
            self.chip_count = 0
            self.upgrade_level = 0  # 0=M1, 1=M2, 2=M3, 3=M4, 4=DIAMOND

    def reset_fs_spin(self):
        """Initialize free spins state."""
        super().reset_fs_spin()
        # Initialize free spins tracking variables
        self.in_freespins = True
        self.chip_count = 0
        self.upgrade_level = 0

    def end_freespin(self):
        """Clean up free spins state."""
        super().end_freespin()
        # Reset state when exiting free spins
        self.in_freespins = False
        self.chip_count = 0
        self.upgrade_level = 0

    def assign_special_sym_function(self):
        """Define special symbol behavior."""
        self.special_symbol_functions = {}
        
        # During free spins, WILD symbols get multipliers
        if hasattr(self, 'in_freespins') and self.in_freespins:
            self.special_symbol_functions["WILD"] = [self.assign_wild_multiplier]
        
        # CHIP collection only happens during free spins
        if hasattr(self, 'in_freespins') and self.in_freespins:
            self.special_symbol_functions["CHIP"] = [self.collect_chip]

    def assign_wild_multiplier(self, symbol):
        """Assign x2 or x3 multiplier to WILD symbols during free spins."""
        if hasattr(self, 'in_freespins') and self.in_freespins:
            # Get multiplier values from distribution conditions
            conditions = self.get_current_distribution_conditions()
            if "wild_mult_values" in conditions:
                multiplier_value = get_random_outcome(conditions["wild_mult_values"])
            else:
                # Default to x2 or x3 with equal probability
                multiplier_value = get_random_outcome({2: 50, 3: 50})
            symbol.assign_attribute({"multiplier": multiplier_value})

    def collect_chip(self, symbol):
        """Collect CHIP symbol during free spins."""
        if hasattr(self, 'in_freespins') and self.in_freespins:
            self.chip_count += 1
            # Check for upgrade thresholds
            # Every 3 chips = 1 upgrade level
            new_upgrade_level = min(self.chip_count // 3, 4)
            if new_upgrade_level > self.upgrade_level:
                self.upgrade_level = new_upgrade_level
                self.apply_symbol_upgrade()

    def apply_symbol_upgrade(self):
        """
        Upgrade symbols based on chip collection:
        Level 0 (0-2 chips): Base symbols (M1, M2, M3, M4)
        Level 1 (3-5 chips): M1 -> M2
        Level 2 (6-8 chips): M1,M2 -> M3
        Level 3 (9-11 chips): M1,M2,M3 -> M4
        Level 4 (12+ chips): M1,M2,M3,M4 -> DIAMOND
        """
        upgrade_map = {
            1: {"M1": "M2"},
            2: {"M1": "M3", "M2": "M3"},
            3: {"M1": "M4", "M2": "M4", "M3": "M4"},
            4: {"M1": "DIAMOND", "M2": "DIAMOND", "M3": "DIAMOND", "M4": "DIAMOND"},
        }
        
        if self.upgrade_level in upgrade_map:
            upgrade_rules = upgrade_map[self.upgrade_level]
            # Apply upgrades to current board
            for reel in self.board:
                for symbol in reel:
                    if symbol.name in upgrade_rules:
                        symbol.name = upgrade_rules[symbol.name]

    def check_game_repeat(self):
        """Verify final simulation outcomes satisfied all distribution/criteria conditions."""
        if self.repeat is False:
            win_criteria = self.get_current_betmode_distributions().get_win_criteria()
            if win_criteria is not None and self.final_win != win_criteria:
                self.repeat = True
