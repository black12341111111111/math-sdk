# Crypto Stacks Metavault - Game Setup Progress

## Overview
This document tracks the setup progress for the "Crypto Stacks Metavault" slot game using Stake Engine's Math SDK (Python) and Web SDK (Node.js).

## Current Status

### ✅ Completed Tasks

1. **Environment Setup**
   - Python 3.12.3 ✓
   - Node.js v20.19.5 ✓
   - pnpm v10.5.0 ✓
   - Rust 1.91.1 ✓

2. **Math SDK Setup**
   - Cloned from https://github.com/StakeEngine/math-sdk.git to `./math_sdk_project/`
   - Ran `make setup` to install Python dependencies
   - Created game directory: `games/crypto_stacks_metavault/`
   - Configured `game_config.py`:
     - Game ID: `crypto_stacks_metavault`
     - 5 reels × 4 rows = 1024 ways
     - RTP: 96%
     - Win cap: 10000x
   - Implemented symbols:
     - Premium: DIAMOND, M4, M3, M2, M1, CHIP
     - High cards: A, K
     - Low cards: Q, J, 10, 9
     - Special: WILD (substitutes + multipliers x2/x3), SCATTER (free spins)
   - Created reel files: BR0.csv, FR0.csv, FRWCAP.csv
   - Configured features:
     - Free Spins: 3+ SCATTER symbols trigger 10/15/20 spins
     - Wild Multipliers: x1 (60%), x2 (25%), x3 (15%)

### 🚫 Blocked Tasks

**Assets Download:** Cannot access Google Drive to download `assets.zip`
- Google Drive domain is blocked in this environment
- Need alternative upload method

**Solution Needed:**
1. Upload `assets.zip` directly to this repository (e.g., in `uploads/` folder), OR
2. Provide alternative download link (GitHub release, direct HTTP URL, etc.)

### 📋 Remaining Tasks

Once assets are available:

1. **Complete Math SDK**
   - Debug and fix reel configuration issues
   - Run `make run GAME=crypto_stacks_metavault`
   - Verify `library/publish_files/` output generation

2. **Web SDK Implementation**
   - Clone https://github.com/StakeEngine/web-sdk.git to `./web_sdk_project/`
   - Run `pnpm install`
   - Create `apps/crypto_stacks_metavault/` from template
   - Copy assets:
     - `temp_assets/symbols/*` → `apps/crypto_stacks_metavault/assets/symbols/`
     - `temp_assets/audio/*` → `apps/crypto_stacks_metavault/assets/audio/`
     - `temp_assets/fonts/primary-font.ttf` → `apps/crypto_stacks_metavault/assets/fonts/`
     - `temp_assets/background.jpg` → `apps/crypto_stacks_metavault/assets/`
   - Install `stake-engine-client`: `pnpm add stake-engine-client`
   - Implement RGS integration (requestBet, requestEndRound)
   - Update `vite.config.ts`: Add `base: "./"`
   - Wire up fonts and audio
   - Build: `pnpm run build --filter=crypto_stacks_metavault`

3. **Final Packaging**
   - Create `deployment/` directory structure:
     ```
     deployment/
     ├── math-sdk/          (from library/publish_files/)
     ├── frontend-sdk/      (from web_sdk_project/apps/crypto_stacks_metavault/dist/)
     │   └── assets/        (from temp_assets/)
     └── config/
         └── game.config.json
     ```
   - Compress to `SUBMISSION_PACKAGE.zip`

## Directory Structure (in progress)

```
/home/runner/work/math-sdk/math-sdk/
├── math_sdk_project/               # Cloned Math SDK
│   └── games/crypto_stacks_metavault/
│       ├── game_config.py          # Game configuration
│       ├── gamestate.py            # Game logic
│       ├── game_override.py        # Custom overrides
│       ├── run.py                  # Simulation runner
│       └── reels/                  # Reel strip files
│           ├── BR0.csv             # Base game reels
│           ├── FR0.csv             # Free game reels
│           └── FRWCAP.csv          # Free game wincap reels
├── web_sdk_project/                # To be cloned
├── temp_assets/                    # To be extracted from assets.zip
└── deployment/                     # Final package (to be created)
```

## Game Features Implemented

### Symbols & Paytable
| Symbol   | Type      | 5-of-a-kind | 4-of-a-kind | 3-of-a-kind |
|----------|-----------|-------------|-------------|-------------|
| DIAMOND  | Premium   | 50x         | 20x         | 10x         |
| M4       | Premium   | 30x         | 12x         | 5x          |
| M3       | Premium   | 20x         | 8x          | 3x          |
| M2       | Premium   | 15x         | 6x          | 2.5x        |
| M1       | Premium   | 10x         | 4x          | 2x          |
| CHIP     | Premium   | 8x          | 3x          | 1.5x        |
| A        | High      | 5x          | 2x          | 1x          |
| K        | High      | 4x          | 1.5x        | 0.8x        |
| Q        | Low       | 3x          | 1.2x        | 0.6x        |
| J        | Low       | 2.5x        | 1x          | 0.5x        |
| 10       | Low       | 2x          | 0.8x        | 0.4x        |
| 9        | Low       | 1.5x        | 0.6x        | 0.3x        |
| WILD     | Special   | Substitutes all except SCATTER |
| SCATTER  | Special   | Triggers free spins             |

### Features
1. **Free Spins**: 3/4/5 SCATTER → 10/15/20 free spins
2. **Wild Multipliers**: WILD symbols have random multipliers (x1/x2/x3)
3. **Collection Feature**: CHIP symbols can upgrade M1→M4→DIAMOND (to be implemented in gamestate.py)

## Next Steps

**Immediate:** Waiting for assets.zip file to be uploaded to proceed with:
- Extracting and verifying assets
- Completing Math SDK simulation
- Setting up Web SDK
- Building final package

## Notes
- Math SDK uses Python for server-side game logic and lookup table generation
- Web SDK uses Node.js/pnpm for frontend build
- No Rust/WASM compilation needed for game logic (only for optimization algorithm in Math SDK)
- The frontend communicates with RGS via `stake-engine-client` npm package
