"""
Data management module for AWS Service Typing Game
"""

import json
from pathlib import Path
from typing import Any, Dict, List


class DataManager:
    """Manages game data including AWS services and user statistics"""

    def __init__(self, aws_data_file: str = None, save_file: str = "save_data.json"):
        # Set default path for AWS data file relative to package
        if aws_data_file is None:
            # Get the path to the data directory within the package
            package_dir = Path(__file__).parent.parent
            self.aws_data_file = package_dir / "data" / "aws_services_data.json"
        else:
            self.aws_data_file = aws_data_file
        self.save_file = save_file
        self.aws_data = None
        self.save_data = None
        self.load_aws_data()
        self.load_save_data()

    def load_aws_data(self) -> None:
        """Load AWS services data from JSON file"""
        try:
            with open(self.aws_data_file, encoding="utf-8") as f:
                self.aws_data = json.load(f)
        except FileNotFoundError:
            print(f"Warning: {self.aws_data_file} not found. Using fallback data.")
            self.aws_data = self._get_fallback_aws_data()
        except json.JSONDecodeError as e:
            print(f"Error loading AWS data: {e}")
            self.aws_data = self._get_fallback_aws_data()

    def load_save_data(self) -> None:
        """Load user save data from JSON file"""
        try:
            with open(self.save_file, encoding="utf-8") as f:
                self.save_data = json.load(f)
        except FileNotFoundError:
            self.save_data = self._get_default_save_data()
        except json.JSONDecodeError as e:
            print(f"Error loading save data: {e}")
            self.save_data = self._get_default_save_data()

    def save_user_data(self) -> None:
        """Save user data to JSON file"""
        try:
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(self.save_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving user data: {e}")

    def get_all_sentences(self) -> List[str]:
        """Get all typing sentences from all categories"""
        sentences = []
        if self.aws_data and "categories" in self.aws_data:
            for category in self.aws_data["categories"].values():
                sentences.extend(category.get("sentences", []))
        return sentences

    def get_sentences_by_category(self, category: str) -> List[str]:
        """Get sentences for a specific category"""
        if self.aws_data and "categories" in self.aws_data:
            return self.aws_data["categories"].get(category, {}).get("sentences", [])
        return []

    def get_service_description(self, service_name: str) -> str:
        """Get description for a specific service"""
        if self.aws_data and "categories" in self.aws_data:
            for category in self.aws_data["categories"].values():
                descriptions = category.get("descriptions", {})
                if service_name in descriptions:
                    return descriptions[service_name]
        return "説明が見つかりません"

    def get_sentence_translation(self, sentence: str) -> str:
        """Get Japanese translation for a sentence"""
        clean_sentence = sentence.replace("<", "").replace(">", "")
        if self.aws_data and "categories" in self.aws_data:
            for category in self.aws_data["categories"].values():
                translations = category.get("translations", {})
                if clean_sentence in translations:
                    return translations[clean_sentence]
        return "翻訳が見つかりません"

    def get_high_score(self) -> int:
        """Get the current high score"""
        return self.save_data.get("high_score", 0)

    def update_high_score(self, score: int) -> bool:
        """Update high score if new score is higher"""
        current_high = self.get_high_score()
        if score > current_high:
            self.save_data["high_score"] = score
            self.save_data["last_updated"] = self._get_current_timestamp()
            self.save_user_data()
            return True
        return False

    def add_game_session(
        self,
        score: int,
        mistakes: int,
        total_chars: int,
        elapsed_time: float,
        answered_services: List[str],
    ) -> None:
        """Add a new game session - now only updates high score"""
        # This method is kept for compatibility but only updates high score
        # No session history is stored anymore

    def get_game_statistics(self) -> Dict[str, Any]:
        """Get game statistics - now returns only high score info"""
        return {
            "high_score": self.get_high_score(),
            "last_updated": self.save_data.get("last_updated", None),
        }

    def _get_default_save_data(self) -> Dict[str, Any]:
        """Get default save data structure"""
        return {"high_score": 0, "created_at": self._get_current_timestamp(), "last_updated": None}

    def _get_current_timestamp(self) -> str:
        """Get current timestamp as string"""
        import datetime

        return datetime.datetime.now().isoformat()

    def _get_fallback_aws_data(self) -> Dict[str, Any]:
        """Get minimal fallback data if JSON file is not available"""
        return {
            "categories": {
                "computing": {
                    "services": ["EC2", "Lambda"],
                    "sentences": [
                        "My <EC2> instance is having an identity crisis",
                        "I wrote a <Lambda> function to feed my cat",
                    ],
                    "translations": {
                        "My EC2 instance is having an identity crisis": "私のEC2インスタンスはアイデンティティの危機に陥っています",
                        "I wrote a Lambda function to feed my cat": "猫に餌をやるためにLambda関数を書きました",
                    },
                    "descriptions": {
                        "EC2": "仮想サーバーを提供する基本的なコンピューティングサービス",
                        "Lambda": "サーバーレスでコードを実行できるコンピューティングサービス",
                    },
                }
            }
        }
