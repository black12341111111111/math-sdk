"""Game logic and event emission for Crypto Stacks Metavault."""

from game_override import GameStateOverride


class GameState(GameStateOverride):
    """Handle basegame and freegame logic for Crypto Stacks Metavault."""

    def run_spin(self, sim: int, simulation_seed=None) -> None:
        """Execute a single base game spin."""
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.draw_board(emit_event=True)

            # Evaluate base-game board (1024 ways)
            self.evaluate_ways_board()

            self.win_manager.update_gametype_wins(self.gametype)
            
            # Check for scatter triggers (3+ SCATTER symbols)
            if self.check_fs_condition() and self.check_freespin_entry():
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self) -> None:
        """Execute free spins with special mechanics."""
        self.reset_fs_spin()
        
        while self.fs < self.tot_fs:
            self.update_freespin()
            self.draw_board(emit_event=True)

            # Evaluate ways with multiplying wilds and chip collection
            self.evaluate_ways_board()

            # Check for retrigger (3+ scatters during free spins)
            if self.check_fs_condition():
                self.update_fs_retrigger_amt()

            self.win_manager.update_gametype_wins(self.gametype)
            
        self.end_freespin()
