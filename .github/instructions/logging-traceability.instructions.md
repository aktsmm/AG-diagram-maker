```instructions
# ロギング・トレーサビリティ仕様 v5.0

> **適用対象**: 全エージェント、Logger モジュール
> **最終更新**: 2025-12-12

このインストラクションは、ワークフロー全体のロギングとデバッグ性を確保するための仕様を定義します。

---

## 🎯 目的

### ロギングの3つの目的

1. **トレーサビリティ**: 障害発生時に「どの段階で何が起きたか」を追跡可能にする
2. **再現性**: 同一ログから同一結果を再現できるようにする
3. **監査性**: 生成過程の記録を保持し、品質検証を可能にする

---

## 📁 ログ構造

### ディレクトリ構造

```

outputs/
├── .workflow/
│ └── {workflow_id}/
│ ├── workflow.log # 統合ワークフローログ
│ ├── ir.v1.json # IR バージョン 1
│ ├── ir.v2.json # IR バージョン 2（再生成時）
│ ├── validation.v1.json # 検証結果 1
│ ├── checkpoint.json # 最新チェックポイント
│ ├── checkpoint.cp1.json # チェックポイント 1
│ ├── checkpoint.cp2.json # チェックポイント 2
│ └── error.json # エラー詳細（発生時）
├── .cache/
│ ├── analysis/
│ │ └── {input_hash}.json # 入力分析キャッシュ
│ └── mcp/
│ └── {query_hash}.json # MCP 結果キャッシュ
└── {output_file}.drawio # 最終成果物

````

---

## 📝 ログフォーマット

### 統合ワークフローログ (workflow.log)

```json
{
  "workflow_id": "550e8400-e29b-41d4-a716-446655440000",
  "version": "5.0",
  "started_at": "2025-12-12T10:00:00.000Z",
  "completed_at": "2025-12-12T10:15:32.456Z",
  "status": "completed",
  "input_hash": "a1b2c3d4e5f6...",
  "events": [
    {
      "timestamp": "2025-12-12T10:00:00.123Z",
      "level": "INFO",
      "phase": "coordinator",
      "event": "workflow_started",
      "data": {
        "input_type": "text",
        "input_length": 256
      }
    },
    {
      "timestamp": "2025-12-12T10:00:01.456Z",
      "level": "INFO",
      "phase": "ir_builder",
      "event": "ir_generation_started",
      "data": {}
    },
    {
      "timestamp": "2025-12-12T10:00:05.789Z",
      "level": "INFO",
      "phase": "ir_builder",
      "event": "ir_generation_completed",
      "data": {
        "ir_path": "outputs/.workflow/550e8400.../ir.v1.json",
        "element_count": 8,
        "connection_count": 7
      }
    }
  ]
}
````

### ログレベル定義

| レベル  | 用途               | 例                               |
| ------- | ------------------ | -------------------------------- |
| `DEBUG` | 詳細なデバッグ情報 | 変数値、中間計算結果             |
| `INFO`  | 通常のイベント     | フェーズ開始/終了、成功          |
| `WARN`  | 警告（続行可能）   | 非推奨形式の使用、軽微な問題     |
| `ERROR` | エラー（続行不可） | 検証失敗、ファイル書き込みエラー |

### イベントタイプ

```yaml
event_types:
  workflow:
    - workflow_started
    - workflow_completed
    - workflow_failed
    - workflow_resumed

  coordinator:
    - phase_started
    - phase_completed
    - delegation_started
    - delegation_completed
    - checkpoint_saved
    - checkpoint_loaded
    - error_routing

  ir_builder:
    - parse_started
    - parse_completed
    - ir_generation_started
    - ir_generation_completed
    - mcp_query_started
    - mcp_query_completed

  ir_validator:
    - validation_started
    - validation_completed
    - blocking_issue_found
    - warning_found

  ir_renderer:
    - transform_started
    - transform_completed
    - position_calculation_completed
    - mxcell_generation_completed
    - pre_output_validation_started
    - pre_output_validation_completed
    - file_output_completed
```

---

## 📦 IR アーカイブ仕様

### 必須保存

```yaml
ir_archiving:
  mandatory: true

  save_points:
    - on_ir_creation: "ir.v{n}.json"
    - on_ir_regeneration: "ir.v{n+1}.json"

  retention:
    success: "keep_latest_only" # 成功時は最新のみ保持
    failure: "keep_all" # 失敗時は全バージョン保持

  format:
    type: "JSON"
    schema: ".github/schemas/diagram-ir.schema.json"
    pretty_print: true
```

### IR ファイル構造

```json
{
  "_meta": {
    "version": 1,
    "created_at": "2025-12-12T10:00:05.789Z",
    "created_by": "ir_builder",
    "input_hash": "a1b2c3d4..."
  },
  "version": "5.0",
  "metadata": {
    /* IR メタデータ */
  },
  "canvas": {
    /* キャンバス設定 */
  },
  "elements": [
    /* ノード定義 */
  ],
  "connections": [
    /* エッジ定義 */
  ],
  "output": {
    /* 出力設定 */
  }
}
```

---

## ✅ 検証結果ログ

### ValidationResult 保存

```json
{
  "_meta": {
    "version": 1,
    "validated_at": "2025-12-12T10:00:10.123Z",
    "ir_version": 1,
    "ir_path": "outputs/.workflow/.../ir.v1.json"
  },
  "valid": false,
  "score": 75,
  "issues": [
    {
      "severity": "error",
      "code": "REF_INTEGRITY_ERROR",
      "message": "接続 'conn_1' の target 'node_x' が存在しません",
      "path": "$.connections[0].to",
      "blocking": true
    },
    {
      "severity": "warning",
      "code": "LABEL_TOO_LONG",
      "message": "ノード 'node_a' のラベルが50文字を超えています",
      "path": "$.elements[0].label",
      "blocking": false,
      "suggestion": "ラベルを短縮することを推奨"
    }
  ],
  "blocking_issues": [
    {
      /* 上記の blocking=true の issue */
    }
  ],
  "summary": {
    "total_issues": 2,
    "errors": 1,
    "warnings": 1,
    "blocking_count": 1
  }
}
```

---

## 📍 チェックポイント仕様

### チェックポイント構造

```json
{
  "_meta": {
    "checkpoint_id": 3,
    "saved_at": "2025-12-12T10:05:00.000Z",
    "phase": "ir_validation_pass"
  },
  "workflow_id": "550e8400-e29b-41d4-a716-446655440000",
  "input_hash": "a1b2c3d4...",
  "current_phase": "ir_validation_pass",
  "completed_phases": [
    "coordinator_start",
    "ir_generation",
    "ir_validation_pass"
  ],
  "state": {
    "ir_path": "outputs/.workflow/.../ir.v1.json",
    "ir_version": 1,
    "validation_score": 95,
    "iteration_count": 0
  },
  "next_phase": "ir_rendering"
}
```

### チェックポイント一覧

| ID  | フェーズ                 | 説明             |
| --- | ------------------------ | ---------------- |
| 1   | `coordinator_start`      | ワークフロー開始 |
| 2   | `ir_generation`          | IR 生成完了      |
| 3   | `ir_validation_pass`     | IR 検証通過      |
| 4   | `ir_rendering`           | レンダリング完了 |
| 5   | `output_validation_pass` | 出力検証通過     |
| 6   | `file_output`            | ファイル出力完了 |

---

## ❌ エラーログ仕様

### エラー詳細 (error.json)

```json
{
  "_meta": {
    "error_id": "err_001",
    "occurred_at": "2025-12-12T10:08:00.000Z",
    "phase": "ir_renderer",
    "event": "pre_output_validation_failed"
  },
  "error": {
    "code": "MXCELL_COUNT_MISMATCH",
    "message": "mxCell数が不足しています（期待: 17, 実際: 15）",
    "severity": "BLOCKING"
  },
  "context": {
    "ir_path": "outputs/.workflow/.../ir.v1.json",
    "expected_mxcells": 17,
    "actual_mxcells": 15,
    "missing_elements": ["node_7", "conn_5"]
  },
  "recovery": {
    "action": "route_to_ir_builder",
    "reason": "IR に含まれる要素が変換されていない",
    "iteration": 1
  },
  "stack_trace": [
    "ir_renderer.transform_started",
    "ir_renderer.mxcell_generation_completed",
    "ir_renderer.pre_output_validation_started",
    "ir_renderer.pre_output_validation_failed"
  ]
}
```

---

## 🔧 Logger モジュール API

### ログ出力関数

```yaml
logger_api:
  functions:
    - name: "log"
      params:
        level: "DEBUG | INFO | WARN | ERROR"
        phase: "coordinator | ir_builder | ir_validator | ir_renderer"
        event: "string (event_type)"
        data: "object (optional)"
      example: |
        log(INFO, "ir_builder", "ir_generation_completed", {
          ir_path: "...",
          element_count: 8
        })

    - name: "save_ir"
      params:
        ir: "DiagramIR object"
        version: "number"
      returns: "ir_path: string"

    - name: "save_checkpoint"
      params:
        checkpoint_id: "number"
        state: "object"
      returns: "checkpoint_path: string"

    - name: "save_validation_result"
      params:
        result: "ValidationResult object"
        ir_version: "number"
      returns: "validation_path: string"

    - name: "save_error"
      params:
        error: "ErrorDetail object"
      returns: "error_path: string"

    - name: "get_workflow_summary"
      params: {}
      returns: |
        {
          workflow_id: string,
          status: string,
          duration_ms: number,
          phase_count: number,
          error_count: number,
          final_output: string | null
        }
```

---

## 📊 デバッグ情報

### 障害分析用の情報

```yaml
debug_info:
  always_capture:
    - workflow_id
    - input_hash
    - current_phase
    - last_successful_checkpoint
    - iteration_count

  on_error_capture:
    - full_ir_state
    - validation_result
    - stack_trace
    - environment_info

  environment_info:
    - timestamp
    - agent_version
    - schema_version
```

### トラブルシューティングガイド

| 症状                 | 確認ポイント    | ログ参照先                       |
| -------------------- | --------------- | -------------------------------- |
| 図が真っ白           | mxCell 数確認   | validation.json, error.json      |
| エッジが表示されない | 参照整合性      | validation.json の REF_INTEGRITY |
| レイアウト崩れ       | 座標計算        | ir.json の position              |
| 無限ループ           | iteration_count | checkpoint.json                  |

---

## 🔄 ログローテーション

```yaml
log_rotation:
  workflow_logs:
    retention: "7 days"
    on_success: "archive to outputs/.archive/{date}/"
    on_failure: "keep in place"

  cache:
    analysis_cache:
      ttl: "24 hours"
      max_entries: 100

    mcp_cache:
      ttl: "1 hour"
      max_entries: 50

  cleanup:
    trigger: "on_workflow_complete"
    action: |
      if status == "completed":
        remove ir.v1..v{n-1}.json  # 最新以外削除
        archive workflow.log
      else:
        keep_all  # 失敗時は保持
```

```

```
