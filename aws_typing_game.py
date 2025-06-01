import pygame
import sys
import random
import time
import os
from pathlib import Path

# Pygameの初期化
pygame.init()

# 画面設定
WIDTH, HEIGHT = 1000, 700  # ウィンドウサイズを拡大
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

# 評価カテゴリ用の色
GOLD = (255, 215, 0)      # Hero用の金色
PURPLE = (128, 0, 128)    # Specialty用の紫色
EMERALD = (80, 200, 120)  # Professional用のエメラルド色
BLUE_CATEGORY = (0, 102, 204)  # Associate用の青色
GRAY_CATEGORY = (128, 128, 128)  # Foundational用の灰色
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
    small_font = pygame.font.Font(font_path, 18)
else:
    # フォントが見つからない場合はシステムフォントを使用
    title_font = pygame.font.SysFont('Arial', 48)
    game_font = pygame.font.SysFont('Arial', 36)
    score_font = pygame.font.SysFont('Arial', 24)
    small_font = pygame.font.SysFont('Arial', 18)
# AWSサービス名とユースケースを反映した文章のリスト
aws_service_sentences = [
    # コンピューティング
    "My <EC2> instance is having an identity crisis",
    "I wrote a <Lambda> function to feed my cat",
    "Running <Batch> jobs while taking a bath",
    "My website on <Lightsail> is lighter than air",
    "<Outposts> brought AWS to my basement",
    "<App Runner> is faster than my marathon time",
    "<Elastic Beanstalk> grew into a giant cloud",
    
    # コンテナ
    "My containers in <ECS> are playing hide and seek",
    "Managing <EKS> is easier than my kids",
    "<Fargate> launched my app to the moon",
    "Storing docker images in <ECR> like treasures",
    
    # ストレージ
    "I lost my keys in an <S3> bucket",
    "My <EBS> volume is full of cat pictures",
    "<EFS> shares files better than my coworkers",
    "<FSx> makes Windows admins smile again",
    "<Storage Gateway> is my portal to the cloud",
    "The <Snow Family> reunion was ice cold",
    "<S3 Glacier> froze my data for centuries",
    
    # データベース
    "<RDS> manages my database while I sleep",
    "<DynamoDB> scales faster than rumors",
    "<Aurora> database shines brighter than stars",
    "<ElastiCache> makes my app faster than coffee",
    "<Neptune> graphs my complex family tree",
    "<Redshift> warehouses data like Costco",
    "<DocumentDB> stores docs better than my desk",
    "<Timestream> records time better than history",
    "<QLDB> ledger is more trusted than my memory",
    
    # ネットワーキング
    "My <VPC> is more private than my diary",
    "<CloudFront> delivers content faster than pizza",
    "<Route53> routes traffic better than GPS",
    "<API Gateway> guards my APIs like a bouncer",
    "<Direct Connect> is my express lane to AWS",
    "<Global Accelerator> makes my app supersonic",
    "<Transit Gateway> connects networks like gossip",
    
    # セキュリティ
    "<IAM> permissions are stricter than my parents",
    "<Cognito> remembers users better than I do",
    "<WAF> blocks attacks like a ninja",
    "<Shield> protects against DDoS like a superhero",
    "<GuardDuty> detects threats in their sleep",
    "<Inspector> finds flaws better than my spouse",
    "<Macie> finds sensitive data like a detective",
    "<Detective> solves cloud mysteries like Sherlock",
    "<Security Hub> centralizes alerts like a boss",
    
    # 管理ツール
    "<CloudWatch> monitors more than my mother",
    "<CloudFormation> builds infrastructure like LEGO",
    "<CloudTrail> logs actions like Santa's list",
    "<Config> tracks changes better than historians",
    "<Systems Manager> manages more than my manager",
    "<Control Tower> governs accounts like a dictator",
    "<Organizations> organizes better than Marie Kondo",
    
    # 開発者ツール
    "<CodeCommit> stores code safer than my brain",
    "<CodeBuild> builds code faster than caffeine",
    "<CodeDeploy> deploys smoother than butter",
    "<CodePipeline> pipelines code like plumbing",
    "<CodeStar> makes projects shine like Hollywood",
    "<Cloud9> IDE works on cloud nine",
    "<X-Ray> sees through code like Superman",
    
    # 分析
    "<Athena> queries data with godlike power",
    "<EMR> processes big data like a food processor",
    "<Kinesis> streams data like a river",
    "<QuickSight> visualizes data like an artist",
    "<Glue> sticks my data pipeline together",
    "<Lake Formation> builds data lakes without water",
    "<Data Exchange> trades data like baseball cards",
    
    # 機械学習
    "<SageMaker> builds ML models like a wizard",
    "<Rekognition> identifies faces better than me",
    "<Comprehend> understands text like a scholar",
    "<Lex> chats better than my teenager",
    "<Polly> speaks clearer than my GPS",
    "<Textract> extracts text like dental surgery",
    "<Forecast> predicts better than fortune cookies",
    "<Kendra> searches smarter than my colleagues",
    
    # メッセージング
    "<SNS> notifies faster than office gossip",
    "<SQS> queues messages like Black Friday lines",
    "<EventBridge> connects events like a matchmaker",
    "<Step Functions> orchestrates like a conductor",
    "<MQ> messages more reliably than texting",
    
    # モバイル
    "<Amplify> builds mobile apps like magic",
    "<AppSync> syncs data like synchronized swimmers",
    "<Device Farm> tests on devices like a zoo",
    
    # その他
    "<WorkSpaces> desktops float in the cloud",
    "<Connect> routes calls better than receptionists",
    "<Managed Blockchain> chains blocks without chains",
    "<IoT Core> connects things that shouldn't talk",
    "<Ground Station> talks to satellites like E.T."
]
# AWSサービス文の日本語訳
aws_service_sentences_jp = {
    # コンピューティング
    "My EC2 instance is having an identity crisis": "私のEC2インスタンスはアイデンティティの危機に陥っています",
    "I wrote a Lambda function to feed my cat": "猫に餌をやるためにLambda関数を書きました",
    "Running Batch jobs while taking a bath": "お風呂に入りながらBatchジョブを実行しています",
    "My website on Lightsail is lighter than air": "Lightsailで作ったウェブサイトは空気より軽いです",
    "Outposts brought AWS to my basement": "OutpostsがAWSを私の地下室に持ってきました",
    "App Runner is faster than my marathon time": "App Runnerは私のマラソンタイムより速いです",
    "Elastic Beanstalk grew into a giant cloud": "Elastic Beanstalkは巨大なクラウドに成長しました",
    
    # コンテナ
    "My containers in ECS are playing hide and seek": "ECSのコンテナが鬼ごっこをしています",
    "Managing EKS is easier than my kids": "EKSの管理は子供の世話より簡単です",
    "Fargate launched my app to the moon": "Fargateが私のアプリを月まで打ち上げました",
    "Storing docker images in ECR like treasures": "ECRにDockerイメージを宝物のように保存しています",
    
    # ストレージ
    "I lost my keys in an S3 bucket": "S3バケットの中で鍵をなくしました",
    "My EBS volume is full of cat pictures": "EBSボリュームが猫の写真でいっぱいです",
    "EFS shares files better than my coworkers": "EFSは同僚よりもファイル共有が上手です",
    "FSx makes Windows admins smile again": "FSxはWindowsの管理者を再び笑顔にします",
    "Storage Gateway is my portal to the cloud": "Storage Gatewayはクラウドへの私のポータルです",
    "The Snow Family reunion was ice cold": "Snow Familyの再会は氷のように冷たかったです",
    "S3 Glacier froze my data for centuries": "S3 Glacierは私のデータを何世紀もの間凍結しました",
    
    # データベース
    "RDS manages my database while I sleep": "RDSは私が眠っている間にデータベースを管理します",
    "DynamoDB scales faster than rumors": "DynamoDBは噂よりも速くスケールします",
    "Aurora database shines brighter than stars": "Auroraデータベースは星よりも明るく輝きます",
    "ElastiCache makes my app faster than coffee": "ElastiCacheは私のアプリをコーヒーより速くします",
    "Neptune graphs my complex family tree": "Neptuneは私の複雑な家系図をグラフ化します",
    "Redshift warehouses data like Costco": "RedshiftはCostcoのようにデータを倉庫化します",
    "DocumentDB stores docs better than my desk": "DocumentDBは私の机よりも上手に文書を保存します",
    "Timestream records time better than history": "Timestreamは歴史よりも時間を記録します",
    "QLDB ledger is more trusted than my memory": "QLDB台帳は私の記憶よりも信頼できます",
    
    # ネットワーキング
    "My VPC is more private than my diary": "私のVPCは日記よりもプライベートです",
    "CloudFront delivers content faster than pizza": "CloudFrontはピザよりも速くコンテンツを配信します",
    "Route53 routes traffic better than GPS": "Route53はGPSよりも上手にトラフィックをルーティングします",
    "API Gateway guards my APIs like a bouncer": "API Gatewayはバウンサーのように私のAPIを守ります",
    "Direct Connect is my express lane to AWS": "Direct ConnectはAWSへの私の専用レーンです",
    "Global Accelerator makes my app supersonic": "Global Acceleratorは私のアプリを超音速にします",
    "Transit Gateway connects networks like gossip": "Transit Gatewayは噂のようにネットワークを接続します",
    
    # セキュリティ
    "IAM permissions are stricter than my parents": "IAMの権限は私の両親よりも厳しいです",
    "Cognito remembers users better than I do": "Cognitoは私よりもユーザーをよく覚えています",
    "WAF blocks attacks like a ninja": "WAFは忍者のように攻撃をブロックします",
    "Shield protects against DDoS like a superhero": "ShieldはスーパーヒーローのようにDDoS攻撃から守ります",
    "GuardDuty detects threats in their sleep": "GuardDutyは睡眠中に脅威を検出します",
    "Inspector finds flaws better than my spouse": "Inspectorは配偶者よりも欠陥を見つけるのが上手です",
    "Macie finds sensitive data like a detective": "Macieは探偵のように機密データを見つけます",
    "Detective solves cloud mysteries like Sherlock": "Detectiveはシャーロックのようにクラウドの謎を解きます",
    "Security Hub centralizes alerts like a boss": "Security Hubはボスのようにアラートを一元管理します",
    
    # 管理ツール
    "CloudWatch monitors more than my mother": "CloudWatchは母親以上に監視します",
    "CloudFormation builds infrastructure like LEGO": "CloudFormationはレゴのようにインフラを構築します",
    "CloudTrail logs actions like Santa's list": "CloudTrailはサンタのリストのように行動を記録します",
    "Config tracks changes better than historians": "Configは歴史家よりも変更を追跡します",
    "Systems Manager manages more than my manager": "Systems Managerは上司以上に管理します",
    "Control Tower governs accounts like a dictator": "Control Towerは独裁者のようにアカウントを統治します",
    "Organizations organizes better than Marie Kondo": "Organizationsはマリー・コンドウよりも整理が上手です",
    
    # 開発者ツール
    "CodeCommit stores code safer than my brain": "CodeCommitは私の脳よりも安全にコードを保存します",
    "CodeBuild builds code faster than caffeine": "CodeBuildはカフェインよりも速くコードをビルドします",
    "CodeDeploy deploys smoother than butter": "CodeDeployはバターよりも滑らかにデプロイします",
    "CodePipeline pipelines code like plumbing": "CodePipelineは配管のようにコードをパイプライン化します",
    "CodeStar makes projects shine like Hollywood": "CodeStarはハリウッドのようにプロジェクトを輝かせます",
    "Cloud9 IDE works on cloud nine": "Cloud9 IDEは雲の上で動作します",
    "X-Ray sees through code like Superman": "X-Rayはスーパーマンのようにコードを透視します",
    
    # 分析
    "Athena queries data with godlike power": "Athenaは神のような力でデータをクエリします",
    "EMR processes big data like a food processor": "EMRはフードプロセッサーのようにビッグデータを処理します",
    "Kinesis streams data like a river": "Kinesisは川のようにデータをストリーミングします",
    "QuickSight visualizes data like an artist": "QuickSightはアーティストのようにデータを可視化します",
    "Glue sticks my data pipeline together": "Glueは私のデータパイプラインを接着します",
    "Lake Formation builds data lakes without water": "Lake Formationは水なしでデータレイクを構築します",
    "Data Exchange trades data like baseball cards": "Data Exchangeは野球カードのようにデータを交換します",
    
    # 機械学習
    "SageMaker builds ML models like a wizard": "SageMakerは魔法使いのようにMLモデルを構築します",
    "Rekognition identifies faces better than me": "Rekognitionは私よりも顔の識別が上手です",
    "Comprehend understands text like a scholar": "Comprehendは学者のようにテキストを理解します",
    "Lex chats better than my teenager": "Lexは10代の子供よりもチャットが上手です",
    "Polly speaks clearer than my GPS": "PollyはGPSよりも明確に話します",
    "Textract extracts text like dental surgery": "Textractは歯科手術のようにテキストを抽出します",
    "Forecast predicts better than fortune cookies": "Forecastはフォーチュンクッキーよりも予測が上手です",
    "Kendra searches smarter than my colleagues": "Kendraは同僚よりも賢く検索します",
    
    # メッセージング
    "SNS notifies faster than office gossip": "SNSはオフィスの噂よりも速く通知します",
    "SQS queues messages like Black Friday lines": "SQSはブラックフライデーの列のようにメッセージを並べます",
    "EventBridge connects events like a matchmaker": "EventBridgeは仲人のようにイベントを接続します",
    "Step Functions orchestrates like a conductor": "Step Functionsは指揮者のようにオーケストレーションします",
    "MQ messages more reliably than texting": "MQはテキストメッセージよりも確実にメッセージを送ります",
    
    # モバイル
    "Amplify builds mobile apps like magic": "Amplifyは魔法のようにモバイルアプリを構築します",
    "AppSync syncs data like synchronized swimmers": "AppSyncはシンクロナイズドスイマーのようにデータを同期します",
    "Device Farm tests on devices like a zoo": "Device Farmは動物園のようにデバイスでテストします",
    
    # その他
    "WorkSpaces desktops float in the cloud": "WorkSpacesのデスクトップはクラウドに浮かんでいます",
    "Connect routes calls better than receptionists": "Connectは受付係よりも上手に通話をルーティングします",
    "Managed Blockchain chains blocks without chains": "Managed Blockchainは鎖なしでブロックをつなぎます",
    "IoT Core connects things that shouldn't talk": "IoT Coreは話すべきでないものを接続します",
    "Ground Station talks to satellites like E.T.": "Ground StationはE.T.のように衛星と通信します"
}
# AWSサービス名リスト（サービス情報表示用）
aws_services = [
    # コンピューティング
    "EC2", "Lambda", "Batch", "Lightsail", "Outposts", "App Runner", "Elastic Beanstalk",
    # コンテナ
    "ECS", "EKS", "Fargate", "ECR",
    # ストレージ
    "S3", "EBS", "EFS", "FSx", "Storage Gateway", "Snow Family", "S3 Glacier",
    # データベース
    "RDS", "DynamoDB", "Aurora", "ElastiCache", "Neptune", "Redshift", "DocumentDB", "Timestream", "QLDB",
    # ネットワーキング
    "VPC", "CloudFront", "Route53", "API Gateway", "Direct Connect", "Global Accelerator", "Transit Gateway",
    # セキュリティ
    "IAM", "Cognito", "WAF", "Shield", "GuardDuty", "Inspector", "Macie", "Detective", "Security Hub",
    # 管理ツール
    "CloudWatch", "CloudFormation", "CloudTrail", "Config", "Systems Manager", "Control Tower", "Organizations",
    # 開発者ツール
    "CodeCommit", "CodeBuild", "CodeDeploy", "CodePipeline", "CodeStar", "Cloud9", "X-Ray",
    # 分析
    "Athena", "EMR", "Kinesis", "QuickSight", "Glue", "Lake Formation", "Data Exchange",
    # 機械学習
    "SageMaker", "Rekognition", "Comprehend", "Lex", "Polly", "Textract", "Forecast", "Kendra",
    # メッセージング
    "SNS", "SQS", "EventBridge", "Step Functions", "MQ", "AppSync",
    # モバイル
    "Amplify", "Device Farm",
    # その他
    "WorkSpaces", "Connect", "Managed Blockchain", "IoT Core", "Ground Station"
]
# AWSサービスの簡単な概要
aws_services_descriptions = {
    # コンピューティング
    "EC2": "仮想サーバーを提供する基本的なコンピューティングサービス",
    "Lambda": "サーバーレスでコードを実行できるコンピューティングサービス",
    "Batch": "バッチコンピューティングジョブを効率的に実行するサービス",
    "Lightsail": "シンプルな仮想プライベートサーバー(VPS)を提供するサービス",
    "Outposts": "AWSインフラをオンプレミス環境に拡張するサービス",
    "App Runner": "コンテナ化されたWebアプリケーションを簡単にデプロイするサービス",
    "Elastic Beanstalk": "アプリケーションのデプロイと管理を自動化するサービス",
    
    # コンテナ
    "ECS": "コンテナ化されたアプリケーションを実行・管理するサービス",
    "EKS": "マネージド型Kubernetesサービス",
    "Fargate": "コンテナ向けのサーバーレスコンピューティングエンジン",
    "ECR": "コンテナイメージを保存、管理、デプロイするレジストリサービス",
    
    # ストレージ
    "S3": "スケーラブルなオブジェクトストレージサービス",
    "EBS": "EC2インスタンス用のブロックストレージボリューム",
    "EFS": "EC2インスタンス用のスケーラブルなファイルストレージ",
    "FSx": "Windows、Lustre向けの高性能ファイルシステム",
    "Storage Gateway": "オンプレミスとクラウドストレージを統合するサービス",
    "Snow Family": "物理デバイスを使用した大量データ転送ソリューション",
    "S3 Glacier": "長期アーカイブ向けの低コストストレージサービス",
    
    # データベース
    "RDS": "リレーショナルデータベースを簡単に設定・運用・スケールするサービス",
    "DynamoDB": "フルマネージド型NoSQLデータベースサービス",
    "Aurora": "MySQLおよびPostgreSQLと互換性のある高性能データベース",
    "ElastiCache": "インメモリキャッシュを提供するサービス",
    "Neptune": "グラフデータベースサービス",
    "Redshift": "データウェアハウスサービス",
    "DocumentDB": "MongoDBと互換性のあるドキュメントデータベース",
    "Timestream": "時系列データベースサービス",
    "QLDB": "台帳データベースサービス",
    
    # ネットワーキング
    "VPC": "仮想ネットワークを作成・管理するサービス",
    "CloudFront": "コンテンツ配信ネットワーク(CDN)サービス",
    "Route53": "スケーラブルなDNSウェブサービス",
    "API Gateway": "APIの作成、公開、維持、監視、保護を行うサービス",
    "Direct Connect": "AWSへの専用ネットワーク接続を提供するサービス",
    "Global Accelerator": "アプリケーションの可用性と性能を向上させるサービス",
    "Transit Gateway": "VPCとオンプレミスネットワークを接続するサービス",
    
    # セキュリティ
    "IAM": "AWSリソースへのアクセスを安全に制御するサービス",
    "Cognito": "ウェブ・モバイルアプリに認証機能を追加するサービス",
    "WAF": "ウェブアプリケーションを保護するファイアウォール",
    "Shield": "DDoS攻撃からアプリケーションを保護するサービス",
    "GuardDuty": "インテリジェントな脅威検出サービス",
    "Inspector": "自動セキュリティ評価サービス",
    "Macie": "機密データの自動検出と保護を行うサービス",
    "Detective": "セキュリティ問題の分析と調査を支援するサービス",
    "Security Hub": "セキュリティアラートと状態を一元管理するサービス",
    
    # 管理ツール
    "CloudWatch": "AWSリソースとアプリケーションの監視サービス",
    "CloudFormation": "AWSリソースをテンプレートで管理するサービス",
    "CloudTrail": "AWSアカウントのガバナンス、コンプライアンス、監査を支援するサービス",
    "Config": "AWSリソースの設定を評価・監査・管理するサービス",
    "Systems Manager": "AWSリソースを一元管理するサービス",
    "Control Tower": "複数のAWSアカウントを設定・管理するサービス",
    "Organizations": "複数のAWSアカウントを一元管理するサービス",
    
    # 開発者ツール
    "CodeCommit": "プライベートGitリポジトリを提供するサービス",
    "CodeBuild": "ソースコードをコンパイルしてテストを実行し、パッケージを作成するサービス",
    "CodeDeploy": "コードデプロイを自動化するサービス",
    "CodePipeline": "継続的デリバリーサービス",
    "CodeStar": "クラウドアプリケーションの開発、ビルド、デプロイを支援するサービス",
    "Cloud9": "クラウドベースの統合開発環境(IDE)",
    "X-Ray": "アプリケーションの分析とデバッグを支援するサービス",
    
    # 分析
    "Athena": "S3のデータに対してSQLクエリを実行するサービス",
    "EMR": "ビッグデータフレームワークを実行するサービス",
    "Kinesis": "リアルタイムのデータストリーミング処理サービス",
    "QuickSight": "ビジネスインテリジェンスサービス",
    "Glue": "ETL(抽出、変換、ロード)サービス",
    "Lake Formation": "データレイクを簡単に設定するサービス",
    "Data Exchange": "クラウドでデータ製品を検索、購読、使用するサービス",
    
    # 機械学習
    "SageMaker": "機械学習モデルの構築、トレーニング、デプロイを支援するサービス",
    "Rekognition": "画像・動画分析サービス",
    "Comprehend": "自然言語処理サービス",
    "Lex": "会話型インターフェイスを構築するサービス",
    "Polly": "テキストを音声に変換するサービス",
    "Textract": "ドキュメントからテキストやデータを抽出するサービス",
    "Forecast": "時系列予測サービス",
    "Kendra": "機械学習を活用した検索サービス",
    
    # メッセージング
    "SNS": "通知サービス",
    "SQS": "メッセージキューイングサービス",
    "EventBridge": "イベント駆動型アプリケーションを構築するサービス",
    "Step Functions": "分散アプリケーションのワークフローを調整するサービス",
    "MQ": "マネージド型メッセージブローカーサービス",
    
    # モバイル
    "Amplify": "モバイル・ウェブアプリケーションの構築と展開を支援するサービス",
    "AppSync": "リアルタイムデータ同期とオフラインプログラミング機能を提供するサービス",
    "Device Farm": "実際のデバイスでモバイルアプリをテストするサービス",
    
    # その他
    "WorkSpaces": "クラウドデスクトップサービス",
    "Connect": "クラウドコンタクトセンターサービス",
    "Managed Blockchain": "ブロックチェーンネットワークを作成・管理するサービス",
    "IoT Core": "IoTデバイスをクラウドに接続するサービス",
    "Ground Station": "衛星通信のためのフルマネージドサービス"
}
class Game:
    def __init__(self):
        self.reset_game()
        self.game_state = "menu"  # menu, playing, game_over, service_info
        self.high_score = 0
        self.answered_services = []  # 回答したサービスのリスト
        self.current_service_index = 0  # サービス情報画面で表示中のサービスインデックス
        self.current_service_name = ""  # 現在のサービス名（色を変えるため）
        self.total_chars = 0  # 入力した総文字数
    
    def reset_game(self):
        self.current_word = ""
        self.typed_text = ""
        self.score = 0
        self.mistakes = 0
        self.start_time = time.time()
        self.time_limit = 60  # 60秒
        self.answered_services = []  # 回答したサービスをリセット
        self.total_chars = 0  # 入力した総文字数を追加
        self.select_new_word()
    
    def select_new_word(self):
        # ランダムな文章を選択
        self.current_word = random.choice(aws_service_sentences)
        self.typed_text = ""
        
        # サービス名を抽出（<>で囲まれた部分）
        import re
        service_match = re.search(r'<([^>]+)>', self.current_word)
        if service_match:
            self.current_service_name = service_match.group(1)
        else:
            self.current_service_name = ""
    
    def update(self, events, ignore_space=False):
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
                    # <>を除いた文字列で比較（大文字・小文字を区別）
                    clean_current_word = self.current_word.replace('<', '').replace('>', '')
                    if self.typed_text == clean_current_word:  # 大文字・小文字を区別
                        self.score += len(clean_current_word)
                        self.total_chars += len(clean_current_word)  # 正解した文字数を追加
                        # 正解したサービスを記録
                        if self.current_service_name and self.current_service_name not in self.answered_services:
                            self.answered_services.append(self.current_service_name)
                        self.select_new_word()
                    else:
                        self.mistakes += 1
                # スペースキーを無視するオプションが有効な場合、スペースキーの入力を無視
                elif event.unicode.isprintable() and not (ignore_space and event.key == pygame.K_SPACE):
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
        pygame.draw.rect(screen, (30, 35, 45), (WIDTH//2 - 400, 120, 800, 450), 0, 10)
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 400, 120, 800, 450), 1, 10)
        
        # パネルヘッダー
        pygame.draw.rect(screen, BLUE, (WIDTH//2 - 400, 120, 800, 40), 0, 10, 10, 0, 0)
        panel_title = score_font.render("AWS サービス文章入力", True, WHITE)
        screen.blit(panel_title, (WIDTH//2 - panel_title.get_width()//2, 130))
        
        # 現在のワード表示 - AWS風のコンソール出力
        word_label = score_font.render("入力する文章:", True, LIGHT_GRAY)
        screen.blit(word_label, (WIDTH//2 - 350, 180))
        
        # サービス名を色付きで表示するための処理
        if self.current_service_name:
            # <>を除いた文字列を取得
            clean_word = self.current_word.replace('<', '').replace('>', '')
            
            # サービス名の位置を特定
            service_start = clean_word.find(self.current_service_name)
            if service_start != -1:
                service_end = service_start + len(self.current_service_name)
                
                # 文章を3つの部分に分割して描画
                before_service = clean_word[:service_start]
                service = clean_word[service_start:service_end]
                after_service = clean_word[service_end:]
                
                # 文章の幅を計算
                before_text = score_font.render(before_service, True, WHITE)
                service_text = score_font.render(service, True, ORANGE)
                after_text = score_font.render(after_service, True, WHITE)
                
                total_width = before_text.get_width() + service_text.get_width() + after_text.get_width()
                start_x = WIDTH//2 - total_width//2
                
                # 3つの部分を順番に描画
                screen.blit(before_text, (start_x, 220))
                screen.blit(service_text, (start_x + before_text.get_width(), 220))
                screen.blit(after_text, (start_x + before_text.get_width() + service_text.get_width(), 220))
            else:
                # サービス名が見つからない場合は通常通り表示
                word_text = score_font.render(clean_word, True, WHITE)
                screen.blit(word_text, (WIDTH//2 - word_text.get_width()//2, 220))
        else:
            # サービス名がない場合は通常通り表示
            word_text = score_font.render(self.current_word, True, WHITE)
            screen.blit(word_text, (WIDTH//2 - word_text.get_width()//2, 220))
        
        # 入力フィールド - AWS風の入力ボックス
        pygame.draw.rect(screen, (40, 45, 55), (WIDTH//2 - 350, 280, 700, 50), 0, 5)
        pygame.draw.rect(screen, LIGHT_BLUE if len(self.typed_text) > 0 else GRAY, 
                        (WIDTH//2 - 350, 280, 700, 50), 2, 5)
        
        # 入力中のテキスト表示
        if len(self.typed_text) > 0:
            typed_text = score_font.render(self.typed_text, True, WHITE)
            screen.blit(typed_text, (WIDTH//2 - 340, 295))
        else:
            placeholder = score_font.render("ここにタイプしてください...", True, GRAY)
            screen.blit(placeholder, (WIDTH//2 - 340, 295))
        
        # 正誤判定の視覚的フィードバック
        feedback_color = GREEN
        clean_current_word = self.current_word.replace('<', '').replace('>', '')
        for i, char in enumerate(self.typed_text):
            if i >= len(clean_current_word) or char != clean_current_word[i]:  # 大文字・小文字を区別
                feedback_color = RED
                break
        
        if len(self.typed_text) > 0:
            pygame.draw.rect(screen, feedback_color, (WIDTH//2 - 350, 335, 700, 3))
        
        # 入力ガイド
        guide_text = small_font.render("※ サービス名を含む文章全体を入力してください（大文字・小文字も区別）", True, LIGHT_GRAY)
        screen.blit(guide_text, (WIDTH//2 - guide_text.get_width()//2, 350))
        
        # 文字数表示を追加
        char_count_text = small_font.render(f"文字数: {len(self.typed_text)} / {len(clean_current_word)}", True, LIGHT_GRAY)
        screen.blit(char_count_text, (WIDTH//2 - 350, 380))
        
        # CPM表示を追加 - 文字数の下に表示
        elapsed_time = max(0.1, time.time() - self.start_time)  # 0除算を防ぐ
        current_cpm = int(self.total_chars / (elapsed_time / 60))
        cpm_text = small_font.render(f"CPM: {current_cpm} 文字/分", True, LIGHT_GRAY)
        screen.blit(cpm_text, (WIDTH//2 - 350, 405))
        
        # 評価表示 - CPMの下に表示
        # 評価カテゴリを決定
        if current_cpm >= 300:
            evaluation = "Hero"
            eval_color = GOLD
        elif current_cpm >= 250:
            evaluation = "Specialty"
            eval_color = PURPLE
        elif current_cpm >= 200:
            evaluation = "Professional"
            eval_color = EMERALD
        elif current_cpm >= 100:
            evaluation = "Associate"
            eval_color = BLUE_CATEGORY
        else:
            evaluation = "Foundational"
            eval_color = GRAY_CATEGORY
            
        eval_text = small_font.render(f"評価: {evaluation}", True, eval_color)
        screen.blit(eval_text, (WIDTH//2 - 350, 430))
        
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
        pygame.draw.rect(screen, (30, 35, 45), (WIDTH//2 - 400, 150, 800, 350), 0, 10)
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 400, 150, 800, 350), 1, 10)
        
        # パネルヘッダー
        pygame.draw.rect(screen, BLUE, (WIDTH//2 - 400, 150, 800, 40), 0, 10, 10, 0, 0)
        panel_title = score_font.render("結果サマリー", True, WHITE)
        screen.blit(panel_title, (WIDTH//2 - panel_title.get_width()//2, 160))
        
        # 結果表示 - AWS風のメトリクス表示
        
        # 最終スコア
        score_label = score_font.render("最終スコア:", True, LIGHT_GRAY)
        screen.blit(score_label, (WIDTH//2 - 250, 220))
        
        score_value = game_font.render(f"{self.score}", True, ORANGE)
        screen.blit(score_value, (WIDTH//2 + 50, 215))
        
        # 評価を表示
        elapsed_time = min(self.time_limit, time.time() - self.start_time)  # 実際の経過時間（最大60秒）
        cpm = 0 if elapsed_time == 0 else int(self.total_chars / (elapsed_time / 60))
        
        # 評価カテゴリを決定
        if cpm >= 300:
            evaluation = "Hero"
            eval_color = GOLD
        elif cpm >= 250:
            evaluation = "Specialty"
            eval_color = PURPLE
        elif cpm >= 200:
            evaluation = "Professional"
            eval_color = EMERALD
        elif cpm >= 100:
            evaluation = "Associate"
            eval_color = BLUE_CATEGORY
        else:
            evaluation = "Foundational"
            eval_color = GRAY_CATEGORY
        
        # 評価表示
        eval_label = score_font.render("評価:", True, LIGHT_GRAY)
        screen.blit(eval_label, (WIDTH//2 - 250, 270))
        eval_value = game_font.render(evaluation, True, eval_color)
        screen.blit(eval_value, (WIDTH//2 + 50, 265))
        
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
        pygame.draw.line(screen, GRAY, (WIDTH//2 - 350, 370), (WIDTH//2 + 350, 370), 1)
        
        # サービス情報ボタン（新機能）
        if len(self.answered_services) > 0:
            info_text = score_font.render("Iキー: サービス情報を見る", True, LIGHT_BLUE)
            screen.blit(info_text, (WIDTH//2 - info_text.get_width()//2, 390))
        
        # リスタート指示（背景なしで直接表示）
        restart_text = game_font.render("スペースキーでリスタート", True, ORANGE)
        restart_width = restart_text.get_width()
        restart_height = restart_text.get_height()
        # 中央に配置
        restart_x = WIDTH//2 - restart_width//2
        restart_y = 430
        screen.blit(restart_text, (restart_x, restart_y))
        
        # メニューに戻る指示
        menu_text = score_font.render("ESCキーでメニューに戻る", True, LIGHT_GRAY)
        screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, 480))
        
        # AWS風のフッター
        pygame.draw.rect(screen, BLUE, (0, HEIGHT - 30, WIDTH, 30))
    def draw_service_info(self):
        """サービス情報画面を描画"""
        # AWS風の濃い青背景
        screen.fill(DARK_BG)
        
        # AWS風のヘッダー
        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 50))
        pygame.draw.rect(screen, ORANGE, (0, 0, WIDTH, 3))
        
        # ヘッダータイトル
        header_title = score_font.render("AWS サービス情報", True, WHITE)
        screen.blit(header_title, (20, 15))
        
        # 回答したサービス数
        service_count = score_font.render(f"回答したサービス数: {len(self.answered_services)}", True, LIGHT_GRAY)
        screen.blit(service_count, (WIDTH - service_count.get_width() - 20, 15))
        
        # サービスがない場合
        if len(self.answered_services) == 0:
            no_service_text = game_font.render("回答したサービスがありません", True, LIGHT_GRAY)
            screen.blit(no_service_text, (WIDTH//2 - no_service_text.get_width()//2, HEIGHT//2 - 20))
            
            back_text = score_font.render("ESCキーで戻る", True, LIGHT_GRAY)
            screen.blit(back_text, (WIDTH//2 - back_text.get_width()//2, HEIGHT//2 + 40))
            return
        
        # 現在のサービス名
        current_service = self.answered_services[self.current_service_index]
        
        # サービス情報パネル
        pygame.draw.rect(screen, (30, 35, 45), (WIDTH//2 - 450, 80, 900, 500), 0, 10)
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 450, 80, 900, 500), 1, 10)
        
        # パネルヘッダー
        pygame.draw.rect(screen, BLUE, (WIDTH//2 - 450, 80, 900, 40), 0, 10, 10, 0, 0)
        service_title = score_font.render(f"サービス: {current_service}", True, WHITE)
        screen.blit(service_title, (WIDTH//2 - service_title.get_width()//2, 90))
        
        # サービスの説明
        description = aws_services_descriptions.get(current_service, "説明が見つかりません")
        
        # 説明テキストを複数行に分割して表示
        max_width = 850  # 幅を拡大
        words = description.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            test_text = score_font.render(test_line, True, WHITE)
            if test_text.get_width() < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        
        if current_line:
            lines.append(current_line)
        
        # 説明テキストを表示
        y_pos = 150
        for line in lines:
            desc_text = score_font.render(line, True, WHITE)
            screen.blit(desc_text, (WIDTH//2 - 420, y_pos))
            y_pos += 30
        
        # タイピングテキストを表示
        y_pos += 20
        example_title = score_font.render("Typing Text:", True, LIGHT_BLUE)
        screen.blit(example_title, (WIDTH//2 - 420, y_pos))
        y_pos += 30
        
        # このサービスを含む例文を探す
        examples = []
        for sentence in aws_service_sentences:
            if f"<{current_service}>" in sentence:
                clean_sentence = sentence.replace(f"<{current_service}>", current_service)
                examples.append(clean_sentence)
                break
        
        if examples:
            for example in examples:
                example_text = score_font.render(example, True, LIGHT_GRAY)
                screen.blit(example_text, (WIDTH//2 - 420, y_pos))
                y_pos += 30
                
                # 日本語訳を表示
                jp_translation = aws_service_sentences_jp.get(example, "翻訳が見つかりません")
                jp_text = score_font.render(f"日本語訳: {jp_translation}", True, LIGHT_GRAY)
                
                # 長い翻訳は複数行に分割
                if jp_text.get_width() > 850:
                    jp_words = jp_translation.split()
                    jp_lines = []
                    jp_current_line = "日本語訳: "
                    
                    for word in jp_words:
                        test_line = jp_current_line + word + " "
                        test_text = score_font.render(test_line, True, LIGHT_GRAY)
                        if test_text.get_width() < 850:
                            jp_current_line = test_line
                        else:
                            jp_lines.append(jp_current_line)
                            jp_current_line = word + " "
                    
                    if jp_current_line:
                        jp_lines.append(jp_current_line)
                    
                    for jp_line in jp_lines:
                        jp_line_text = score_font.render(jp_line, True, LIGHT_GRAY)
                        screen.blit(jp_line_text, (WIDTH//2 - 420, y_pos))
                        y_pos += 30
                else:
                    screen.blit(jp_text, (WIDTH//2 - 420, y_pos))
                    y_pos += 30
        else:
            no_example_text = score_font.render("例文が見つかりません", True, LIGHT_GRAY)
            screen.blit(no_example_text, (WIDTH//2 - 420, y_pos))
        
        # ナビゲーションボタン
        pygame.draw.rect(screen, (40, 45, 55), (WIDTH//2 - 420, 500, 840, 50), 0, 5)
        
        # 前のサービスボタン
        if len(self.answered_services) > 1:
            prev_text = score_font.render("← 前のサービス (A)", True, LIGHT_BLUE)
            screen.blit(prev_text, (WIDTH//2 - 400, 515))
        
        # 次のサービスボタン
        if len(self.answered_services) > 1:
            next_text = score_font.render("次のサービス (D) →", True, LIGHT_BLUE)
            screen.blit(next_text, (WIDTH//2 + 200, 515))
        
        # ページ番号
        page_text = score_font.render(f"{self.current_service_index + 1} / {len(self.answered_services)}", True, LIGHT_GRAY)
        screen.blit(page_text, (WIDTH//2 - page_text.get_width()//2, 515))
        
        # AWS風のフッター
        pygame.draw.rect(screen, BLUE, (0, HEIGHT - 40, WIDTH, 40))
        
        # 操作ガイド
        guide_text = score_font.render("ESC: 結果画面に戻る", True, WHITE)
        screen.blit(guide_text, (WIDTH//2 - guide_text.get_width()//2, HEIGHT - 30))
def main():
    clock = pygame.time.Clock()
    game = Game()
    space_key_released = True  # スペースキーが離されたかどうかを追跡する変数
    ignore_next_space = False  # 次のスペースキー入力を無視するフラグ
    
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game.game_state == "menu" and event.key == pygame.K_SPACE and space_key_released:
                    game.reset_game()
                    game.game_state = "playing"
                    space_key_released = False  # スペースキーが押されたのでフラグを下げる
                    ignore_next_space = True    # 次のスペースキー入力を無視するフラグを立てる
                elif game.game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        game.reset_game()
                        game.game_state = "playing"
                        space_key_released = False  # スペースキーが押されたのでフラグを下げる
                        ignore_next_space = True    # 次のスペースキー入力を無視するフラグを立てる
                    elif event.key == pygame.K_ESCAPE:
                        game.game_state = "menu"
                    elif event.key == pygame.K_i and len(game.answered_services) > 0:
                        # サービス情報画面に移動
                        game.current_service_index = 0
                        game.game_state = "service_info"
                elif game.game_state == "service_info":
                    if event.key == pygame.K_ESCAPE:
                        game.game_state = "game_over"
                    elif event.key == pygame.K_a and len(game.answered_services) > 1:
                        # 前のサービスに移動
                        game.current_service_index = (game.current_service_index - 1) % len(game.answered_services)
                    elif event.key == pygame.K_d and len(game.answered_services) > 1:
                        # 次のサービスに移動
                        game.current_service_index = (game.current_service_index + 1) % len(game.answered_services)
            
            # スペースキーが離されたことを検知
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                space_key_released = True
        
        if game.game_state == "playing":
            game.update(events, ignore_next_space)
            ignore_next_space = False  # 1フレームだけ無視するので、フラグをリセット
        
        # 描画
        if game.game_state == "menu":
            game.draw_menu()
        elif game.game_state == "playing":
            game.draw_game()
        elif game.game_state == "game_over":
            game.draw_game_over()
        elif game.game_state == "service_info":
            game.draw_service_info()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
