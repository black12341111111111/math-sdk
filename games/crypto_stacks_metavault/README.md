# Crypto Stacks Metavault

A 5-reel, 4-row video slot game with 1024 ways-to-win featuring innovative free spins mechanics with chip collection and symbol upgrades.

## Game Specifications

### Grid Layout
- **Reels:** 5
- **Rows:** 4
- **Win Type:** 1024 Ways-to-Win

### Symbols

#### Premium Symbols
- **DIAMOND** - Highest paying symbol

#### Special Symbols
- **WILD** - Substitutes for all symbols except SCATTER and CHIP
  - Appears only on reels 2, 3, and 4 during base game
  - During free spins: WILD symbols receive multipliers (x2 or x3)
- **SCATTER** - Free spins trigger symbol
- **CHIP** - Collector symbol (active only during free spins)

#### Medium Symbols
- **M4** - High-medium symbol
- **M3** - Medium symbol
- **M2** - Medium symbol
- **M1** - Low-medium symbol

#### Low Symbols
- **A, K, Q, J, 10, 9** - Standard card symbols

## Base Game

- Standard 1024 ways-to-win evaluation
- WILD symbols substitute for all paying symbols
- SCATTER symbols can trigger free spins

## Free Spins Feature

### Trigger
- **3 SCATTER symbols:** 10 free spins
- **4 SCATTER symbols:** 15 free spins
- **5 SCATTER symbols:** 20 free spins

### Retrigger (During Free Spins)
- **3 SCATTER symbols:** +5 free spins
- **4 SCATTER symbols:** +10 free spins
- **5 SCATTER symbols:** +15 free spins

### Special Mechanics

#### 1. Multiplying Wilds
During free spins, WILD symbols receive random multipliers:
- **x2 multiplier** - 50% chance
- **x3 multiplier** - 50% chance

#### 2. CHIP Collection System
CHIP symbols appear during free spins and are collected when they land on the reels.

#### 3. Symbol Upgrade System
As CHIP symbols are collected, medium symbols automatically upgrade to higher-value symbols:

| Chips Collected | Upgrade Level | Symbol Upgrades |
|----------------|---------------|-----------------|
| 0-2 chips | Level 0 | No upgrades (base symbols) |
| 3-5 chips | Level 1 | M1 → M2 |
| 6-8 chips | Level 2 | M1, M2 → M3 |
| 9-11 chips | Level 3 | M1, M2, M3 → M4 |
| 12+ chips | Level 4 | M1, M2, M3, M4 → DIAMOND |

**Important:** The CHIP collection count and symbol upgrades are **stateless** - they reset at the end of each free spins round and do not carry over to subsequent features.

## Technical Details

### RTP
- Target RTP: 96%
- Win Cap: 5000x

### Distribution
The game uses multiple outcome distributions:
- **Free Game Distribution** (20%): Guarantees free spins trigger
- **Zero Win Distribution** (30%): No win outcomes
- **Base Game Distribution** (50%): Standard base game wins

### File Structure
```
games/crypto_stacks_metavault/
├── game_config.py          # Game configuration and paytables
├── game_calculations.py    # Custom calculations
├── game_events.py          # Event definitions
├── game_executables.py     # Ways-to-win evaluation
├── game_override.py        # Custom mechanics (chips, upgrades, multipliers)
├── gamestate.py           # Main game logic flow
├── game_optimization.py    # Optimization parameters
├── run.py                 # Simulation execution script
└── reels/
    ├── BR0.csv            # Base game reels
    └── FR0.csv            # Free spins reels
```

## Running the Game

To generate simulation results and configuration files:

```bash
# From the math-sdk root directory
make run GAME=crypto_stacks_metavault
```

Or using the virtual environment directly:

```bash
cd /path/to/math-sdk
source env/bin/activate
python games/crypto_stacks_metavault/run.py
```

## Output Files

After running, the game generates:
- **Books:** Simulation results (compressed)
- **Config Files:** Frontend configuration (JSON)
- **Force Files:** Distribution enforcement data
- **Lookup Tables:** Optimization tables

All output files are located in `games/crypto_stacks_metavault/library/`
