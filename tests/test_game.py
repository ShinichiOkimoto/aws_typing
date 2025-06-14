"""Tests for the core game logic."""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from aws_typing_game.core.game import Game
from aws_typing_game.managers.data_manager import DataManager


class TestGame:
    """Test cases for Game class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.data_manager = DataManager()
        self.game = Game(self.data_manager)

    def test_game_initialization(self):
        """Test that game initializes correctly."""
        assert self.game.game_state == "menu"
        assert self.game.score == 0
        assert self.game.mistakes == 0
        assert self.game.total_chars == 0
        assert self.game.correct_chars == 0

    def test_game_reset(self):
        """Test that game resets correctly."""
        # Modify game state
        self.game.score = 100
        self.game.mistakes = 5
        self.game.total_chars = 50
        self.game.correct_chars = 45

        # Reset game
        self.game.reset_game()

        # Check values are reset
        assert self.game.score == 0
        assert self.game.mistakes == 0
        assert self.game.total_chars == 0
        assert self.game.correct_chars == 0
        assert self.game.current_word != ""

    def test_accuracy_calculation(self):
        """Test accuracy rate calculation."""
        # Set up test data
        self.game.correct_chars = 95
        self.game.mistakes = 5

        accuracy = self.game.get_accuracy_rate()
        expected = 1.0 - (5 / 100)  # 95% accuracy

        assert accuracy == expected

    def test_wpm_calculation(self):
        """Test WPM calculation."""
        # This is a basic test - in real testing we'd mock time.time()
        self.game.correct_chars = 50
        wpm = self.game.get_current_wpm()

        # WPM should be >= 0
        assert wpm >= 0
