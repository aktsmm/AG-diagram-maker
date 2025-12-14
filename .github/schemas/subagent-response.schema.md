# SubAgent Response Schema

> runSubagent 呼び出し時の標準戻り値形式を定義するスキーマ。

## 目的

- runSubagent の呼び出し結果を標準化
- エージェント間のインターフェースを明確化
- エラーハンドリングとフィードバックループの制御を容易化

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SubAgent Response Schema",
  "description": "runSubagent 呼び出し時の標準戻り値形式",
  "type": "object",
  "required": ["status", "agent_name", "execution_time"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["success", "partial", "failed", "needs_revision"],
      "description": "実行結果のステータス"
    },
    "agent_name": {
      "type": "string",
      "description": "実行したエージェント名"
    },
    "execution_time": {
      "type": "number",
      "description": "実行時間（秒）"
    },
    "output_path": {
      "type": "string",
      "description": "生成されたファイルのパス（該当する場合）"
    },
    "score": {
      "type": "number",
      "minimum": 0,
      "maximum": 100,
      "description": "品質スコア（レビュー系エージェントの場合）"
    },
    "round": {
      "type": "integer",
      "minimum": 1,
      "maximum": 4,
      "description": "レビューラウンド番号（レビュー系エージェントの場合）"
    },
    "issues": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["severity", "description"],
        "properties": {
          "severity": {
            "type": "string",
            "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
          },
          "description": {
            "type": "string"
          },
          "action": {
            "type": "string",
            "description": "推奨される修正アクション"
          }
        }
      },
      "description": "検出された問題のリスト"
    },
    "next_action": {
      "type": "string",
      "enum": ["proceed", "revise", "regenerate", "escalate"],
      "description": "次に取るべきアクション"
    },
    "revision_target": {
      "type": "string",
      "description": "needs_revision 時の差し戻し先エージェント名"
    },
    "metadata": {
      "type": "object",
      "description": "追加のメタ情報",
      "properties": {
        "complexity": {
          "type": "string",
          "enum": ["simple", "moderate", "complex"]
        },
        "estimated_nodes": {
          "type": "integer"
        },
        "estimated_edges": {
          "type": "integer"
        }
      }
    }
  }
}
```

## ステータス定義

| ステータス       | 説明                           | 次のアクション           |
| ---------------- | ------------------------------ | ------------------------ |
| `success`        | 正常完了                       | `proceed` - 次フェーズへ |
| `partial`        | 部分的に完了（軽微な問題あり） | `proceed` or `revise`    |
| `failed`         | 失敗（再試行不可）             | `escalate` - 報告        |
| `needs_revision` | 差し戻しが必要                 | `revise` - 指定先へ戻る  |

## 次アクション定義

| アクション   | 説明                                 | トリガー条件                     |
| ------------ | ------------------------------------ | -------------------------------- |
| `proceed`    | 次のフェーズへ進行                   | status = success, score >= 90    |
| `revise`     | 指定されたエージェントへ差し戻し     | 根本的誤解釈、構造的問題         |
| `regenerate` | 再生成を要求                         | SVG レビューで修正困難な問題検出 |
| `escalate`   | ユーザーまたは上位エージェントに報告 | 失敗、上限到達                   |

## 使用例（v4.1 - 3 エージェント構成）

> **Note**: v4.0 以降、router-agent, planner-agent, manifest-review, svg-review は廃止され、
> Flow Orchestrator に統合されました。以下は現行の 3 エージェント構成での例です。

### Manifest Gateway の戻り値（成功）

```yaml
status: "success"
agent_name: "manifest-gateway"
execution_time: 300
output_path: "outputs/.workflow/a1b2c3d4/manifest.v1.md"
next_action: "proceed"
metadata:
  input_type: "text"
  complexity: "moderate"
  early_quality_score: 78
```

### Manifest Gateway の戻り値（早期品質チェック失敗）

```yaml
status: "needs_revision"
agent_name: "manifest-gateway"
execution_time: 120
score: 65
issues:
  - severity: "HIGH"
    description: "ノード定義が不足。入力から抽出できる要素が反映されていない"
    action: "入力を再解析し、ノードを追加"
next_action: "revise"
revision_target: "manifest-gateway" # 自己修正
```

### SVG Forge の戻り値（成功）

```yaml
status: "success"
agent_name: "svg-forge"
execution_time: 480
output_path: "outputs/user-registration-flow.drawio.svg"
next_action: "proceed"
metadata:
  node_count: 8
  edge_count: 10
  self_validation: "passed"
```

### SVG Forge の戻り値（自己検証失敗）

```yaml
status: "needs_revision"
agent_name: "svg-forge"
execution_time: 300
issues:
  - severity: "CRITICAL"
    description: "content属性内のrootが空。mxCell定義がない"
    action: "全図形をmxCell形式で再定義"
  - severity: "HIGH"
    description: "エッジのsource/targetが存在しないノードを参照"
    action: "参照整合性を修正"
next_action: "regenerate"
revision_target: "svg-forge" # 自己修正
```

### SVG Forge の戻り値（マニフェスト問題検出）

```yaml
status: "needs_revision"
agent_name: "svg-forge"
execution_time: 180
issues:
  - severity: "HIGH"
    description: "マニフェストのノード定義がdraw.ioで表現困難"
    action: "マニフェストのノード形状を修正"
next_action: "revise"
revision_target: "manifest-gateway" # マニフェスト修正が必要
```

## フィードバックループとの連携（v4.1）

```
┌─────────────────────────────────────────────────────────────┐
│     SubAgent Response → Flow Orchestrator (v4.1)            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【Manifest Gateway からの戻り】                             │
│  status: success → Orchestrator内蔵Review → SVG Forge       │
│  status: needs_revision → manifest-gateway（自己修正）      │
│                                                             │
│  【SVG Forge からの戻り】                                    │
│  status: success → Orchestrator内蔵Review → 完了            │
│  status: needs_revision (structural) → svg-forge（自己修正）│
│  status: needs_revision (content) → manifest-gateway        │
│  status: failed → ユーザーに報告                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## バリデーション（v4.1 更新）

戻り値を受け取った際のバリデーションチェック:

```yaml
validation_rules:
  required_fields:
    - status
    - agent_name
    - execution_time

  conditional_required:
    - if: status == "success" AND agent is review-type
      then: score is required
    - if: status == "needs_revision"
      then: revision_target is required
    - if: next_action == "regenerate"
      then: issues is required

  value_constraints:
    - score: 0-100
    - execution_time: "> 0"

  # v4.1: 有効なrevision_target（2エージェントのみ）
  valid_revision_targets:
    - manifest-gateway
    - svg-forge
    # 廃止: router-agent, planner-agent, manifest-review, svg-review
```
