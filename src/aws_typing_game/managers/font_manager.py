"""
Font management module for AWS Service Typing Game
"""

import os
import sys

import pygame

from ..core.config import FontConfig


class FontManager:
    """Manages font loading and initialization for different platforms"""

    def __init__(self):
        self.font_path = self._get_font_path()
        self.fonts = {}
        self._initialize_fonts()

    def _get_font_path(self) -> str:
        """Get appropriate font path based on the current platform"""
        if sys.platform == "darwin":  # macOS
            font_paths = FontConfig.MACOS_FONTS
        elif sys.platform == "win32":  # Windows
            font_paths = FontConfig.WINDOWS_FONTS
        else:  # Linux/other
            font_paths = FontConfig.LINUX_FONTS

        # Return the first existing font path
        for path in font_paths:
            if os.path.exists(path):
                return path

        # Return None if no fonts found (will use system fonts)
        return None

    def _initialize_fonts(self) -> None:
        """Initialize all required fonts"""
        if self.font_path:
            self.fonts = {
                "title": pygame.font.Font(self.font_path, FontConfig.TITLE_SIZE),
                "game": pygame.font.Font(self.font_path, FontConfig.GAME_SIZE),
                "game_small": pygame.font.Font(self.font_path, FontConfig.GAME_SIZE_SMALL),
                "game_tiny": pygame.font.Font(self.font_path, FontConfig.GAME_SIZE_TINY),
                "score": pygame.font.Font(self.font_path, FontConfig.SCORE_SIZE),
                "small": pygame.font.Font(self.font_path, FontConfig.SMALL_SIZE),
            }
        else:
            # Fallback to system fonts with better emoji support
            fallback_fonts = [
                "Arial Unicode MS",
                "Segoe UI Emoji",
                "Apple Color Emoji",
                "Noto Color Emoji",
                "Arial",
            ]
            system_font = None
            for font_name in fallback_fonts:
                if pygame.font.match_font(font_name):
                    system_font = font_name
                    break

            if system_font is None:
                system_font = "Arial"

            self.fonts = {
                "title": pygame.font.SysFont(system_font, FontConfig.TITLE_SIZE),
                "game": pygame.font.SysFont(system_font, FontConfig.GAME_SIZE),
                "game_small": pygame.font.SysFont(system_font, FontConfig.GAME_SIZE_SMALL),
                "game_tiny": pygame.font.SysFont(system_font, FontConfig.GAME_SIZE_TINY),
                "score": pygame.font.SysFont(system_font, FontConfig.SCORE_SIZE),
                "small": pygame.font.SysFont(system_font, FontConfig.SMALL_SIZE),
            }

    def get_font(self, font_type: str) -> pygame.font.Font:
        """Get a specific font by type"""
        return self.fonts.get(font_type, self.fonts["score"])

    def render_text(
        self, text: str, font_type: str, color: tuple, antialias: bool = True
    ) -> pygame.Surface:
        """Render text with specified font and color"""
        font = self.get_font(font_type)
        return font.render(text, antialias, color)

    def get_text_size(self, text: str, font_type: str) -> tuple:
        """Get the size of rendered text"""
        font = self.get_font(font_type)
        return font.size(text)
