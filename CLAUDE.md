# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AWS Service Typing Game - A Pygame-based typing practice game featuring 80+ AWS services. Players type humorous English sentences containing AWS service names within a 60-second time limit. The game includes Japanese translations, comprehensive scoring system based on accuracy and speed, and various accessibility features.

## Development Commands

### Running the Game
```bash
# Recommended - using uv
uv run aws-typing-game

# Development mode
uv run python src/aws_typing_game/main.py

# Using development script
uv run scripts/dev.py game
```

### Environment Setup
```bash
# Using uv (recommended) - automatic dependency management
uv sync --dev

# Manual installation with uv
uv pip install -e .
```

### Testing & Quality Assurance
```bash
# Run tests
uv run scripts/dev.py test
# or: uv run pytest tests/

# Run linting and type checking
uv run scripts/dev.py lint

# Format code
uv run scripts/dev.py format

# Run all quality checks
uv run scripts/dev.py check

# Using just (if installed)
just test
just lint
just check
```

## Project Structure

```
src/
├── aws_typing_game/
│   ├── __init__.py
│   ├── main.py              # Main entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── game.py          # Core game logic
│   │   └── config.py        # Configuration constants
│   ├── managers/
│   │   ├── __init__.py
│   │   ├── audio_manager.py
│   │   ├── data_manager.py
│   │   ├── font_manager.py
│   │   ├── ui_manager.py
│   │   ├── animation_manager.py
│   │   ├── accessibility_manager.py
│   │   └── responsive_manager.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── aws_services_data.json
│   ├── ui/
│   │   ├── __init__.py
│   │   └── ui_manager.py
│   └── utils/
│       └── __init__.py
tests/
├── __init__.py
├── test_game.py
└── test_data_manager.py
assets/
├── sounds/
├── music/
└── images/
docs/
```

## Architecture

### Core Game Loop (main.py → core/game.py → ui/ui_manager.py)
The game follows a state-based architecture where `src/aws_typing_game/main.py` orchestrates the game loop, `core/game.py` manages game logic and state transitions, and `ui/ui_manager.py` handles all rendering. Game states include: menu, playing, game_over, and service_info.

### Manager Pattern
The codebase uses a manager pattern where specialized managers handle specific concerns:
- **FontManager**: Cross-platform font detection and loading (particularly important for Japanese text)
- **DataManager**: AWS service data loading and high score persistence
- **UIManager**: All rendering logic with responsive design support
- **AudioManager**: Sound effects and background music
- **AnimationManager**: Visual effects and transitions
- **AccessibilityManager**: Color blindness modes and high contrast support
- **ResponsiveManager**: Dynamic UI scaling based on screen size

### Scoring System
Score = Accuracy Rate × WPM (Words Per Minute)
- Accuracy Rate = (1 - (mistakes / (correct_chars + mistakes))) × 100%
- Character-by-character validation prevents incorrect input
- Immediate feedback on typing errors

### Data Flow
1. **AWS Service Data**: Loaded from `aws_services_data.json` containing 80+ services with sentences and translations
2. **Save Data**: Only high scores are persisted in `save_data.json` (no session history)
3. **Real-time Updates**: Score updates on each correct word completion

## Key Implementation Details

### Character-by-Character Typing Validation
The game validates each character as it's typed (src/aws_typing_game/core/game.py lines 90-113):
- Only correct characters are accepted
- Mistakes increment error counter but don't appear on screen
- Modifier keys (Shift, Ctrl, etc.) are explicitly ignored to prevent false mistakes

### Responsive UI Scaling
UI elements automatically scale based on screen size (src/aws_typing_game/managers/responsive_manager.py):
- Minimum window size: 800x600
- Maximum: 80% of screen dimensions
- Font sizes and UI elements scale proportionally

### Cross-Platform Font Support
The game automatically detects and loads appropriate Japanese fonts for each platform (src/aws_typing_game/managers/font_manager.py):
- macOS: Hiragino Kaku Gothic Pro
- Windows: Meiryo, MS Gothic
- Linux: Noto Sans CJK

### Evaluation Levels (src/aws_typing_game/core/config.py)
- **Hero**: Score ≥ 80 (requires ~80 WPM with perfect accuracy)
- **Specialty**: Score ≥ 60
- **Professional**: Score ≥ 45
- **Associate**: Score ≥ 30
- **Foundational**: Score ≥ 0

## Important Game Mechanics

1. **Auto-advance on completion**: Words automatically advance when typed correctly (no Enter required)
2. **Service name highlighting**: AWS service names are visually highlighted in sentences
3. **Positive reinforcement**: All typing sentences use positive, encouraging humor
4. **Real-time feedback**: Visual and audio feedback for correct/incorrect typing

## Common Modifications

### Adding New AWS Services
1. Edit `src/aws_typing_game/data/aws_services_data.json`
2. Add service to appropriate category
3. Include sentence with `<ServiceName>` format
4. Add Japanese translation
5. Add service description

### Adjusting Difficulty
- Modify evaluation thresholds in `src/aws_typing_game/core/config.py` → `EvaluationConfig`
- Change time limit in `src/aws_typing_game/core/config.py` → `GameConfig.TIME_LIMIT`

### UI Customization
- Colors: Modify `src/aws_typing_game/core/config.py` → `Colors` class
- Layout: Adjust `src/aws_typing_game/core/config.py` → `UIConfig` spacing values
- Fonts: Update `src/aws_typing_game/core/config.py` → `FontConfig` for different sizes

## Dependencies
- pygame==2.6.1
- numpy>=1.21.0 (for audio generation)

## File Structure Notes
- Game saves only high score (no session history) in `save_data.json`
- `assets/sounds/` and `assets/music/` directories are auto-created if custom audio files are added
- All UI text supports Japanese characters
- Service data is external to code in JSON format for easy updates