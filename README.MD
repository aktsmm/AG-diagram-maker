# AG-Diagram Maker

GitHub Copilot と Draw.io を活用して、**編集可能な画像ファイル**を AI で自動生成するリポジトリです。

## 概要

VS Code の [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) 拡張機能を使用して、**画像として表示でき、かつ Draw.io で編集可能なファイル**（`.drawio.svg`）を AI が自動生成します。

---

## ⚖️ ライセンスと使用条件

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

本プロジェクトは **CC BY-NC-SA 4.0**（表示-非営利-継承）ライセンスの下で提供されています。

- ✅ 共有・翻案は自由（非営利目的に限る）
- ✅ クレジット表示が必要
- ⚠️ AI 学習データとしての使用は禁止

詳細は [LICENSE](./LICENSE) を参照してください。

---

## 🚀 Quick Start

### 前提条件・セットアップ

1. **VS Code** + **GitHub Copilot** サブスクリプション
2. 拡張機能をインストール：
   - [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) - Draw.io 編集（必須）
   - [Excel Viewer](https://marketplace.visualstudio.com/items?itemName=GrapeCity.gc-excelviewer) - Excel プレビュー（推奨）
3. リポジトリをクローン：
   ```bash
   git clone https://github.com/<your-username>/AG-Diagram Maker.git
   cd AG-Diagram Maker && code .
   ```

### ☁️ クラウドアイコンの有効化（Azure / AWS）

生成した図で **Azure や AWS のアイコンを表示する**には、draw.io でライブラリを有効化する必要があります。

1. 生成した `.drawio` または `.drawio.svg` ファイルを VS Code で開く
2. 左下の **「+ その他の図形」** をクリック
3. 以下にチェックを入れる：
   - ✅ **Azure** - Azure リソースアイコン
   - ✅ **AWS** - AWS サービスアイコン
4. **「適用」** をクリック

> 💡 一度有効化すれば、以降は自動的に適用されます。

### まずは試してみよう（1 行で OK）

Copilot Chat（`Ctrl+Shift+I`）を開いて、以下をコピペ：

```
inputs/Sample-jiki-kikan-system-vdi-requirements.md から必要なシステム構成図をつくってください
```

```
inputs/Sample_20251114_procurement_request_for_information_outline_02.xlsx の内容をフローチャートにして
```

```
inputs/Sample_Azure_Architecture.png を参考に構成図を再作成して
```

> 💡 出力先を指定しない場合、AI が適切なファイル名を自動で決めて `outputs/` に保存します（推奨形式: `.drawio`）。

> 🎯 **複雑な図を生成する場合**: Copilot Chat で `@flow-orchestrator` エージェントを選択すると、マニフェスト作成 → レビュー → 生成の段階的ワークフローで品質が向上します。

### 入力ファイルなしで試す（テキスト指示のみ）

入力ファイルがなくても、テキストで要件を伝えるだけで図面を生成できます。

```
Intuneの通信フローを書いて
```

```
経費精算の申請フローを作成して（申請→承認/差戻し→経理確認→支払い）
```

### 生成後の確認

1. `outputs/` フォルダに `.drawio` ファイルが作成される
2. VS Code でファイルをクリック → Draw.io エディタで開く
3. 必要に応じて手動で微調整

---

## 📂 サンプル入力ファイル

`inputs/` フォルダにサンプルファイルが用意されています。

| ファイル                                                                                                                                            | 内容                           | 難易度 |
| --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | ------ |
| [Sample-jiki-kikan-system-vdi-requirements.md](./inputs/Sample-jiki-kikan-system-vdi-requirements.md)                                               | VDI 要件定義書（276 行）       | ⭐⭐⭐ |
| [Sample_20251114_procurement_request_for_information_outline_02.xlsx](./inputs/Sample_20251114_procurement_request_for_information_outline_02.xlsx) | 調達情報依頼概要（Excel）      | ⭐⭐   |
| [Sample_Azure_Architecture.png](./inputs/Sample_Azure_Architecture.png)                                                                             | Azure アーキテクチャ図（画像） | ⭐⭐   |

### もう少し詳しく指示したい場合

**Markdown から（特定セクション指定）**

```
inputs/Sample-jiki-kikan-system-vdi-requirements.md の「6. アーキテクチャ概要」から
Azure/AWS/オンプレのハブ&スポーク構成図を作成して
```

**Excel から（図の種類を指定）**

```
inputs/Sample_20251114_procurement_request_for_information_outline_02.xlsx から
関係者間のやり取りをスイムレーン図で作成して
```

**画像から（再作成）**

```
inputs/Sample_Azure_Architecture.png を参考に、
同じ構成の draw.io 編集可能な図を作成して
```

### プロンプトのコツ

| やりたいこと       | プロンプトのコツ                                     |
| ------------------ | ---------------------------------------------------- |
| 特定セクションだけ | `「6. アーキテクチャ概要」セクションをもとに` と指定 |
| 詳細度を調整       | `概要レベルで` / `詳細に全コンポーネントを含めて`    |
| 図の種類を指定     | `スイムレーン図で` / `フローチャートで`              |

---

## 🔑 仕組み：なぜ AI で画像生成ができるのか

### AI は「画像を描いている」のではなく「XML を生成している」

**SVG（Scalable Vector Graphics）** は「テキストで記述できるベクター画像」です。AI がテキスト（XML）を生成するだけで、画像として表示できます。

```
┌─────────────┐      ┌─────────────────────┐      ┌─────────────┐
│  自然言語   │  →   │  XML/SVG テキスト   │  →   │   画像表示  │
│  Markdown   │      │  (mxGraphModel)     │      │  (ブラウザ) │
└─────────────┘      └─────────────────────┘      └─────────────┘
      ↑                       ↑                         ↑
   人間が入力            AI が生成              SVG として描画
```

### .drawio.svg ファイルの構造

```xml
<svg xmlns="http://www.w3.org/2000/svg" ...>
  <!-- 1. 画像として表示される部分（通常の SVG 要素） -->
  <rect x="100" y="50" width="120" height="60" fill="#dae8fc" stroke="#6c8ebf"/>
  <text x="160" y="85">ノード名</text>

  <!-- 2. draw.io 編集用のメタデータ（非表示だが埋め込まれている） -->
  <mxfile ...>
    <mxGraphModel ...>
      <mxCell id="1" value="ノード名" style="rounded=1;..." vertex="1">
        <mxGeometry x="100" y="50" width="120" height="60"/>
      </mxCell>
    </mxGraphModel>
  </mxfile>
</svg>
```

| 視点         | 処理内容                                         |
| ------------ | ------------------------------------------------ |
| **ブラウザ** | SVG 要素を描画 → 画像として表示                  |
| **draw.io**  | mxGraphModel を読み取り → 編集可能な図として開く |
| **AI**       | XML/SVG テキストを生成しているだけ               |

### このシステムの強み

| 特徴                   | 説明                                                        |
| ---------------------- | ----------------------------------------------------------- |
| **編集可能な出力**     | 生成物を draw.io で後から人間が修正可能                     |
| **構造化マニフェスト** | テキスト → マニフェスト → SVG の 2 段階変換で精度向上       |
| **適応型レビュー**     | 複雑度に応じて 1-3 ラウンドのレビュー（品質駆動の早期終了） |

### ファイル形式について

| 拡張子                       | 説明                                        | 推奨           |
| ---------------------------- | ------------------------------------------- | -------------- |
| `*.drawio` / `*.dio`         | Draw.io ネイティブ形式（最も安定）          | ⭐ **推奨**    |
| `*.drawio.svg` / `*.dio.svg` | SVG 画像として表示可能 + Draw.io で編集可能 | 画像埋め込み時 |
| `*.drawio.png` / `*.dio.png` | PNG 画像として表示可能 + Draw.io で編集可能 | -              |

> 📋 形式選択の詳細は [docs/drawio-format-selection-guide.md](./docs/drawio-format-selection-guide.md) を参照

**`.drawio` 推奨理由**: draw.io での編集安定性が最も高い / ファイルサイズが小さい / 複数ページ対応  
**`.drawio.svg` 用途**: Markdown や Web ページに画像として埋め込みたい場合

---

## 📁 ディレクトリ構造

```
AG-Diagram Maker/
├── README.MD                 # このファイル
├── AGENTS.md                 # エージェントカタログ（v5.1）
├── outputs/                  # 生成された SVG ファイル
├── image_manifest/           # 図作成用マニフェスト
├── inputs/                   # 入力ファイル（テキスト/画像/Excel）
├── docs/                     # ドキュメント
└── .github/
    ├── agents/               # エージェント定義（3 エージェント）
    ├── instructions/         # 共通ルール・ガイドライン
    └── copilot-instructions.md
```

---

## 🤖 エージェント・マニフェスト（上級者向け）

### エージェント一覧（v5.1）

| エージェント        | 用途                                                  |
| ------------------- | ----------------------------------------------------- |
| `flow-orchestrator` | 全体統括 + 入力分析 + **Review Engine 内蔵**          |
| `manifest-gateway`  | マニフェスト生成（text/visual/portrait 全タイプ対応） |
| `svg-forge`         | 図面生成 + 自己検証 + **保存前ゲート**                |

> **Note**: v5.1 で Review Engine が `flow-orchestrator` に内蔵され、`svg-forge` に保存前ゲートが追加されました。
>
> 詳細は [AGENTS.md](./AGENTS.md) を参照

### モデル要件（重要）

- **前提**: 本リポジトリのエージェントワークフロー（`flow-orchestrator` → `manifest-gateway` → `svg-forge`）は、エージェントワークフローに対応した AI モデルが必要です。非対応モデルでは、分割実行・レビュー内蔵・保存前ゲートなどの段階的処理が動作しません。
- **推奨モデル**: Opus（エージェントワークフロー互換。複雑な図面生成に強く、レビュー反復の安定性が高い）
- **動作保証の範囲**: 上記モデルでの動作を前提に品質ゲート・チェックポイント設計を行っています。他モデルを使用する場合は、生成フェーズを単体実行に切り替えるか、手動レビューを前提にしてください。

### マニフェストの活用

`image_manifest/` ディレクトリには、生成されたマニフェストファイルが保存されます。

| ファイル                                                  | 図の種類             |
| --------------------------------------------------------- | -------------------- |
| `azure-firewall-vnet-architecture.md`                     | アーキテクチャ図     |
| `application-form-creation-system-architecture.md`        | システム構成図       |
| `application-form-creation-ponchi-e.md`                   | ポンチ絵             |
| `administrative-application-form-builder-architecture.md` | 管理系アーキテクチャ |
| `procurement-application-form-system-architecture.md`     | 調達システム構成     |
| `procurement-application-form-system-detail.md`           | 詳細フロー           |

---

## ⚠️ 依存関係とセキュリティ

### 外部依存（サプライチェーン）

このリポジトリは **npm/pip 等のパッケージ管理ツールを使用しておらず**、サプライチェーン攻撃のリスクは低いです。

| 依存対象                                                                                        | 種別             | リスク評価              |
| ----------------------------------------------------------------------------------------------- | ---------------- | ----------------------- |
| [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) | VS Code 拡張機能 | ⚠️ 中（外部提供）       |
| GitHub Copilot                                                                                  | SaaS サービス    | ✅ 低（Microsoft 提供） |

### 注意事項

- **VS Code 拡張機能**: `hediet.vscode-drawio` は第三者が開発・保守しています。インストール前に [GitHub リポジトリ](https://github.com/hediet/vscode-drawio) で最新のセキュリティ状況を確認してください
- **入力ファイル**: `inputs/` に配置するファイルは信頼できるソースからのみ使用してください
- **AI 生成物**: 生成された SVG ファイルは人間によるレビューを推奨します

---

## 参考リンク

- [_.drawio.png と _.drawio.svg とはなんなのか - Zenn](https://zenn.dev/kaakaa/articles/qiita-20200728-ff9ab5933cc0fb6fd8d8)  
  → `.drawio.svg` 形式の仕組みを詳しく解説。本リポジトリの技術的基盤
- [VS Code Draw.io Integration - Marketplace](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio)  
  → 本リポジトリで必須の拡張機能。VS Code 内で draw.io 編集を可能にする
- [hediet/vscode-drawio - GitHub](https://github.com/hediet/vscode-drawio)  
  → 上記拡張機能のソースコード。mxGraphModel 構造の参考に
