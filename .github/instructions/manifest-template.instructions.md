# マニフェスト テンプレート（draw.io SVG/PNG 用）

> 全ゲートウェイエージェント共通のマニフェスト作成ガイドライン。

## スコープ

- 対象: draw.io 編集可能な出力（`*.drawio.svg` 推奨）
- 入力経路: text / visual / portrait gateways
- 出力先: `image_manifest/{topic}.md`

## マニフェスト構造

### 必須項目

| 項目          | 説明               | 例                                          |
| ------------- | ------------------ | ------------------------------------------- |
| `title`       | 図のタイトル       | "ユーザー登録フロー"                        |
| `purpose`     | 図の目的・用途     | "新規ユーザーの登録プロセスを可視化"        |
| `page_size`   | ページサイズと向き | "A4_portrait", "A4_landscape"               |
| `elements`    | ノード定義の配列   | (後述)                                      |
| `connections` | エッジ定義の配列   | (後述)                                      |
| `output_path` | 出力ファイルパス   | "outputs/user-registration-flow.drawio.svg" |

### 任意項目

| 項目       | 説明           | 例                        |
| ---------- | -------------- | ------------------------- |
| `style`    | スタイル指定   | (後述)                    |
| `groups`   | グループ定義   | (後述)                    |
| `layout`   | レイアウト指定 | "hierarchical", "organic" |
| `metadata` | 追加メタ情報   | author, version, date     |

## スキーマ定義

### 完全なマニフェストスキーマ

```yaml
# マニフェスト完全スキーマ
manifest:
  # === 必須項目 ===
  title: string # 図のタイトル
  purpose: string # 図の目的
  page_size: enum # A4_portrait | A4_landscape | A3_portrait | A3_landscape | Letter | custom

  elements: # ノード定義
    - id: string # 一意のID（英数字、アンダースコア）
      type: enum # rectangle | rounded_rectangle | ellipse | diamond | cylinder | cloud | actor | document
      label: string # 表示テキスト
      x: number # X座標（省略時は自動配置）
      y: number # Y座標（省略時は自動配置）
      width: number # 幅（省略時はデフォルト120）
      height: number # 高さ（省略時はデフォルト60）
      style: object # 個別スタイル（任意）

  connections: # エッジ定義
    - from: string # 始点ノードID
      to: string # 終点ノードID
      type: enum # arrow | line | bidirectional | dashed
      label: string # ラベル（任意）
      style: object # 個別スタイル（任意）

  output_path: string # outputs/*.drawio.svg 形式

  # === 任意項目 ===
  style: # グローバルスタイル
    color_scheme: enum # corporate | pastel | monochrome | azure | custom
    font_family: string # フォントファミリー
    font_size: number # 基本フォントサイズ
    colors: # カスタムカラー
      primary: string # 主要色 (#RRGGBB)
      secondary: string # 副次色
      accent: string # アクセント色
      background: string # 背景色

  groups: # グループ定義
    - id: string # グループID
      label: string # グループラベル
      members: array # 含まれるノードID
      style: object # グループスタイル

  layout: # レイアウト指定
    type: enum # hierarchical | organic | circle | tree | grid
    direction: enum # TB | BT | LR | RL (hierarchical用)
    spacing: number # ノード間隔

  metadata: # メタ情報
    author: string # 作成者
    version: string # バージョン
    created_at: string # 作成日時
    source: string # 入力ソース（text/visual/portrait）
```

### ノードタイプ一覧

| タイプ              | 用途                     | draw.io 形状 |
| ------------------- | ------------------------ | ------------ |
| `rectangle`         | 処理、一般ボックス       | 矩形         |
| `rounded_rectangle` | ソフトな処理、カード     | 角丸矩形     |
| `ellipse`           | 開始/終了、状態          | 楕円/円      |
| `diamond`           | 判断、分岐               | ひし形       |
| `cylinder`          | データベース、ストレージ | 円筒         |
| `parallelogram`     | 入出力、データ           | 平行四辺形   |
| `cloud`             | クラウド、外部サービス   | 雲           |
| `actor`             | ユーザー、アクター       | 人型         |
| `document`          | ドキュメント             | 書類型       |
| `hexagon`           | 準備、手動処理           | 六角形       |

### 接続タイプ一覧

| タイプ          | 用途                 | 矢印       |
| --------------- | -------------------- | ---------- |
| `arrow`         | フロー、依存         | 片方向矢印 |
| `line`          | 関連、参照           | 矢印なし   |
| `bidirectional` | 双方向通信           | 両方向矢印 |
| `dashed`        | オプション、弱い関連 | 破線矢印   |

## レイアウトパターン

### 1. 階層型（hierarchical）

```yaml
layout:
  type: "hierarchical"
  direction: "TB" # Top to Bottom
  spacing: 80
```

用途: フローチャート、組織図、ツリー構造

### 2. 有機型（organic）

```yaml
layout:
  type: "organic"
  spacing: 100
```

用途: ネットワーク図、関係図、自由配置

### 3. グリッド型（grid）

```yaml
layout:
  type: "grid"
  columns: 3
  spacing: 60
```

用途: 一覧表示、カタログ、タイル配置

### 4. 放射型（circle）

```yaml
layout:
  type: "circle"
  center_node: "main"
```

用途: マインドマップ、中心-周辺構造

## 手順

1. **要件整理** - ユーザープロンプトから目的と範囲を特定
2. **ノード列挙** - 主要な要素をリストアップし、タイプを決定
3. **エッジ定義** - ノード間の関係を特定し、接続タイプを決定
4. **レイアウト選定** - 内容に最適なレイアウトパターンを選択
5. **スタイル指定** - 必要に応じてカラースキーム、フォントを指定
6. **パス決定** - `outputs/` 配下の kebab-case パスを設定
7. **セルフレビュー** - チェックリストで確認
8. **保存** - `image_manifest/{topic}.md` に保存

## 具体例

### Example 1: シンプルなフローチャート

```yaml
manifest:
  title: "ユーザー登録フロー"
  purpose: "新規ユーザーの登録プロセスを可視化"
  page_size: "A4_portrait"

  elements:
    - { id: "start", type: "ellipse", label: "開始" }
    - { id: "input_form", type: "rectangle", label: "情報入力" }
    - { id: "validate", type: "diamond", label: "入力チェック" }
    - { id: "save_db", type: "cylinder", label: "DB保存" }
    - { id: "send_email", type: "rectangle", label: "確認メール送信" }
    - { id: "end", type: "ellipse", label: "完了" }
    - { id: "error", type: "rectangle", label: "エラー表示" }

  connections:
    - { from: "start", to: "input_form", type: "arrow" }
    - { from: "input_form", to: "validate", type: "arrow" }
    - { from: "validate", to: "save_db", type: "arrow", label: "OK" }
    - { from: "validate", to: "error", type: "arrow", label: "NG" }
    - { from: "error", to: "input_form", type: "arrow" }
    - { from: "save_db", to: "send_email", type: "arrow" }
    - { from: "send_email", to: "end", type: "arrow" }

  layout:
    type: "hierarchical"
    direction: "TB"

  output_path: "outputs/user-registration-flow.drawio.svg"
```

### Example 2: システムアーキテクチャ図

```yaml
manifest:
  title: "Webアプリケーション構成図"
  purpose: "システム構成と通信フローを可視化"
  page_size: "A4_landscape"

  elements:
    - { id: "client", type: "rectangle", label: "クライアント\n(Browser)" }
    - { id: "cdn", type: "cloud", label: "CDN" }
    - { id: "lb", type: "ellipse", label: "Load Balancer" }
    - { id: "web1", type: "rectangle", label: "Web Server 1" }
    - { id: "web2", type: "rectangle", label: "Web Server 2" }
    - { id: "api", type: "rectangle", label: "API Gateway" }
    - { id: "db_primary", type: "cylinder", label: "Primary DB" }
    - { id: "db_replica", type: "cylinder", label: "Replica DB" }
    - { id: "cache", type: "parallelogram", label: "Redis Cache" }

  connections:
    - { from: "client", to: "cdn", type: "arrow" }
    - { from: "cdn", to: "lb", type: "arrow" }
    - { from: "lb", to: "web1", type: "arrow" }
    - { from: "lb", to: "web2", type: "arrow" }
    - { from: "web1", to: "api", type: "arrow" }
    - { from: "web2", to: "api", type: "arrow" }
    - { from: "api", to: "db_primary", type: "bidirectional" }
    - { from: "api", to: "cache", type: "bidirectional" }
    - {
        from: "db_primary",
        to: "db_replica",
        type: "arrow",
        label: "Replication",
      }

  groups:
    - { id: "frontend", label: "Frontend Layer", members: ["client", "cdn"] }
    - {
        id: "backend",
        label: "Backend Layer",
        members: ["lb", "web1", "web2", "api"],
      }
    - {
        id: "data",
        label: "Data Layer",
        members: ["db_primary", "db_replica", "cache"],
      }

  style:
    color_scheme: "azure"

  layout:
    type: "hierarchical"
    direction: "LR"

  output_path: "outputs/webapp-architecture.drawio.svg"
```

### Example 3: 組織図

```yaml
manifest:
  title: "開発部組織図"
  purpose: "開発部門の組織構成を可視化"
  page_size: "A4_landscape"

  elements:
    - { id: "cto", type: "rounded_rectangle", label: "CTO\n山田太郎" }
    - { id: "dev_mgr", type: "rounded_rectangle", label: "開発部長\n鈴木一郎" }
    - { id: "qa_mgr", type: "rounded_rectangle", label: "QA部長\n田中花子" }
    - { id: "team_a", type: "rectangle", label: "チームA\n(5名)" }
    - { id: "team_b", type: "rectangle", label: "チームB\n(4名)" }
    - { id: "qa_team", type: "rectangle", label: "QAチーム\n(3名)" }

  connections:
    - { from: "cto", to: "dev_mgr", type: "line" }
    - { from: "cto", to: "qa_mgr", type: "line" }
    - { from: "dev_mgr", to: "team_a", type: "line" }
    - { from: "dev_mgr", to: "team_b", type: "line" }
    - { from: "qa_mgr", to: "qa_team", type: "line" }

  style:
    color_scheme: "corporate"

  layout:
    type: "hierarchical"
    direction: "TB"

  output_path: "outputs/dev-org-chart.drawio.svg"
```

## カラースキーム

> **Note**: SVG 生成時もこのカラースキームを参照する（`svg-forge-template.instructions.md` と共通）。

### 定義済みスキーム詳細

```yaml
color_schemes:
  corporate:
    primary: "#4285F4" # Google Blue - メインカラー
    secondary: "#34A853" # Google Green - 成功、完了
    accent: "#FBBC05" # Google Yellow - 注意、警告
    warning: "#EA4335" # Google Red - エラー、危険
    background: "#FFFFFF" # 背景
    stroke: "#333333" # 境界線
    font: "#000000" # テキスト
    用途: "ビジネス文書、プロフェッショナル"

  azure:
    primary: "#0078D4" # Azure Blue
    secondary: "#50E6FF" # Azure Cyan
    accent: "#FFB900" # Azure Yellow
    warning: "#D83B01" # Azure Orange
    background: "#FFFFFF"
    stroke: "#333333"
    font: "#000000"
    用途: "Azure関連図、Microsoft製品"

  pastel:
    primary: "#B3E5FC" # Light Blue
    secondary: "#C8E6C9" # Light Green
    accent: "#FFF9C4" # Light Yellow
    warning: "#FFCCBC" # Light Orange
    background: "#FAFAFA"
    stroke: "#9E9E9E"
    font: "#424242"
    用途: "プレゼン、カジュアル、柔らかい印象"

  monochrome:
    primary: "#E0E0E0" # Light Gray
    secondary: "#BDBDBD" # Medium Gray
    accent: "#9E9E9E" # Gray
    warning: "#757575" # Dark Gray
    background: "#FFFFFF"
    stroke: "#424242"
    font: "#212121"
    用途: "印刷向け、モノクロ出力"
```

### カスタムカラー例

```yaml
style:
  color_scheme: "custom"
  colors:
    primary: "#1976D2"
    secondary: "#43A047"
    accent: "#FFA000"
    background: "#FAFAFA"
```

## 品質チェックリスト

マニフェスト完成前に確認:

- [ ] タイトルが内容を適切に表している
- [ ] 目的が明確に記述されている
- [ ] すべてのノードに一意の ID がある
- [ ] ノードタイプが内容に適切
- [ ] 接続の from/to が存在するノードを参照している
- [ ] レイアウトが内容に適切
- [ ] 出力パスが `outputs/` 配下の kebab-case
- [ ] 拡張子が `.drawio.svg`（または指定形式）

## 関連ファイル

| ファイル                              | 用途                        |
| ------------------------------------- | --------------------------- |
| `text-manifest-gateway.agent.md`      | テキスト → マニフェスト変換 |
| `visual-manifest-gateway.agent.md`    | 画像 → マニフェスト変換     |
| `portrait-manifest-gateway.agent.md`  | 人物写真 → マニフェスト変換 |
| `svg-forge-template.instructions.md`  | SVG 生成ガイド              |
| `svg-review-template.instructions.md` | SVG レビューガイド          |
