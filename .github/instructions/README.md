# `.github/instructions` ディレクトリ

> エージェントが参照する共通ルール・ガイドラインを管理するディレクトリ。

## 概要

このディレクトリには、複数のエージェントが共通で参照するドメイン別のガイドラインを配置します。各 `.agent.md` ファイルの `Instructions:` フィールドから参照され、一貫した動作を保証します。

## ファイル一覧

| ファイル                              | 用途                                   | 参照元                    |
| ------------------------------------- | -------------------------------------- | ------------------------- |
| `agent-workflow-v5.instructions.md`   | 全体ワークフロー、共通ルール、禁止事項 | 全エージェント            |
| `manifest-template.instructions.md`   | マニフェストのスキーマ、必須項目、例   | manifest-gateway.agent.md |
| `svg-forge-template.instructions.md`  | SVG 生成の詳細手順、draw.io 互換性     | svg-forge.agent.md        |
| `svg-review-template.instructions.md` | レビュー観点、スコアリング基準         | svg-review.agent.md       |

## ファイル詳細

### agent-workflow-v5.instructions.md

**全エージェント共通のワークフロー定義 (v5.0)**

- 全体フロー概要図
- 入力種別判定ルール
- 出力規約（パス、拡張子、編集可能性）
- レビュープロセス（スコアリング基準）
- runSubagent 利用基準
- 禁止事項
- エラーハンドリング共通規約

### manifest-template.instructions.md

**マニフェスト作成の詳細ガイド**

- 必須/任意項目一覧
- 完全な YAML スキーマ定義
- ノードタイプ一覧（rectangle, ellipse, diamond, cylinder 等）
- 接続タイプ一覧（arrow, line, bidirectional, dashed）
- レイアウトパターン（hierarchical, organic, grid, circle）
- カラースキーム定義
- 具体例（フローチャート、アーキテクチャ図、組織図）

### svg-forge-template.instructions.md

**SVG 生成の技術詳細**

- 入力バリデーション
- キャンバス設定（ページサイズ、グリッド、マージン）
- ノード配置（形状マッピング、レイアウトアルゴリズム）
- コネクタ描画（エッジスタイル、ルーティング）
- スタイル適用（カラースキーム、タイポグラフィ）
- draw.io メタ情報の埋め込み方法
- mxfile XML 構造
- 事後チェック項目

### svg-review-template.instructions.md

**SVG レビューの詳細基準**

- 4 カテゴリのチェックリスト（各 25 点満点）
  - マニフェスト整合
  - 視認性
  - スタイル準拠
  - 技術確認
- スコアリング基準（0-100 点、累積評価）
- 適応型 1-3 ラウンド運用（複雑度に応じて早期終了）
- 完了条件
- レビュー実行手順

## 命名規約

```
<topic>.instructions.md
```

- `<topic>`: 内容を表す英語の短い名前（kebab-case 推奨）
- 例: `agent-workflow`, `manifest-template`, `svg-forge-template`

## 新規ファイル追加時のガイドライン

1. **目的の明確化**: 何のためのガイドラインか明記
2. **スコープ定義**: 対象エージェント/処理を特定
3. **構造化**: 見出し、リスト、テーブルで整理
4. **具体例**: 抽象的な説明だけでなく具体例を含める
5. **関連ファイル**: 関連する他ファイルへのリンクを追加

## 依存関係

```
agent-workflow-v5.instructions.md (v5.0)
    │
    ├── manifest-template.instructions.md
    │       └── manifest-gateway.agent.md が参照
    │
    ├── svg-forge-template.instructions.md
    │       └── svg-forge.agent.md が参照
    │
    └── svg-review-template.instructions.md
            └── svg-review.agent.md が参照
```

## 更新時の注意

- 共通ルールを変更する場合は、影響を受けるエージェントを確認
- スキーマ変更時は、既存マニフェストとの互換性を考慮
- バージョン管理: 大きな変更時はファイル内にバージョン履歴を追加

## 関連ディレクトリ

| ディレクトリ      | 用途                           |
| ----------------- | ------------------------------ |
| `.github/agents/` | エージェント定義（.agent.md）  |
| `image_manifest/` | 生成されたマニフェストファイル |
| `outputs/`        | 生成された SVG/PNG ファイル    |
