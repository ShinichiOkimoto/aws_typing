"""
UI management module for AWS Service Typing Game
"""

from typing import List, Tuple

import pygame

from ..core.config import Colors, EvaluationConfig, GameConfig, UIConfig
from ..managers.font_manager import FontManager


class UIManager:
    """Manages all UI rendering for the game with modern design system"""

    def __init__(self, screen: pygame.Surface, font_manager: FontManager):
        self.screen = screen
        self.font_manager = font_manager
        self.responsive_manager = None
        self.accessibility_manager = None
        self.animation_manager = None

    def set_responsive_manager(self, responsive_manager):
        """Set the responsive design manager"""
        self.responsive_manager = responsive_manager

    def set_accessibility_manager(self, accessibility_manager):
        """Set the accessibility manager"""
        self.accessibility_manager = accessibility_manager

    def set_animation_manager(self, animation_manager):
        """Set the animation manager"""
        self.animation_manager = animation_manager

    def _draw_modern_card(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        background_color: Tuple[int, int, int] = None,
        border_color: Tuple[int, int, int] = None,
        elevation: bool = True,
    ) -> pygame.Rect:
        """Draw a modern card with shadow and rounded corners"""
        if background_color is None:
            background_color = Colors.SURFACE

        # Draw shadow for elevation effect
        if elevation:
            shadow_offset = 2
            shadow_color = (0, 0, 0, 30)  # Semi-transparent black
            shadow_rect = (x + shadow_offset, y + shadow_offset, width, height)
            pygame.draw.rect(self.screen, (0, 0, 0), shadow_rect, 0, UIConfig.CARD_RADIUS)

        # Draw main card
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, background_color, card_rect, 0, UIConfig.CARD_RADIUS)

        # Draw border if specified
        if border_color:
            pygame.draw.rect(self.screen, border_color, card_rect, 1, UIConfig.CARD_RADIUS)

        return card_rect

    def _draw_modern_button(
        self, x: int, y: int, width: int, text: str, style: str = "primary", state: str = "normal"
    ) -> pygame.Rect:
        """Draw a modern button with proper styling"""
        button_rect = pygame.Rect(x, y, width, UIConfig.BUTTON_HEIGHT)

        # Determine colors based on style and state
        if style == "primary":
            if state == "hover":
                bg_color = Colors.PRIMARY_VARIANT
                text_color = Colors.ON_SURFACE
            elif state == "pressed":
                bg_color = Colors.PRIMARY_DARK
                text_color = Colors.ON_SURFACE
            else:
                bg_color = Colors.PRIMARY
                text_color = Colors.ON_SURFACE
        elif style == "secondary":
            if state == "hover":
                bg_color = Colors.SECONDARY_VARIANT
                text_color = Colors.ON_SURFACE
            else:
                bg_color = Colors.SECONDARY
                text_color = Colors.ON_SURFACE
        else:  # outline
            bg_color = Colors.SURFACE_VARIANT
            text_color = Colors.ON_SURFACE_VARIANT

        # Draw button background
        pygame.draw.rect(self.screen, bg_color, button_rect, 0, UIConfig.BUTTON_RADIUS)

        # Draw button text
        text_surface = self.font_manager.render_text(text, "score", text_color)
        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (UIConfig.BUTTON_HEIGHT - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))

        return button_rect

    def _draw_progress_bar(
        self,
        x: int,
        y: int,
        width: int,
        progress: float,
        color: Tuple[int, int, int] = None,
        background_color: Tuple[int, int, int] = None,
    ) -> None:
        """Draw a modern progress bar"""
        if color is None:
            color = Colors.PRIMARY
        if background_color is None:
            background_color = Colors.SURFACE_VARIANT

        height = UIConfig.PROGRESS_BAR_HEIGHT
        radius = height // 2

        # Draw background
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, background_color, bg_rect, 0, radius)

        # Draw progress
        if progress > 0:
            progress_width = int(width * min(progress, 1.0))
            progress_rect = pygame.Rect(x, y, progress_width, height)
            pygame.draw.rect(self.screen, color, progress_rect, 0, radius)

    def _draw_gradient_background(
        self, start_color: Tuple[int, int, int] = None, end_color: Tuple[int, int, int] = None
    ) -> None:
        """Draw a subtle gradient background"""
        if start_color is None:
            start_color = Colors.BACKGROUND
        if end_color is None:
            end_color = Colors.SURFACE

        width = self.screen.get_width()
        height = self.screen.get_height()

        for y in range(height):
            ratio = y / height
            # Linear interpolation between colors
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            color = (r, g, b)
            pygame.draw.line(self.screen, color, (0, y), (width, y))

    def _wrap_text(self, text: str, font_size: str, max_width: int) -> List[str]:
        """Wrap text to fit within the specified width"""
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            # Test if adding this word would exceed max width
            test_line = current_line + (" " if current_line else "") + word
            test_surface = self.font_manager.render_text(test_line, font_size, Colors.ON_SURFACE)

            if test_surface.get_width() <= max_width:
                current_line = test_line
            # If current line is not empty, save it and start new line
            elif current_line:
                lines.append(current_line)
                current_line = word
            else:
                # Single word is too long, force break
                lines.append(word)
                current_line = ""

        # Add the last line if it exists
        if current_line:
            lines.append(current_line)

        return lines if lines else [text]

    def _get_adaptive_font_size(self, text: str, max_width: int) -> str:
        """Determine the best font size for the given text and width"""
        clean_text = text.replace("<", "").replace(">", "")

        # Try different font sizes
        font_sizes = ["game", "game_small", "game_tiny"]

        for font_size in font_sizes:
            test_surface = self.font_manager.render_text(clean_text, font_size, Colors.ON_SURFACE)
            if test_surface.get_width() <= max_width:
                return font_size

        # If even tiny doesn't fit, we'll need wrapping
        return "game_tiny"

    def _draw_enhanced_word(
        self, current_word: str, service_name: str, x: int, y: int, max_width: int
    ) -> int:
        """Draw the current word with enhanced service name highlighting and text wrapping
        Returns the height used by the text"""

        # Clean the word for width calculation
        clean_word = current_word.replace("<", "").replace(">", "")

        # Get the optimal font size
        font_size = self._get_adaptive_font_size(clean_word, max_width)

        # Check if text needs wrapping even with adaptive font size
        test_surface = self.font_manager.render_text(clean_word, font_size, Colors.ON_SURFACE)
        line_height = test_surface.get_height() + 4  # Add some line spacing

        if test_surface.get_width() <= max_width:
            # Text fits on one line, draw normally
            self._draw_single_line_word(current_word, service_name, x, y, font_size)
            return line_height
        else:
            # Text needs wrapping
            return self._draw_wrapped_word(
                current_word, service_name, x, y, max_width, line_height, font_size
            )

    def _draw_single_line_word(
        self, current_word: str, service_name: str, x: int, y: int, font_size: str = "game"
    ) -> None:
        """Draw a single line word with service highlighting"""
        if "<" in current_word and ">" in current_word:
            # Split the sentence into parts
            parts = current_word.split("<")
            if len(parts) > 1:
                before_service = parts[0]
                service_and_after = parts[1].split(">")
                if len(service_and_after) > 1:
                    service = service_and_after[0]
                    after_service = service_and_after[1]

                    # Ensure the extracted service matches the expected service name
                    if service != service_name:
                        # Fallback: just draw the text without highlighting
                        clean_text = current_word.replace("<", "").replace(">", "")
                        text_surface = self.font_manager.render_text(
                            clean_text, font_size, Colors.ON_SURFACE
                        )
                        self.screen.blit(text_surface, (x, y))
                        return

                    current_x = x

                    # Draw text before service name
                    if before_service:
                        before_surface = self.font_manager.render_text(
                            before_service, font_size, Colors.ON_SURFACE
                        )
                        self.screen.blit(before_surface, (current_x, y))
                        current_x += before_surface.get_width()

                    # Draw service name with modern highlight
                    service_surface = self.font_manager.render_text(
                        service, font_size, Colors.ON_SURFACE
                    )
                    service_width = service_surface.get_width()
                    service_height = service_surface.get_height()

                    # Modern service highlight background - precisely aligned
                    highlight_padding = 4
                    highlight_vertical_padding = 2
                    highlight_rect = pygame.Rect(
                        current_x - highlight_padding,
                        y - highlight_vertical_padding,
                        service_width + highlight_padding * 2,
                        service_height + highlight_vertical_padding * 2,
                    )
                    pygame.draw.rect(self.screen, Colors.PRIMARY, highlight_rect, 0, 6)

                    # Draw service text at the exact same position
                    self.screen.blit(service_surface, (current_x, y))
                    current_x += service_width

                    # Draw text after service name
                    if after_service:
                        after_surface = self.font_manager.render_text(
                            after_service, font_size, Colors.ON_SURFACE
                        )
                        self.screen.blit(after_surface, (current_x, y))
        else:
            # No service highlighting needed
            text_surface = self.font_manager.render_text(current_word, font_size, Colors.ON_SURFACE)
            self.screen.blit(text_surface, (x, y))

    def _draw_wrapped_word(
        self,
        current_word: str,
        service_name: str,
        x: int,
        y: int,
        max_width: int,
        line_height: int,
        font_size: str = "game",
    ) -> int:
        """Draw a wrapped word with service highlighting across multiple lines"""
        # For long text, we need to handle service name highlighting carefully
        if "<" in current_word and ">" in current_word:
            # Extract service parts
            parts = current_word.split("<")
            if len(parts) > 1:
                before_service = parts[0]
                service_and_after = parts[1].split(">")
                if len(service_and_after) > 1:
                    service = service_and_after[0]
                    after_service = service_and_after[1]

                    # Reconstruct text with markers for wrapping
                    full_text = (
                        before_service
                        + "【SERVICE_START】"
                        + service
                        + "【SERVICE_END】"
                        + after_service
                    )

                    # Wrap the text
                    wrapped_lines = self._wrap_text_with_markers(full_text, max_width, font_size)

                    # Draw each line with proper highlighting
                    current_y = y
                    for line in wrapped_lines:
                        self._draw_line_with_service_highlight(
                            line, x, current_y, service, font_size
                        )
                        current_y += line_height

                    return len(wrapped_lines) * line_height

        # Fallback: simple text wrapping without service highlighting
        clean_text = current_word.replace("<", "").replace(">", "")
        wrapped_lines = self._wrap_text(clean_text, font_size, max_width)

        current_y = y
        for line in wrapped_lines:
            text_surface = self.font_manager.render_text(line, font_size, Colors.ON_SURFACE)
            self.screen.blit(text_surface, (x, current_y))
            current_y += line_height

        return len(wrapped_lines) * line_height

    def _wrap_text_with_markers(
        self, text: str, max_width: int, font_size: str = "game"
    ) -> List[str]:
        """Wrap text while preserving service markers"""
        # Split by spaces but keep service markers intact
        parts = []
        current_part = ""
        i = 0

        while i < len(text):
            if text[i : i + 15] == "【SERVICE_START】":
                if current_part:
                    parts.append(current_part)
                    current_part = ""
                parts.append("【SERVICE_START】")
                i += 15
            elif text[i : i + 13] == "【SERVICE_END】":
                if current_part:
                    parts.append(current_part)
                    current_part = ""
                parts.append("【SERVICE_END】")
                i += 13
            elif text[i] == " ":
                if current_part:
                    parts.append(current_part)
                    current_part = ""
                parts.append(" ")
                i += 1
            else:
                current_part += text[i]
                i += 1

        if current_part:
            parts.append(current_part)

        # Now wrap the parts into lines
        lines = []
        current_line_parts = []
        current_line_width = 0

        for part in parts:
            if part in ["【SERVICE_START】", "【SERVICE_END】"]:
                current_line_parts.append(part)
                continue

            part_surface = self.font_manager.render_text(
                part if part != " " else "A", font_size, Colors.ON_SURFACE
            )
            part_width = part_surface.get_width() if part != " " else part_surface.get_width() // 2

            if current_line_width + part_width <= max_width:
                current_line_parts.append(part)
                current_line_width += part_width
            else:
                # Start new line
                if current_line_parts:
                    lines.append("".join(current_line_parts))
                current_line_parts = [part]
                current_line_width = part_width

        if current_line_parts:
            lines.append("".join(current_line_parts))

        return lines

    def _draw_line_with_service_highlight(
        self, line: str, x: int, y: int, service_name: str, font_size: str = "game"
    ) -> None:
        """Draw a line with service name highlighting if present"""
        if "【SERVICE_START】" in line and "【SERVICE_END】" in line:
            # This line contains the service name
            parts = line.split("【SERVICE_START】")
            before = parts[0]
            service_and_after = parts[1].split("【SERVICE_END】")
            service = service_and_after[0]
            after = service_and_after[1]

            current_x = x

            # Draw before text
            if before:
                before_surface = self.font_manager.render_text(before, font_size, Colors.ON_SURFACE)
                self.screen.blit(before_surface, (current_x, y))
                current_x += before_surface.get_width()

            # Draw service with highlight
            if service:
                service_surface = self.font_manager.render_text(
                    service, font_size, Colors.ON_SURFACE
                )
                service_width = service_surface.get_width()
                service_height = service_surface.get_height()

                # Precisely aligned highlight background
                highlight_padding = 4
                highlight_vertical_padding = 2
                highlight_rect = pygame.Rect(
                    current_x - highlight_padding,
                    y - highlight_vertical_padding,
                    service_width + highlight_padding * 2,
                    service_height + highlight_vertical_padding * 2,
                )
                pygame.draw.rect(self.screen, Colors.PRIMARY, highlight_rect, 0, 6)

                # Draw service text at the exact same position
                self.screen.blit(service_surface, (current_x, y))
                current_x += service_width

            # Draw after text
            if after:
                after_surface = self.font_manager.render_text(after, font_size, Colors.ON_SURFACE)
                self.screen.blit(after_surface, (current_x, y))
        else:
            # Regular line without service highlighting
            clean_line = line.replace("【SERVICE_START】", "").replace("【SERVICE_END】", "")
            if clean_line:
                text_surface = self.font_manager.render_text(
                    clean_line, font_size, Colors.ON_SURFACE
                )
                self.screen.blit(text_surface, (x, y))

    def _draw_metric_card(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        label: str,
        value: str,
        color: Tuple[int, int, int],
        icon: str = "",
    ) -> None:
        """Draw a metric card with proper centered layout"""
        # Card background
        self._draw_modern_card(x, y, width, height, Colors.SURFACE_VARIANT, elevation=True)

        padding = UIConfig.SPACE_MD
        content_width = width - padding * 2

        # Label (centered at top)
        label_surface = self.font_manager.render_text(label, "small", Colors.ON_SURFACE_VARIANT)
        label_x = x + (width - label_surface.get_width()) // 2
        label_y = y + padding
        self.screen.blit(label_surface, (label_x, label_y))

        # Value (centered in middle)
        value_surface = self.font_manager.render_text(value, "game", color)
        value_x = x + (width - value_surface.get_width()) // 2
        value_y = y + (height - value_surface.get_height()) // 2 + padding // 2
        self.screen.blit(value_surface, (value_x, value_y))

    def _calculate_accuracy(self, correct_chars: int, mistakes: int) -> int:
        """Calculate typing accuracy as percentage"""
        total_attempts = correct_chars + mistakes
        if total_attempts == 0:
            return 100
        accuracy = int((1.0 - (mistakes / total_attempts)) * 100)
        return max(0, min(100, accuracy))

    def _draw_wrapped_description(self, description: str, x: int, y: int, max_width: int) -> None:
        """Draw wrapped description text"""
        wrapped_lines = self._wrap_text(description, "score", max_width)
        current_y = y
        line_height = 25

        for line in wrapped_lines:
            if line.strip():  # Skip empty lines
                text_surface = self.font_manager.render_text(
                    line.strip(), "score", Colors.ON_SURFACE_VARIANT
                )
                self.screen.blit(text_surface, (x, current_y))
            current_y += line_height

    def draw_menu(
        self, high_score: int, sfx_enabled: bool = False, music_enabled: bool = False
    ) -> None:
        """Draw the modern main menu screen"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Modern gradient background
        self._draw_gradient_background()

        # Modern header bar
        header_rect = pygame.Rect(0, 0, screen_width, 60)
        pygame.draw.rect(self.screen, Colors.SURFACE, header_rect)
        pygame.draw.rect(self.screen, Colors.PRIMARY, (0, 0, screen_width, 3))

        # Modern AWS logo badge
        logo_text = self.font_manager.render_text("AWS", "score", Colors.ON_SURFACE)
        logo_width = logo_text.get_width()
        logo_height = logo_text.get_height()
        logo_badge = pygame.Rect(
            UIConfig.SPACE_LG,
            (60 - logo_height - 8) // 2,
            logo_width + UIConfig.SPACE_MD,
            logo_height + 8,
        )
        pygame.draw.rect(self.screen, Colors.PRIMARY, logo_badge, 0, 8)
        self.screen.blit(
            logo_text, (UIConfig.SPACE_LG + UIConfig.SPACE_SM, (60 - logo_height) // 2)
        )

        # Hero section card
        hero_width = min(600, screen_width - UIConfig.SPACE_XL * 2)
        hero_height = 400
        hero_x = (screen_width - hero_width) // 2
        hero_y = 120

        hero_card = self._draw_modern_card(
            hero_x, hero_y, hero_width, hero_height, Colors.SURFACE, elevation=True
        )

        # Title with modern typography
        title_y = hero_y + UIConfig.SPACE_XL
        title = self.font_manager.render_text(GameConfig.WINDOW_TITLE, "title", Colors.ON_SURFACE)
        title_x = (screen_width - title.get_width()) // 2
        self.screen.blit(title, (title_x, title_y))

        # Subtitle
        subtitle_y = title_y + 60
        subtitle = self.font_manager.render_text(
            "AWSサービス名のタイピングスキルを向上させよう", "score", Colors.ON_SURFACE_VARIANT
        )
        subtitle_x = (screen_width - subtitle.get_width()) // 2
        self.screen.blit(subtitle, (subtitle_x, subtitle_y))

        # Primary action button
        button_width = 240
        button_x = (screen_width - button_width) // 2
        button_y = subtitle_y + UIConfig.SPACE_XL + UIConfig.SPACE_LG  # Moved down more
        self._draw_modern_button(button_x, button_y, button_width, "スタート", "primary")

        # Stats section
        if high_score > 0:
            stats_y = (
                button_y + UIConfig.BUTTON_HEIGHT + UIConfig.SPACE_XL
            )  # More space between start button and high score

            # High score card
            score_card_width = 200
            score_card_height = 80
            score_card_x = (screen_width - score_card_width) // 2
            score_card_y = stats_y

            self._draw_modern_card(
                score_card_x,
                score_card_y,
                score_card_width,
                score_card_height,
                Colors.SURFACE_VARIANT,
                elevation=False,
            )

            # Score label
            score_label = self.font_manager.render_text(
                "ハイスコア", "small", Colors.ON_SURFACE_VARIANT
            )
            label_x = score_card_x + (score_card_width - score_label.get_width()) // 2
            self.screen.blit(score_label, (label_x, score_card_y + UIConfig.SPACE_MD))

            # Score value
            score_value = self.font_manager.render_text(str(high_score), "game", Colors.PRIMARY)
            value_x = score_card_x + (score_card_width - score_value.get_width()) // 2
            self.screen.blit(score_value, (value_x, score_card_y + UIConfig.SPACE_MD + 20))

        # Audio control buttons
        audio_buttons_y = hero_y + hero_height + UIConfig.SPACE_LG

        # Calculate button layout - wider buttons to fit Japanese text
        button_width = 140  # Increased width for Japanese text
        button_spacing = UIConfig.SPACE_LG  # Increased spacing to prevent overlap
        total_buttons_width = button_width * 2 + button_spacing
        buttons_start_x = (screen_width - total_buttons_width) // 2

        # SFX button
        sfx_button_x = buttons_start_x
        sfx_button_text = f"効果音: {'ON' if sfx_enabled else 'OFF'}"
        sfx_button_style = "primary" if sfx_enabled else "outline"
        self._draw_modern_button(
            sfx_button_x, audio_buttons_y, button_width, sfx_button_text, sfx_button_style
        )

        # Music button
        music_button_x = sfx_button_x + button_width + button_spacing
        music_button_text = f"BGM: {'ON' if music_enabled else 'OFF'}"
        music_button_style = "primary" if music_enabled else "outline"
        self._draw_modern_button(
            music_button_x, audio_buttons_y, button_width, music_button_text, music_button_style
        )

        # Instructions
        instructions_y = audio_buttons_y + UIConfig.BUTTON_HEIGHT + UIConfig.SPACE_MD
        instruction_text = self.font_manager.render_text(
            "スペースキー: スタート  |  F3: 効果音  |  F4: BGM  |  ESC: 終了",
            "small",
            Colors.ON_SURFACE_VARIANT,
        )
        instruction_x = (screen_width - instruction_text.get_width()) // 2
        self.screen.blit(instruction_text, (instruction_x, instructions_y))

        # Modern footer
        footer_height = 40
        footer_y = screen_height - footer_height
        pygame.draw.rect(
            self.screen, Colors.SURFACE_VARIANT, (0, footer_y, screen_width, footer_height)
        )

        version_text = self.font_manager.render_text("v2.0", "small", Colors.ON_SURFACE_VARIANT)
        self.screen.blit(
            version_text,
            (
                screen_width - version_text.get_width() - UIConfig.SPACE_MD,
                footer_y + (footer_height - version_text.get_height()) // 2,
            ),
        )

    def get_menu_button_rects(self, screen_width: int, screen_height: int) -> dict:
        """Get button rectangles for menu screen click detection"""
        hero_width = min(600, screen_width - UIConfig.SPACE_XL * 2)
        hero_height = 400
        hero_x = (screen_width - hero_width) // 2
        hero_y = 120

        # Audio buttons position
        audio_buttons_y = hero_y + hero_height + UIConfig.SPACE_LG
        button_width = 140  # Same as in draw_menu
        button_spacing = UIConfig.SPACE_LG  # Same as in draw_menu
        total_buttons_width = button_width * 2 + button_spacing
        buttons_start_x = (screen_width - total_buttons_width) // 2

        # Calculate start button position (same logic as in draw_menu)
        subtitle_y = hero_y + UIConfig.SPACE_XL + 60
        start_button_y = subtitle_y + UIConfig.SPACE_XL + UIConfig.SPACE_LG

        return {
            "sfx_button": pygame.Rect(
                buttons_start_x, audio_buttons_y, button_width, UIConfig.BUTTON_HEIGHT
            ),
            "music_button": pygame.Rect(
                buttons_start_x + button_width + button_spacing,
                audio_buttons_y,
                button_width,
                UIConfig.BUTTON_HEIGHT,
            ),
            "start_button": pygame.Rect(
                (screen_width - 240) // 2, start_button_y, 240, UIConfig.BUTTON_HEIGHT
            ),
        }

    def draw_game(
        self,
        current_word: str,
        typed_text: str,
        service_name: str,
        score: int,
        mistakes: int,
        remaining_time: float,
        total_chars: int,
        start_time: float,
    ) -> None:
        """Draw the modern main game screen"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Modern dark background for focus
        self.screen.fill(Colors.BACKGROUND)

        # Modern header bar with stats
        header_height = 80
        pygame.draw.rect(self.screen, Colors.SURFACE, (0, 0, screen_width, header_height))
        pygame.draw.rect(self.screen, Colors.PRIMARY, (0, 0, screen_width, 3))

        # Time display with modern circular progress
        time_x = UIConfig.SPACE_LG
        time_y = UIConfig.SPACE_MD
        time_ratio = remaining_time / GameConfig.TIME_LIMIT

        # Time card
        time_card_width = 160
        time_card_height = 50
        self._draw_modern_card(
            time_x,
            time_y,
            time_card_width,
            time_card_height,
            Colors.SURFACE_VARIANT,
            elevation=False,
        )

        time_label = self.font_manager.render_text("時間", "small", Colors.ON_SURFACE_VARIANT)
        self.screen.blit(time_label, (time_x + UIConfig.SPACE_SM, time_y + 8))

        time_value = self.font_manager.render_text(
            f"{int(remaining_time)}s", "score", Colors.ON_SURFACE
        )
        self.screen.blit(time_value, (time_x + UIConfig.SPACE_SM, time_y + 24))

        # Time progress bar (modern style)
        progress_x = time_x + 80
        progress_y = time_y + 20
        progress_width = 65
        bar_color = (
            Colors.SUCCESS
            if time_ratio > 0.5
            else Colors.WARNING
            if time_ratio > 0.2
            else Colors.ERROR
        )
        self._draw_progress_bar(progress_x, progress_y, progress_width, time_ratio, bar_color)

        # Score card
        score_card_width = 120
        score_x = screen_width - score_card_width - UIConfig.SPACE_LG
        self._draw_modern_card(
            score_x,
            time_y,
            score_card_width,
            time_card_height,
            Colors.SURFACE_VARIANT,
            elevation=False,
        )

        score_label = self.font_manager.render_text("スコア", "small", Colors.ON_SURFACE_VARIANT)
        self.screen.blit(score_label, (score_x + UIConfig.SPACE_SM, time_y + 8))

        score_value = self.font_manager.render_text(str(score), "score", Colors.PRIMARY)
        self.screen.blit(score_value, (score_x + UIConfig.SPACE_SM, time_y + 24))

        # Mistakes indicator
        if mistakes > 0:
            mistakes_card_width = 80
            mistakes_x = score_x - mistakes_card_width - UIConfig.SPACE_MD
            self._draw_modern_card(
                mistakes_x,
                time_y,
                mistakes_card_width,
                time_card_height,
                Colors.ERROR,
                elevation=False,
            )

            mistakes_label = self.font_manager.render_text("ミス", "small", Colors.ON_SURFACE)
            self.screen.blit(mistakes_label, (mistakes_x + UIConfig.SPACE_SM, time_y + 8))

            mistakes_value = self.font_manager.render_text(
                str(mistakes), "score", Colors.ON_SURFACE
            )
            self.screen.blit(mistakes_value, (mistakes_x + UIConfig.SPACE_SM, time_y + 24))

        # Main typing panel with dynamic sizing
        panel_margin = min(UIConfig.PANEL_MARGIN, screen_width // 3)
        panel_width = panel_margin * 2

        # Calculate required height based on content
        # Quick calculation for text height to determine panel size
        clean_word = current_word.replace("<", "").replace(">", "")
        test_surface = self.font_manager.render_text(clean_word, "game", Colors.ON_SURFACE)
        text_display_width = panel_width - UIConfig.CARD_PADDING * 2

        # Estimate number of lines needed
        if test_surface.get_width() > text_display_width:
            estimated_lines = (test_surface.get_width() // text_display_width) + 1
        else:
            estimated_lines = 1

        # Calculate minimum panel height needed
        line_height = test_surface.get_height() + 4
        text_area_height = estimated_lines * line_height

        # Total content height calculation
        header_card_height = 50
        content_spacing = UIConfig.SPACE_LG  # After header
        sentence_label_height = 20
        text_spacing = 30  # After label
        input_spacing = UIConfig.SPACE_MD  # After text
        input_height = UIConfig.INPUT_FIELD_HEIGHT
        stats_spacing = UIConfig.SPACE_LG  # After input
        stats_height = 80  # Progress + metrics
        bottom_padding = UIConfig.CARD_PADDING

        required_height = (
            header_card_height
            + content_spacing
            + sentence_label_height
            + text_spacing
            + text_area_height
            + input_spacing
            + input_height
            + stats_spacing
            + stats_height
            + bottom_padding
        )

        # Set panel height with minimum and maximum bounds
        min_panel_height = 350
        max_panel_height = screen_height - 160  # Leave space for header and footer
        panel_height = max(min_panel_height, min(required_height, max_panel_height))

        panel_x = (screen_width - panel_width) // 2
        panel_y = header_height + UIConfig.SPACE_XL

        # Modern main card
        main_card = self._draw_modern_card(
            panel_x, panel_y, panel_width, panel_height, Colors.SURFACE, elevation=True
        )

        # Card header
        header_height_card = 50
        pygame.draw.rect(
            self.screen,
            Colors.SURFACE_BRIGHT,
            (panel_x, panel_y, panel_width, header_height_card),
            0,
            UIConfig.CARD_RADIUS,
            UIConfig.CARD_RADIUS,
            0,
            0,
        )

        panel_title = self.font_manager.render_text(
            "AWS サービス タイピング", "score", Colors.ON_SURFACE
        )
        title_x = panel_x + (panel_width - panel_title.get_width()) // 2
        self.screen.blit(panel_title, (title_x, panel_y + UIConfig.SPACE_MD))

        # Content area
        content_y = panel_y + header_height_card + UIConfig.SPACE_LG

        # Target sentence display
        sentence_label = self.font_manager.render_text(
            "入力する文章:", "small", Colors.ON_SURFACE_VARIANT
        )
        self.screen.blit(sentence_label, (panel_x + UIConfig.CARD_PADDING, content_y))

        # Enhanced word display with better highlighting and dynamic sizing
        word_y = content_y + 30
        text_display_width = panel_width - UIConfig.CARD_PADDING * 2
        text_height_used = self._draw_enhanced_word(
            current_word, service_name, panel_x + UIConfig.CARD_PADDING, word_y, text_display_width
        )

        # Modern input field - position based on actual text height
        input_y = word_y + max(text_height_used, 40) + UIConfig.SPACE_MD
        input_width = panel_width - UIConfig.CARD_PADDING * 2
        input_rect = pygame.Rect(
            panel_x + UIConfig.CARD_PADDING, input_y, input_width, UIConfig.INPUT_FIELD_HEIGHT
        )

        # Input field background with state-based styling
        input_bg_color = Colors.SURFACE_VARIANT
        if len(typed_text) > 0:
            # Check if typing is correct
            clean_current_word = current_word.replace("<", "").replace(">", "")
            is_correct = True
            for i, char in enumerate(typed_text):
                if i >= len(clean_current_word) or char != clean_current_word[i]:
                    is_correct = False
                    break
            input_bg_color = Colors.SURFACE_BRIGHT if is_correct else Colors.SURFACE_VARIANT

        pygame.draw.rect(self.screen, input_bg_color, input_rect, 0, 8)

        # Input border with state indication
        border_color = Colors.PRIMARY if len(typed_text) > 0 else Colors.ON_SURFACE_VARIANT
        pygame.draw.rect(self.screen, border_color, input_rect, 2, 8)

        # Input text with better typography and overflow protection
        text_x = input_rect.x + UIConfig.SPACE_MD
        text_y = input_rect.y + (UIConfig.INPUT_FIELD_HEIGHT - 24) // 2
        available_text_width = input_width - UIConfig.SPACE_MD * 2

        if len(typed_text) > 0:
            typed_surface = self.font_manager.render_text(typed_text, "score", Colors.ON_SURFACE)

            # Check if text fits within input field
            if typed_surface.get_width() <= available_text_width:
                # Text fits, draw normally
                self.screen.blit(typed_surface, (text_x, text_y))
            else:
                # Text is too long, implement smart scrolling
                # Show the most recent characters (right side) while maintaining readability
                overflow = typed_surface.get_width() - available_text_width

                # Create a clipping rectangle for the input field text area
                clip_rect = pygame.Rect(
                    text_x, text_y, available_text_width, typed_surface.get_height()
                )

                # Set clipping area to prevent text from drawing outside input field
                original_clip = self.screen.get_clip()
                self.screen.set_clip(clip_rect)

                # Calculate scroll offset to show the typing cursor area
                # Keep some padding so user can see a bit of context
                padding = min(50, available_text_width // 4)  # Show some context
                scroll_offset = -(overflow + padding)
                scroll_offset = max(scroll_offset, -overflow)  # Don't scroll too far

                self.screen.blit(typed_surface, (text_x + scroll_offset, text_y))

                # Restore original clipping
                self.screen.set_clip(original_clip)

                # Add subtle scroll indicator to show there's more text to the left
                if scroll_offset < 0:
                    indicator_x = text_x + 2
                    indicator_y = text_y + typed_surface.get_height() // 2
                    pygame.draw.circle(
                        self.screen, Colors.ON_SURFACE_VARIANT, (indicator_x, indicator_y), 2
                    )
        else:
            placeholder = self.font_manager.render_text(
                "ここにタイプしてください...", "score", Colors.DISABLED
            )
            # Ensure placeholder also doesn't overflow
            if placeholder.get_width() <= available_text_width:
                self.screen.blit(placeholder, (text_x, text_y))
            else:
                # Truncate placeholder if needed
                shorter_placeholder = self.font_manager.render_text(
                    "入力してください...", "score", Colors.DISABLED
                )
                self.screen.blit(shorter_placeholder, (text_x, text_y))

        # Real-time feedback indicator
        if len(typed_text) > 0:
            clean_current_word = current_word.replace("<", "").replace(">", "")
            feedback_color = Colors.SUCCESS
            for i, char in enumerate(typed_text):
                if i >= len(clean_current_word) or char != clean_current_word[i]:
                    feedback_color = Colors.ERROR
                    break

            # Modern feedback bar
            feedback_y = input_y + UIConfig.INPUT_FIELD_HEIGHT + 4
            feedback_height = 3
            pygame.draw.rect(
                self.screen,
                feedback_color,
                (input_rect.x, feedback_y, input_width, feedback_height),
                0,
                2,
            )

        # Statistics section
        stats_y = input_y + UIConfig.INPUT_FIELD_HEIGHT + UIConfig.SPACE_LG

        # Character progress
        clean_current_word = current_word.replace("<", "").replace(">", "")
        char_progress = len(typed_text) / max(len(clean_current_word), 1)

        progress_label = self.font_manager.render_text(
            f"進捗: {len(typed_text)} / {len(clean_current_word)}",
            "small",
            Colors.ON_SURFACE_VARIANT,
        )
        self.screen.blit(progress_label, (panel_x + UIConfig.CARD_PADDING, stats_y))

        # Progress bar
        progress_bar_y = stats_y + 20
        progress_bar_width = panel_width - UIConfig.CARD_PADDING * 2
        self._draw_progress_bar(
            panel_x + UIConfig.CARD_PADDING,
            progress_bar_y,
            progress_bar_width,
            char_progress,
            Colors.PRIMARY,
        )

        # Performance metrics
        import time

        elapsed_time = max(0.1, time.time() - start_time)
        current_cpm = int(total_chars / (elapsed_time / 60))

        metrics_y = progress_bar_y + UIConfig.SPACE_LG

        # WPM display (based on correct characters)
        wpm_text = self.font_manager.render_text(
            f"速度: {score} WPM", "small", Colors.ON_SURFACE_VARIANT
        )
        self.screen.blit(wpm_text, (panel_x + UIConfig.CARD_PADDING, metrics_y))

        # Evaluation badge
        evaluation, eval_color = self._get_evaluation(score)
        eval_text = self.font_manager.render_text(evaluation, "small", Colors.ON_SURFACE)
        eval_width = eval_text.get_width() + UIConfig.SPACE_MD
        eval_height = 24

        eval_x = panel_x + panel_width - UIConfig.CARD_PADDING - eval_width
        eval_rect = pygame.Rect(eval_x, metrics_y - 2, eval_width, eval_height)
        pygame.draw.rect(self.screen, eval_color, eval_rect, 0, 6)

        text_x = eval_x + (eval_width - eval_text.get_width()) // 2
        text_y = metrics_y + (eval_height - eval_text.get_height()) // 2 - 2
        self.screen.blit(eval_text, (text_x, text_y))

        # Help text
        help_y = panel_y + panel_height + UIConfig.SPACE_MD
        help_text = self.font_manager.render_text(
            "Enter: 確定  |  ESC: メニューに戻る", "small", Colors.ON_SURFACE_VARIANT
        )
        help_x = (screen_width - help_text.get_width()) // 2
        self.screen.blit(help_text, (help_x, help_y))

        # Modern footer
        footer_height = 30
        footer_y = screen_height - footer_height
        pygame.draw.rect(self.screen, Colors.SURFACE, (0, footer_y, screen_width, footer_height))

    def draw_game_over(
        self,
        score: int,
        high_score: int,
        total_chars: int,
        start_time: float,
        answered_services: List[str],
        correct_chars: int = 0,
        mistakes: int = 0,
    ) -> None:
        """Draw the modern game over/results screen"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Modern gradient background
        self._draw_gradient_background()

        # Modern header bar
        header_rect = pygame.Rect(0, 0, screen_width, 60)
        pygame.draw.rect(self.screen, Colors.SURFACE, header_rect)
        pygame.draw.rect(self.screen, Colors.SUCCESS, (0, 0, screen_width, 3))

        # Header title without icon
        header_title = self.font_manager.render_text("結果発表", "title", Colors.ON_SURFACE)
        title_x = max(UIConfig.SPACE_MD, (screen_width - header_title.get_width()) // 2)
        self.screen.blit(header_title, (title_x, 80))

        # Calculate performance metrics
        import time

        elapsed_time = min(GameConfig.TIME_LIMIT, time.time() - start_time)
        cpm = 0 if elapsed_time == 0 else int(total_chars / (elapsed_time / 60))
        evaluation, eval_color = self._get_evaluation(score)
        accuracy = self._calculate_accuracy(correct_chars, mistakes)

        # Main results container with proper bounds checking
        container_width = min(800, screen_width - UIConfig.SPACE_XL * 2)
        container_x = max(UIConfig.SPACE_MD, (screen_width - container_width) // 2)
        container_y = 160

        # Calculate available height for content
        available_height = screen_height - container_y - 60  # Leave space for footer

        # Performance summary cards row with proper spacing
        cards_y = container_y
        card_spacing = UIConfig.SPACE_MD
        total_spacing = card_spacing * 2  # Space between 3 cards
        card_width = max(150, (container_width - total_spacing) // 3)
        card_height = min(120, available_height // 4)  # Adjust based on available space

        # Score card
        score_card_x = container_x
        self._draw_metric_card(
            score_card_x, cards_y, card_width, card_height, "スコア", str(score), Colors.PRIMARY, ""
        )

        # Accuracy card
        wpm_card_x = score_card_x + card_width + card_spacing
        self._draw_metric_card(
            wpm_card_x, cards_y, card_width, card_height, "正答率", f"{accuracy}%", Colors.INFO, ""
        )

        # Level card
        level_card_x = wpm_card_x + card_width + card_spacing
        self._draw_metric_card(
            level_card_x, cards_y, card_width, card_height, "レベル", evaluation, eval_color, ""
        )

        # Detailed results panel with dynamic sizing
        panel_y = cards_y + card_height + UIConfig.SPACE_LG
        remaining_height = (
            available_height - card_height - UIConfig.SPACE_LG * 3 - UIConfig.BUTTON_HEIGHT - 60
        )
        panel_height = max(200, min(280, remaining_height))

        main_panel = self._draw_modern_card(
            container_x, panel_y, container_width, panel_height, Colors.SURFACE, elevation=True
        )

        # Panel header
        header_height = 50
        pygame.draw.rect(
            self.screen,
            Colors.SURFACE_BRIGHT,
            (container_x, panel_y, container_width, header_height),
            0,
            UIConfig.CARD_RADIUS,
            UIConfig.CARD_RADIUS,
            0,
            0,
        )

        panel_title = self.font_manager.render_text("詳細結果", "score", Colors.ON_SURFACE)
        title_x = max(
            container_x + UIConfig.SPACE_MD,
            container_x + (container_width - panel_title.get_width()) // 2,
        )
        self.screen.blit(panel_title, (title_x, panel_y + UIConfig.SPACE_MD))

        # Results content
        content_y = panel_y + header_height + UIConfig.SPACE_LG
        content_x = container_x + UIConfig.CARD_PADDING

        # High score comparison
        if score >= high_score:
            # New record
            record_text = "新記録達成！"
            record_color = Colors.SUCCESS
            record_surface = self.font_manager.render_text(record_text, "game", record_color)
            self.screen.blit(record_surface, (content_x, content_y))

            high_score_detail = self.font_manager.render_text(
                f"前回記録: {high_score} → 今回: {score}", "score", Colors.ON_SURFACE_VARIANT
            )
            self.screen.blit(high_score_detail, (content_x, content_y + 35))
        else:
            # Existing record
            current_text = f"今回のスコア: {score}"
            current_surface = self.font_manager.render_text(
                current_text, "score", Colors.ON_SURFACE
            )
            self.screen.blit(current_surface, (content_x, content_y))

            record_text = f"最高記録: {high_score}"
            record_surface = self.font_manager.render_text(
                record_text, "score", Colors.ON_SURFACE_VARIANT
            )
            self.screen.blit(record_surface, (content_x, content_y + 25))

        # Performance breakdown - only show if there's enough space
        breakdown_y = content_y + 70

        # Check if we have enough space for metrics
        available_metric_space = panel_y + panel_height - breakdown_y - UIConfig.SPACE_MD
        if available_metric_space > 100:  # Only show metrics if we have enough space
            # Progress bars for metrics
            metrics = [
                ("入力文字数", total_chars, 200, Colors.PRIMARY),
                ("正確性", accuracy, 100, Colors.SUCCESS),
                ("速度レベル", min(cpm, 300), 300, Colors.INFO),
            ]

            # Calculate metric spacing to fit available space
            metric_spacing = min(35, available_metric_space // 3)

            for i, (label, value, max_val, color) in enumerate(metrics):
                metric_y = breakdown_y + i * metric_spacing

                # Skip if would overflow panel
                if metric_y + 25 > panel_y + panel_height - UIConfig.SPACE_MD:
                    break

                # Label
                label_surface = self.font_manager.render_text(
                    label, "small", Colors.ON_SURFACE_VARIANT
                )
                self.screen.blit(label_surface, (content_x, metric_y))

                # Value
                if label == "正確性":
                    value_text = f"{value}%"
                else:
                    value_text = str(value)
                value_surface = self.font_manager.render_text(
                    value_text, "small", Colors.ON_SURFACE
                )
                value_x = content_x + 100
                self.screen.blit(value_surface, (value_x, metric_y))

                # Progress bar
                bar_x = content_x + 180
                bar_width = max(100, container_width - UIConfig.CARD_PADDING * 2 - 180)
                progress = min(value / max_val, 1.0)
                self._draw_progress_bar(bar_x, metric_y + 4, min(bar_width, 150), progress, color)

        # Controls help - ensure it fits on screen
        controls_y = panel_y + panel_height + UIConfig.SPACE_LG
        controls_text = self.font_manager.render_text(
            "スペース: 再挑戦  |  I: サービス情報  |  ESC: メニュー",
            "small",
            Colors.ON_SURFACE_VARIANT,
        )
        controls_x = max(UIConfig.SPACE_MD, (screen_width - controls_text.get_width()) // 2)

        # Only show if it fits on screen
        if controls_y + 20 < screen_height - 40:
            self.screen.blit(controls_text, (controls_x, controls_y))

        # Modern footer
        footer_height = 30
        footer_y = screen_height - footer_height
        pygame.draw.rect(self.screen, Colors.SURFACE, (0, footer_y, screen_width, footer_height))

    def draw_service_info(
        self,
        answered_services: List[str],
        current_service_index: int,
        service_description: str,
        example_sentence: str,
        translation: str,
    ) -> None:
        """Draw the modern service information screen"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Modern gradient background
        self._draw_gradient_background()

        # Modern header bar
        header_rect = pygame.Rect(0, 0, screen_width, 60)
        pygame.draw.rect(self.screen, Colors.SURFACE, header_rect)
        pygame.draw.rect(self.screen, Colors.INFO, (0, 0, screen_width, 3))

        # Header title with safe text
        header_title = self.font_manager.render_text("AWS サービス情報", "score", Colors.ON_SURFACE)
        title_x = max(UIConfig.SPACE_MD, UIConfig.SPACE_LG)
        self.screen.blit(header_title, (title_x, 20))

        # Service counter badge
        if len(answered_services) > 0:
            counter_text = f"{len(answered_services)} サービス"
            counter_surface = self.font_manager.render_text(
                counter_text, "small", Colors.ON_SURFACE
            )
            counter_width = counter_surface.get_width() + UIConfig.SPACE_MD
            counter_height = 24
            counter_x = screen_width - counter_width - UIConfig.SPACE_LG
            counter_y = (60 - counter_height) // 2

            # Counter badge
            counter_rect = pygame.Rect(counter_x, counter_y, counter_width, counter_height)
            pygame.draw.rect(self.screen, Colors.INFO, counter_rect, 0, 6)
            text_x = counter_x + (counter_width - counter_surface.get_width()) // 2
            text_y = counter_y + (counter_height - counter_surface.get_height()) // 2
            self.screen.blit(counter_surface, (text_x, text_y))

        # Check if no services
        if len(answered_services) == 0:
            # Empty state
            empty_card_width = 400
            empty_card_height = 200
            empty_card_x = (screen_width - empty_card_width) // 2
            empty_card_y = (screen_height - empty_card_height) // 2

            self._draw_modern_card(
                empty_card_x,
                empty_card_y,
                empty_card_width,
                empty_card_height,
                Colors.SURFACE,
                elevation=True,
            )

            # Empty state text (removed problematic emoji)
            empty_text_y = empty_card_y + 60

            empty_text = self.font_manager.render_text(
                "回答したサービスがありません", "game", Colors.ON_SURFACE_VARIANT
            )
            text_x = empty_card_x + (empty_card_width - empty_text.get_width()) // 2
            self.screen.blit(empty_text, (text_x, empty_text_y))

            back_text = self.font_manager.render_text(
                "ESCキーで戻る", "score", Colors.ON_SURFACE_VARIANT
            )
            back_x = empty_card_x + (empty_card_width - back_text.get_width()) // 2
            self.screen.blit(back_text, (back_x, empty_card_y + 140))
            return

        current_service = answered_services[current_service_index]

        # Main content container with safe positioning
        container_width = min(900, screen_width - UIConfig.SPACE_XL * 2)
        container_x = max(UIConfig.SPACE_MD, (screen_width - container_width) // 2)
        container_y = 100

        # Calculate available height for content
        available_height = screen_height - container_y - 80  # Leave space for footer and controls

        # Service title card
        title_card_height = 80
        title_card = self._draw_modern_card(
            container_x,
            container_y,
            container_width,
            title_card_height,
            Colors.PRIMARY,
            elevation=True,
        )

        # Service title without problematic icons
        service_title = self.font_manager.render_text(
            f"AWS {current_service}", "game", Colors.ON_SURFACE
        )
        title_text_x = container_x + UIConfig.SPACE_LG
        self.screen.blit(service_title, (title_text_x, container_y + 25))

        # Page indicator
        page_indicator = self.font_manager.render_text(
            f"{current_service_index + 1}/{len(answered_services)}", "small", Colors.ON_SURFACE
        )
        page_x = container_x + container_width - page_indicator.get_width() - UIConfig.SPACE_LG
        self.screen.blit(page_indicator, (page_x, container_y + 30))

        # Description card with dynamic sizing
        desc_card_y = container_y + title_card_height + UIConfig.SPACE_MD
        desc_card_height = min(120, available_height // 4)
        desc_card = self._draw_modern_card(
            container_x,
            desc_card_y,
            container_width,
            desc_card_height,
            Colors.SURFACE,
            elevation=True,
        )

        # Description header
        desc_header_height = 40
        pygame.draw.rect(
            self.screen,
            Colors.SURFACE_BRIGHT,
            (container_x, desc_card_y, container_width, desc_header_height),
            0,
            UIConfig.CARD_RADIUS,
            UIConfig.CARD_RADIUS,
            0,
            0,
        )

        desc_header = self.font_manager.render_text("サービス説明", "score", Colors.ON_SURFACE)
        self.screen.blit(desc_header, (container_x + UIConfig.CARD_PADDING, desc_card_y + 12))

        # Description content
        desc_content_y = desc_card_y + desc_header_height + UIConfig.SPACE_MD
        desc_content_width = container_width - UIConfig.CARD_PADDING * 2
        self._draw_wrapped_description(
            service_description,
            container_x + UIConfig.CARD_PADDING,
            desc_content_y,
            desc_content_width,
        )

        # Example sentence card with proper sizing for Japanese text
        example_card_y = desc_card_y + desc_card_height + UIConfig.SPACE_MD
        remaining_height = (
            available_height
            - title_card_height
            - desc_card_height
            - UIConfig.SPACE_MD * 4
            - UIConfig.BUTTON_HEIGHT
            - 60
        )

        # Define header height first
        example_header_height = 40

        # Calculate required height for content (header + English + Japanese + padding)
        # More generous height calculation to ensure Japanese text fits
        base_content_height = (
            25 + 45 + UIConfig.SPACE_MD + 25 + 35
        )  # English label + text + space + JP label + text
        required_height = (
            example_header_height + UIConfig.SPACE_MD + base_content_height + UIConfig.SPACE_MD
        )  # ~180px

        # Reserve space for navigation controls (buttons + help + controls + footer)
        reserved_bottom_space = UIConfig.BUTTON_HEIGHT * 2 + 60 + 80  # Conservative estimate
        max_allowed_height = remaining_height - reserved_bottom_space

        example_card_height = max(required_height, min(max_allowed_height, 220))
        example_card = self._draw_modern_card(
            container_x,
            example_card_y,
            container_width,
            example_card_height,
            Colors.SURFACE,
            elevation=True,
        )

        # Example header
        pygame.draw.rect(
            self.screen,
            Colors.SURFACE_BRIGHT,
            (container_x, example_card_y, container_width, example_header_height),
            0,
            UIConfig.CARD_RADIUS,
            UIConfig.CARD_RADIUS,
            0,
            0,
        )

        example_header = self.font_manager.render_text("タイピング例文", "score", Colors.ON_SURFACE)
        self.screen.blit(example_header, (container_x + UIConfig.CARD_PADDING, example_card_y + 12))

        # Example content
        if example_sentence:
            content_y = example_card_y + example_header_height + UIConfig.SPACE_MD
            content_x = container_x + UIConfig.CARD_PADDING

            # English sentence
            en_label = self.font_manager.render_text("English:", "small", Colors.INFO)
            self.screen.blit(en_label, (content_x, content_y))

            # Enhanced word display with highlighting
            sentence_y = content_y + 25
            sentence_width = container_width - UIConfig.CARD_PADDING * 2
            english_height_used = self._draw_enhanced_word(
                example_sentence, current_service, content_x, sentence_y, sentence_width
            )

            # Japanese translation - positioned dynamically based on English text height
            if translation:
                jp_y = sentence_y + max(english_height_used, 40) + UIConfig.SPACE_MD

                # Check if Japanese section fits within card bounds
                if jp_y + 50 <= example_card_y + example_card_height - UIConfig.SPACE_MD:
                    jp_label = self.font_manager.render_text("日本語:", "small", Colors.SUCCESS)
                    self.screen.blit(jp_label, (content_x, jp_y))

                    jp_text_y = jp_y + 25
                    # Check if text fits, if not wrap it
                    jp_surface = self.font_manager.render_text(
                        translation, "score", Colors.ON_SURFACE_VARIANT
                    )
                    if (
                        content_x + jp_surface.get_width()
                        <= container_x + container_width - UIConfig.CARD_PADDING
                    ):
                        self.screen.blit(jp_surface, (content_x, jp_text_y))
                    else:
                        # Wrap Japanese text if it's too long
                        max_jp_width = container_width - UIConfig.CARD_PADDING * 2
                        self._draw_wrapped_description(
                            translation, content_x, jp_text_y, max_jp_width
                        )

        # Navigation controls - ensure they fit on screen
        available_bottom_space = (
            screen_height - (example_card_y + example_card_height) - 60
        )  # Reserve space for footer

        # Calculate required space for navigation
        nav_button_height = UIConfig.BUTTON_HEIGHT
        nav_help_height = 25 if len(answered_services) > 1 else 0
        back_button_height = UIConfig.BUTTON_HEIGHT
        controls_height = 20
        total_nav_height = (
            nav_button_height
            + nav_help_height
            + UIConfig.SPACE_MD
            + back_button_height
            + UIConfig.SPACE_MD
            + controls_height
        )

        # Adjust spacing if content doesn't fit
        if total_nav_height > available_bottom_space:
            nav_spacing = max(
                UIConfig.SPACE_SM,
                (available_bottom_space - nav_button_height - back_button_height - controls_height)
                // 3,
            )
        else:
            nav_spacing = UIConfig.SPACE_LG

        nav_y = example_card_y + example_card_height + nav_spacing

        if len(answered_services) > 1:
            # Previous button
            if current_service_index > 0:
                prev_button_width = 120
                self._draw_modern_button(container_x, nav_y, prev_button_width, "< 前へ", "outline")
                prev_help = self.font_manager.render_text(
                    "Aキー", "small", Colors.ON_SURFACE_VARIANT
                )
                self.screen.blit(prev_help, (container_x, nav_y + UIConfig.BUTTON_HEIGHT + 5))

            # Next button
            if current_service_index < len(answered_services) - 1:
                next_button_width = 120
                next_button_x = container_x + container_width - next_button_width
                self._draw_modern_button(
                    next_button_x, nav_y, next_button_width, "次へ >", "outline"
                )
                next_help = self.font_manager.render_text(
                    "Dキー", "small", Colors.ON_SURFACE_VARIANT
                )
                next_help_x = next_button_x + next_button_width - next_help.get_width()
                self.screen.blit(next_help, (next_help_x, nav_y + UIConfig.BUTTON_HEIGHT + 5))

        # Back button - ensure it's visible on screen
        back_button_width = 140
        back_button_x = (screen_width - back_button_width) // 2
        back_button_y = nav_y + (
            nav_button_height + nav_help_height + nav_spacing if len(answered_services) > 1 else 0
        )

        # Ensure back button fits on screen
        max_back_button_y = (
            screen_height - UIConfig.BUTTON_HEIGHT - 40
        )  # Leave space for controls and footer
        back_button_y = min(back_button_y, max_back_button_y)

        self._draw_modern_button(back_button_x, back_button_y, back_button_width, "戻る", "primary")

        # Controls help - ensure it fits on screen
        controls_y = back_button_y + UIConfig.BUTTON_HEIGHT + UIConfig.SPACE_MD
        controls_text = self.font_manager.render_text(
            "A/D: ナビゲーション  |  ESC: 結果画面に戻る", "small", Colors.ON_SURFACE_VARIANT
        )
        controls_x = max(UIConfig.SPACE_MD, (screen_width - controls_text.get_width()) // 2)

        # Only show if it fits on screen
        if controls_y + 20 < screen_height - 40:
            self.screen.blit(controls_text, (controls_x, controls_y))

        # Modern footer
        footer_height = 30
        footer_y = screen_height - footer_height
        pygame.draw.rect(self.screen, Colors.SURFACE, (0, footer_y, screen_width, footer_height))

    def _draw_highlighted_word(self, word: str, service_name: str, y_pos: int) -> None:
        """Draw word with highlighted service name"""
        if service_name:
            clean_word = word.replace("<", "").replace(">", "")
            service_start = clean_word.find(service_name)

            if service_start != -1:
                service_end = service_start + len(service_name)

                before_service = clean_word[:service_start]
                service = clean_word[service_start:service_end]
                after_service = clean_word[service_end:]

                before_text = self.font_manager.render_text(before_service, "score", Colors.WHITE)
                service_text = self.font_manager.render_text(service, "score", Colors.ORANGE)
                after_text = self.font_manager.render_text(after_service, "score", Colors.WHITE)

                total_width = (
                    before_text.get_width() + service_text.get_width() + after_text.get_width()
                )
                start_x = GameConfig.WIDTH // 2 - total_width // 2

                self.screen.blit(before_text, (start_x, y_pos))
                self.screen.blit(service_text, (start_x + before_text.get_width(), y_pos))
                self.screen.blit(
                    after_text,
                    (start_x + before_text.get_width() + service_text.get_width(), y_pos),
                )
            else:
                word_text = self.font_manager.render_text(clean_word, "score", Colors.WHITE)
                self.screen.blit(
                    word_text, (GameConfig.WIDTH // 2 - word_text.get_width() // 2, y_pos)
                )
        else:
            word_text = self.font_manager.render_text(word, "score", Colors.WHITE)
            self.screen.blit(word_text, (GameConfig.WIDTH // 2 - word_text.get_width() // 2, y_pos))

    def _draw_multiline_text(
        self, text: str, x: int, y: int, max_width: int, font_type: str, color: tuple
    ) -> int:
        """Draw multiline text and return the final y position"""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            test_width = self.font_manager.get_text_size(test_line, font_type)[0]
            if test_width < max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word + " "

        if current_line:
            lines.append(current_line)

        current_y = y
        for line in lines:
            line_text = self.font_manager.render_text(line, font_type, color)
            self.screen.blit(line_text, (x, current_y))
            current_y += 30

        return current_y

    def _get_evaluation(self, score: int) -> Tuple[str, tuple]:
        """Get evaluation level and color based on score"""
        for level, config in EvaluationConfig.LEVELS.items():
            if score >= config["threshold"]:
                return level, config["color"]
        return "Foundational", EvaluationConfig.LEVELS["Foundational"]["color"]
