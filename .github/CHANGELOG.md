# Changelog

すべてのエージェント・インストラクションの変更履歴を集約したファイルです。

---

## v5.1 (2025-12-12)

### 二段階アーキテクチャ適用版

| 対象                                          | 変更内容                                                                  |
| --------------------------------------------- | ------------------------------------------------------------------------- |
| **diagram-ir.schema.json**                    | 新規作成。DiagramIR の厳密な JSON Schema 定義                             |
| **agent-responsibilities-v5.instructions.md** | 新規作成。責務分離の 5 層定義 (Parse/Generate/Validate/Transform/Produce) |
| **deterministic-transform.instructions.md**   | 新規作成。IR → mxCell の決定的変換ルール                                  |
| **logging-traceability.instructions.md**      | 新規作成。全フェーズのロギング仕様                                        |
| **config.schema.json**                        | 新規作成。環境設定の JSON Schema                                          |
| **config.default.yaml**                       | 新規作成。デフォルト設定ファイル                                          |

**設計原則の適用**:

1. **入力 → IR → 最終出力** の二段階アーキテクチャに統一
2. **IR を JSON Schema で厳密に仕様化** - 曖昧な自然言語を排除
3. **責務の厳密分離** - Parse/Generate/Validate/Transform/Produce を混在させない
4. **変換処理の決定論化** - 同一 IR → 常に同一成果物
5. **バリデーション強化** - 自動補完禁止、エラー報告のみ
6. **ロギング必須化** - IR の保存を必須に変更
7. **環境非依存設計** - 設定ファイルによる抽象化
8. **拡張性確保** - IR 中心の設計で新形式追加が容易

**新エージェント構成提案**:

| v4.x              | v5.1 提案    | 変更                     |
| ----------------- | ------------ | ------------------------ |
| Flow Orchestrator | Coordinator  | Review Engine を分離     |
| Manifest Gateway  | IR-Builder   | Parse + Generate のみ    |
| SVG Forge         | IR-Renderer  | Transform + Produce のみ |
| (内蔵)            | IR-Validator | Validate を独立化        |
| (なし)            | Logger       | 横断的関心事を分離       |

**参照**: [docs/workflow-architecture-v5.1-report.md](../docs/workflow-architecture-v5.1-report.md)

---

## v4.5 (2025-12-12)

### インストラクション分離と集約

| 対象                                     | 変更内容                                                          |
| ---------------------------------------- | ----------------------------------------------------------------- |
| **agent-common.instructions.md**         | 新規作成。共通構造、WorkflowContext、冪等性、MCP 活用ルールを集約 |
| **drawio-compatibility.instructions.md** | 新規作成。mxCell 構造、スタイル、検証チェックリストを集約         |
| 全エージェント                           | インストラクション参照テーブルを追加、重複ルールを削除            |

**メリット**:

- エージェント間でのルール重複を排除
- 1 箇所の修正で全エージェントに反映
- ドキュメントの見通し改善

---

## v4.4 (2025-12-12)

### Azure/AWS アイコン使用ルール

| 対象                            | 変更内容                                             |
| ------------------------------- | ---------------------------------------------------- |
| **cloud-icons.instructions.md** | 新規作成。Azure/AWS アイコンの正式フォーマットを定義 |
| svg-forge                       | Azure/AWS アイコン使用ルールを追加                   |

**Azure アイコン形式**:

```
image=img/lib/azure2/{category}/{icon}.svg
```

**AWS アイコン形式**:

```
shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{service}
```

---

## v4.3 (2025-12-12)

### 出力形式選択ルール

| 対象                              | 変更内容                                          |
| --------------------------------- | ------------------------------------------------- |
| **output-format.instructions.md** | 新規作成。.drawio vs .drawio.svg 選択ルールを定義 |
| svg-forge                         | 出力形式選択ルールを追加                          |

**問題**: `.drawio.svg` で content 属性のみだと描画要素が空になる  
**解決**: `.drawio` (XML) 形式を推奨

---

## v4.2 (2025-12-12)

### mxCell 完全性ブロッキング

| 対象                              | 変更内容                                    |
| --------------------------------- | ------------------------------------------- |
| **quality-gates.instructions.md** | 新規作成。mxCell 検証、保存前ゲートを定義   |
| svg-forge                         | mxCell 完全性ブロッキング、保存前ゲート追加 |
| flow-orchestrator                 | SVG 受領時即時検証を追加                    |

**必須条件**: `mxCell数 >= 2 + ノード数 + エッジ数`

---

## v4.1 (2025-12-12)

### draw.io 互換性強制

| 対象              | 変更内容                                      |
| ----------------- | --------------------------------------------- |
| flow-orchestrator | 情報充足性検証、ファイル重複チェック追加      |
| manifest-gateway  | ファイル重複チェック、draw.io 互換性確認追加  |
| svg-forge         | mxCell 必須検証強化、ファイル重複チェック追加 |

**禁止パターン**:

- 空の content 属性
- mxCell 定義のない空の mxGraphModel
- SVG 要素のみで mxCell 定義なし

---

## v4.0 (2025-12-11)

### Review Engine 内包（3 エージェント体制）

| 対象              | 変更内容                            |
| ----------------- | ----------------------------------- |
| flow-orchestrator | manifest-review, svg-review を内包  |
| manifest-review   | **廃止** → flow-orchestrator に統合 |
| svg-review        | **廃止** → flow-orchestrator に統合 |

**チェックポイント方式**:

1. 入力分析完了
2. マニフェスト作成完了
3. マニフェストレビュー通過
4. SVG 生成完了
5. SVG レビュー通過

---

## v3.0 (2025-12-11)

### Gateway 統合

| 対象                      | 変更内容                                    |
| ------------------------- | ------------------------------------------- |
| manifest-gateway          | 3 Gateway を統合、早期品質チェック追加      |
| text-manifest-gateway     | **廃止** → manifest-gateway に統合          |
| visual-manifest-gateway   | **廃止** → manifest-gateway に統合          |
| portrait-manifest-gateway | **廃止** → manifest-gateway に統合          |
| flow-orchestrator         | Router/Planner を内包、WorkflowContext 導入 |

---

## v2.0 (2025-12-11)

### Router/Planner 追加

| 対象              | 変更内容                                |
| ----------------- | --------------------------------------- |
| flow-orchestrator | Router/Planner 委譲、適応型ラウンド追加 |

---

## v1.0 (2025-12-01)

### 初版

- flow-orchestrator 初版作成
- 各タイプ別 Gateway 初版作成
- svg-forge 初版作成

---

## 廃止されたエージェント

| エージェント              | 廃止バージョン | 理由                     |
| ------------------------- | -------------- | ------------------------ |
| router-agent              | v3.0           | flow-orchestrator に統合 |
| planner-agent             | v3.0           | flow-orchestrator に統合 |
| text-manifest-gateway     | v3.0           | manifest-gateway に統合  |
| visual-manifest-gateway   | v3.0           | manifest-gateway に統合  |
| portrait-manifest-gateway | v3.0           | manifest-gateway に統合  |
| manifest-review           | v4.0           | flow-orchestrator に統合 |
| svg-review                | v4.0           | flow-orchestrator に統合 |
