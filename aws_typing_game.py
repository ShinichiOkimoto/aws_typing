import pygame
import sys
import random
import time
import os

# Pygameの初期化
pygame.init()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AWS サービス名タイピングゲーム")

# 色の定義 - AWS風の配色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (35, 134, 54)  # AWS成功色
RED = (207, 0, 15)     # AWS警告色
BLUE = (18, 44, 82)    # AWSダークブルー
LIGHT_BLUE = (51, 153, 255)  # AWSライトブルー
ORANGE = (255, 153, 0)  # AWSオレンジ
DARK_ORANGE = (232, 114, 0)  # AWSダークオレンジ
GRAY = (84, 91, 100)   # AWSグレー
LIGHT_GRAY = (242, 243, 243)  # AWSライトグレー
DARK_BG = (22, 27, 34)  # AWSダーク背景

# 日本語フォントの設定
def get_font_path():
    """システムに応じた日本語フォントのパスを返す"""
    if sys.platform == 'darwin':  # macOS
        font_paths = [
            '/System/Library/Fonts/Hiragino Sans GB.ttc',
            '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
            '/System/Library/Fonts/AppleGothic.ttf',
            '/Library/Fonts/Arial Unicode.ttf'
        ]
    elif sys.platform == 'win32':  # Windows
        font_paths = [
            'C:\\Windows\\Fonts\\meiryo.ttc',
            'C:\\Windows\\Fonts\\msgothic.ttc',
            'C:\\Windows\\Fonts\\YuGothM.ttc'
        ]
    else:  # Linux/その他
        font_paths = [
            '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc'
        ]
    
    # 存在するフォントパスを返す
    for path in font_paths:
        if os.path.exists(path):
            return path
    
    # デフォルトフォント（存在しなくてもPygameが適当なフォントを選ぶ）
    return None

# フォント設定
font_path = get_font_path()
if font_path:
    title_font = pygame.font.Font(font_path, 48)
    game_font = pygame.font.Font(font_path, 36)
    score_font = pygame.font.Font(font_path, 24)
else:
    # フォントが見つからない場合はシステムフォントを使用
    title_font = pygame.font.SysFont('Arial', 48)
    game_font = pygame.font.SysFont('Arial', 36)
    score_font = pygame.font.SysFont('Arial', 24)

# AWSサービス名リスト
aws_services = [
    "EC2", "S3", "Lambda", "DynamoDB", "RDS", "CloudFront", "Route53", "IAM",
    "SNS", "SQS", "CloudWatch", "CloudFormation", "ECS", "EKS", "Fargate",
    "API Gateway", "Cognito", "Amplify", "AppSync", "Athena", "Aurora",
    "Batch", "CodeBuild", "CodeCommit", "CodeDeploy", "CodePipeline",
    "Comprehend", "Connect", "DataSync", "Detective", "DocumentDB", "EBS",
    "ECR", "EFS", "ElastiCache", "EMR", "EventBridge", "FSx", "Glue",
    "GuardDuty", "Kinesis", "KMS", "Lake Formation", "Lex", "Macie",
    "MSK", "Neptune", "Polly", "QuickSight", "Redshift", "SageMaker",
    "Secrets Manager", "Step Functions", "Storage Gateway", "Textract",
    "Transcribe", "Transfer", "VPC", "WAF", "X-Ray"
]

class Game:
    def __init__(self):
        self.reset_game()
        self.game_state = "menu"  # menu, playing, game_over
        self.high_score = 0
    
    def reset_game(self):
        self.current_word = ""
        self.typed_text = ""
        self.score = 0
        self.mistakes = 0
        self.start_time = time.time()
        self.time_limit = 60  # 60秒
        self.select_new_word()
    
    def select_new_word(self):
        self.current_word = random.choice(aws_services)
        self.typed_text = ""
    
    def update(self, events):
        remaining_time = max(0, self.time_limit - (time.time() - self.start_time))
        
        if remaining_time <= 0:
            self.game_state = "game_over"
            if self.score > self.high_score:
                self.high_score = self.score
            return
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "menu"
                elif event.key == pygame.K_BACKSPACE:
                    self.typed_text = self.typed_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.typed_text.lower() == self.current_word.lower():
                        self.score += len(self.current_word)
                        self.select_new_word()
                    else:
                        self.mistakes += 1
                elif event.unicode.isprintable():
                    self.typed_text += event.unicode
    
    def draw_menu(self):
        # AWS風の濃い青背景
        screen.fill(DARK_BG)
        
        # AWSロゴ風の装飾 - 上部ナビゲーションバー（シンプル化）
        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 50))
        pygame.draw.rect(screen, ORANGE, (0, 0, WIDTH, 3))
        
        # AWSロゴ（位置とサイズを調整）
        aws_logo_text = score_font.render("AWS", True, WHITE)
        aws_logo_width = aws_logo_text.get_width()
        aws_logo_height = aws_logo_text.get_height()
        pygame.draw.rect(screen, ORANGE, (20, 13, aws_logo_width + 10, aws_logo_height + 4), 0, 4)
        screen.blit(aws_logo_text, (25, 15))
        
        # タイトル表示（中央配置、サイズ調整）
        title_text = "AWS サービス名タイピングゲーム"
        title = title_font.render(title_text, True, WHITE)
        title_width = title.get_width()
        screen.blit(title, (WIDTH//2 - title_width//2, 100))
        
        # AWS風のアイコン装飾（シンプル化）
        icon_size = 50
        # 外側の菱形
        pygame.draw.polygon(screen, ORANGE, [
            (WIDTH//2 - icon_size, 200),
            (WIDTH//2, 200 - icon_size),
            (WIDTH//2 + icon_size, 200),
            (WIDTH//2, 200 + icon_size)
        ], 0)
        
        # ゲーム説明テキスト（位置調整）
        desc_text = score_font.render("AWSサービス名のタイピングスキルを向上させよう！", True, LIGHT_GRAY)
        desc_width = desc_text.get_width()
        screen.blit(desc_text, (WIDTH//2 - desc_width//2, 280))
        
        # スタートテキスト（背景なしで直接表示）
        start_text = game_font.render("スペースキーを押してスタート", True, ORANGE)
        start_width = start_text.get_width()
        start_height = start_text.get_height()
        # 中央に配置
        start_x = WIDTH//2 - start_width//2
        start_y = 330 + (45 - start_height)//2  # 元のボタン位置を基準に調整
        screen.blit(start_text, (start_x, start_y))
        
        # ハイスコア表示（シンプル化、位置調整）
        if self.high_score > 0:
            high_score_text = score_font.render(f"ハイスコア: {self.high_score}", True, LIGHT_GRAY)
            high_score_width = high_score_text.get_width()
            screen.blit(high_score_text, (WIDTH//2 - high_score_width//2, 400))
        
        # 操作説明（位置調整）
        instructions = score_font.render("ESCキーで終了", True, LIGHT_GRAY)
        instructions_width = instructions.get_width()
        screen.blit(instructions, (WIDTH//2 - instructions_width//2, 450))
        
        # AWS風のフッター（シンプル化）
        pygame.draw.rect(screen, BLUE, (0, HEIGHT - 30, WIDTH, 30))
        
        # バージョン情報（位置調整）
        version_text = score_font.render("v1.0", True, LIGHT_GRAY)
        screen.blit(version_text, (WIDTH - version_text.get_width() - 10, HEIGHT - 25))
        
        # Powered by AWS（位置調整）
        aws_text = score_font.render("Powered by AWS", True, WHITE)
        screen.blit(aws_text, (10, HEIGHT - 25))
    
    def draw_game(self):
        # AWS風の濃い青背景
        screen.fill(DARK_BG)
        
        # AWS風のヘッダー
        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 80))
        pygame.draw.rect(screen, ORANGE, (0, 0, WIDTH, 4))
        
        # 残り時間表示
        remaining_time = max(0, self.time_limit - (time.time() - self.start_time))
        time_label = score_font.render("残り時間:", True, LIGHT_GRAY)
        screen.blit(time_label, (20, 20))
        
        time_value = score_font.render(f"{int(remaining_time)}秒", True, WHITE)
        screen.blit(time_value, (120, 20))
        
        # タイムバー - AWS風のプログレスバー
        time_ratio = remaining_time / self.time_limit
        pygame.draw.rect(screen, GRAY, (20, 50, 200, 15), 0, 7)
        
        # 残り時間に応じて色を変える
        bar_color = GREEN if time_ratio > 0.5 else ORANGE if time_ratio > 0.2 else RED
        if time_ratio > 0:
            pygame.draw.rect(screen, bar_color, (20, 50, int(200 * time_ratio), 15), 0, 7)
        
        # スコア表示 - AWS風のメトリクス表示
        score_label = score_font.render("スコア:", True, LIGHT_GRAY)
        screen.blit(score_label, (WIDTH - 200, 20))
        
        score_value = score_font.render(f"{self.score}", True, WHITE)
        screen.blit(score_value, (WIDTH - 120, 20))
        
        # ミス表示
        mistakes_label = score_font.render("ミス:", True, LIGHT_GRAY)
        screen.blit(mistakes_label, (WIDTH - 200, 50))
        
        mistakes_value = score_font.render(f"{self.mistakes}", True, RED if self.mistakes > 0 else WHITE)
        screen.blit(mistakes_value, (WIDTH - 120, 50))
        
        # AWS風のコンソールパネル
        pygame.draw.rect(screen, (30, 35, 45), (WIDTH//2 - 300, 120, 600, 350), 0, 10)
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 300, 120, 600, 350), 1, 10)
        
        # パネルヘッダー
        pygame.draw.rect(screen, BLUE, (WIDTH//2 - 300, 120, 600, 40), 0, 10, 10, 0, 0)
        panel_title = score_font.render("AWS サービス名入力", True, WHITE)
        screen.blit(panel_title, (WIDTH//2 - panel_title.get_width()//2, 130))
        
        # 現在のワード表示 - AWS風のコンソール出力
        word_label = score_font.render("入力するサービス名:", True, LIGHT_GRAY)
        screen.blit(word_label, (WIDTH//2 - 250, 180))
        
        word_text = game_font.render(self.current_word, True, ORANGE)
        screen.blit(word_text, (WIDTH//2 - word_text.get_width()//2, 220))
        
        # 入力フィールド - AWS風の入力ボックス
        pygame.draw.rect(screen, (40, 45, 55), (WIDTH//2 - 250, 290, 500, 50), 0, 5)
        pygame.draw.rect(screen, LIGHT_BLUE if len(self.typed_text) > 0 else GRAY, 
                        (WIDTH//2 - 250, 290, 500, 50), 2, 5)
        
        # 入力中のテキスト表示
        if len(self.typed_text) > 0:
            typed_text = game_font.render(self.typed_text, True, WHITE)
            screen.blit(typed_text, (WIDTH//2 - 240, 300))
        else:
            placeholder = score_font.render("ここにタイプしてください...", True, GRAY)
            screen.blit(placeholder, (WIDTH//2 - 240, 305))
        
        # 正誤判定の視覚的フィードバック
        feedback_color = GREEN
        for i, char in enumerate(self.typed_text):
            if i >= len(self.current_word) or char.lower() != self.current_word[i].lower():
                feedback_color = RED
                break
        
        if len(self.typed_text) > 0:
            pygame.draw.rect(screen, feedback_color, (WIDTH//2 - 250, 345, 500, 3))
        
        # AWS風のフッター
        pygame.draw.rect(screen, BLUE, (0, HEIGHT - 40, WIDTH, 40))
        
        # 操作ガイド
        guide_text = score_font.render("Enter: 確定  |  Backspace: 削除  |  ESC: メニューに戻る", True, WHITE)
        screen.blit(guide_text, (WIDTH//2 - guide_text.get_width()//2, HEIGHT - 30))
    
    def draw_game_over(self):
        # AWS風の濃い青背景
        screen.fill(DARK_BG)
        
        # AWS風のヘッダー
        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 8))
        pygame.draw.rect(screen, ORANGE, (0, 0, WIDTH, 4))
        
        # ゲームオーバーテキスト
        game_over_text = title_font.render("ゲームオーバー", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 80))
        
        # AWS風の結果パネル
        pygame.draw.rect(screen, (30, 35, 45), (WIDTH//2 - 300, 150, 600, 300), 0, 10)
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 300, 150, 600, 300), 1, 10)
        
        # パネルヘッダー
        pygame.draw.rect(screen, BLUE, (WIDTH//2 - 300, 150, 600, 40), 0, 10, 10, 0, 0)
        panel_title = score_font.render("結果サマリー", True, WHITE)
        screen.blit(panel_title, (WIDTH//2 - panel_title.get_width()//2, 160))
        
        # 結果表示 - AWS風のメトリクス表示
        
        # 最終スコア
        score_label = score_font.render("最終スコア:", True, LIGHT_GRAY)
        screen.blit(score_label, (WIDTH//2 - 250, 220))
        
        score_value = game_font.render(f"{self.score}", True, ORANGE)
        screen.blit(score_value, (WIDTH//2 + 50, 215))
        
        # 正確さ
        accuracy = 0 if self.score + self.mistakes == 0 else self.score / (self.score + self.mistakes) * 100
        
        accuracy_label = score_font.render("正確さ:", True, LIGHT_GRAY)
        screen.blit(accuracy_label, (WIDTH//2 - 250, 270))
        
        accuracy_value = game_font.render(f"{accuracy:.1f}%", True, 
                                         GREEN if accuracy > 80 else ORANGE if accuracy > 50 else RED)
        screen.blit(accuracy_value, (WIDTH//2 + 50, 265))
        
        # ハイスコア表示
        high_score_label = score_font.render("ハイスコア:", True, LIGHT_GRAY)
        screen.blit(high_score_label, (WIDTH//2 - 250, 320))
        
        if self.score >= self.high_score:
            # 新記録達成時（背景なしで直接表示）
            high_score_text = game_font.render(f"{self.score} (新記録!)", True, ORANGE)
            screen.blit(high_score_text, (WIDTH//2 + 50, 315))
        else:
            high_score_value = game_font.render(f"{self.high_score}", True, WHITE)
            screen.blit(high_score_value, (WIDTH//2 + 50, 315))
        
        # AWS風のセパレーター
        pygame.draw.line(screen, GRAY, (WIDTH//2 - 250, 370), (WIDTH//2 + 250, 370), 1)
        
        # リスタート指示（背景なしで直接表示）
        restart_text = game_font.render("スペースキーでリスタート", True, ORANGE)
        restart_width = restart_text.get_width()
        restart_height = restart_text.get_height()
        # 中央に配置
        restart_x = WIDTH//2 - restart_width//2
        restart_y = 390 + (40 - restart_height)//2  # 元のボタン位置を基準に調整
        screen.blit(restart_text, (restart_x, restart_y))
        
        # メニューに戻る指示
        menu_text = score_font.render("ESCキーでメニューに戻る", True, LIGHT_GRAY)
        screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, 450))
        
        # AWS風のフッター
        pygame.draw.rect(screen, BLUE, (0, HEIGHT - 30, WIDTH, 30))
        
        # AWS風のロゴテキスト
        aws_text = score_font.render("Powered by AWS", True, WHITE)
        screen.blit(aws_text, (10, HEIGHT - aws_text.get_height() - 5))

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game.game_state == "menu" and event.key == pygame.K_SPACE:
                    game.reset_game()
                    game.game_state = "playing"
                elif game.game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        game.reset_game()
                        game.game_state = "playing"
                    elif event.key == pygame.K_ESCAPE:
                        game.game_state = "menu"
        
        if game.game_state == "playing":
            game.update(events)
        
        # 描画
        if game.game_state == "menu":
            game.draw_menu()
        elif game.game_state == "playing":
            game.draw_game()
        elif game.game_state == "game_over":
            game.draw_game_over()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
