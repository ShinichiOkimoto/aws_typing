"""
Game logic module for AWS Service Typing Game
"""

import random
import re
import time

from ..managers.data_manager import DataManager
from .config import EvaluationConfig, GameConfig


class Game:
    """Main game logic and state management"""

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.audio_manager = None
        self.animation_manager = None
        self.reset_game()
        self.game_state = "menu"  # menu, playing, game_over, service_info
        self.answered_services = []
        self.current_service_index = 0
        self.current_service_name = ""
        self.total_chars = 0

    def set_audio_manager(self, audio_manager):
        """Set the audio manager"""
        self.audio_manager = audio_manager

    def set_animation_manager(self, animation_manager):
        """Set the animation manager"""
        self.animation_manager = animation_manager

    def reset_game(self) -> None:
        """Reset game state for a new game"""
        self.current_word = ""
        self.typed_text = ""
        self.score = 0
        self.mistakes = 0
        self.start_time = time.time()
        self.answered_services = []
        self.total_chars = 0
        self.correct_chars = 0  # 正解した文字数を追跡
        self.select_new_word()

    def select_new_word(self) -> None:
        """Select a new random sentence"""
        sentences = self.data_manager.get_all_sentences()
        if sentences:
            self.current_word = random.choice(sentences)
        else:
            # Fallback sentence if no data is available
            self.current_word = "My <EC2> instance is having an identity crisis"

        self.typed_text = ""

        # Extract service name from brackets
        service_match = re.search(r"<([^>]+)>", self.current_word)
        if service_match:
            self.current_service_name = service_match.group(1)
        else:
            self.current_service_name = ""

    def update(self, events, ignore_space: bool = False) -> None:
        """Update game state during gameplay"""
        remaining_time = max(0, GameConfig.TIME_LIMIT - (time.time() - self.start_time))

        if remaining_time <= 0:
            self._end_game()
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "menu"
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.typed_text) > 0:
                        self.typed_text = self.typed_text[:-1]
                        # Adjust correct_chars count when backspacing
                        if self.correct_chars > 0:
                            self.correct_chars -= 1
                elif event.key == pygame.K_RETURN:
                    self._check_answer()
                # Ignore modifier keys (Shift, Ctrl, Alt, etc.)
                elif event.key in [
                    pygame.K_LSHIFT,
                    pygame.K_RSHIFT,
                    pygame.K_LCTRL,
                    pygame.K_RCTRL,
                    pygame.K_LALT,
                    pygame.K_RALT,
                    pygame.K_LMETA,
                    pygame.K_RMETA,
                    pygame.K_CAPSLOCK,
                    pygame.K_NUMLOCK,
                    pygame.K_SCROLLOCK,
                ]:
                    # Do nothing for modifier keys
                    pass
                elif (
                    event.unicode
                    and event.unicode.isprintable()
                    and not (ignore_space and event.key == pygame.K_SPACE)
                ):
                    # Check if the new character is correct before adding
                    clean_current_word = self.current_word.replace("<", "").replace(">", "")
                    current_pos = len(self.typed_text)

                    if (
                        current_pos < len(clean_current_word)
                        and event.unicode == clean_current_word[current_pos]
                    ):
                        # Correct character
                        self.typed_text += event.unicode
                        self.correct_chars += 1  # 正解文字数をカウント
                        # Play typing sound
                        if self.audio_manager:
                            self.audio_manager.play_typing_sound()
                        # Create typing particle effect
                        if self.animation_manager:
                            self.animation_manager.add_particle_effect(
                                400, 300, (100, 150, 255), "typing"
                            )

                        # Check if word is complete
                        if self.typed_text == clean_current_word:
                            # Automatically proceed to next word without pressing Enter
                            self._complete_word()
                    else:
                        # Wrong character - increment mistakes
                        self.mistakes += 1
                        # Play error sound
                        if self.audio_manager:
                            self.audio_manager.play_error_sound()
                        # Create error particle effect
                        if self.animation_manager:
                            self.animation_manager.add_particle_effect(
                                400, 300, (255, 0, 0), "error"
                            )

    def handle_menu_events(self, events) -> None:
        """Handle events in menu state"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.game_state = "playing"

    def handle_game_over_events(self, events) -> None:
        """Handle events in game over state"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.game_state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = "menu"
                elif event.key == pygame.K_i and len(self.answered_services) > 0:
                    self.current_service_index = 0
                    self.game_state = "service_info"

    def handle_service_info_events(self, events) -> None:
        """Handle events in service info state"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "game_over"
                elif event.key == pygame.K_a and len(self.answered_services) > 1:
                    self.current_service_index = (self.current_service_index - 1) % len(
                        self.answered_services
                    )
                elif event.key == pygame.K_d and len(self.answered_services) > 1:
                    self.current_service_index = (self.current_service_index + 1) % len(
                        self.answered_services
                    )

    def get_remaining_time(self) -> float:
        """Get remaining time in seconds"""
        return max(0, GameConfig.TIME_LIMIT - (time.time() - self.start_time))

    def get_current_cpm(self) -> int:
        """Get current characters per minute"""
        elapsed_time = max(0.1, time.time() - self.start_time)
        return int(self.total_chars / (elapsed_time / 60))

    def get_current_wpm(self) -> int:
        """Get current words per minute (based on correct characters)"""
        elapsed_time = max(0.1, time.time() - self.start_time)
        return int((self.correct_chars / 5) / (elapsed_time / 60))

    def get_accuracy_rate(self) -> float:
        """Get current accuracy rate (0.0 to 1.0)"""
        total_attempts = self.correct_chars + self.mistakes
        if total_attempts == 0:
            return 1.0
        return 1.0 - (self.mistakes / total_attempts)

    def get_evaluation(self) -> tuple:
        """Get current evaluation level and color based on score"""
        for level, config in EvaluationConfig.LEVELS.items():
            if self.score >= config["threshold"]:
                return level, config["color"]
        return "Foundational", EvaluationConfig.LEVELS["Foundational"]["color"]

    def get_high_score(self) -> int:
        """Get the current high score"""
        return self.data_manager.get_high_score()

    def get_service_info(self) -> tuple:
        """Get current service information for display"""
        if not self.answered_services:
            return "", "", ""

        current_service = self.answered_services[self.current_service_index]
        description = self.data_manager.get_service_description(current_service)

        # Find example sentence for this service
        example_sentence = ""
        translation = ""
        sentences = self.data_manager.get_all_sentences()

        for sentence in sentences:
            if f"<{current_service}>" in sentence:
                example_sentence = sentence.replace(f"<{current_service}>", current_service)
                translation = self.data_manager.get_sentence_translation(example_sentence)
                break

        return description, example_sentence, translation

    def _complete_word(self) -> None:
        """Complete the current word successfully"""
        clean_current_word = self.current_word.replace("<", "").replace(">", "")

        # Track total characters attempted
        self.total_chars += len(clean_current_word)

        # Calculate new score based on accuracy and WPM
        self._update_score()

        # Record answered service
        if self.current_service_name and self.current_service_name not in self.answered_services:
            self.answered_services.append(self.current_service_name)

        # Play success sound and create particle effect
        if self.audio_manager:
            self.audio_manager.play_success_sound()
        if self.animation_manager:
            self.animation_manager.add_particle_effect(500, 300, (0, 255, 0), "success")
            self.animation_manager.create_score_popup(500, 300, len(clean_current_word))

        self.select_new_word()

        # Play new word sound
        if self.audio_manager:
            self.audio_manager.play_new_word_sound()

    def _update_score(self) -> None:
        """Update score based on accuracy rate * WPM"""
        if self.total_chars == 0:
            self.score = 0
            return

        # Calculate accuracy rate (0.0 to 1.0)
        accuracy_rate = self.correct_chars / self.total_chars if self.total_chars > 0 else 0

        # Calculate WPM (Words Per Minute) - assuming 5 characters per word
        elapsed_time = max(0.1, time.time() - self.start_time)
        wpm = (self.correct_chars / 5) / (elapsed_time / 60)

        # Calculate score as accuracy_rate * WPM
        self.score = int(accuracy_rate * wpm)

    def _check_answer(self) -> None:
        """Check if the typed answer is correct (called when Enter is pressed)"""
        clean_current_word = self.current_word.replace("<", "").replace(">", "")
        if self.typed_text == clean_current_word:
            # Correct answer - complete the word
            self._complete_word()
        else:
            # Wrong answer - this shouldn't happen with character-by-character validation
            # but keep for backward compatibility
            self.mistakes += 1

            # Play error sound and create particle effect
            if self.audio_manager:
                self.audio_manager.play_error_sound()
            if self.animation_manager:
                self.animation_manager.add_particle_effect(500, 300, (255, 0, 0), "error")

    def _end_game(self) -> None:
        """End the game and save statistics"""
        self.game_state = "game_over"

        # Update final score based on current stats
        self._update_score()

        # Play game over sound
        if self.audio_manager:
            self.audio_manager.play_game_over_sound()

        # Update high score
        self.data_manager.update_high_score(self.score)

        # Save game session
        elapsed_time = min(GameConfig.TIME_LIMIT, time.time() - self.start_time)
        self.data_manager.add_game_session(
            score=self.score,
            mistakes=self.mistakes,
            total_chars=self.total_chars,
            elapsed_time=elapsed_time,
            answered_services=self.answered_services,
        )


# Import pygame here to avoid circular imports
import pygame
