"""
AWS Service Typing Game

A typing practice game featuring AWS service names with Japanese translations.
"""

__version__ = "2.0.0"
__author__ = "AWS Typing Game Team"
__description__ = "Learn AWS services while improving your typing skills"

from .core.game import Game
from .managers.data_manager import DataManager

__all__ = ["Game", "DataManager"]
