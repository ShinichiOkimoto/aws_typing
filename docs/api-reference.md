# APIリファレンス

## 概要

AWS Typing Game の主要クラスとメソッドのAPIリファレンスです。開発者が各コンポーネントを理解し、拡張・カスタマイズを行うためのガイドとして提供されています。

## コアクラス

### `Game` クラス

**場所**: `src/aws_typing_game/core/game.py`

ゲームの中核となるロジックを管理するクラスです。

#### 初期化

```python
def __init__(self, data_manager: DataManager)
```

**パラメータ**:
- `data_manager`: データアクセスを提供するDataManagerインスタンス

#### 主要プロパティ

```python
game_state: str              # ゲーム状態 ("menu", "playing", "game_over", "service_info")
score: int                   # 現在のスコア
mistakes: int                # ミス数
total_chars: int            # 総入力文字数
correct_chars: int          # 正解文字数
current_word: str           # 現在のタイピング対象
current_service_name: str   # 現在のAWSサービス名
```

#### 主要メソッド

##### `reset_game()`
```python
def reset_game() -> None
```
ゲームの状態を初期化し、新しいゲームを開始できる状態にします。

##### `get_accuracy_rate()`
```python
def get_accuracy_rate() -> float
```
**戻り値**: 現在の正答率（0.0〜1.0）

**計算式**: `1.0 - (mistakes / (correct_chars + mistakes))`

##### `get_current_wpm()`
```python
def get_current_wpm() -> float
```
**戻り値**: 現在のWPM（Words Per Minute）

##### `update()`
```python
def update(events: List[pygame.event.Event], ignore_space: bool) -> None
```
ゲーム状態を更新します。

**パラメータ**:
- `events`: Pygameイベントリスト
- `ignore_space`: スペースキー入力を無視するかどうか

## マネージャークラス

### `DataManager` クラス

**場所**: `src/aws_typing_game/managers/data_manager.py`

AWSサービスデータとハイスコアを管理します。

#### 初期化

```python
def __init__(self, aws_data_file: Optional[str] = None, save_file: str = "save_data.json")
```

**パラメータ**:
- `aws_data_file`: AWSデータファイルのパス（省略時は内部データを使用）
- `save_file`: セーブデータファイルのパス

#### 主要メソッド

##### `get_random_aws_service()`
```python
def get_random_aws_service() -> Tuple[str, str, str, str]
```
**戻り値**: `(service_name, sentence, translation, category)`

ランダムなAWSサービス情報を取得します。

##### `get_high_score()`
```python
def get_high_score() -> int
```
**戻り値**: 現在のハイスコア

##### `save_high_score()`
```python
def save_high_score(score: int) -> None
```
ハイスコアを更新・保存します。

### `UIManager` クラス

**場所**: `src/aws_typing_game/ui/ui_manager.py`

ユーザーインターフェースの描画を管理します。

#### 初期化

```python
def __init__(self, screen: pygame.Surface, font_manager: FontManager)
```

**パラメータ**:
- `screen`: Pygame描画サーフェス
- `font_manager`: フォント管理インスタンス

#### 依存関係設定

```python
def set_responsive_manager(self, responsive_manager: ResponsiveManager) -> None
def set_accessibility_manager(self, accessibility_manager: AccessibilityManager) -> None
def set_animation_manager(self, animation_manager: AnimationManager) -> None
```

#### 描画メソッド

##### `draw_menu()`
```python
def draw_menu(self, high_score: int, sfx_enabled: bool, music_enabled: bool) -> None
```
メニュー画面を描画します。

##### `draw_game()`
```python
def draw_game(self, current_word: str, typed_text: str, service_name: str, 
              score: int, mistakes: int, remaining_time: float, 
              total_chars: int, start_time: float) -> None
```
ゲーム画面を描画します。

##### `draw_game_over()`
```python
def draw_game_over(self, score: int, high_score: int, total_chars: int,
                   start_time: float, answered_services: List[str],
                   correct_chars: int, mistakes: int) -> None
```
ゲーム終了画面を描画します。

### `AudioManager` クラス

**場所**: `src/aws_typing_game/managers/audio_manager.py`

音響効果とBGMを管理します。

#### 初期化

```python
def __init__(self)
```

#### 設定プロパティ

```python
sfx_enabled: bool      # 効果音の有効/無効
music_enabled: bool    # BGMの有効/無効
audio_enabled: bool    # 全体音響の有効/無効
```

#### 音響制御メソッド

##### `toggle_sfx()`
```python
def toggle_sfx() -> None
```
効果音のON/OFFを切り替えます。

##### `toggle_music()`
```python
def toggle_music() -> None
```
BGMのON/OFFを切り替えます。

##### `play_menu_sound()`
```python
def play_menu_sound(self, sound_type: str) -> None
```
メニュー音を再生します。

**sound_type**: "select", "hover", "error" など

##### `start_background_music()`
```python
def start_background_music() -> None
```
背景音楽を開始します。

### `ResponsiveManager` クラス

**場所**: `src/aws_typing_game/managers/responsive_manager.py`

レスポンシブデザインと画面適応を管理します。

#### 初期化

```python
def __init__(self, base_width: int = 1000, base_height: int = 700)
```

**パラメータ**:
- `base_width`: 基準幅
- `base_height`: 基準高さ

#### プロパティ

```python
scale_factor: float    # スケール係数
current_width: int     # 現在の幅
current_height: int    # 現在の高さ
```

#### スケーリングメソッド

##### `get_screen_size()`
```python
def get_screen_size() -> Tuple[int, int]
```
**戻り値**: `(width, height)`

最適化された画面サイズを取得します。

##### `scale_value()`
```python
def scale_value(self, value: int) -> int
```
値をスケール係数に基づいて調整します。

##### `scale_position()`
```python
def scale_position(self, x: int, y: int) -> Tuple[int, int]
```
座標をスケール係数に基づいて調整します。

### `AccessibilityManager` クラス

**場所**: `src/aws_typing_game/managers/accessibility_manager.py`

アクセシビリティ機能を管理します。

#### 初期化

```python
def __init__(self)
```

#### プロパティ

```python
color_blind_mode: str    # 色覚モード ("normal", "protanopia", "deuteranopia", "tritanopia")
high_contrast: bool      # ハイコントラストモード
```

#### アクセシビリティメソッド

##### `set_color_blind_mode()`
```python
def set_color_blind_mode(self, mode: str) -> None
```
色覚サポートモードを設定します。

##### `toggle_high_contrast()`
```python
def toggle_high_contrast() -> None
```
ハイコントラストモードを切り替えます。

##### `adjust_color()`
```python
def adjust_color(self, color: Tuple[int, int, int]) -> Tuple[int, int, int]
```
設定に基づいて色を調整します。

## 設定クラス

### `GameConfig` クラス

**場所**: `src/aws_typing_game/core/config.py`

ゲーム設定の定数を定義します。

```python
class GameConfig:
    TIME_LIMIT: int = 60           # 制限時間（秒）
    TARGET_FPS: int = 60           # 目標フレームレート
    WINDOW_TITLE: str = "AWS Service Typing Game"
    MIN_WORD_LENGTH: int = 3       # 最小単語長
    MAX_MISTAKES_PER_WORD: int = 3 # 単語あたりの最大ミス数
```

### `Colors` クラス

色定義とテーマを管理します。

```python
class Colors:
    # 基本色
    PRIMARY: Tuple[int, int, int] = (52, 152, 219)    # AWS Blue
    SECONDARY: Tuple[int, int, int] = (230, 126, 34)   # AWS Orange
    
    # UI色
    BACKGROUND: Tuple[int, int, int] = (44, 62, 80)
    TEXT: Tuple[int, int, int] = (236, 240, 241)
    
    # ステータス色
    SUCCESS: Tuple[int, int, int] = (46, 204, 113)
    ERROR: Tuple[int, int, int] = (231, 76, 60)
    WARNING: Tuple[int, int, int] = (241, 196, 15)
```

### `EvaluationConfig` クラス

評価基準を定義します。

```python
class EvaluationConfig:
    HERO_THRESHOLD: int = 80        # ヒーローレベル
    SPECIALTY_THRESHOLD: int = 60   # スペシャリティレベル
    PROFESSIONAL_THRESHOLD: int = 45 # プロフェッショナルレベル
    ASSOCIATE_THRESHOLD: int = 30   # アソシエイトレベル
    FOUNDATIONAL_THRESHOLD: int = 0 # ファンデーショナルレベル
```

## 拡張のためのフック

### カスタムマネージャーの作成

```python
class CustomManager:
    def __init__(self):
        # 初期化処理
        pass
    
    def update(self) -> None:
        # 更新処理
        pass
    
    def cleanup(self) -> None:
        # クリーンアップ処理
        pass

# main.py での使用
custom_manager = CustomManager()
# ゲームループで update() を呼び出し
```

### カスタムUI画面の追加

```python
class CustomUIManager(UIManager):
    def draw_custom_screen(self, custom_data: dict) -> None:
        # カスタム画面の描画
        self.screen.fill(Colors.BACKGROUND)
        # 描画処理...
        pygame.display.flip()
```

### 新しいゲーム状態の追加

```python
# game.py に新しい状態を追加
def handle_custom_state_events(self, events: List[pygame.event.Event]) -> None:
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_state = "menu"

# main.py のゲームループに追加
elif game.game_state == "custom_state":
    game.handle_custom_state_events(events)
```

## エラーハンドリング

### 標準的なエラーハンドリング例

```python
try:
    data_manager = DataManager()
    aws_services = data_manager.get_all_services()
except FileNotFoundError:
    print("AWSデータファイルが見つかりません")
    # フォールバック処理
except json.JSONDecodeError:
    print("AWSデータファイルの形式が正しくありません")
    # エラー処理
except Exception as e:
    print(f"予期しないエラー: {e}")
    # ログ出力やクリーンアップ
```

## デバッグとログ

### デバッグ情報の表示

```python
# game.py
def get_debug_info(self) -> dict:
    return {
        "score": self.score,
        "accuracy": self.get_accuracy_rate(),
        "wpm": self.get_current_wpm(),
        "mistakes": self.mistakes,
        "state": self.game_state
    }

# 使用例
debug_info = game.get_debug_info()
print(f"Debug: {debug_info}")
```

## テスト用ユーティリティ

### モックオブジェクトの作成

```python
class MockDataManager:
    def get_random_aws_service(self):
        return ("S3", "Test sentence", "テスト文", "Storage")
    
    def get_high_score(self):
        return 100

# テストでの使用
mock_data_manager = MockDataManager()
game = Game(mock_data_manager)
```

## パフォーマンス最適化

### プロファイリング

```python
import cProfile
import pstats

def profile_game():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # ゲーム実行
    main()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # 上位10件を表示
```

### メモリ使用量監視

```python
import psutil
import os

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB単位
```

---

このAPIリファレンスは、AWS Typing Gameの拡張と保守を支援するために作成されています。新機能の開発や既存機能の改修時の参考としてご活用ください。