# Justfile for AWS Typing Game
# 使用方法: just [command] or uv run --with just -- just [command]

# デフォルトコマンド（コマンド一覧を表示）
default:
    @just --list

# ゲームを起動
game:
    uv run aws-typing-game

# ゲームを開発モードで起動
dev-game:
    uv run python src/aws_typing_game/main.py

# テストを実行
test:
    uv run pytest tests/ -v

# テストを詳細表示で実行
test-verbose:
    uv run pytest tests/ -v -s

# テストカバレッジを実行
test-cov:
    uv run pytest tests/ --cov=aws_typing_game --cov-report=html

# リンターを実行
lint:
    @echo "🔍 Running Ruff linting..."
    uv run ruff check src/ tests/
    @echo "🔍 Running Ruff format check..."
    uv run ruff format --check src/ tests/
    @echo "🔍 Running mypy type check..."
    uv run mypy src/aws_typing_game/

# コードフォーマットを実行
format:
    @echo "🎨 Running Ruff format..."
    uv run ruff format src/ tests/
    @echo "🎨 Running Ruff auto-fix..."
    uv run ruff check --fix src/ tests/

# 全ての品質チェックを実行
check: format lint test
    @echo "✅ All checks completed!"

# 依存関係をインストール
install:
    uv sync --dev

# 依存関係を更新
update:
    uv lock --upgrade

# 開発環境をセットアップ
setup:
    uv sync --dev
    @echo "✅ Development environment setup complete!"

# プロジェクトをクリーンアップ
clean:
    @echo "🧹 Cleaning up..."
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    rm -rf .pytest_cache/
    rm -rf .mypy_cache/
    rm -rf htmlcov/
    rm -rf .coverage
    @echo "✅ Cleanup complete!"

# パッケージをビルド
build:
    uv build

# パッケージをビルドしてインストール
build-install: build
    uv pip install dist/*.whl --force-reinstall