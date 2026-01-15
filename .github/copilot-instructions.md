````instructions
## Copilot 共通指針 (v5.1)

- モデル: GPT-5.1-Codex-Max (Preview)。作業前にこのファイルと `.github/agents/*.agent.md` を読み、既存変更は保持する。
- 主用途: 画像/図面生成フローのオーケストレーション。
- draw.io での編集可能性を常に優先し、各ラウンドで確認する。

> **📋 詳細ルールは `.github/instructions/` 配下を参照。変更履歴は `.github/CHANGELOG.md` を参照。**
> **📋 インストラクション/スキーマ/エージェント/フローの詳細一覧は `AGENTS.md` を参照。**

## 🚨 必須ルール（サマリ）

| ルール | 内容 | 参照 |
|--------|------|------|
| **WorkflowContext** | 全処理で状態管理 | `agent-common` |
| **出力パス** | `outputs/` 配下、`*.drawio` 推奨 | `output-format` |
| **mxCell完全性** | mxCell数 >= 2 + ノード数 + エッジ数 | `quality-gates` |
| **generator属性** | mxfileに `generator="aktsmm/Ag-diagram-maker"` 必須 | `drawio-compatibility` |
| **クラウドアイコン** | Azure/AWS 公式アイコン使用 | `cloud-icons` |
| **IR スキーマ準拠** | DiagramIR は JSON Schema に準拠 | `diagram-ir.schema.json` |
| **決定的変換** | 同一 IR → 同一出力 | `deterministic-transform` |
| **ターミナル操作** | Git/ファイル操作前にカレントディレクトリを確認 | 下記参照 |

## 🚨 ターミナル操作ルール

**Git コマンドやファイル操作を実行する前に、必ずカレントディレクトリを確認すること。**

```powershell
# 必須: コマンド実行前にワークスペースルートに移動
Set-Location "d:\03_github\Ag-diagram-maker"
Get-Location  # 確認

# その後 Git コマンドを実行
git status
```

| チェック項目 | 確認方法 |
|-------------|---------|
| **カレントディレクトリ** | `Get-Location` または `pwd` で確認 |
| **Git リポジトリルート** | `git rev-parse --show-toplevel` で確認 |
| **期待するパス** | ワークスペースフォルダと一致するか確認 |

**禁止事項:**
- カレントディレクトリを確認せずに `git` コマンドを実行
- ドライブルート（`D:\` など）で Git 操作を実行
- 相対パスのみでファイル操作を実行（絶対パス推奨）

**必須事項:**
- **git コマンドは必ずリポジトリルートで実行**: `cd` が省略されると親ディレクトリの `.git` を参照する可能性あり
- **複合コマンドでは `cd` を最初に**: `cd "d:\03_github\Ag-diagram-maker"; git status` のように明示的に移動

## 🚨 ドキュメント管理方針

### インストラクション分離の原則

**このファイル（copilot-instructions.md）には詳細ルールを書かない。**

```yaml
copilot_instructions:
  purpose: "サマリと参照先の提示のみ"
  prohibited:
    - 詳細な処理手順の記載
    - YAML/コード例の埋め込み
    - バージョンごとの変更詳細
  required:
    - インストラクションへの参照
    - エージェントへの参照
    - 必須ルールのサマリ（1行以内）

instructions:
  purpose: "共通ルール・処理の詳細定義"
  location: ".github/instructions/*.instructions.md"
  when_to_create:
    - 複数エージェントで共有されるルール
    - 繰り返し参照される処理手順
    - 技術的な詳細（mxCell構造、アイコン形式など）

agents:
  purpose: "エージェント固有の責務・ワークフロー"
  location: ".github/agents/*.agent.md"
  content:
    - Job Responsibility / Non-goal
    - Inputs / Outputs
    - ワークフロー図
    - エージェント固有の処理ステップ

changelog:
  purpose: "変更履歴の集約"
  location: ".github/CHANGELOG.md"
````

### 新しいルールを追加する場合

1. **共通ルールの場合** → 既存インストラクションに追記、または新規インストラクション作成
2. **エージェント固有の場合** → 該当エージェントファイルに追記
3. **このファイルには** → 参照先とサマリのみ追記

### 参照パターン

```markdown
## ルール名

> **📋 詳細は `xxx.instructions.md` を参照**

| ルール       | 内容       |
| ------------ | ---------- |
| **ルール 1** | 1 行サマリ |
```

## 禁止事項

- マニフェスト指示からの乖離・過剰な自動補完
- 機密/個人情報の出力
- **このファイルへの詳細ルール・処理手順の直接記載**

```

```
