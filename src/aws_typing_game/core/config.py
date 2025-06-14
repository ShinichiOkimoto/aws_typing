"""
Configuration constants for AWS Service Typing Game
"""


class GameConfig:
    """Game-related configuration"""

    WIDTH = 1000
    HEIGHT = 700
    TIME_LIMIT = 60  # seconds
    TARGET_FPS = 60
    WINDOW_TITLE = "AWS Service Typing"


class Colors:
    """Modern color system with improved contrast and hierarchy"""

    # Core background colors
    BACKGROUND = (15, 17, 21)  # Deep dark for better focus
    SURFACE = (25, 28, 35)  # Card/panel background
    SURFACE_VARIANT = (35, 38, 45)  # Interactive surface
    SURFACE_BRIGHT = (45, 48, 55)  # Highlighted surface

    # Primary colors (AWS-inspired but modernized)
    PRIMARY = (52, 168, 83)  # Modern AWS green
    PRIMARY_VARIANT = (76, 175, 80)  # Lighter green
    PRIMARY_DARK = (27, 94, 32)  # Darker green

    # Secondary colors
    SECONDARY = (255, 193, 7)  # Warm gold/amber
    SECONDARY_VARIANT = (255, 213, 79)  # Light amber
    SECONDARY_DARK = (255, 160, 0)  # Orange accent

    # Semantic colors
    SUCCESS = (76, 175, 80)  # Success green
    WARNING = (255, 152, 0)  # Warning orange
    ERROR = (244, 67, 54)  # Error red
    INFO = (33, 150, 243)  # Info blue

    # Text colors with proper contrast
    ON_SURFACE = (255, 255, 255)  # Primary text
    ON_SURFACE_VARIANT = (189, 193, 198)  # Secondary text
    ON_BACKGROUND = (245, 245, 245)  # Background text
    DISABLED = (117, 117, 117)  # Disabled text

    # Legacy aliases for backward compatibility
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = PRIMARY
    RED = ERROR
    BLUE = (18, 44, 82)
    LIGHT_BLUE = INFO
    ORANGE = WARNING
    DARK_ORANGE = SECONDARY_DARK
    GRAY = (84, 91, 100)
    LIGHT_GRAY = ON_SURFACE_VARIANT
    DARK_BG = BACKGROUND

    # Evaluation category colors (modernized)
    GOLD = (255, 215, 0)  # Hero level
    PURPLE = (156, 39, 176)  # Specialty level
    EMERALD = (76, 175, 80)  # Professional level
    BLUE_CATEGORY = (33, 150, 243)  # Associate level
    GRAY_CATEGORY = (117, 117, 117)  # Foundational level


class FontConfig:
    """Font configuration"""

    TITLE_SIZE = 48
    GAME_SIZE = 36
    GAME_SIZE_SMALL = 30  # For long text that doesn't fit
    GAME_SIZE_TINY = 24  # For very long text
    SCORE_SIZE = 24
    SMALL_SIZE = 18

    # Platform-specific font paths
    MACOS_FONTS = [
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/AppleGothic.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ]

    WINDOWS_FONTS = [
        "C:\\Windows\\Fonts\\meiryo.ttc",
        "C:\\Windows\\Fonts\\msgothic.ttc",
        "C:\\Windows\\Fonts\\YuGothM.ttc",
    ]

    LINUX_FONTS = [
        "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]


class EvaluationConfig:
    """Typing evaluation thresholds (Score = Accuracy Rate * WPM)"""

    HERO_THRESHOLD = 80  # 100% accuracy * 80 WPM or 95% accuracy * 84 WPM
    SPECIALTY_THRESHOLD = 60  # 100% accuracy * 60 WPM or 95% accuracy * 63 WPM
    PROFESSIONAL_THRESHOLD = 45  # 100% accuracy * 45 WPM or 90% accuracy * 50 WPM
    ASSOCIATE_THRESHOLD = 30  # 100% accuracy * 30 WPM or 85% accuracy * 35 WPM

    LEVELS = {
        "Hero": {"threshold": HERO_THRESHOLD, "color": Colors.GOLD},
        "Specialty": {"threshold": SPECIALTY_THRESHOLD, "color": Colors.PURPLE},
        "Professional": {"threshold": PROFESSIONAL_THRESHOLD, "color": Colors.EMERALD},
        "Associate": {"threshold": ASSOCIATE_THRESHOLD, "color": Colors.BLUE_CATEGORY},
        "Foundational": {"threshold": 0, "color": Colors.GRAY_CATEGORY},
    }


class UIConfig:
    """Modern UI layout configuration"""

    # Card-based design system
    CARD_RADIUS = 16  # Larger radius for modern look
    CARD_ELEVATION = 8  # Shadow depth
    CARD_PADDING = 24  # Internal padding

    # Spacing system (8dp grid)
    SPACE_XS = 4
    SPACE_SM = 8
    SPACE_MD = 16
    SPACE_LG = 24
    SPACE_XL = 32
    SPACE_XXL = 48

    # Layout dimensions
    HEADER_HEIGHT = 80
    HEADER_BORDER_HEIGHT = 4
    PANEL_MARGIN = 400
    PANEL_HEIGHT = 450
    PANEL_BORDER_RADIUS = CARD_RADIUS  # Use modern radius
    INPUT_FIELD_HEIGHT = 56  # Increased for better touch
    INPUT_FIELD_MARGIN = 350
    PROGRESS_BAR_WIDTH = 200
    PROGRESS_BAR_HEIGHT = 8  # Thinner, modern progress bar

    # Button specifications
    BUTTON_HEIGHT = 48
    BUTTON_PADDING_H = 24
    BUTTON_PADDING_V = 12
    BUTTON_RADIUS = 12

    # Animation timing
    TRANSITION_FAST = 150  # ms
    TRANSITION_NORMAL = 300  # ms
    TRANSITION_SLOW = 500  # ms


class FileConfig:
    """File paths and names"""

    SAVE_FILE = "save_data.json"
    AWS_DATA_FILE = "aws_services.json"


class AccessibilityConfig:
    """Accessibility configuration"""

    ENABLE_KEYBOARD_NAVIGATION = True
    ENABLE_COLOR_BLIND_SUPPORT = True
    ENABLE_HIGH_CONTRAST = False
    ENABLE_FOCUS_INDICATORS = True
    ENABLE_SCREEN_READER_SUPPORT = True


class AnimationConfig:
    """Animation configuration"""

    ENABLE_ANIMATIONS = True
    ENABLE_PARTICLE_EFFECTS = True
    ENABLE_TRANSITIONS = True
    ANIMATION_SPEED_MULTIPLIER = 1.0
    PARTICLE_COUNT_MULTIPLIER = 1.0


class AudioConfig:
    """Audio configuration"""

    ENABLE_AUDIO = True
    ENABLE_SFX = True
    ENABLE_MUSIC = True
    MASTER_VOLUME = 0.7
    SFX_VOLUME = 0.8
    MUSIC_VOLUME = 0.5
    SOUNDS_FOLDER = "sounds"
    MUSIC_FOLDER = "music"
