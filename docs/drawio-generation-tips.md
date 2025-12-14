# draw.io 図生成 TIPS

> 他のワークスペースで draw.io 編集可能な図を生成させるためのガイド

## 🚀 クイックスタート

### 最小プロンプト（コピペで使える）

```
draw.io編集可能なSVGを生成。形式はmxfile XML、全図形をmxCellで定義。SVGネイティブ要素(rect,ellipse,path)は使わない。outputs/ファイル名.drawio.svg に保存。
```

---

## 📋 copilot-instructions.md に追加するテンプレート

### 最小構成

```markdown
## 図の生成ルール

draw.io で編集可能な図を生成する際は以下を守ること：

1. **出力形式**: `outputs/*.drawio.svg`
2. **XML 形式**: 純粋な mxfile（SVG 要素で描画しない）
3. **全図形**: `<mxCell vertex="1">` で定義
4. **全接続線**: `<mxCell edge="1">` で定義
5. **色指定**: `fillColor=#RRGGBB;strokeColor=#RRGGBB;`

### 基本テンプレート

\`\`\`xml
<mxfile host="app.diagrams.net">
<diagram name="図の名前" id="diagram-1">
<mxGraphModel dx="800" dy="600" grid="1" gridSize="10">
<root>
<mxCell id="0"/>
<mxCell id="1" parent="0"/>

<!-- ここに図形を追加 -->
</root>
</mxGraphModel>
</diagram>
</mxfile>
\`\`\`
```

### 詳細構成（推奨）

```markdown
## 図の生成ルール

draw.io で編集可能な図を生成してください。

### 出力形式

- 拡張子: `*.drawio.svg`
- 形式: mxfile XML（純粋な draw.io 形式）
- 全図形を `<mxCell>` で定義すること
- **❌ 禁止**: SVG ネイティブ要素（`<rect>`, `<ellipse>`, `<path>`）での描画

### 使用可能な図形スタイル

| 用途     | style 属性                                                                 |
| -------- | -------------------------------------------------------------------------- |
| 矩形     | `rounded=0;whiteSpace=wrap;html=1;`                                        |
| 角丸矩形 | `rounded=1;whiteSpace=wrap;html=1;`                                        |
| 楕円/円  | `ellipse;whiteSpace=wrap;html=1;`                                          |
| ひし形   | `rhombus;whiteSpace=wrap;html=1;`                                          |
| 円柱(DB) | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;` |
| 雲       | `ellipse;shape=cloud;whiteSpace=wrap;html=1;`                              |
| 人型     | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;`    |
| 書類     | `shape=document;whiteSpace=wrap;html=1;boundedLbl=1;`                      |
| 六角形   | `shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;`        |

### 接続線スタイル

| 用途       | style 属性                                    |
| ---------- | --------------------------------------------- |
| 矢印       | `endArrow=classic;html=1;`                    |
| 双方向矢印 | `endArrow=classic;startArrow=classic;html=1;` |
| 破線矢印   | `endArrow=classic;dashed=1;html=1;`           |
| 線のみ     | `endArrow=none;html=1;`                       |

### 色の指定方法

\`\`\`
fillColor=#FFFFFF;strokeColor=#333333;fontColor=#000000;
\`\`\`

### 図形の定義例

\`\`\`xml

<!-- ノード（図形） -->
<mxCell id="node1" value="ラベル" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>

<!-- エッジ（接続線） -->
<mxCell id="edge1" style="endArrow=classic;html=1;strokeColor=#333333;" edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- ラベル付き接続線 -->
<mxCell id="edge2" value="ラベル" style="endArrow=classic;html=1;" edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 📁 ファイル構成（このワークスペースからコピー推奨）

```
.github/
├── copilot-instructions.md          # 基本ルール
└── instructions/
    ├── svg-forge-template.instructions.md   # ★ 最重要：SVG生成詳細ルール
    └── manifest-template.instructions.md    # マニフェスト定義（オプション）
```

**最低限コピーすべきファイル**: `svg-forge-template.instructions.md`

---

## ⚠️ よくある失敗と対策

### 失敗 1: draw.io で開くと真っ白

**原因**: SVG ネイティブ要素で描画している

```xml
<!-- ❌ NG: SVG要素での描画 -->
<svg>
  <ellipse cx="200" cy="180" rx="70" ry="85" fill="#F5D6C6"/>
  <rect x="100" y="100" width="120" height="60"/>
</svg>
```

**対策**: 全て mxCell で定義

```xml
<!-- ✅ OK: mxCellでの定義 -->
<mxCell id="shape1" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#F5D6C6;" vertex="1" parent="1">
  <mxGeometry x="130" y="95" width="140" height="170" as="geometry"/>
</mxCell>
```

### 失敗 1.5: draw.io で開けるが中身が空（見落としやすい！）

**原因**: `content` 属性に mxfile があるが、`<root>` 内に図形の mxCell が定義されていない

```xml
<!-- ❌ NG: content属性のrootが空で、SVG要素で描画 -->
<svg content="&lt;mxfile&gt;&lt;diagram&gt;&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;">
  <rect x="100" y="100" width="200" height="100" fill="#dae8fc"/>
  <text x="200" y="150">開始</text>
</svg>
```

**症状**:

- ファイルは draw.io で開ける ✅
- しかしキャンバスが空っぽ ❌
- ブラウザで直接開くと SVG は表示される

**対策**: `content` 属性内の `<root>` に全図形を mxCell で定義

```xml
<!-- ✅ OK: content属性内に全図形を定義 -->
<svg content="&lt;mxfile&gt;&lt;diagram&gt;&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;mxCell id=&quot;start&quot; value=&quot;開始&quot; style=&quot;ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;&quot; vertex=&quot;1&quot; parent=&quot;1&quot;&gt;&lt;mxGeometry x=&quot;100&quot; y=&quot;100&quot; width=&quot;100&quot; height=&quot;50&quot; as=&quot;geometry&quot;/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;">
</svg>
```

> **🚨 重要**: draw.io は **`content` 属性内の XML だけ**を解釈する。SVG のネイティブ要素は完全に無視される。

### 失敗 2: ファイルが開けない

**原因**: XML が不正、または必須要素が欠落

**対策**: 以下の構造を必ず含める

```xml
<mxfile>
  <diagram>
    <mxGraphModel>
      <root>
        <mxCell id="0"/>           <!-- ルートセル（必須） -->
        <mxCell id="1" parent="0"/> <!-- 親セル（必須） -->
        <!-- 図形はここに追加 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 失敗 3: 接続線がノードに繋がらない

**原因**: source/target 属性が未設定

**対策**:

```xml
<mxCell id="edge1" style="endArrow=classic;html=1;" edge="1" parent="1"
        source="node1" target="node2">  <!-- source/target必須 -->
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 🎨 カラースキーム例

### Azure 風

```
primary: #0078D4
secondary: #50E6FF
accent: #FFB900
background: #FFFFFF
stroke: #333333
```

### Corporate 風

```
primary: #4285F4
secondary: #34A853
accent: #FBBC05
warning: #EA4335
background: #FFFFFF
```

### Pastel 風

```
primary: #B3E5FC
secondary: #C8E6C9
accent: #FFF9C4
background: #FAFAFA
stroke: #9E9E9E
```

---

## 💡 実際のプロンプト例

### シンプルなフローチャート

```
ユーザー登録フローの図をdraw.ioで編集可能な形式で作成して。
開始→入力フォーム→バリデーション→DB保存→完了の流れ。
outputs/user-registration-flow.drawio.svg に保存。
```

### システム構成図

```
Webアプリのシステム構成図を作成。
クライアント、CDN、ロードバランサー、Webサーバー×2、APIサーバー、DB、Redisを含める。
draw.io編集可能なmxfile形式で outputs/system-architecture.drawio.svg に出力。
```

### 組織図

```
開発部の組織図を作成。
CTO配下に開発部長とQA部長、それぞれの配下にチームがある構成。
draw.io形式で outputs/org-chart.drawio.svg に保存。
```

---

## 📚 参考リンク

- [draw.io 公式ドキュメント](https://www.drawio.com/doc/)
- [mxGraph 形式リファレンス](https://jgraph.github.io/mxgraph/docs/manual.html)
- このリポジトリの実装例: `outputs/*.drawio.svg`

---

## 🔧 トラブルシューティング

| 症状               | 原因                       | 対策                             |
| ------------------ | -------------------------- | -------------------------------- |
| draw.io で真っ白   | SVG 要素で描画             | mxCell に変更                    |
| **開けるが中身空** | **content 内の root が空** | **content 属性内に mxCell 定義** |
| ファイルが開けない | XML 構文エラー             | mxCell id="0","1"を確認          |
| 線が繋がらない     | source/target 未設定       | 属性を追加                       |
| 色が反映されない   | 色形式が不正               | `#RRGGBB`形式に                  |
| 日本語が文字化け   | エンコーディング           | UTF-8 で保存                     |
