"""Crypto Stacks Metavault game configuration."""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):
    """Game specific configuration class for Crypto Stacks Metavault."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "crypto_stacks_metavault"
        self.provider_number = 0
        self.working_name = "Crypto Stacks Metavault"
        self.wincap = 5000
        self.win_type = "ways"
        self.rtp = 0.96
        self.construct_paths()

        # Game Dimensions - 5 reels, 4 rows, 1024 ways
        self.num_reels = 5
        self.num_rows = [4] * self.num_reels

        # Paytable definitions
        # Premium: DIAMOND
        # Scatter: SCATTER (no pays, just triggers)
        # Wild: WILD (substitutes, no pays)
        # Collector: CHIP (no pays, collects during free spins)
        # Medium: M1, M2, M3, M4
        # Low: A, K, Q, J, 10, 9
        self.paytable = {
            # Premium - DIAMOND
            (5, "DIAMOND"): 50,
            (4, "DIAMOND"): 20,
            (3, "DIAMOND"): 10,
            # Medium High - M4
            (5, "M4"): 25,
            (4, "M4"): 10,
            (3, "M4"): 5,
            # Medium - M3
            (5, "M3"): 15,
            (4, "M3"): 6,
            (3, "M3"): 3,
            # Medium - M2
            (5, "M2"): 10,
            (4, "M2"): 4,
            (3, "M2"): 2,
            # Medium Low - M1
            (5, "M1"): 7.5,
            (4, "M1"): 3,
            (3, "M1"): 1.5,
            # Low - A
            (5, "A"): 5,
            (4, "A"): 2,
            (3, "A"): 1,
            # Low - K
            (5, "K"): 4,
            (4, "K"): 1.5,
            (3, "K"): 0.8,
            # Low - Q
            (5, "Q"): 3,
            (4, "Q"): 1.2,
            (3, "Q"): 0.6,
            # Low - J
            (5, "J"): 2.5,
            (4, "J"): 1,
            (3, "J"): 0.5,
            # Low - 10
            (5, "10"): 2,
            (4, "10"): 0.8,
            (3, "10"): 0.4,
            # Low - 9
            (5, "9"): 1.5,
            (4, "9"): 0.6,
            (3, "9"): 0.3,
        }

        self.include_padding = True
        # WILD appears on reels 2, 3, 4 (indices 1, 2, 3)
        # SCATTER triggers free spins
        # CHIP is the collector symbol
        self.special_symbols = {
            "wild": ["WILD"],
            "scatter": ["SCATTER"],
            "multiplier": [],
            "collector": ["CHIP"],
        }

        # Free spin triggers: 3+ scatters in base game, 2+ in free game for retrigger
        self.freespin_triggers = {
            self.basegame_type: {3: 10, 4: 15, 5: 20},
            self.freegame_type: {3: 5, 4: 10, 5: 15},
        }
        self.anticipation_triggers = {self.basegame_type: 2, self.freegame_type: 2}

        # Reels
        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="freegame",
                        quota=0.2,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "force_wincap": False,
                            "force_freegame": True,
                            "scatter_triggers": {3: 100, 4: 20, 5: 5},
                            "wild_mult_values": {2: 50, 3: 50},
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.3,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.5,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
        ]
