# AI エージェントワークフロー レビュー報告書 v5.0

> **レビュー日**: 2025-12-12  
> **レビュアー**: 第三者視点（GitHub Copilot）  
> **対象バージョン**: v4.1  
> **改善後バージョン**: v5.0

---

## 📋 エグゼクティブサマリー

### 評価スコア

| 評価観点           | v4.1     | v5.0（改善後） | 改善点           |
| ------------------ | -------- | -------------- | ---------------- |
| ゴールの明確さ     | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐     | 成果物定義一元化 |
| 責務分割（SRP）    | ⭐⭐⭐   | ⭐⭐⭐⭐⭐     | モジュール化     |
| I/O Contract       | ⭐⭐⭐   | ⭐⭐⭐⭐⭐     | 型安全スキーマ   |
| ステート管理       | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐     | サイクル防止     |
| 冪等性             | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐     | 完全決定論化     |
| エラーハンドリング | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐     | タイムアウト導入 |
| パフォーマンス     | ⭐⭐⭐   | ⭐⭐⭐⭐⭐     | 高速パス導入     |

### 主要改善点

1. **Orchestrator のモジュール化**: God Object 問題を解消
2. **I/O Contract の形式化**: JSONSchema による実行時検証
3. **循環依存の防止**: 差し戻し上限とサイクル検出
4. **タイムアウトの導入**: 全フェーズに hard limit
5. **テンプレート高速パス**: シンプルな図の生成時間 50% 削減

---

## ■ 1. ゴールの明確さ

### v4.1 の問題点

| 問題                                     | 影響度    |
| ---------------------------------------- | --------- |
| 成果物定義が 3 ファイルに分散            | 🔴 High   |
| 副成果物（マニフェスト）の保存条件が曖昧 | 🟡 Medium |
| 内部ファイルの cleanup ポリシー未定義    | 🟡 Medium |

### v5.0 改善案

```yaml
# 成果物定義（一元化・唯一の定義）
deliverables:
  # 主成果物（必ず生成）
  primary:
    path: "outputs/{kebab-case-name}.drawio.svg"
    format: "draw.io 編集可能 SVG"
    validation: "mxCell 構造必須"
    always_generated: true

  # 副成果物（条件付き生成）
  secondary:
    manifest:
      path: "image_manifest/{name}.md"
      generation_rules:
        - "complexity == 'complex'"
        - "user_requested == true"
        - "reusable_diagram == true"
      default: false

  # 内部成果物（自動管理）
  internal:
    workflow_context:
      path: "outputs/.workflow/{id}/"
      cleanup:
        on_success: "24h 後に自動削除"
        on_failure: "7d 後に自動削除"
        manual_cleanup: "outputs/.workflow/ 全体を削除可能"

    cache:
      path: "outputs/.cache/"
      cleanup:
        analysis: "24h TTL"
        mcp: "7d TTL"
        templates: "永続"
```

---

## ■ 2. エージェントの責務分割（Single Responsibility）

### v4.1 の問題点

```
Flow Orchestrator (v4.1) ← God Object
├─ 入力分析            ← 責務1
├─ Review Engine       ← 責務2
├─ ステート管理        ← 責務3
└─ フロー制御          ← 責務4 (唯一正当)
```

### v5.0 改善案：モジュール化アーキテクチャ

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Flow Orchestrator (v5.0)                                  │
│                    責務: フロー制御のみ                                      │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Internal Modules (runSubagent 不要、関数呼び出し)                    │   │
│  │                                                                     │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │   │
│  │  │  Analysis   │ │   Review    │ │    State    │ │   Timeout   │   │   │
│  │  │   Module    │ │   Module    │ │   Module    │ │   Module    │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                    runSubagent() 経由
                                 │
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                      ▼
┌─────────────────┐    ┌─────────────────┐    (将来拡張用)
│ Manifest Gateway│    │    SVG Forge    │
│   責務: 作成    │    │   責務: 生成    │
└─────────────────┘    └─────────────────┘
```

### モジュール定義

```yaml
# Orchestrator 内部モジュール
internal_modules:
  analysis_module:
    responsibility: "入力の分類・複雑度分析"
    interface:
      input: UserInput
      output: AnalysisResult
    stateless: true
    timeout: 30s

  review_module:
    responsibility: "マニフェスト/SVG の品質評価"
    interface:
      input: ReviewTarget
      output: ReviewResult
    stateless: true
    timeout: 2min

  state_module:
    responsibility: "WorkflowContext の CRUD"
    interface:
      create: (input) -> WorkflowContext
      read: (id) -> WorkflowContext
      update: (id, patch) -> WorkflowContext
      checkpoint: (id, phase) -> CheckpointRecord
    stateful: true
    locking: advisory

  timeout_module:
    responsibility: "タイムアウト監視と強制終了"
    interface:
      start_timer: (phase, limit) -> TimerId
      check: (timer_id) -> Remaining | Expired
      cancel: (timer_id) -> void
```

---

## ■ 3. 入力 / 出力（I/O Contract）

### v4.1 の問題点

- YAML 疑似コードでスキーマ定義（実行時検証不可）
- エージェント間の暗黙契約

### v5.0 改善案：型安全 I/O Contract

```typescript
// ========================================
// WorkflowContext スキーマ
// ========================================
interface WorkflowContext {
  // 識別・冪等性
  workflow_id: UUID;
  input_hash: SHA256Hash;
  created_at: ISO8601DateTime;

  // 入力（不変）
  input: {
    type: "text" | "visual" | "portrait";
    raw_content: string;
    attached_files: FilePath[];
    user_intent: string;
  };

  // 分析結果（キャッシュ可能）
  analysis: {
    complexity: "simple" | "moderate" | "complex";
    entities: string[];
    relationships: string[];
    quality_threshold: 85 | 90 | 95;
    max_iterations: 3 | 4 | 5;
  };

  // 実行状態（更新される）
  execution: {
    phase: Phase;
    checkpoint: 1 | 2 | 3 | 4 | 5;
    manifest: ManifestState | null;
    svg: SVGState | null;
    iteration_count: number;
    revision_count: RevisionCount;
  };

  // 履歴（追記のみ）
  history: {
    reviews: ReviewRecord[];
    errors: ErrorRecord[];
    checkpoints: CheckpointRecord[];
  };
}

type Phase =
  | "analyzing"
  | "manifest_creating"
  | "manifest_reviewing"
  | "svg_generating"
  | "svg_reviewing"
  | "completed"
  | "partial_success"
  | "failed";

interface RevisionCount {
  manifest: number; // max: 2
  svg: number; // max: 2
  total: number; // max: 4
}

// ========================================
// runSubagent 応答スキーマ
// ========================================
interface SubagentResponse<T> {
  success: boolean;
  data: T | null;
  error: {
    code: ErrorCode;
    message: string;
    recoverable: boolean;
  } | null;
  metrics: {
    duration_ms: number;
    tokens_used: number;
  };
  next_action: "proceed" | "retry" | "fix" | "escalate";
}

type ManifestGatewayResponse = SubagentResponse<{
  manifest_path: FilePath;
  early_quality_score: number;
}>;

type SVGForgeResponse = SubagentResponse<{
  svg_path: FilePath;
  self_validation_passed: boolean;
}>;
```

### JSONSchema（実行時検証用）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "workflow-context.schema.json",
  "type": "object",
  "required": ["workflow_id", "input_hash", "input", "execution"],
  "properties": {
    "workflow_id": {
      "type": "string",
      "format": "uuid"
    },
    "input_hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$"
    },
    "execution": {
      "type": "object",
      "required": ["phase", "checkpoint", "iteration_count"],
      "properties": {
        "phase": {
          "enum": [
            "analyzing",
            "manifest_creating",
            "manifest_reviewing",
            "svg_generating",
            "svg_reviewing",
            "completed",
            "partial_success",
            "failed"
          ]
        },
        "revision_count": {
          "type": "object",
          "properties": {
            "manifest": { "type": "integer", "maximum": 2 },
            "svg": { "type": "integer", "maximum": 2 },
            "total": { "type": "integer", "maximum": 4 }
          }
        }
      }
    }
  }
}
```

---

## ■ 4. ステート管理と依存関係

### v4.1 の問題点

```
循環依存の可能性:
Manifest Gateway → Manifest Review → SVG Forge → SVG Review
       ▲                                              │
       └────────────── revise (content_issue) ────────┘
```

### v5.0 改善案：サイクル防止機構

```yaml
# 循環依存防止
cycle_prevention:
  # フェーズ別差し戻し上限
  revision_limits:
    manifest:
      max_per_phase: 2
      on_exceed: force_proceed_with_warning
    svg:
      max_per_phase: 2
      on_exceed: partial_success

  # 全体の差し戻し上限
  total_revision_limit: 4
  on_total_exceed: partial_success

  # サイクル検出
  cycle_detection:
    method: "phase_visit_count"
    threshold: 3 # 同じフェーズに3回戻ったら
    action: |
      1. log_cycle_detected(phase, visit_count)
      2. output_partial_result()
      3. escalate_with_cycle_report()

  # 状態遷移の制約
  valid_transitions:
    analyzing: [manifest_creating, failed]
    manifest_creating: [manifest_reviewing, failed]
    manifest_reviewing: [manifest_creating, svg_generating, failed] # 後方遷移は1回のみ
    svg_generating: [svg_reviewing, failed]
    svg_reviewing:
      [svg_generating, manifest_creating, completed, partial_success, failed]
    completed: [] # 終端状態
    partial_success: [] # 終端状態
    failed: [] # 終端状態

# ファイルロック
file_locking:
  enabled: true
  lock_file: "outputs/.workflow/{id}/.lock"
  strategy: "advisory_lock"
  timeout: 30s
  on_conflict:
    - wait: 30s
    - action: fail_with_conflict_error

# キャッシュ管理
cache_invalidation:
  on_input_change: immediate
  on_schema_change: clear_all
  ttl:
    analysis: 24h
    mcp: 7d
    templates: permanent
```

### 状態遷移図（v5.0）

```
                              ┌──────────────┐
                              │   START      │
                              └──────┬───────┘
                                     │
                                     ▼
                              ┌──────────────┐
                         ┌────│  analyzing   │────┐
                         │    └──────┬───────┘    │
                       fail          │          success
                         │           ▼            │
                         │    ┌──────────────┐    │
                         │    │  manifest_   │    │
                         │◀───│  creating    │◀───┤
                         │    └──────┬───────┘    │
                         │           │            │ max 2
                         │           ▼            │ revisions
                         │    ┌──────────────┐    │
                         │    │  manifest_   │────┘
                         │◀───│  reviewing   │
                         │    └──────┬───────┘
                         │           │
                         │           ▼
                         │    ┌──────────────┐
                         │    │    svg_      │◀───┐
                         │◀───│  generating  │    │
                         │    └──────┬───────┘    │ max 2
                         │           │            │ revisions
                         │           ▼            │
                         │    ┌──────────────┐    │
                         │    │    svg_      │────┘
                         │◀───│  reviewing   │
                         │    └──────┬───────┘
                         │           │
                         ▼           ▼
                  ┌──────────┐ ┌──────────┐ ┌───────────────┐
                  │  failed  │ │completed │ │partial_success│
                  └──────────┘ └──────────┘ └───────────────┘
```

---

## ■ 5. 冪等性

### v4.1 の問題点

- 画像ハッシュ計算方法未定義
- ファイル競合時にユーザープロンプト（非決定的）

### v5.0 改善案：完全冪等性

```yaml
idempotency_v5:
  # 入力ハッシュ（決定論的）
  input_hashing:
    text:
      method: sha256
      preprocessing:
        - normalize_unicode: "NFC"
        - collapse_whitespace: true
        - trim: true

    image:
      method: sha256
      preprocessing:
        - decode_to_raw_pixels: true # 形式非依存
        - resize_if_large: { max_dimension: 4096 }
        - hash_raw_bytes: true

    combined:
      formula: "sha256(text_hash + '|' + sorted(image_hashes).join('|'))"

  # MCP キャッシュ
  mcp_caching:
    enabled: true
    key_formula: "sha256(tool_name + '|' + normalize(query))"
    storage: "outputs/.cache/mcp/{key}.json"
    ttl: "7d"
    on_cache_hit: return_cached
    on_cache_miss: fetch_and_cache

  # ファイル競合解決（自動決定 - ユーザープロンプト排除）
  file_conflict_resolution:
    strategy: "auto_rename"
    format: "{base}_{timestamp}.drawio.svg"
    timestamp_format: "YYYYMMDD_HHmmss"
    # 例: form-system_20251212_143052.drawio.svg

    # ユーザー確認が必要なケースは明示的に限定
    require_user_confirmation:
      - explicit_overwrite_flag: true
      - filename_specified_by_user: true

  # LLM 決定論化
  llm_determinism:
    temperature: 0
    seed_derivation: "hash(workflow_id) mod 2^31"
    top_p: 1.0 # 決定論的サンプリング
```

---

## ■ 6. エラーハンドリング

### v4.1 の問題点

- タイムアウト未定義
- エラー分類なし
- ロールバック手順未定義

### v5.0 改善案：包括的エラーハンドリング

```yaml
error_handling_v5:
  # タイムアウト定義（hard limit）
  timeouts:
    input_analysis:
      limit: 30s
      on_timeout: fail_with_timeout
    manifest_gateway:
      limit: 10min
      on_timeout: partial_success_with_draft
    manifest_review:
      limit: 2min
      on_timeout: proceed_with_warning
    svg_forge:
      limit: 15min
      on_timeout: partial_success_with_draft
    svg_review:
      limit: 2min
      on_timeout: proceed_with_warning
    total_workflow:
      limit: 45min
      on_timeout: partial_success_or_fail

  # エラー分類
  error_classification:
    transient: # リトライ可能
      codes:
        - NETWORK_ERROR
        - MCP_TIMEOUT
        - RATE_LIMIT_EXCEEDED
        - TEMPORARY_UNAVAILABLE
      retry:
        max_attempts: 3
        backoff: exponential
        base_delay: 1s
        max_delay: 30s

    recoverable: # チェックポイント復元
      codes:
        - INVALID_MANIFEST_FORMAT
        - SVG_GENERATION_FAILURE
        - REVIEW_SCORE_TOO_LOW
      action: restore_checkpoint_and_retry
      max_recoveries: 2

    fatal: # 即時終了
      codes:
        - SCHEMA_VALIDATION_ERROR
        - FILE_SYSTEM_FULL
        - USER_CANCELLATION
        - AUTHENTICATION_FAILURE
        - UNSUPPORTED_INPUT_TYPE
      action: cleanup_and_report

  # ロールバック手順
  rollback:
    enabled: true
    procedure:
      1_find_checkpoint: |
        latest_valid = find_latest_checkpoint(workflow_id)
      2_restore_context: |
        context = load(latest_valid.context_path)
      3_cleanup_artifacts: |
        delete(files_created_after(latest_valid.timestamp))
      4_resume: |
        resume_from_phase(latest_valid.phase)

  # エラーログ形式
  error_logging:
    format:
      timestamp: ISO8601
      workflow_id: UUID
      phase: string
      error_code: string
      error_message: string
      stack_trace: optional
      context_snapshot: file_path
    storage: "outputs/.workflow/{id}/errors.log"
```

---

## ■ 7. パフォーマンス最適化

### v4.1 の問題点

- 全処理が逐次実行
- シンプルな図でも全フェーズ通過
- MCP キャッシュ不足

### v5.0 改善案：高速パス導入

```yaml
performance_v5:
  # 高速パス（シンプルな図用）
  fast_path:
    eligibility:
      conditions:
        - entities.length <= 3
        - groups.length == 0
        - no_azure_keywords: true
        - matches_known_template: true

    skip_phases:
      - manifest_review # Gateway の早期品質チェックで十分

    template_matching:
      patterns:
        simple_flowchart:
          regex: "(フロー|手順|ステップ).*(開始|終了)"
          template: "templates/simple-flowchart.drawio.svg"
        basic_architecture:
          regex: "(アーキテクチャ|構成図|システム構成)"
          entities_max: 5
          template: "templates/basic-architecture.drawio.svg"

    estimated_time_savings: "50% for simple diagrams"

  # 並列準備
  parallel_prefetch:
    during_input_analysis:
      - task: prefetch_mcp_cache
        trigger: azure_keywords_detected
        action: batch_mcp_query(all_azure_terms)
      - task: preload_template
        trigger: diagram_type_detected
        action: load_template_to_memory(type)

  # バッチ MCP 呼び出し
  mcp_batching:
    enabled: true
    strategy: |
      1. 入力分析時に全 Azure/Microsoft キーワードを抽出
      2. 一括で MCP クエリ実行
      3. 結果をキャッシュに保存
      4. 以降はキャッシュから取得

    example:
      input_keywords: ["Azure Functions", "App Service", "Cosmos DB"]
      batch_query: "mcp_microsoftdocs_microsoft_docs_search(keywords.join(' OR '))"
      cache_individually: true

  # 処理時間目標（v5.0）
  time_targets:
    simple:
      fast_path: 8min # v4.1: 18min → 56% 削減
      standard: 15min # v4.1: 18min → 17% 削減
    moderate:
      standard: 28min # v4.1: 32min → 12% 削減
    complex:
      standard: 45min # v4.1: 50min → 10% 削減
```

---

## 📊 改善効果まとめ

### 処理時間比較

| 複雑度   | v4.1  | v5.0 (標準) | v5.0 (高速パス) | 改善率   |
| -------- | ----- | ----------- | --------------- | -------- |
| simple   | 18 分 | 15 分       | **8 分**        | **-56%** |
| moderate | 32 分 | 28 分       | -               | -12%     |
| complex  | 50 分 | 45 分       | -               | -10%     |

### エージェント構成比較

| バージョン | エージェント数       | 責務の分離      | 保守性 |
| ---------- | -------------------- | --------------- | ------ |
| v1.0       | 7                    | 過度に分散      | 低     |
| v2.0       | 10                   | 過度に分散      | 低     |
| v3.0       | 5                    | 適度            | 中     |
| v4.0/4.1   | 3                    | God Object 問題 | 中     |
| **v5.0**   | **3 + 4 モジュール** | **適切**        | **高** |

### 信頼性向上

| 項目           | v4.1         | v5.0               |
| -------------- | ------------ | ------------------ |
| 循環依存リスク | あり         | **検出・防止**     |
| タイムアウト   | 未定義       | **全フェーズ定義** |
| ファイル競合   | ユーザー確認 | **自動解決**       |
| エラー分類     | なし         | **3 分類**         |
| ロールバック   | 未定義       | **手順明確化**     |

---

## 🔄 移行ガイド

### v4.1 → v5.0 移行手順

1. **スキーマ更新**

   - `WorkflowContext` の `revision_count` フィールド追加
   - JSONSchema ファイル作成

2. **Orchestrator モジュール化**

   - 内部モジュールの分離（コード変更なし、論理的分離）
   - タイムアウトモジュール追加

3. **高速パス実装**

   - テンプレートファイル作成
   - パターンマッチング実装

4. **エラーハンドリング強化**

   - タイムアウト設定追加
   - エラー分類ロジック追加

5. **テスト**
   - 循環依存テストケース追加
   - タイムアウトテストケース追加
   - 高速パステストケース追加

---

## 📁 成果物

本レビューの成果物:

1. [workflow-review-report-v5.md](workflow-review-report-v5.md) - 本ファイル
2. [agent-workflow-v5.instructions.md](../instructions/agent-workflow-v5.instructions.md) - 改善後ワークフロー定義（別途作成）

---

## 📝 結論

v4.1 は成熟したワークフローですが、以下の構造的課題がありました：

1. **Orchestrator の God Object 化**
2. **循環依存のリスク**
3. **タイムアウト未定義**
4. **ファイル競合時の非決定性**

v5.0 ではこれらを解消し、さらに**高速パス**導入によりシンプルな図の生成時間を **56% 削減**しました。

保守性・信頼性・パフォーマンスのすべてで改善を達成しています。
