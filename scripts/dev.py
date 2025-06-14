#!/usr/bin/env python3
"""
Development script runner for AWS Typing Game
使用方法: uv run scripts/dev.py [command]
"""

import subprocess
import sys

def run_command(cmd: list[str], description: str = "") -> int:
    """Run a command and return exit code"""
    if description:
        print(f"🔨 {description}")
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd).returncode

def run_tests():
    """Run test suite"""
    return run_command(["uv", "run", "pytest", "tests/", "-v"], "Running tests")

def run_game():
    """Run the game"""
    return run_command(["uv", "run", "aws-typing-game"], "Starting AWS Typing Game")

def run_lint():
    """Run linting"""
    print("🔍 Running code quality checks...")
    exit_codes = []
    
    # Run ruff check
    exit_codes.append(run_command(["uv", "run", "ruff", "check", "src/", "tests/"], "Ruff linting"))
    
    # Run ruff format check
    exit_codes.append(run_command(["uv", "run", "ruff", "format", "--check", "src/", "tests/"], "Ruff format check"))
    
    # Run mypy
    exit_codes.append(run_command(["uv", "run", "mypy", "src/aws_typing_game/"], "Type checking"))
    
    return max(exit_codes) if exit_codes else 0

def run_format():
    """Format code"""
    print("🎨 Formatting code...")
    exit_codes = []
    
    # Run ruff format
    exit_codes.append(run_command(["uv", "run", "ruff", "format", "src/", "tests/"], "Ruff formatting"))
    
    # Run ruff fix
    exit_codes.append(run_command(["uv", "run", "ruff", "check", "--fix", "src/", "tests/"], "Ruff auto-fix"))
    
    return max(exit_codes) if exit_codes else 0

def run_check():
    """Run full code quality check"""
    print("🚀 Running full quality check...")
    exit_codes = []
    
    exit_codes.append(run_format())
    exit_codes.append(run_lint())
    exit_codes.append(run_tests())
    
    if max(exit_codes) == 0:
        print("✅ All checks passed!")
    else:
        print("❌ Some checks failed!")
    
    return max(exit_codes)

def show_help():
    """Show help message"""
    print("""
AWS Typing Game - Development Commands

使用方法: uv run scripts/dev.py [command]

利用可能なコマンド:
  test      テストを実行
  game      ゲームを起動
  lint      リンターとタイプチェックを実行
  format    コードフォーマットを実行
  check     全ての品質チェックを実行（format + lint + test）
  help      このヘルプを表示

例:
  uv run scripts/dev.py test
  uv run scripts/dev.py game
  uv run scripts/dev.py check
""")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        show_help()
        return 0
    
    command = sys.argv[1].lower()
    
    commands = {
        "test": run_tests,
        "game": run_game,
        "lint": run_lint,
        "format": run_format,
        "check": run_check,
        "help": show_help,
    }
    
    if command in commands:
        return commands[command]()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())