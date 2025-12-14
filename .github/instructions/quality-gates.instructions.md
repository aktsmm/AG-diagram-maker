# 品質ゲートルール (v1.0)

> **適用対象**: すべての draw.io 図面生成エージェント
> **最終更新**: 2025-12-12

このインストラクションは、図面生成の品質を保証するためのゲートルールを定義します。

---

## mxCell 完全性チェック

### 基本ルール

| ルール               | 内容                                      |
| -------------------- | ----------------------------------------- |
| **mxCell 必須**      | content 属性に有効な mxCell 定義が必須    |
| **空コンテンツ禁止** | mxCell 定義のない空の mxGraphModel は禁止 |
| **完全性検証**       | mxCell 数 >= 2 + ノード数 + エッジ数      |

### 完全性計算式

```yaml
mxcell_completeness:
  formula: |
    expected_mxcells = 2 + manifest.nodes.length + manifest.edges.length
    actual_mxcells = count(<mxCell> in content)

    MUST: actual_mxcells >= expected_mxcells

  explanation:
    base_cells: 2 # id="0" と id="1" の親セル
    node_cells: "マニフェストで定義されたノード数"
    edge_cells: "マニフェストで定義されたエッジ数"

  example:
    manifest:
      nodes: ["A", "B", "C"] # 3ノード
      edges: ["A→B", "B→C"] # 2エッジ
    expected: 2 + 3 + 2 = 7 # 最低7つの mxCell が必要
```

### 検証タイミング

```yaml
validation_points:
  - point: "SVG 生成完了時（svg-forge 内）"
    action: "自己検証で mxCell 数を確認"

  - point: "保存前ゲート"
    action: "最終検証、失敗時は保存ブロック"

  - point: "Orchestrator 受領時"
    action: "即時検証、mxCell 数の整合性確認"
```

---

## 保存前ゲート

### 実行内容

```yaml
pre_save_gate:
  description: "保存前の最終検証。失敗時は保存をブロック。"

  checks:
    - name: "mxcell_count_valid"
      condition: "actual >= expected"

    - name: "content_not_empty"
      condition: "content 属性が空でない"

    - name: "all_nodes_have_mxcell"
      condition: "マニフェストの全ノードに対応する mxCell が存在"

    - name: "all_edges_have_mxcell"
      condition: "マニフェストの全エッジに対応する mxCell が存在"

  on_fail:
    action: "block_and_retry"
    max_retries: 2
    fallback: "エラー報告してユーザーに確認"
```

### ブロック時のアクション

```yaml
blocking_action:
  severity: CRITICAL

  steps:
    1: "エラー内容を特定（どの mxCell が不足しているか）"
    2: "マニフェストから不足分の mxCell を再生成"
    3: "再度保存前ゲートを通過させる"
    4: "2回失敗した場合、部分成功またはエスカレーション"
```

---

## draw.io 互換性チェック

### 必須検証項目

```yaml
drawio_compatibility:
  mandatory_checks:
    - name: "generator 属性の存在"
      target: "mxfile タグ"
      condition: 'generator="aktsmm/Ag-diagram-maker" が設定されている'

    - name: "content 属性の存在"
      target: ".drawio.svg 形式の場合"

    - name: "mxGraphModel 構造"
      condition: "<mxGraphModel> タグが正しく存在"

    - name: "mxCell 定義の存在"
      condition: "空でない mxCell が含まれる"

    - name: "視覚要素との対応"
      condition: "SVG の場合、描画要素と mxCell が対応"

  prohibited_patterns:
    - "空の content 属性"
    - "mxCell 定義のない空の mxGraphModel"
    - "SVG 要素のみで mxCell 定義なし"
    - "generator 属性なしの mxfile"
```

---

## スコア帯別アクション

### 判定基準

| スコア帯 | アクション          | 遷移先                 |
| -------- | ------------------- | ---------------------- |
| 90-100   | `proceed`           | 次フェーズ             |
| 85-89    | `proceed_with_note` | 次フェーズ（注記付き） |
| 70-84    | `fix_and_retry`     | 同フェーズ             |
| 50-69    | `auto_simplify`     | 簡略化して再試行       |
| 30-49    | `partial_success`   | 部分成功として提示     |
| 0-29     | `escalate`          | ユーザー確認           |

### 各アクションの詳細

```yaml
actions:
  proceed:
    description: "品質基準を満たした。次のフェーズへ進む。"

  proceed_with_note:
    description: "軽微な問題あり。注記を付けて次へ進む。"
    note_example: "一部のラベルが長いため、draw.io で調整推奨"

  fix_and_retry:
    description: "修正可能な問題あり。同フェーズで修正後、再評価。"
    max_attempts: 2

  auto_simplify:
    description: "複雑すぎる。自動的に簡略化して再試行。"
    simplification_methods:
      - "重要度の低いノードを削除"
      - "ラベルを短縮"
      - "シンプルな図形に変更"

  partial_success:
    description: "一部のみ成功。成功部分を提示してユーザー判断を仰ぐ。"
    output:
      partial_result: "生成できた部分"
      issues_summary: "残っている問題点"
      manual_fix_guide: "手動での修正方法"

  escalate:
    description: "根本的な問題あり。ユーザーに確認が必要。"
    output:
      error_summary: "何が問題か"
      attempted_interpretation: "こう解釈しました"
      clarification_questions: "確認したい点"
```

---

## 適応型レビュー

### 複雑度別設定

| 複雑度   | 最大イテレーション | 品質閾値 | 早期終了         |
| -------- | ------------------ | -------- | ---------------- |
| simple   | 3                  | 85 点    | 閾値達成で即終了 |
| moderate | 4                  | 90 点    | 閾値達成で即終了 |
| complex  | 5                  | 95 点    | 閾値達成で即終了 |

### 複雑度判定

```yaml
complexity_rules:
  simple:
    condition: "entities.length <= 5"
    examples: ["ログインフロー", "単純なER図"]

  moderate:
    condition: "5 < entities.length <= 15"
    examples: ["中規模アーキテクチャ図", "業務フロー"]

  complex:
    condition: "entities.length > 15"
    examples: ["マイクロサービス構成", "大規模ネットワーク図"]
```

---

## エラーリカバリー

### ファイル操作エラー

```yaml
file_operation_errors:
  duplicate_file:
    action: "自動リネーム（_01, _02, ...）"

  permission_error:
    action: "代替パスを使用"
    fallback: "outputs/temp/"

  write_error:
    action: "一時ファイルに保存"
    notify: "ユーザーに通知"
```

### 生成エラー

```yaml
generation_errors:
  mxcell_incomplete:
    type: "CRITICAL_MXCELL_INCOMPLETE"
    action: "マニフェストから再生成を試行"
    max_retries: 2

  content_empty:
    type: "CRITICAL_CONTENT_EMPTY"
    action: "エラー報告、ユーザー確認"

  format_invalid:
    type: "WARNING_FORMAT_INVALID"
    action: "自動修正を試行"
```

---

## チェックポイント

### 保存ポイント

```yaml
checkpoints:
  - id: 1
    after: "input_analysis"
    description: "入力分析完了"

  - id: 2
    after: "manifest_creation"
    description: "マニフェスト作成完了"

  - id: 3
    after: "manifest_review_pass"
    description: "マニフェストレビュー通過"

  - id: 4
    after: "diagram_generation"
    description: "図面生成完了"

  - id: 5
    after: "diagram_review_pass"
    description: "図面レビュー通過（完了）"

recovery:
  on_failure: |
    1. find_latest_checkpoint()
    2. load_context_snapshot()
    3. resume_from_phase(checkpoint.phase)
```

---

## まとめ

| 品質ゲート       | 必須度 | タイミング       |
| ---------------- | ------ | ---------------- |
| mxCell 完全性    | 必須   | 生成後、保存前   |
| 保存前ゲート     | 必須   | 保存直前         |
| draw.io 互換性   | 必須   | 生成後           |
| スコア判定       | 必須   | レビュー時       |
| チェックポイント | 推奨   | 各フェーズ完了時 |
