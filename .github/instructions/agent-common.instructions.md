# エージェント共通構造 (v1.0)

> **適用対象**: すべてのエージェントファイル
> **最終更新**: 2025-12-12

このインストラクションは、エージェントファイルの共通構造と必須セクションを定義します。

---

## エージェント構成（v4.x）

### 3 エージェント体制

| Agent             | 責務                                   | 委譲先        |
| ----------------- | -------------------------------------- | ------------- |
| Flow Orchestrator | 全体統括、入力分析、Review Engine 内包 | Gateway/Forge |
| Manifest Gateway  | マニフェスト作成（全入力タイプ対応）   | なし          |
| SVG Forge         | 図面生成、自己検証、保存前ゲート       | なし          |

### 廃止されたエージェント

| エージェント              | 廃止バージョン | 理由                     |
| ------------------------- | -------------- | ------------------------ |
| router-agent              | v3.0           | Flow Orchestrator に統合 |
| planner-agent             | v3.0           | Flow Orchestrator に統合 |
| text-manifest-gateway     | v3.0           | manifest-gateway に統合  |
| visual-manifest-gateway   | v3.0           | manifest-gateway に統合  |
| portrait-manifest-gateway | v3.0           | manifest-gateway に統合  |
| manifest-review           | v4.0           | Orchestrator に内包      |
| svg-review                | v4.0           | Orchestrator に内包      |

---

## 共通セクション構造

各エージェントファイルは以下のセクションを含むこと：

```yaml
required_sections:
  - header: # chatagent ブロック（Instructions, Tools, Purpose, Version）
  - changelog: # 変更履歴テーブル
  - responsibilities # Job Responsibility / Non-goal
  - inputs_outputs: # 入力と出力の定義
  - workflow: # ワークフロー図
  - error_handling: # エラーハンドリングテーブル
  - related_agents: # 関連エージェント参照

optional_sections:
  - instructions_ref: # 共通インストラクション参照テーブル
  - steps: # 詳細ステップ
  - examples: # 出力例
```

---

## 共通エラーハンドリング

### 全エージェント共通

| エラー               | 対応                               |
| -------------------- | ---------------------------------- |
| Context 不正         | Orchestrator にエラー報告          |
| ファイル重複         | 自動リネーム（`_01`, `_02`...）    |
| ファイル書き込み失敗 | パス確認、リトライ（最大 2 回）    |
| タイムアウト         | 現状を保存して Orchestrator に報告 |

### ファイル重複チェック

```yaml
file_duplicate_check:
  required: true
  method: "list_dir(output_directory)"

  on_duplicate:
    action: "auto_rename"
    format: "{base}_{nn}.{ext}"
    example: "azure-diagram_01.drawio"
```

---

## WorkflowContext

### 構造

```yaml
workflow_context:
  path: "outputs/.workflow/{workflow_id}/context.yaml"

  required_fields:
    - workflow_id: "一意のワークフロー識別子"
    - input_hash: "入力のSHA256ハッシュ（冪等性キー）"
    - input_type: "text | visual | portrait"
    - complexity: "simple | moderate | complex"
    - current_phase: "analysis | manifest | review | svg | complete"

  optional_fields:
    - checkpoint_id: "最新のチェックポイント番号 (1-5)"
    - manifest_path: "マニフェストファイルパス"
    - svg_path: "生成済み図面パス"
    - quality_score: "最新の品質スコア"
```

### チェックポイント

```yaml
checkpoints:
  save_points:
    - id: 1
      after: "input_analysis"
    - id: 2
      after: "manifest_creation"
    - id: 3
      after: "manifest_review_pass"
    - id: 4
      after: "svg_generation"
    - id: 5
      after: "svg_review_pass"

  file_format: "outputs/.workflow/{id}/context.cp{1-5}.yaml"
```

---

## 冪等性ルール

```yaml
idempotency:
  input_hashing:
    algorithm: "sha256"
    inputs: ["user_input", "attached_files_hash"]

  cache:
    analysis: "outputs/.cache/analysis/{hash}.yaml"
    mcp_results: "outputs/.cache/mcp/{query_hash}.yaml"

  llm_config:
    temperature: 0
    seed: "derived_from_workflow_id"
```

---

## 委譲ルール

### runSubagent 使用対象

```yaml
delegation:
  use_runSubagent:
    - "manifest-gateway" # マニフェスト作成
    - "svg-forge" # 図面生成

  direct_execution:
    - "input_analysis" # Orchestrator 内蔵
    - "manifest_review" # Orchestrator 内蔵
    - "svg_review" # Orchestrator 内蔵

  required_params:
    - workflow_id
    - context_path
    - current_phase
```

---

## 繰り返し上限

| 複雑度   | 最大イテレーション | 品質閾値 |
| -------- | ------------------ | -------- |
| simple   | 3                  | 85 点    |
| moderate | 4                  | 90 点    |
| complex  | 5                  | 95 点    |

---

## 出力パス規則

```yaml
output_paths:
  base: "outputs/"

  patterns:
    diagram: "outputs/{name}.drawio"
    manifest: "outputs/.workflow/{id}/manifest.v{n}.md"
    context: "outputs/.workflow/{id}/context.yaml"
    cache: "outputs/.cache/{type}/{hash}.yaml"

  naming:
    format: "kebab-case"
    prohibited:
      - スペース
      - 日本語文字
      - 特殊文字（`&`, `?`, `#` など）
```

---

## MCP 活用ルール

### Azure/Microsoft 関連の図

```yaml
mcp_usage:
  trigger: "Azure|Microsoft|Power|Office|Teams|Entra"

  tools:
    - mcp_microsoftdocs_microsoft_docs_search
    - mcp_microsoftdocs_microsoft_code_sample_search

  use_cases:
    - "正式サービス名の確認"
    - "公式アーキテクチャ参照"
    - "アイコン名の確認"

  caching:
    enabled: true
    ttl: "24h"
    path: "outputs/.cache/mcp/"
```

### クエリ例

```yaml
mcp_queries:
  service_name: "Azure {service} official name documentation"
  architecture: "Azure {service} reference architecture diagram"
  icon: "Azure {service} icon draw.io"
```
