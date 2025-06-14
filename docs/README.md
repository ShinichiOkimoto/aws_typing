# ドキュメント索引

AWS Service Typing Game のドキュメント一覧です。各ドキュメントは異なる視点からプロジェクトを説明しており、目的に応じて参照してください。

## 📚 ドキュメント一覧

### 🏗️ [プロジェクト構造 (project-structure.md)](./project-structure.md)
- **対象読者**: 新規開発者、プロジェクト理解を深めたい方
- **内容**: 
  - ディレクトリ構造の詳細説明
  - 各ディレクトリの役割と責務
  - ファイル間の関係性
  - 設計パターンの説明

### 🏛️ [アーキテクチャ (architecture.md)](./architecture.md)
- **対象読者**: 技術設計者、システムの内部構造を理解したい方
- **内容**:
  - システム全体のアーキテクチャ概要
  - レイヤー別の詳細設計
  - データフローと制御フロー
  - 設計原則と哲学
  - パフォーマンス最適化戦略

### 📖 [APIリファレンス (api-reference.md)](./api-reference.md)
- **対象読者**: 機能拡張・カスタマイズを行う開発者
- **内容**:
  - 主要クラスとメソッドの仕様
  - 使用方法とコード例
  - 拡張のためのフック
  - エラーハンドリング方法
  - テスト用ユーティリティ

## 🎯 用途別ガイド

### 🚀 初回セットアップ時
1. **[メインREADME](../README.md)** - インストールと基本的な使用方法
2. **[プロジェクト構造](./project-structure.md)** - プロジェクト全体の理解

### 🔧 開発・カスタマイズ時
1. **[アーキテクチャ](./architecture.md)** - システム設計の理解
2. **[APIリファレンス](./api-reference.md)** - 実装の詳細
3. **[CLAUDE.md](../CLAUDE.md)** - 開発ガイダンス

### 🐛 トラブルシューティング時
1. **[APIリファレンス](./api-reference.md)** - エラーハンドリング
2. **[アーキテクチャ](./architecture.md)** - データフローの確認
3. **[CLAUDE.md](../CLAUDE.md)** - 開発コマンドとツール

### 📈 機能拡張時
1. **[アーキテクチャ](./architecture.md)** - 拡張性設計の理解
2. **[APIリファレンス](./api-reference.md)** - 拡張ポイントの確認
3. **[プロジェクト構造](./project-structure.md)** - 適切な配置場所の決定

## 🔍 キーワード別索引

### マネージャーパターン
- [プロジェクト構造 - マネージャー群](./project-structure.md#🛠️-managers---マネージャー群)
- [アーキテクチャ - Manager Layer](./architecture.md#2-manager-layer-マネージャー層)
- [APIリファレンス - マネージャークラス](./api-reference.md#マネージャークラス)

### スコアリングシステム
- [アーキテクチャ - スコアリングアーキテクチャ](./architecture.md#スコアリングアーキテクチャ)
- [APIリファレンス - Game クラス](./api-reference.md#game-クラス)

### アクセシビリティ
- [プロジェクト構造 - アクセシビリティマネージャー](./project-structure.md#accessibility_managerpy---アクセシビリティ)
- [アーキテクチャ - アクセシビリティアーキテクチャ](./architecture.md#アクセシビリティアーキテクチャ)
- [APIリファレンス - AccessibilityManager](./api-reference.md#accessibilitymanager-クラス)

### データ管理
- [プロジェクト構造 - データ管理](./project-structure.md#data_managerpy---データ管理)
- [アーキテクチャ - データアクセスフロー](./architecture.md#3-データアクセスフロー)
- [APIリファレンス - DataManager](./api-reference.md#datamanager-クラス)

### UI・描画システム
- [プロジェクト構造 - UI管理](./project-structure.md#🎨-ui---ユーザーインターフェース)
- [アーキテクチャ - UIマネージャー群](./architecture.md#uiマネージャー群)
- [APIリファレンス - UIManager](./api-reference.md#uimanager-クラス)

### 音響システム
- [プロジェクト構造 - 音響管理](./project-structure.md#audio_managerpy---音響管理)
- [アーキテクチャ - 音響マネージャー群](./architecture.md#音響マネージャー群)
- [APIリファレンス - AudioManager](./api-reference.md#audiomanager-クラス)

### レスポンシブデザイン
- [プロジェクト構造 - レスポンシブ設計](./project-structure.md#responsive_managerpy---レスポンシブ設計)
- [アーキテクチャ - レスポンシブ設計](./architecture.md#レスポンシブ設計)
- [APIリファレンス - ResponsiveManager](./api-reference.md#responsivemanager-クラス)

## 📝 更新履歴

| 日付 | ドキュメント | 更新内容 |
|------|-------------|----------|
| 2024-06-07 | 全ドキュメント | 初版作成 |

## 🤝 コントリビューション

ドキュメントの改善や追加に関する提案は歓迎いたします。以下の点にご留意ください：

### ドキュメント作成ガイドライン
1. **明確性**: 技術的な内容も分かりやすく説明
2. **完全性**: 必要な情報を漏れなく記載
3. **一貫性**: 他のドキュメントとの整合性を保持
4. **実用性**: 実際の作業で使える具体的な情報

### 更新プロセス
1. ドキュメントの内容について Issue を作成
2. 変更内容を Pull Request で提出
3. レビューと承認を経て反映

## 📞 サポート

ドキュメントに関する質問や不明点がある場合は、以下の方法でお問い合わせください：

- **GitHub Issues**: バグレポートや機能要望
- **Discussions**: 一般的な質問や議論

---

**注意**: このドキュメントは AWS Service Typing Game v2.0.0 に基づいて作成されています。バージョンアップにより内容が変更される場合があります。