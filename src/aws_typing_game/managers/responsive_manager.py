"""
Responsive design manager for AWS Service Typing Game
"""

from typing import Dict, Tuple

import pygame


class ResponsiveManager:
    """Manages responsive design for different screen sizes"""

    def __init__(self, base_width: int = 1000, base_height: int = 700):
        self.base_width = base_width
        self.base_height = base_height
        self.current_width = base_width
        self.current_height = base_height
        self.scale_factor = 1.0
        self.min_width = 1000  # Ensure minimum size shows all content
        self.min_height = 700

        # Get display info safely
        try:
            display_info = pygame.display.Info()
            self.screen_width = display_info.current_w
            self.screen_height = display_info.current_h
        except pygame.error:
            # Fallback to common resolutions if pygame not initialized
            self.screen_width = 1920
            self.screen_height = 1080

        # Calculate optimal window size
        self._calculate_optimal_size()

    def _calculate_optimal_size(self) -> None:
        """Calculate optimal window size based on screen resolution"""
        # Use 90% of screen size as maximum, but leave room for system UI
        max_width = int(self.screen_width * 0.9)
        max_height = int(self.screen_height * 0.85)  # Leave more room for dock/taskbar

        # Calculate scale factors
        width_scale = max_width / self.base_width
        height_scale = max_height / self.base_height

        # Use the smaller scale to maintain aspect ratio, but be more generous with scaling
        self.scale_factor = min(width_scale, height_scale)

        # Don't scale down below 1.0 unless absolutely necessary
        if self.scale_factor < 1.0:
            # Check if base size fits in 95% of screen
            if (
                self.base_width <= self.screen_width * 0.95
                and self.base_height <= self.screen_height * 0.95
            ):
                self.scale_factor = 1.0

        # Calculate final size
        self.current_width = max(int(self.base_width * self.scale_factor), self.min_width)
        self.current_height = max(int(self.base_height * self.scale_factor), self.min_height)

        # Debug output
        print(f"Screen resolution: {self.screen_width}x{self.screen_height}")
        print(f"Scale factor: {self.scale_factor:.2f}")
        print(f"Window size: {self.current_width}x{self.current_height}")

    def get_screen_size(self) -> Tuple[int, int]:
        """Get the calculated screen size"""
        return self.current_width, self.current_height

    def scale_value(self, value: int) -> int:
        """Scale a value based on current scale factor"""
        return int(value * self.scale_factor)

    def scale_position(self, x: int, y: int) -> Tuple[int, int]:
        """Scale a position based on current scale factor"""
        return int(x * self.scale_factor), int(y * self.scale_factor)

    def scale_rect(self, x: int, y: int, width: int, height: int) -> Tuple[int, int, int, int]:
        """Scale a rectangle based on current scale factor"""
        return (
            int(x * self.scale_factor),
            int(y * self.scale_factor),
            int(width * self.scale_factor),
            int(height * self.scale_factor),
        )

    def get_responsive_font_sizes(self) -> Dict[str, int]:
        """Get responsive font sizes"""
        return {
            "title": max(24, int(48 * self.scale_factor)),
            "game": max(18, int(36 * self.scale_factor)),
            "score": max(14, int(24 * self.scale_factor)),
            "small": max(12, int(18 * self.scale_factor)),
        }

    def get_panel_dimensions(self) -> Dict[str, int]:
        """Get responsive panel dimensions"""
        return {
            "margin": int(400 * self.scale_factor),
            "height": int(450 * self.scale_factor),
            "border_radius": max(5, int(10 * self.scale_factor)),
            "input_height": int(50 * self.scale_factor),
            "header_height": int(80 * self.scale_factor),
        }

    def center_x(self, width: int) -> int:
        """Calculate centered X position"""
        return (self.current_width - width) // 2

    def center_y(self, height: int) -> int:
        """Calculate centered Y position"""
        return (self.current_height - height) // 2

    def is_small_screen(self) -> bool:
        """Check if current screen is considered small"""
        return self.scale_factor < 0.9

    def is_large_screen(self) -> bool:
        """Check if current screen is considered large"""
        return self.scale_factor > 1.2

    def get_layout_mode(self) -> str:
        """Get current layout mode based on screen size"""
        if self.is_small_screen():
            return "compact"
        elif self.is_large_screen():
            return "expanded"
        else:
            return "normal"
