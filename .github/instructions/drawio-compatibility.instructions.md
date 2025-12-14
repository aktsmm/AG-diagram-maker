# draw.io 互換性ルール (v1.0)

> **適用対象**: svg-forge、図面を生成するすべてのエージェント
> **最終更新**: 2025-12-12

このインストラクションは、draw.io で編集可能な図面を生成するための必須ルールを定義します。

---

## 🚨 必須条件

draw.io で編集可能にするには、**すべての図形を mxCell として定義**する必要があります。

### mxfile 構造

```xml
<mxfile host="app.diagrams.net" modified="..." agent="..." generator="aktsmm/Ag-diagram-maker">
  <diagram id="..." name="Page-1">
    <mxGraphModel dx="..." dy="..." grid="1" gridSize="10" ...>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- ここにノード・エッジの mxCell を定義 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### mxfile 属性

| 属性        | 必須 | 説明                                     |
| ----------- | ---- | ---------------------------------------- |
| `host`      | ✅   | 生成元アプリ識別子                       |
| `generator` | ✅   | **`aktsmm/Ag-diagram-maker`** を必ず設定 |
| `modified`  | -    | 最終更新日時（ISO 8601 形式）            |
| `agent`     | -    | ブラウザ/ツール情報                      |

### 必須要素

| 要素                       | 説明              | 必須 |
| -------------------------- | ----------------- | ---- |
| `mxCell id="0"`            | ルートセル        | ✅   |
| `mxCell id="1" parent="0"` | デフォルト親セル  | ✅   |
| ノード用 mxCell            | vertex="1" を持つ | ✅   |
| エッジ用 mxCell            | edge="1" を持つ   | ✅   |

---

## ❌ やってはいけないこと

### SVG 要素のみで描画

```xml
<!-- NG: draw.io では真っ白になる -->
<svg content="&lt;mxfile&gt;...空のroot...&lt;/mxfile&gt;">
  <rect x="100" y="100" width="200" height="100"/>
  <text x="200" y="150">ノード</text>
</svg>
```

### 空の content 属性

```xml
<!-- NG: mxCell がない -->
<svg content="&lt;mxfile&gt;&lt;diagram&gt;&lt;mxGraphModel&gt;&lt;root&gt;
  &lt;mxCell id=&quot;0&quot;/&gt;
  &lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;
  <!-- 図形の mxCell がない！ -->
&lt;/root&gt;&lt;/mxGraphModel&gt;&lt;/diagram&gt;&lt;/mxfile&gt;">
</svg>
```

---

## ✅ 正しい mxCell 定義

### ノード（四角形）

```xml
<mxCell id="node1" value="ノード名"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

### ノード（楕円）

```xml
<mxCell id="start" value="開始"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="80" height="50" as="geometry"/>
</mxCell>
```

### ノード（菱形 - 判断）

```xml
<mxCell id="decision1" value="条件?"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="80" as="geometry"/>
</mxCell>
```

### エッジ（矢印）

```xml
<mxCell id="edge1" value=""
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
        edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### エッジ（ラベル付き）

```xml
<mxCell id="edge2" value="Yes"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
        edge="1" parent="1" source="decision1" target="node3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## グループ（コンテナ）

```xml
<!-- グループ/コンテナ -->
<mxCell id="group1" value="グループ名"
        style="swimlane;horizontal=1;startSize=30;fillColor=#f5f5f5;strokeColor=#666666;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="300" height="200" as="geometry"/>
</mxCell>

<!-- グループ内のノード（parent="group1" を指定） -->
<mxCell id="child1" value="子ノード"
        style="rounded=1;whiteSpace=wrap;html=1;"
        vertex="1" parent="group1">
  <mxGeometry x="20" y="40" width="100" height="50" as="geometry"/>
</mxCell>
```

---

## 標準スタイル

### ノード色

| 用途         | fillColor | strokeColor |
| ------------ | --------- | ----------- |
| 標準         | `#dae8fc` | `#6c8ebf`   |
| 開始/終了    | `#d5e8d4` | `#82b366`   |
| 判断         | `#fff2cc` | `#d6b656`   |
| エラー/警告  | `#f8cecc` | `#b85450`   |
| 外部システム | `#e1d5e7` | `#9673a6`   |
| グレー       | `#f5f5f5` | `#666666`   |

### エッジスタイル

```yaml
edge_styles:
  orthogonal: "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
  curved: "edgeStyle=elbowEdgeStyle;elbow=horizontal;rounded=1;"
  straight: "endArrow=classic;html=1;"
```

---

## HTML エンコーディング

content 属性内の XML は HTML エンコードが必要：

| 文字 | エンコード |
| ---- | ---------- |
| `<`  | `&lt;`     |
| `>`  | `&gt;`     |
| `"`  | `&quot;`   |
| `&`  | `&amp;`    |

### 例

```xml
<svg content="&lt;mxfile host=&quot;app.diagrams.net&quot;&gt;...&lt;/mxfile&gt;">
```

---

## 検証チェックリスト

生成前に確認：

- [ ] `mxCell id="0"` と `id="1"` が存在する
- [ ] すべてのノードに `vertex="1"` がある
- [ ] すべてのエッジに `edge="1"` がある
- [ ] エッジの `source` / `target` が存在するノード ID を参照
- [ ] `mxGeometry` が各 mxCell に定義されている
- [ ] content 属性が正しく HTML エンコードされている
- [ ] mxCell 数 >= 2 + ノード数 + エッジ数

---

## トラブルシューティング

### 「draw.io で開くと真っ白」

1. content 属性が空でないか確認
2. mxCell 定義が root 内にあるか確認
3. HTML エンコーディングが正しいか確認

### 「一部の図形が表示されない」

1. 該当図形の mxCell が存在するか確認
2. `vertex="1"` または `edge="1"` が設定されているか確認
3. mxGeometry が正しく定義されているか確認

### 「エッジが表示されない」

1. source / target の ID が正しいか確認
2. 参照先のノードが存在するか確認
3. edge="1" が設定されているか確認
