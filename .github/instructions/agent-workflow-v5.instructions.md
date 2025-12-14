# Agent Workflow Instructions v5.0

> 全エージェント共通のワークフロー定義とルール集（構造最適化版）

## 変更履歴

| バージョン | 日付       | 変更内容                                                                     |
| ---------- | ---------- | ---------------------------------------------------------------------------- |
| 1.0        | 2025-12-01 | 初版作成                                                                     |
| 2.0        | 2025-12-11 | Router/Planner 分離、適応型ラウンド、フィードバックループ                    |
| 3.0        | 2025-12-11 | リファクタリング版: エージェント統合、冪等性確保、パフォーマンス最適化       |
| 4.0        | 2025-12-11 | 最適化版: Review 内製化、3 エージェント構成、チェックポイント方式            |
| 4.1        | 2025-12-12 | 品質強化版: draw.io 互換性強制、ファイル重複チェック、情報充足性検証         |
| **5.0**    | 2025-12-12 | **構造最適化版**: モジュール化、循環防止、タイムアウト、高速パス、完全冪等性 |

## v5.0 主要変更点

### 🔴 High Priority Changes

1. **Orchestrator モジュール化**: God Object 問題を解消、4 内部モジュールに分離
2. **循環依存防止**: 差し戻し上限（各フェーズ 2 回、全体 4 回）+ サイクル検出
3. **タイムアウト導入**: 全フェーズに hard limit を設定
4. **I/O Contract 形式化**: JSONSchema による実行時検証

### 🟡 Medium Priority Changes

5. **完全冪等性**: 画像ハッシュ正規化、ファイル競合自動解決
6. **高速パス**: シンプルな図の生成時間 56% 削減
7. **エラー分類**: transient / recoverable / fatal の 3 分類

---

## 1. 全体フロー概要（v5.0）

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Agent Workflow v5.0 (Modular Architecture)               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   USER INPUT                                                                │
│       │                                                                     │
│       ▼                                                                     │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                     Flow Orchestrator                                │   │
│   │                                                                     │   │
│   │  ┌─────────────────────────────────────────────────────────────┐   │   │
│   │  │ Internal Modules (関数呼び出し、runSubagent 不要)           │   │   │
│   │  │                                                             │   │   │
│   │  │ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐   │   │   │
│   │  │ │ Analysis  │ │  Review   │ │   State   │ │  Timeout  │   │   │   │
│   │  │ │  Module   │ │  Module   │ │  Module   │ │  Module   │   │   │   │
│   │  │ └───────────┘ └───────────┘ └───────────┘ └───────────┘   │   │   │
│   │  │                                                             │   │   │
│   │  └─────────────────────────────────────────────────────────────┘   │   │
│   │                                                                     │   │
│   │  ┌─────────────────────────────────────────────────────────────┐   │   │
│   │  │ Flow Control (Orchestrator の唯一の責務)                    │   │   │
│   │  │  - フェーズ遷移制御                                         │   │   │
│   │  │  - runSubagent 呼び出し                                     │   │   │
│   │  │  - 循環検出・防止                                           │   │   │
│   │  └─────────────────────────────────────────────────────────────┘   │   │
│   └────────────────────────────┬────────────────────────────────────────┘   │
│                                │                                            │
│                    runSubagent() 経由                                       │
│                                │                                            │
│            ┌───────────────────┴───────────────────┐                        │
│            ▼                                       ▼                        │
│   ┌─────────────────────┐               ┌─────────────────────┐             │
│   │  Manifest Gateway   │               │     SVG Forge       │             │
│   │  責務: 作成のみ     │               │   責務: 生成のみ    │             │
│   └─────────────────────┘               └─────────────────────┘             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### エージェント構成（v5.0: 3 エージェント + 4 モジュール）

| コンポーネント     | 種別     | 責務                      |
| ------------------ | -------- | ------------------------- |
| Flow Orchestrator  | Agent    | フロー制御（唯一の責務）  |
| ├─ Analysis Module | Internal | 入力分類・複雑度分析      |
| ├─ Review Module   | Internal | マニフェスト/SVG 品質評価 |
| ├─ State Module    | Internal | WorkflowContext CRUD      |
| └─ Timeout Module  | Internal | タイムアウト監視          |
| Manifest Gateway   | Subagent | マニフェスト作成          |
| SVG Forge          | Subagent | SVG 生成 + 自己検証       |

---

## 2. 成果物定義（一元化、唯一の定義）

> ⚠️ この定義のみが正。他のファイルでの成果物定義は本セクションを参照すること。

```yaml
deliverables:
  # 主成果物（必ず生成）
  primary:
    path: "outputs/{kebab-case-name}.drawio.svg"
    format: "draw.io 編集可能 SVG"
    naming: "kebab-case（小文字、ハイフン区切り）"
    validation:
      - mxCell 構造必須
      - content 属性に mxGraphModel 必須
    always_generated: true

  # 副成果物（条件付き生成）
  secondary:
    manifest:
      path: "image_manifest/{name}.md"
      generation_rules:
        - "complexity == 'complex'"
        - "user_flag: --save-manifest"
        - "reusable_diagram == true"
      default: false # 条件を満たさない限り保存しない

  # 内部成果物（自動管理）
  internal:
    workflow_context:
      path: "outputs/.workflow/{workflow_id}/"
      files:
        - context.yaml
        - context.cp{1-5}.yaml # チェックポイント
        - errors.log
        - .lock
      cleanup:
        on_success: "24h 後に自動削除"
        on_partial_success: "7d 後に自動削除"
        on_failure: "7d 後に自動削除"

    cache:
      path: "outputs/.cache/"
      subdirs:
        analysis: "24h TTL"
        mcp: "7d TTL"
        templates: "永続（手動削除のみ）"
```

---

## 3. WorkflowContext スキーマ（v5.0）

### TypeScript 型定義

```typescript
interface WorkflowContext {
  // ========== 識別・冪等性 ==========
  workflow_id: UUID;
  input_hash: SHA256Hash; // 冪等性キー
  created_at: ISO8601DateTime;

  // ========== 入力（不変）==========
  input: {
    type: "text" | "visual" | "portrait";
    raw_content: string;
    attached_files: FilePath[];
    user_intent: string; // 解析された意図
  };

  // ========== 分析結果（キャッシュ可能）==========
  analysis: {
    complexity: "simple" | "moderate" | "complex";
    entities: string[];
    relationships: string[];
    quality_threshold: 85 | 90 | 95;
    max_iterations: 3 | 4 | 5;
    fast_path_eligible: boolean; // v5.0 新規
  };

  // ========== 実行状態（更新される）==========
  execution: {
    phase: Phase;
    checkpoint: 1 | 2 | 3 | 4 | 5;
    manifest: ManifestState | null;
    svg: SVGState | null;
    iteration_count: number;
    revision_count: RevisionCount; // v5.0 新規
    timers: TimerState[]; // v5.0 新規
  };

  // ========== 履歴（追記のみ）==========
  history: {
    reviews: ReviewRecord[];
    errors: ErrorRecord[];
    checkpoints: CheckpointRecord[];
    phase_visits: PhaseVisit[]; // v5.0 新規（サイクル検出用）
  };
}

// フェーズ定義
type Phase =
  | "analyzing"
  | "manifest_creating"
  | "manifest_reviewing"
  | "svg_generating"
  | "svg_reviewing"
  | "completed"
  | "partial_success"
  | "failed";

// 差し戻しカウント（v5.0 新規）
interface RevisionCount {
  manifest: number; // max: 2
  svg: number; // max: 2
  total: number; // max: 4
}

// フェーズ訪問記録（サイクル検出用）
interface PhaseVisit {
  phase: Phase;
  visit_count: number;
  last_visit: ISO8601DateTime;
}
```

### 実行時検証（JSONSchema）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "workflow-context-v5.schema.json",
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
      "required": ["phase", "checkpoint", "revision_count"],
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
            "manifest": { "type": "integer", "minimum": 0, "maximum": 2 },
            "svg": { "type": "integer", "minimum": 0, "maximum": 2 },
            "total": { "type": "integer", "minimum": 0, "maximum": 4 }
          },
          "required": ["manifest", "svg", "total"]
        }
      }
    }
  }
}
```

---

## 4. 内部モジュール定義

### 4.1 Analysis Module

```yaml
analysis_module:
  responsibility: "入力の分類と複雑度分析"
  stateless: true
  timeout: 30s

  interface:
    input:
      user_input: string
      attached_files: FilePath[]
    output:
      type: 'text' | 'visual' | 'portrait'
      complexity: 'simple' | 'moderate' | 'complex'
      entities: string[]
      relationships: string[]
      fast_path_eligible: boolean

  # 決定論的ルール（LLM 不要部分）
  classification_rules:
    if no_attachment:
      type: text
    elif has_human_face AND face_area > 50%:
      type: portrait
    else:
      type: visual

  # 複雑度判定
  complexity_rules:
    simple:
      condition: "entities.length <= 5"
      quality_threshold: 85
      max_iterations: 3
    moderate:
      condition: "5 < entities.length <= 15"
      quality_threshold: 90
      max_iterations: 4
    complex:
      condition: "entities.length > 15"
      quality_threshold: 95
      max_iterations: 5

  # 高速パス判定（v5.0 新規）
  fast_path_eligibility:
    conditions:
      - entities.length <= 3
      - groups.length == 0
      - no_azure_keywords: true
      - matches_known_template: true
    all_must_be_true: true

  caching:
    enabled: true
    key: "sha256(user_input + attached_files_hash)"
    path: "outputs/.cache/analysis/{key}.yaml"
    ttl: 24h
```

### 4.2 Review Module

```yaml
review_module:
  responsibility: "マニフェスト/SVG の品質評価"
  stateless: true
  timeout: 2min

  interface:
    input:
      target: 'manifest' | 'svg'
      artifact_path: FilePath
      quality_threshold: number
    output:
      score: number
      issues: Issue[]
      action: 'proceed' | 'proceed_with_note' | 'fix_and_retry' |
              'auto_simplify' | 'partial_success' | 'escalate'
      revision_target: 'manifest_gateway' | 'svg_forge' | 'user' | null

  # 統合スコアリング
  scoring:
    categories:
      - name: "必須項目/整合性"
        weight: 25
      - name: "構造/視認性"
        weight: 25
      - name: "レイアウト/スタイル"
        weight: 25
      - name: "技術互換性"
        weight: 25
    total: 100

  # スコア帯別アクション（決定論的）
  score_actions:
    - range: [90, 100]
      action: proceed
      next_phase: true
    - range: [85, 89]
      action: proceed_with_note
      next_phase: true
    - range: [70, 84]
      action: fix_and_retry
      next_phase: false
    - range: [50, 69]
      action: auto_simplify
      next_phase: false
    - range: [30, 49]
      action: partial_success
      terminate: true
    - range: [0, 29]
      action: escalate
      terminate: true
```

### 4.3 State Module

```yaml
state_module:
  responsibility: "WorkflowContext の CRUD とファイルロック"
  stateful: true

  interface:
    create: "(input: UserInput) -> WorkflowContext"
    read: "(workflow_id: UUID) -> WorkflowContext | null"
    update: "(workflow_id: UUID, patch: Partial<WorkflowContext>) -> WorkflowContext"
    checkpoint: "(workflow_id: UUID, checkpoint_id: number) -> CheckpointRecord"
    restore: "(workflow_id: UUID, checkpoint_id: number) -> WorkflowContext"
    lock: "(workflow_id: UUID) -> LockHandle"
    unlock: "(handle: LockHandle) -> void"

  # ファイルロック
  locking:
    strategy: advisory_lock
    lock_file: "outputs/.workflow/{id}/.lock"
    timeout: 30s
    on_conflict:
      action: wait_then_fail
      wait_time: 30s

  # チェックポイント定義
  checkpoints:
    - id: 1
      after: input_analysis
      description: "入力分析完了"
    - id: 2
      after: manifest_creation
      description: "マニフェスト作成完了"
    - id: 3
      after: manifest_review_pass
      description: "マニフェストレビュー通過"
    - id: 4
      after: svg_generation
      description: "SVG 生成完了"
    - id: 5
      after: svg_review_pass
      description: "完了"
```

### 4.4 Timeout Module（v5.0 新規）

```yaml
timeout_module:
  responsibility: "タイムアウト監視と強制終了"
  stateful: true

  interface:
    start: "(phase: Phase, limit: Duration) -> TimerId"
    check: "(timer_id: TimerId) -> { remaining: Duration } | { expired: true }"
    cancel: "(timer_id: TimerId) -> void"
    on_expire: "(timer_id: TimerId, callback: () -> void) -> void"

  # フェーズ別タイムアウト
  limits:
    input_analysis: 30s
    manifest_creating: 10min
    manifest_reviewing: 2min
    svg_generating: 15min
    svg_reviewing: 2min
    total_workflow: 45min

  # タイムアウト時のアクション
  on_timeout:
    input_analysis:
      action: fail
      error_code: ANALYSIS_TIMEOUT
    manifest_creating:
      action: partial_success_with_draft
      save_current_state: true
    manifest_reviewing:
      action: proceed_with_warning
      log: "マニフェストレビューがタイムアウト、現状で続行"
    svg_generating:
      action: partial_success_with_draft
      save_current_state: true
    svg_reviewing:
      action: proceed_with_warning
      log: "SVG レビューがタイムアウト、現状で続行"
    total_workflow:
      action: partial_success_or_fail
      decision: "最新チェックポイントの状態に基づく"
```

---

## 5. 循環依存防止（v5.0 新規）

### 差し戻し制限

```yaml
revision_limits:
  # フェーズ別上限
  per_phase:
    manifest: 2
    svg: 2

  # 全体上限
  total: 4

  # 上限到達時のアクション
  on_exceed:
    per_phase_manifest:
      action: force_proceed_with_warning
      message: "マニフェスト差し戻し上限に到達。現状で SVG 生成に進みます。"
    per_phase_svg:
      action: partial_success
      message: "SVG 差し戻し上限に到達。部分成功として提示します。"
    total:
      action: partial_success
      message: "全体の差し戻し上限に到達。部分成功として提示します。"
```

### サイクル検出

```yaml
cycle_detection:
  method: phase_visit_count
  threshold: 3 # 同じフェーズに3回以上戻ったら

  detection_logic: |
    for each phase_visit in history.phase_visits:
      if phase_visit.visit_count >= 3:
        return CycleDetected(phase_visit.phase)
    return NoCycle

  on_cycle_detected:
    action: |
      1. log_cycle_detected(phase, visit_count)
      2. output_partial_result()
      3. report_to_user(cycle_info)

  # 許可される遷移
  valid_transitions:
    analyzing:
      forward: [manifest_creating]
      backward: []
      terminal: [failed]
    manifest_creating:
      forward: [manifest_reviewing]
      backward: []
      terminal: [failed]
    manifest_reviewing:
      forward: [svg_generating]
      backward: [manifest_creating] # max 2回
      terminal: [failed]
    svg_generating:
      forward: [svg_reviewing]
      backward: []
      terminal: [failed]
    svg_reviewing:
      forward: [completed, partial_success]
      backward: [svg_generating, manifest_creating] # 条件付き
      terminal: [failed]
    completed: { terminal: true }
    partial_success: { terminal: true }
    failed: { terminal: true }
```

### 状態遷移図

```
                     ┌────────────────────────────────────────────────────────┐
                     │                                                        │
                     │         ┌─────────────┐                                │
                     │         │  analyzing  │                                │
                     │         └──────┬──────┘                                │
                     │                │                                       │
                     │                ▼                                       │
                     │         ┌─────────────────┐                            │
                     │  ┌──────│manifest_creating│◀─────┐                     │
                     │  │      └────────┬────────┘      │                     │
                     │  │               │               │ max 2               │
                     │  │               ▼               │ revisions           │
                     │  │      ┌─────────────────┐      │                     │
                     │  │      │manifest_reviewing├─────┘                     │
                     │  │      └────────┬────────┘                            │
                     │  │               │                                     │
                     │  │               ▼                                     │
                     │  │      ┌─────────────────┐                            │
                     │  │  ┌───│ svg_generating  │◀─────┐                     │
                     │  │  │   └────────┬────────┘      │                     │
                     │  │  │            │               │ max 2               │
                     │  │  │            ▼               │ revisions           │
                     │  │  │   ┌─────────────────┐      │                     │
                     │  │  │   │  svg_reviewing  ├──────┘                     │
                     │  │  │   └────────┬────────┘                            │
                     │  │  │            │                                     │
                     │  ▼  ▼            ▼                                     │
                     │ ┌────────┐  ┌──────────┐  ┌───────────────┐            │
                     └▶│ failed │  │completed │  │partial_success│            │
                       └────────┘  └──────────┘  └───────────────┘            │
```

---

## 6. 完全冪等性（v5.0 強化）

```yaml
idempotency:
  # 入力ハッシュ計算
  input_hashing:
    text:
      algorithm: sha256
      preprocessing:
        - normalize_unicode: "NFC"
        - collapse_whitespace: true
        - trim: true
      formula: "sha256(preprocessed_text)"

    image:
      algorithm: sha256
      preprocessing:
        - decode_to_raw_pixels: true
        - resize_if_large: { max_dimension: 4096 }
      formula: "sha256(raw_pixels)"

    combined:
      formula: "sha256(text_hash + '|' + sorted(image_hashes).join('|'))"

  # ファイル競合解決（完全自動化）
  file_conflict:
    strategy: auto_rename
    format: "{base}_{YYYYMMDD_HHmmss}.drawio.svg"
    # 例: form-system_20251212_143052.drawio.svg

    # ユーザー確認が必要なケースを明示的に限定
    require_user_confirmation:
      - "user specified --overwrite flag"
      - "user explicitly named the file"

  # MCP キャッシュ
  mcp_cache:
    enabled: true
    key_formula: "sha256(tool_name + '|' + normalize(query))"
    storage: "outputs/.cache/mcp/{key}.json"
    ttl: 7d
    on_hit: return_cached
    on_miss: fetch_and_cache

  # LLM 決定論化
  llm_config:
    temperature: 0
    seed_derivation: "hash(workflow_id) mod 2147483648"
    top_p: 1.0
```

---

## 7. エラーハンドリング（v5.0 強化）

### エラー分類

```yaml
error_classification:
  transient: # リトライで回復可能
    codes:
      - NETWORK_ERROR
      - MCP_TIMEOUT
      - RATE_LIMIT_EXCEEDED
      - TEMPORARY_UNAVAILABLE
    handling:
      max_retries: 3
      backoff: exponential
      base_delay: 1s
      max_delay: 30s
    example: "MCP サーバー一時的エラー"

  recoverable: # チェックポイントから復旧可能
    codes:
      - INVALID_MANIFEST_FORMAT
      - SVG_GENERATION_FAILURE
      - REVIEW_SCORE_TOO_LOW
    handling:
      action: restore_checkpoint_and_retry
      max_recoveries: 2
    example: "SVG 生成中のフォーマットエラー"

  fatal: # 即時終了
    codes:
      - SCHEMA_VALIDATION_ERROR
      - FILE_SYSTEM_FULL
      - USER_CANCELLATION
      - AUTHENTICATION_FAILURE
      - UNSUPPORTED_INPUT_TYPE
      - CYCLE_DETECTED
    handling:
      action: cleanup_and_report
    example: "入力形式がサポート対象外"
```

### ロールバック手順

```yaml
rollback:
  enabled: true
  procedure:
    1_find_checkpoint:
      action: "find_latest_valid_checkpoint(workflow_id)"
      output: checkpoint_record

    2_restore_context:
      action: "load(checkpoint_record.context_path)"
      output: restored_context

    3_cleanup_artifacts:
      action: "delete(files_created_after(checkpoint_record.timestamp))"
      exclude: [".lock", "errors.log"]

    4_update_state:
      action: |
        context.execution.phase = checkpoint_record.phase
        context.execution.checkpoint = checkpoint_record.id

    5_resume:
      action: "resume_from_phase(checkpoint_record.phase)"
```

### エラーログ形式

```yaml
error_logging:
  format:
    timestamp: ISO8601
    workflow_id: UUID
    phase: Phase
    error_code: string
    error_message: string
    error_category: "transient" | "recoverable" | "fatal"
    retry_count: number
    context_snapshot: FilePath | null
    stack_trace: string | null

  storage: "outputs/.workflow/{id}/errors.log"

  example: |
    {
      "timestamp": "2025-12-12T14:30:52Z",
      "workflow_id": "550e8400-e29b-41d4-a716-446655440000",
      "phase": "svg_generating",
      "error_code": "SVG_GENERATION_FAILURE",
      "error_message": "mxCell 構造の生成に失敗",
      "error_category": "recoverable",
      "retry_count": 1,
      "context_snapshot": "outputs/.workflow/550e8400.../context.cp3.yaml"
    }
```

---

## 8. 高速パス（v5.0 新規）

### 適用条件

```yaml
fast_path:
  eligibility:
    all_conditions_must_be_true:
      - "analysis.entities.length <= 3"
      - "analysis.groups.length == 0"
      - "no_azure_keywords_in_input"
      - "matches_known_template"

  # テンプレートパターン
  template_patterns:
    simple_flowchart:
      detection:
        keywords: ["フロー", "手順", "ステップ", "プロセス"]
        structure: "linear_sequence"
      template: "templates/simple-flowchart.drawio.svg"
      max_nodes: 5

    basic_architecture:
      detection:
        keywords: ["アーキテクチャ", "構成図", "システム構成"]
        structure: "hierarchical"
      template: "templates/basic-architecture.drawio.svg"
      max_nodes: 5

    simple_sequence:
      detection:
        keywords: ["シーケンス", "順序", "タイムライン"]
        structure: "sequence"
      template: "templates/simple-sequence.drawio.svg"
      max_nodes: 4
```

### 高速パスフロー

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Fast Path Flow (v5.0)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   INPUT                                                                     │
│     │                                                                       │
│     ▼                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ Analysis Module                                                     │   │
│   │  └─ fast_path_eligible = true                                       │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│     │                                                                       │
│     │ 高速パス適用                                                          │
│     ▼                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ Template Matching                                                   │   │
│   │  └─ select_template(pattern)                                        │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│     │                                                                       │
│     ▼                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ Template Filling                                                    │   │
│   │  └─ fill_template(entities, relationships)                          │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│     │                                                                       │
│     │ スキップ: manifest_reviewing                                         │
│     │                                                                       │
│     ▼                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ SVG Review (簡易版)                                                 │   │
│   │  └─ 基本的な構造チェックのみ                                        │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│     │                                                                       │
│     ▼                                                                       │
│   COMPLETED (約 8 分、通常の 56% 削減)                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 処理時間比較

| 複雑度   | v4.1  | v5.0 (標準) | v5.0 (高速パス) | 改善率   |
| -------- | ----- | ----------- | --------------- | -------- |
| simple   | 18 分 | 15 分       | **8 分**        | **-56%** |
| moderate | 32 分 | 28 分       | -               | -12%     |
| complex  | 50 分 | 45 分       | -               | -10%     |

---

## 9. runSubagent 応答スキーマ

```yaml
subagent_response:
  # 共通構造
  common:
    success: boolean
    data: T | null
    error:
      code: ErrorCode
      message: string
      recoverable: boolean
    metrics:
      duration_ms: number
      tokens_used: number
    next_action: 'proceed' | 'retry' | 'fix' | 'escalate'

  # Manifest Gateway 固有
  manifest_gateway:
    data:
      manifest_path: FilePath
      early_quality_score: number
      entities_extracted: number
      layout_selected: string

  # SVG Forge 固有
  svg_forge:
    data:
      svg_path: FilePath
      self_validation_passed: boolean
      mxcell_count: number
      file_size_bytes: number
```

---

## 10. クイックリファレンス

### 必須チェックリスト

- [ ] 出力パスは `outputs/` 配下の kebab-case
- [ ] 拡張子は `*.drawio.svg`
- [ ] mxCell 構造が存在（draw.io 編集可能）
- [ ] content 属性が空でない
- [ ] WorkflowContext が更新されている
- [ ] チェックポイントが保存されている
- [ ] 差し戻し上限を超えていない
- [ ] タイムアウト内で完了している
- [ ] ファイル競合は自動解決済み

### 処理時間目安（v5.0）

| 複雑度   | 標準  | 高速パス |
| -------- | ----- | -------- |
| simple   | 15 分 | 8 分     |
| moderate | 28 分 | -        |
| complex  | 45 分 | -        |

### エージェント数の推移

| バージョン | エージェント | モジュール | 合計  |
| ---------- | ------------ | ---------- | ----- |
| v1.0       | 7            | 0          | 7     |
| v2.0       | 10           | 0          | 10    |
| v3.0       | 5            | 0          | 5     |
| v4.0-4.1   | 3            | 0          | 3     |
| **v5.0**   | **3**        | **4**      | **7** |

> v5.0 ではエージェント数は同じだが、内部モジュール化により責務が明確化

---

## 付録 A: バージョン比較表

| 機能             | v4.1           | v5.0              |
| ---------------- | -------------- | ----------------- |
| エージェント構成 | 3 (God Object) | 3 + 4 モジュール  |
| 循環依存防止     | なし           | ✅ 上限 + 検出    |
| タイムアウト     | 未定義         | ✅ 全フェーズ定義 |
| I/O Contract     | YAML 疑似      | ✅ JSONSchema     |
| 冪等性           | 部分的         | ✅ 完全           |
| ファイル競合     | ユーザー確認   | ✅ 自動解決       |
| 高速パス         | なし           | ✅ 56% 短縮       |
| エラー分類       | なし           | ✅ 3 分類         |
| ロールバック     | 未定義         | ✅ 手順明確化     |

---

## 付録 B: 移行チェックリスト

v4.1 → v5.0 移行時の確認事項:

- [ ] WorkflowContext に `revision_count` フィールドを追加
- [ ] WorkflowContext に `fast_path_eligible` フィールドを追加
- [ ] タイムアウト処理を実装
- [ ] サイクル検出ロジックを実装
- [ ] テンプレートファイルを作成（高速パス用）
- [ ] JSONSchema ファイルを作成
- [ ] エラー分類ロジックを実装
- [ ] ファイル競合の自動解決を実装
