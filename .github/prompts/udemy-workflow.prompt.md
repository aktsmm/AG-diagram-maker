# Udemy 問題集作成ワークフロー

このプロンプトは、PDF から Udemy 形式の問題集 CSV を作成するワークフローを実行します。

---

## 使用方法

1. このプロンプトをコピー
2. `{変数}` を実際の値に置き換え
3. Copilot Chat に貼り付けて実行

---

## プロンプトテンプレート

```markdown
# Udemy 問題集作成リクエスト

## 入力情報

| 項目             | 値                   |
| ---------------- | -------------------- |
| **PDF ファイル** | `{PDFファイルパス}`  |
| **試験コード**   | {試験コード}         |
| **試験名**       | {試験名}             |
| **出力先**       | `{出力ディレクトリ}` |
| **元言語**       | {en または ja}       |

## 実行指示

上記 PDF から Udemy 形式の問題集 CSV を作成してください。

### ワークフロー

1. **PDF 抽出**: PDF からテキストを抽出
2. **翻訳**: 英語の場合は日本語に翻訳
3. **構造化**: 問題・選択肢・正解を JSON に構造化
4. **解説生成**: 各選択肢の解説と全体解説を生成
5. **レビュー**: 品質検証（エラー 0 件まで繰り返し）
6. **出力**: Udemy CSV 形式で出力

### 品質基準

以下のレビュー基準に従ってください:

- `.github/instructions/review-criteria.instructions.md`

### 出力ファイル命名規則
```

{試験コード}\_PracticeSet_Part{番号}.csv

```

例: `GH500_PracticeSet_Part1.csv`
```

---

## 使用例

### GH-500 (GitHub Advanced Security)

```markdown
# Udemy 問題集作成リクエスト

## 入力情報

| 項目             | 値                                                             |
| ---------------- | -------------------------------------------------------------- |
| **PDF ファイル** | `d:\03_github\Ag-Udemy\gh-500\GH-500 V12.35 (1).pdf`           |
| **試験コード**   | GH-500                                                         |
| **試験名**       | GitHub Advanced Security                                       |
| **出力先**       | `d:\61_UdemyWorkSpaces\pending_GH-500_GitHubAdvancedSecurity\` |
| **元言語**       | en                                                             |

## 実行指示

上記 PDF から Udemy 形式の問題集 CSV を作成してください。
ワークフローに従って、各フェーズを順番に実行してください。
```

### GH-200 (GitHub Actions)

```markdown
# Udemy 問題集作成リクエスト

## 入力情報

| 項目             | 値                                                        |
| ---------------- | --------------------------------------------------------- |
| **PDF ファイル** | `d:\path\to\GH-200.pdf`                                   |
| **試験コード**   | GH-200                                                    |
| **試験名**       | GitHub Actions                                            |
| **出力先**       | `d:\61_UdemyWorkSpaces\fix_Inreview_GH200_GitHubActions\` |
| **元言語**       | en                                                        |

## 実行指示

上記 PDF から Udemy 形式の問題集 CSV を作成してください。
```

### GH-300 (GitHub Copilot)

```markdown
# Udemy 問題集作成リクエスト

## 入力情報

| 項目             | 値                                                     |
| ---------------- | ------------------------------------------------------ |
| **PDF ファイル** | `d:\path\to\GH-300.pdf`                                |
| **試験コード**   | GH-300                                                 |
| **試験名**       | GitHub Copilot                                         |
| **出力先**       | `d:\61_UdemyWorkSpaces\Inreview_GH-300_GitHubCopilot\` |
| **元言語**       | en                                                     |

## 実行指示

上記 PDF から Udemy 形式の問題集 CSV を作成してください。
```

---

## 対応試験一覧

| 試験コード | 試験名                   | ドメイン例                     |
| ---------- | ------------------------ | ------------------------------ |
| GH-100     | GitHub Administration    | 組織管理、リポジトリ管理       |
| GH-200     | GitHub Actions           | ワークフロー、Action 作成      |
| GH-300     | GitHub Copilot           | コード補完、Chat               |
| GH-500     | GitHub Advanced Security | Code Scanning、Secret Scanning |
| GH-900     | GitHub Foundations       | Git 基礎、コラボレーション     |

---

## 参照エージェント

実行時は以下のエージェントが順番に呼び出されます:

1. `.github/agents/pdf-parser.agent.md`
2. `.github/agents/translator.agent.md`
3. `.github/agents/question-formatter.agent.md`
4. `.github/agents/explanation-generator.agent.md`
5. `.github/agents/review.agent.md`
6. `.github/agents/udemy-exporter.agent.md`

統括: `.github/agents/udemy-orchestrator.agent.md`

---

## 注意事項

- PDF がスキャン画像の場合は OCR が必要（対応外）
- 問題数が多い場合は 25-30 問ごとにファイル分割
- レビューエラーが 0 件になるまで修正ループ
- 最終出力前に `validate_udemy_csv.py` で検証推奨
