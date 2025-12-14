# `.github/agents` ディレクトリ

Copilot で扱う構造化エージェントのマニフェストを置く場所だよ。テンプレとしてこのフォルダをコピーする場合は、以下の手順でエージェントを追加してね。

1. `*.agent.md` 形式でエージェントを定義する。
2. `AGENTS.md` に行を追加して、ここに置いたマニフェストへリンクさせる。
3. 必要に応じて `.github/copilot-instructions.md` やチャットモードから読み込む。
4. runSubagent を使うときは「コンテキスト隔離」が主目的。計画 → 実装 → レビューのように工程を分ける用途に向いている一方、軽いタスクには向かないのでツール選択欄に書きすぎない。
5. runSubagent 自体は Copilot 側のビルトインツールで、ここに置く Markdown では「いつ runSubagent を呼び出すか」「サブエージェントへ何を渡すか」を記述するだけ。`tools: ["runSubagent", ...]` と書けば利用でき、別途 runSubagent 用ファイルを用意する必要はない。
6. 使い方の例: orchestrator.agent.md で `tools` に runSubagent を含め、本文で「#tool:runSubagent で issue.agent.md を呼び出し、要望を Issue に変換」と指示する。VS Code の Copilot Chat でそのエージェントを選んで話しかけると、runSubagent が裏で issue.agent.md 用のサブセッションを起動し、処理結果だけが戻る。

> 参考: `sample.agent.md` が最小構成の例。

- runSubagent を用いたオーケストレーター設計では、エージェントごとに Job Responsibility (やること) と Non-goal (やらないこと) を必ず明記しよう。
- ファイル構成の一例:

  ```
  orchestrator.agent.md  # 進行管理のみ。コード編集は禁止。
  issue.agent.md         # 要望の解像度を高め Issue を生成
  plan.agent.md          # 既存コード調査と設計
  impl.agent.md          # TDD ベースで実装＆テスト
  review.agent.md        # コードレビュー＆リワーク依頼
  pr.agent.md            # PR 作成と最終報告
  ```

  プロジェクトによって最適な役割は変わるため、必要なファイルだけ選んでね。

- 各ファイルをモジュール化することで単体呼び出しや差し替えが簡単になる。issue.agent.md だけ別ブランチで改善する、などの運用がしやすい。
- オーケストレーターには「サブエージェント定義を勝手に改変しない」「ユーザー意図を自力で補わない」といった禁止ルールを書き、責任境界を明文化しておくと暴走しにくい。
- /dev/null へのリダイレクトや無限ループを避ける警告文を `tools` セクションの下に入れておくと、自動実行でも中断しづらい。

## プロジェクト固有のルール

> **Note**: 画像生成フロー、レビュールール、runSubagent 利用基準の詳細は
> `.github/instructions/agent-workflow-v5.instructions.md` を参照。

## 現行エージェント構成（v4.1）

本プロジェクトでは **3 エージェント構成** を採用しています：

| エージェント      | ファイル                     | 役割                                     |
| ----------------- | ---------------------------- | ---------------------------------------- |
| Flow Orchestrator | `flow-orchestrator.agent.md` | 全体統括 + 入力分析 + Review Engine 内蔵 |
| Manifest Gateway  | `manifest-gateway.agent.md`  | マニフェスト生成（全入力タイプ対応）     |
| SVG Forge         | `svg-forge.agent.md`         | SVG 生成 + 自己検証                      |

### 廃止されたエージェント

以下は v4.0 で廃止され、Flow Orchestrator に統合されました：

- `router-agent` (v3.0 で廃止)
- `planner-agent` (v3.0 で廃止)
- `manifest-review` (v4.0 で廃止)
- `svg-review` (v4.0 で廃止)

### runSubagent の使用ルール

v4.1 では以下の 2 エージェントのみ `runSubagent` で呼び出します：

1. **manifest-gateway** - マニフェスト作成
2. **svg-forge** - SVG 生成

Review 処理は Flow Orchestrator 内で直接実行されます（runSubagent 不要）。
