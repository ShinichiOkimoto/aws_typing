"""
Accessibility manager for AWS Service Typing Game
"""

from typing import Dict, List, Tuple

import pygame

from ..core.config import Colors


class AccessibilityManager:
    """Manages accessibility features including color vision support and keyboard navigation"""

    def __init__(self):
        self.color_blind_mode = "normal"  # normal, protanopia, deuteranopia, tritanopia
        self.high_contrast_mode = False
        self.focus_index = 0
        self.focusable_elements = []
        self.keyboard_navigation_enabled = True

        # Color blindness friendly palettes
        self.color_palettes = {
            "normal": {
                "success": Colors.GREEN,
                "error": Colors.RED,
                "warning": Colors.ORANGE,
                "info": Colors.LIGHT_BLUE,
                "primary": Colors.BLUE,
                "accent": Colors.ORANGE,
            },
            "protanopia": {  # Red-blind
                "success": (0, 150, 255),  # Blue
                "error": (255, 140, 0),  # Orange
                "warning": (255, 200, 0),  # Yellow
                "info": (0, 150, 255),  # Blue
                "primary": (70, 130, 180),  # Steel blue
                "accent": (255, 140, 0),  # Orange
            },
            "deuteranopia": {  # Green-blind
                "success": (0, 150, 255),  # Blue
                "error": (255, 140, 0),  # Orange
                "warning": (255, 200, 0),  # Yellow
                "info": (0, 150, 255),  # Blue
                "primary": (70, 130, 180),  # Steel blue
                "accent": (255, 140, 0),  # Orange
            },
            "tritanopia": {  # Blue-blind
                "success": (0, 180, 0),  # Green
                "error": (220, 20, 60),  # Crimson
                "warning": (255, 140, 0),  # Orange
                "info": (255, 20, 147),  # Deep pink
                "primary": (220, 20, 60),  # Crimson
                "accent": (255, 140, 0),  # Orange
            },
        }

        # High contrast alternatives
        self.high_contrast_colors = {
            "background": (0, 0, 0),  # Pure black
            "foreground": (255, 255, 255),  # Pure white
            "success": (0, 255, 0),  # Bright green
            "error": (255, 0, 0),  # Bright red
            "warning": (255, 255, 0),  # Bright yellow
            "info": (0, 255, 255),  # Bright cyan
            "primary": (255, 255, 255),  # White
            "accent": (255, 255, 0),  # Bright yellow
        }

    def set_color_blind_mode(self, mode: str) -> None:
        """Set color blindness support mode"""
        if mode in self.color_palettes:
            self.color_blind_mode = mode

    def toggle_high_contrast(self) -> None:
        """Toggle high contrast mode"""
        self.high_contrast_mode = not self.high_contrast_mode

    def get_color(self, color_type: str) -> Tuple[int, int, int]:
        """Get accessible color based on current settings"""
        if self.high_contrast_mode:
            return self.high_contrast_colors.get(color_type, Colors.WHITE)

        palette = self.color_palettes.get(self.color_blind_mode, self.color_palettes["normal"])
        return palette.get(color_type, Colors.WHITE)

    def get_accessible_colors(self) -> Dict[str, Tuple[int, int, int]]:
        """Get full accessible color set"""
        if self.high_contrast_mode:
            return self.high_contrast_colors.copy()

        return self.color_palettes.get(self.color_blind_mode, self.color_palettes["normal"]).copy()

    def set_focusable_elements(self, elements: List[str]) -> None:
        """Set list of focusable UI elements"""
        self.focusable_elements = elements
        self.focus_index = 0

    def handle_navigation_input(self, event) -> str:
        """Handle keyboard navigation input"""
        if not self.keyboard_navigation_enabled or not self.focusable_elements:
            return ""

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if (
                    pygame.key.get_pressed()[pygame.K_LSHIFT]
                    or pygame.key.get_pressed()[pygame.K_RSHIFT]
                ):
                    # Shift+Tab - previous element
                    self.focus_index = (self.focus_index - 1) % len(self.focusable_elements)
                else:
                    # Tab - next element
                    self.focus_index = (self.focus_index + 1) % len(self.focusable_elements)
                return "focus_changed"

            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Activate focused element
                return f"activate_{self.focusable_elements[self.focus_index]}"

        return ""

    def get_focused_element(self) -> str:
        """Get currently focused element"""
        if self.focusable_elements and 0 <= self.focus_index < len(self.focusable_elements):
            return self.focusable_elements[self.focus_index]
        return ""

    def draw_focus_indicator(
        self, surface, rect: Tuple[int, int, int, int], thickness: int = 3
    ) -> None:
        """Draw focus indicator around an element"""
        focus_color = self.get_color("accent")
        x, y, width, height = rect

        # Draw dashed border for focus indication
        dash_length = 10
        gap_length = 5

        # Top border
        for i in range(0, width, dash_length + gap_length):
            pygame.draw.rect(
                surface, focus_color, (x + i, y - thickness, min(dash_length, width - i), thickness)
            )

        # Bottom border
        for i in range(0, width, dash_length + gap_length):
            pygame.draw.rect(
                surface, focus_color, (x + i, y + height, min(dash_length, width - i), thickness)
            )

        # Left border
        for i in range(0, height, dash_length + gap_length):
            pygame.draw.rect(
                surface,
                focus_color,
                (x - thickness, y + i, thickness, min(dash_length, height - i)),
            )

        # Right border
        for i in range(0, height, dash_length + gap_length):
            pygame.draw.rect(
                surface, focus_color, (x + width, y + i, thickness, min(dash_length, height - i))
            )

    def get_text_with_pattern(self, text: str, pattern_type: str = "none") -> str:
        """Add text patterns for users who can't distinguish colors"""
        if pattern_type == "success":
            return f"✓ {text}"
        elif pattern_type == "error":
            return f"✗ {text}"
        elif pattern_type == "warning":
            return f"⚠ {text}"
        elif pattern_type == "info":
            return f"ℹ {text}"
        return text

    def get_accessibility_info(self) -> Dict[str, str]:
        """Get current accessibility settings info"""
        return {
            "color_blind_mode": self.color_blind_mode,
            "high_contrast": "enabled" if self.high_contrast_mode else "disabled",
            "keyboard_navigation": "enabled" if self.keyboard_navigation_enabled else "disabled",
            "focused_element": self.get_focused_element(),
        }

    def create_screen_reader_text(self, game_state: str, **kwargs) -> str:
        """Create descriptive text for screen readers"""
        if game_state == "menu":
            return "AWS Service Typing Game main menu. Press space to start, or escape to exit."

        elif game_state == "playing":
            score = kwargs.get("score", 0)
            mistakes = kwargs.get("mistakes", 0)
            remaining_time = kwargs.get("remaining_time", 0)
            current_word = kwargs.get("current_word", "")
            return f"Game in progress. Score: {score}, Mistakes: {mistakes}, Time remaining: {int(remaining_time)} seconds. Type: {current_word}"

        elif game_state == "game_over":
            score = kwargs.get("score", 0)
            high_score = kwargs.get("high_score", 0)
            return f"Game over. Final score: {score}, High score: {high_score}. Press space to restart or escape for menu."

        elif game_state == "service_info":
            service_name = kwargs.get("service_name", "")
            return f"Service information for {service_name}. Use A and D keys to navigate, escape to return."

        return "Unknown game state"
