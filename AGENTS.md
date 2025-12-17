# Agents Catalog (v5.1)

リポジトリで使用する構造化エージェントの一覧です。詳細な運用フローは `./.github/copilot-instructions.md` を参照してください。

## エージェント構成（3 エージェント）

| Agent             | Path                                        | Purpose / When to use                                                                               | Output                   | Version |
| ----------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------ | ------- |
| Flow Orchestrator | `.github/agents/flow-orchestrator.agent.md` | 全体フロー統括。**4 内部モジュール（Analysis/Review/State/Timeout）を内包**。チェックポイント管理。 | ハンドオフ指示、完了報告 | v5.0    |
| Manifest Gateway  | `.github/agents/manifest-gateway.agent.md`  | **統合 Gateway**。全入力タイプ（text/visual/portrait）に対応。早期品質チェック。高速パス対応。      | マニフェストドラフト     | v5.0    |
| SVG Forge         | `.github/agents/svg-forge.agent.md`         | レビュー済みマニフェストから draw.io 編集可能な図面を生成。**自己検証 + 保存前ゲート**。            | 生成済み図面             | v5.0    |

## 📋 共通インストラクション一覧

| インストラクション           | Path                                                             | 内容                                       |
| ---------------------------- | ---------------------------------------------------------------- | ------------------------------------------ |
| **エージェント共通**         | `.github/instructions/agent-common.instructions.md`              | 共通構造、WorkflowContext、冪等性          |
| **ワークフロー**             | `.github/instructions/agent-workflow-v5.instructions.md`         | 全体ワークフロー定義 (v5.0)                |
| **責務分離 v5.1**            | `.github/instructions/agent-responsibilities-v5.instructions.md` | 5 層責務分離 (Parse/Generate/Validate/...) |
| **決定的変換**               | `.github/instructions/deterministic-transform.instructions.md`   | IR → mxCell の決定的変換ルール             |
| **ロギング**                 | `.github/instructions/logging-traceability.instructions.md`      | 全フェーズのロギング仕様                   |
| **draw.io 互換性**           | `.github/instructions/drawio-compatibility.instructions.md`      | mxCell 構造、スタイル、検証                |
| **クラウドアイコン**         | `.github/instructions/cloud-icons.instructions.md`               | Azure/AWS アイコン使用ルール               |
| **出力形式**                 | `.github/instructions/output-format.instructions.md`             | .drawio vs .drawio.svg 選択                |
| **品質ゲート**               | `.github/instructions/quality-gates.instructions.md`             | mxCell 検証、保存前ゲート                  |
| **マニフェストテンプレート** | `.github/instructions/manifest-template.instructions.md`         | マニフェスト作成テンプレート               |
| **SVG Forge テンプレート**   | `.github/instructions/svg-forge-template.instructions.md`        | SVG 生成テンプレート                       |
| **SVG レビューテンプレート** | `.github/instructions/svg-review-template.instructions.md`       | SVG レビューテンプレート                   |

## 📋 スキーマ一覧

| スキーマ         | Path                                          | 内容                       |
| ---------------- | --------------------------------------------- | -------------------------- |
| **DiagramIR**    | `.github/schemas/diagram-ir.schema.json`      | 中間表現の JSON Schema     |
| **Config**       | `.github/schemas/config.schema.json`          | 環境設定の JSON Schema     |
| **SubAgent Res** | `.github/schemas/subagent-response.schema.md` | runSubagent 戻り値の標準形 |

## 補足ドキュメント

| ドキュメント                 | Path                                          | 説明                                       |
| ---------------------------- | --------------------------------------------- | ------------------------------------------ |
| **変更履歴**                 | `.github/CHANGELOG.md`                        | 全バージョンの変更履歴                     |
| SubAgent Response Schema     | `.github/schemas/subagent-response.schema.md` | runSubagent 戻り値の標準形式               |
| Workflow Review Report v3    | `docs/workflow-review-report-v3.md`           | v2.0→v3.0 リファクタリングのレビュー報告書 |
| Workflow Review Report v5    | `docs/workflow-review-report-v5.md`           | v5 ワークフローのレビュー報告書            |
| **Architecture Report v5.1** | `docs/workflow-architecture-v5.1-report.md`   | v5.1 二段階アーキテクチャ改善報告書        |

---

## モデル要件（重要）

- **前提**: 本リポジトリのエージェントワークフロー（Flow Orchestrator → Manifest Gateway → SVG Forge）は、エージェントワークフローに対応した AI モデルを前提に設計されています。非対応モデルでは段階的なレビュー/保存前ゲート/チェックポイント連携が正しく動作しない場合があります。
- **推奨モデル**: Opus（複雑な図面生成とレビュー反復の安定性に優れ、エージェントワークフロー互換）
- **代替運用**: 他モデルを利用する場合は、フェーズを単体実行に切り替える、または人手によるレビューを併用してください。

## 標準フロー

> **📋 詳細は `.github/instructions/agent-workflow-v5.instructions.md` を参照**

```
USER INPUT
    │
    ▼
┌─────────────────────────────────────┐
│ Flow Orchestrator                   │
│  [内蔵] Input Analysis (5秒)        │
│  → Checkpoint 1                     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Manifest Gateway (runSubagent)      │
│  → Checkpoint 2                     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ [Orchestrator内蔵] Manifest Review  │
│  → Checkpoint 3                     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ SVG Forge + 自己検証 + 保存前ゲート │
│  → Checkpoint 4                     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ [Orchestrator内蔵] SVG Review       │
│  → Checkpoint 5                     │
└──────────────┬──────────────────────┘
               │
               ▼
       完了 / 部分成功
```

---

## 運用ルール

> **📋 詳細は各インストラクションを参照**

| ルール               | 詳細                                         | 参照            |
| -------------------- | -------------------------------------------- | --------------- |
| **WorkflowContext**  | 全処理で状態管理（冪等性確保）               | `agent-common`  |
| **出力パス**         | `outputs/` 配下、kebab-case、`*.drawio` 推奨 | `output-format` |
| **mxCell 完全性**    | mxCell 数 >= 2 + ノード数 + エッジ数         | `quality-gates` |
| **保存前ゲート**     | 検証失敗時はファイル保存をブロック           | `quality-gates` |
| **クラウドアイコン** | Azure/AWS 公式アイコンを使用                 | `cloud-icons`   |
