```instructions
# エージェント責務分離 v5.0

> **適用対象**: すべてのエージェント
> **最終更新**: 2025-12-12

このインストラクションは、v5.0 で導入される「責務分離の原則」に基づくエージェント構成を定義します。

---

## 🎯 設計原則

### 責務分離の5層

| 層 | 責務 | 説明 | 混在禁止 |
|----|------|------|----------|
| **Parse** | 入力解析 | ユーザー入力を構造化データに変換 | Generate と混在禁止 |
| **Generate** | IR生成 | 構造化データから DiagramIR を生成 | Transform と混在禁止 |
| **Validate** | 検証 | IR/出力のスキーマ検証 | 生成・変換と混在禁止 |
| **Transform** | 変換 | IR → mxGraphModel への決定的変換 | Generate と混在禁止 |
| **Produce** | 出力 | ファイル書き込み、最終出力 | 他すべてと分離 |

### エージェントへのマッピング

```

┌────────────────────────────────────────────────────────────────────────────┐
│ v5.0 エージェント構成 (4 + 1 エージェント) │
├────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ Coordinator (調整役) - 旧 Orchestrator │ │
│ │ 責務: フロー制御、チェックポイント、エラーハンドリング │ │
│ │ 禁止: Parse/Generate/Validate/Transform/Produce のいずれも持たない │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ┌──────────────────┼──────────────────┐ │
│ ▼ ▼ ▼ │
│ ┌────────────┐ ┌────────────────┐ ┌────────────────┐ │
│ │ IR-Builder │ │ IR-Validator │ │ IR-Renderer │ │
│ │ (Parse + │ │ (Validate) │ │ (Transform + │ │
│ │ Generate) │ │ │ │ Produce) │ │
│ └────────────┘ └────────────────┘ └────────────────┘ │
│ │
│ + Logger (横断的関心事、独立モジュール) │
│ │
└────────────────────────────────────────────────────────────────────────────┘

````

---

## 📋 各エージェント仕様

### 1. Coordinator (調整役)

**責務**:
- ワークフロー全体の制御
- チェックポイントの保存・復旧
- エラー時のルーティング（差し戻し先決定）
- ユーザーとの対話（質問・確認）

**禁止**:
- IR の生成・編集
- スキーマ検証の直接実行
- mxGraphModel の変換
- ファイル出力

**入力**: ユーザーリクエスト
**出力**: 完了報告、エラー報告

```yaml
coordinator:
  tools:
    - runSubagent
    - manage_todo_list
    - read_file  # 状態確認のみ

  delegates_to:
    - ir-builder
    - ir-validator
    - ir-renderer

  state_management:
    checkpoint_path: "outputs/.workflow/{id}/checkpoint.json"
    log_path: "outputs/.workflow/{id}/coordinator.log"
````

---

### 2. IR-Builder (Parse + Generate)

**責務**:

- ユーザー入力の解析（Parse）
- DiagramIR の生成（Generate）
- **生成した IR は編集しない**（不正なら再生成）

**禁止**:

- 検証（Validate は別エージェント）
- mxGraphModel への変換
- ファイル出力

**入力**:

- ユーザーリクエスト（テキスト / 画像参照）
- input_type: text | visual | portrait

**出力**:

- DiagramIR (JSON)
- `outputs/.workflow/{id}/ir.v{n}.json`

```yaml
ir_builder:
  tools:
    - read_file
    - create_file
    - semantic_search
    - mcp_microsoftdocs_microsoft_docs_search # Azure用語確認

  output_schema: ".github/schemas/diagram-ir.schema.json"

  rules:
    - 生成した IR は変更しない（再生成はOK）
    - スキーマに合致しない構造は生成しない
    - 曖昧な入力は Coordinator にエスカレート
```

**生成フロー**:

```
入力テキスト
    │
    ▼
┌──────────────┐
│ 1. Parse     │  ユーザー意図を抽出
│   意図抽出    │  → ParseResult
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 2. Extract   │  ノード・エッジを列挙
│   要素抽出    │  → ElementList
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 3. Structure │  DiagramIR 構造を組み立て
│   構造化     │  → DiagramIR (JSON)
└──────┬───────┘
       │
       ▼
    DiagramIR
```

---

### 3. IR-Validator (Validate)

**責務**:

- DiagramIR のスキーマ検証
- 参照整合性チェック（from/to が存在するか）
- 出力前の最終検証
- **検証のみ、修正はしない**

**禁止**:

- IR の生成・編集
- 自動修正（エラー報告のみ）
- ファイル出力

**入力**:

- DiagramIR (JSON)
- 検証対象ファイルパス

**出力**:

- ValidationResult (pass/fail + issues)

```yaml
ir_validator:
  tools:
    - read_file

  schema_path: ".github/schemas/diagram-ir.schema.json"

  validation_types:
    - schema_validation # JSON Schema 適合
    - reference_integrity # from/to 参照チェック
    - semantic_validation # ラベル重複、循環参照など
    - mxcell_readiness # 変換可能性チェック

  output:
    type: ValidationResult
    fields:
      - valid: boolean
      - score: number (0-100)
      - issues: array<Issue>
      - blocking_issues: array<Issue>

  rules:
    - 修正は行わない（エラー報告のみ）
    - blocking_issue があれば valid=false
    - 自動補完は禁止
```

**ValidationResult 構造**:

```json
{
  "valid": true,
  "score": 95,
  "issues": [
    {
      "severity": "warning",
      "code": "LABEL_TOO_LONG",
      "message": "ノード 'node_a' のラベルが50文字を超えています",
      "path": "$.elements[0].label",
      "suggestion": "ラベルを短縮することを推奨"
    }
  ],
  "blocking_issues": [],
  "checked_at": "2025-12-12T10:00:00Z"
}
```

---

### 4. IR-Renderer (Transform + Produce)

**責務**:

- DiagramIR → mxGraphModel への**決定的変換**
- ファイル出力（.drawio / .drawio.svg）
- **創作的判断を一切行わない**

**禁止**:

- IR の解釈・補完
- レイアウトの「自動調整」（IR の指示に従うのみ）
- スキーマ検証（Validator の責務）

**入力**:

- 検証済み DiagramIR
- ValidationResult (pass)

**出力**:

- .drawio ファイル
- 生成レポート

```yaml
ir_renderer:
  tools:
    - read_file
    - create_file
    - list_dir # 重複チェック

  transformation_rules:
    # 変換は完全に決定的
    deterministic: true
    no_creativity: true
    no_auto_adjust: true

  output_formats:
    - drawio # 推奨
    - drawio.svg # 明示要求時のみ

  pre_output_check:
    - mxcell_count >= 2 + elements.length + connections.length
    - all elements have corresponding mxCell
    - all connections have corresponding mxCell
```

**変換ルール（決定的）**:

```yaml
element_to_mxcell:
  # 各要素タイプに対して決定的なスタイル文字列を定義
  rectangle:
    style: "rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"

  rounded_rectangle:
    style: "rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"

  ellipse:
    style: "ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"

  diamond:
    style: "rhombus;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"

  cylinder:
    style: "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;fillColor={fill};strokeColor={stroke};"

  # Azure アイコン
  azure_vm:
    style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;labelPosition=center;verticalLabelPosition=bottom;verticalAlign=top;outlineConnect=0;align=center;shape=mxgraph.azure.virtual_machine;"

  azure_vnet:
    style: "sketch=0;pointerEvents=1;shadow=0;dashed=0;html=1;strokeColor=none;fillColor=#0078D4;shape=mxgraph.azure.virtual_network;"

connection_to_mxcell:
  arrow:
    style: "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=classic;"

  line:
    style: "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;"

  bidirectional:
    style: "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;startArrow=classic;endArrow=classic;"

  dashed:
    style: "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=classic;"
```

---

### 5. Logger (横断的関心事)

**責務**:

- 全フェーズのログ記録
- IR の保存（必須）
- エラートレース
- デバッグ情報の出力

**特徴**:

- エージェントではなくモジュール
- 全エージェントから呼び出し可能
- ワークフロー失敗時のトレーサビリティ確保

```yaml
logger:
  log_levels:
    - DEBUG # 詳細なデバッグ情報
    - INFO # 通常のイベント
    - WARN # 警告（続行可能）
    - ERROR # エラー（続行不可）

  log_targets:
    workflow_log: "outputs/.workflow/{id}/workflow.log"
    ir_archive: "outputs/.workflow/{id}/ir.v{n}.json"
    checkpoint: "outputs/.workflow/{id}/checkpoint.json"

  mandatory_logging:
    - phase_start
    - phase_end
    - ir_creation
    - ir_validation_result
    - transform_start
    - transform_end
    - output_creation
    - error_occurred
```

---

## 🔄 v4.x → v5.0 マッピング

| v4.x エージェント | v5.0 エージェント | 変更内容                                    |
| ----------------- | ----------------- | ------------------------------------------- |
| Flow Orchestrator | **Coordinator**   | Review Engine を除去、純粋な調整役に        |
| Manifest Gateway  | **IR-Builder**    | マニフェスト → DiagramIR (JSON Schema 準拠) |
| SVG Forge         | **IR-Renderer**   | 自己検証を除去、決定的変換のみ              |
| (Review 内蔵)     | **IR-Validator**  | 独立エージェントとして分離                  |
| (なし)            | **Logger**        | 新規追加（横断的関心事）                    |

---

## 🚫 禁止パターン

### 1. 責務の混在

```yaml
# ❌ NG: 生成と検証の混在
ir_builder:
  steps:
    - generate_ir
    - validate_ir # 禁止: Validator の責務
    - fix_if_invalid # 禁止: 生成→検証→修正のループ
```

### 2. 変換時の創作

```yaml
# ❌ NG: 変換時のレイアウト「調整」
ir_renderer:
  steps:
    - transform_elements
    - auto_adjust_positions # 禁止: IR の指示に従うのみ
    - beautify_layout # 禁止: 創作的判断
```

### 3. 自動補完

```yaml
# ❌ NG: 不正な IR の自動修正
ir_validator:
  on_invalid:
    - auto_fix_issues # 禁止: 報告のみ
    - fill_missing_fields # 禁止: 補完しない
```

---

## ✅ 推奨パターン

### 1. 明確な責務境界

```yaml
# ✅ OK: 各エージェントが単一責務
ir_builder:
  does: [parse, generate]
  returns: DiagramIR

ir_validator:
  does: [validate]
  returns: ValidationResult

ir_renderer:
  does: [transform, produce]
  returns: OutputFile
```

### 2. 検証失敗時のルーティング

```yaml
# ✅ OK: Coordinator が差し戻し先を決定
coordinator:
  on_validation_fail:
    routing:
      schema_error: ir_builder # IR 再生成
      reference_error: ir_builder # IR 再生成
      user_intent_unclear: user # ユーザーに確認
```

### 3. 決定的変換

```yaml
# ✅ OK: IR が同じなら常に同じ出力
ir_renderer:
  guarantee:
    - same_ir_same_output: true
    - no_random_elements: true
    - reproducible: true
```

```

```
